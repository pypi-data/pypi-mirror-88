# coding: utf-8
from collections import defaultdict

from supervisely_lib.api.module_api import ApiField, RemoveableBulkModuleApi
from supervisely_lib.io.fs import ensure_base_path, get_file_hash
from supervisely_lib._utils import batched

from supervisely_lib.api.pointcloud.pointcloud_annotation_api import PointcloudAnnotationAPI
from supervisely_lib.api.pointcloud.pointcloud_object_api import PointcloudObjectApi
from supervisely_lib.api.pointcloud.pointcloud_figure_api import PointcloudFigureApi
from supervisely_lib.api.pointcloud.pointcloud_tag_api import PointcloudTagApi
from requests_toolbelt import MultipartDecoder, MultipartEncoder


class PointcloudApi(RemoveableBulkModuleApi):
    def __init__(self, api):
        '''
        :param api: Api class object
        '''
        super().__init__(api)
        self.annotation = PointcloudAnnotationAPI(api)
        self.object = PointcloudObjectApi(api)
        self.figure = PointcloudFigureApi(api)
        self.tag = PointcloudTagApi(api)

    @staticmethod
    def info_sequence():
        return [ApiField.ID,
                ApiField.DESCRIPTION,
                ApiField.NAME,
                ApiField.TEAM_ID,
                ApiField.WORKSPACE_ID,
                ApiField.PROJECT_ID,
                ApiField.DATASET_ID,
                ApiField.LINK,
                ApiField.HASH,
                ApiField.PATH_ORIGINAL,
                #ApiField.PREVIEW,
                ApiField.CLOUD_MIME,
                ApiField.FIGURES_COUNT,
                ApiField.ANN_OBJECTS_COUNT,
                ApiField.TAGS,
                ApiField.CREATED_AT,
                ApiField.UPDATED_AT]

    @staticmethod
    def info_tuple_name():
        return 'PointCloudInfo'

    def _convert_json_info(self, info: dict, skip_missing=True):
        return super(PointcloudApi, self)._convert_json_info(info, skip_missing=skip_missing)

    def get_list(self, dataset_id, filters=None):
        '''
        :param dataset_id: int
        :param filters: list
        :return: list of the pointclouds objects from the dataset with given id
        '''
        return self.get_list_all_pages('point-clouds.list',  {ApiField.DATASET_ID: dataset_id, ApiField.FILTER: filters or []})

    def get_info_by_id(self, id):
        '''
        :param id: int
        :return: PointcloudApi metadata by numeric id
        '''
        return self._get_info_by_id(id, 'point-clouds.info')

    def _download(self, id, is_stream=False):
        '''
        :param id: int
        :param is_stream: bool
        :return: Response object containing pointcloud object with given id
        '''
        response = self._api.post('point-clouds.download', {ApiField.ID: id}, stream=is_stream)
        return response

    def download_path(self, id, path):
        '''
        Download pointcloud with given id on the given path
        :param id: int
        :param path: str
        '''
        response = self._download(id, is_stream=True)
        ensure_base_path(path)
        with open(path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024*1024):
                fd.write(chunk)

    def get_list_related_images(self, id):
        dataset_id = self.get_info_by_id(id).dataset_id
        filters = [{"field": ApiField.ENTITY_ID, "operator": "=", "value": id}]
        return self.get_list_all_pages('point-clouds.images.list',
                                       {ApiField.DATASET_ID: dataset_id, ApiField.FILTER: filters},
                                       convert_json_info_cb=lambda x : x)

    def download_related_image(self, id, path):
        response = self._api.post('point-clouds.images.download', {ApiField.ID: id}, stream=True)
        ensure_base_path(path)
        with open(path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                fd.write(chunk)
        return response

    #@TODO: copypaste from video_api
    def upload_hash(self, dataset_id, name, hash, meta=None):
        meta = {} if meta is None else meta
        return self.upload_hashes(dataset_id, [name], [hash], [meta])[0]

    # @TODO: copypaste from video_api
    def upload_hashes(self, dataset_id, names, hashes, metas=None, progress_cb=None):
        return self._upload_bulk_add(lambda item: (ApiField.HASH, item), dataset_id, names, hashes, metas, progress_cb)

    # @TODO: copypaste from video_api
    def _upload_bulk_add(self, func_item_to_kv, dataset_id, names, items, metas=None, progress_cb=None):
        if metas is None:
            metas = [{}] * len(items)

        results = []
        if len(names) == 0:
            return results
        if len(names) != len(items):
            raise RuntimeError("Can not match \"names\" and \"items\" lists, len(names) != len(items)")

        for batch in batched(list(zip(names, items, metas))):
            images = []
            for name, item, meta in batch:
                item_tuple = func_item_to_kv(item)
                images.append({ApiField.NAME: name,
                               item_tuple[0]: item_tuple[1],
                               ApiField.META: meta if meta is not None else {}})
            response = self._api.post('point-clouds.bulk.add', {ApiField.DATASET_ID: dataset_id,
                                                                ApiField.POINTCLOUDS: images})
            if progress_cb is not None:
                progress_cb(len(images))

            results = [self._convert_json_info(item) for item in response.json()]
            name_to_res = {img_info.name: img_info for img_info in results}
            ordered_results = [name_to_res[name] for name in names]

            return ordered_results

    def add_related_images(self, images_json):
        response = self._api.post('point-clouds.images.add', {ApiField.IMAGES: images_json})
        return response.json()

    def upload_path(self, dataset_id, name, path, meta=None):
        metas = None if meta is None else [meta]
        return self.upload_paths(dataset_id, [name], [path], metas=metas)[0]

    def upload_paths(self, dataset_id, names, paths, progress_cb=None, metas=None):
        def path_to_bytes_stream(path):
            return open(path, 'rb')
        hashes = self._upload_data_bulk(path_to_bytes_stream, get_file_hash, paths, progress_cb)
        return self.upload_hashes(dataset_id, names, hashes, metas=metas)

    def check_existing_hashes(self, hashes):
        results = []
        if len(hashes) == 0:
            return results
        for hashes_batch in batched(hashes, batch_size=900):
            response = self._api.post('images.internal.hashes.list', hashes_batch)
            results.extend(response.json())
        return results

    def _upload_data_bulk(self, func_item_to_byte_stream, func_item_hash, items, progress_cb):
        hashes = []
        if len(items) == 0:
            return hashes

        hash_to_items = defaultdict(list)

        for idx, item in enumerate(items):
            item_hash = func_item_hash(item)
            hashes.append(item_hash)
            hash_to_items[item_hash].append(item)

        unique_hashes = set(hashes)
        remote_hashes = self.check_existing_hashes(list(unique_hashes))
        new_hashes = unique_hashes - set(remote_hashes)

        if progress_cb is not None:
            progress_cb(len(remote_hashes))

        # upload only new images to supervisely server
        items_to_upload = []
        for hash in new_hashes:
            items_to_upload.extend(hash_to_items[hash])

        for batch in batched(items_to_upload):
            content_dict = {}
            for idx, item in enumerate(batch):
                content_dict["{}-file".format(idx)] = (str(idx), func_item_to_byte_stream(item), 'pcd/*')
            encoder = MultipartEncoder(fields=content_dict)
            self._api.post('point-clouds.bulk.upload', encoder)
            if progress_cb is not None:
                progress_cb(len(batch))

        return hashes