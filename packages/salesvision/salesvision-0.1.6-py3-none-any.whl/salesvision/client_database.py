import imagehash
import io
import numpy as np
import pymongo
import requests
from PIL import Image

from salesvision.server_estimation import EstimationTemplate
from salesvision.metrics import set2set_similarity_metric as similarity_metric
from salesvision.image_utils import read_image, compute_image_hash


class LocalDatabaseWithIntegratedEstimator(object):
    """Class for local database usage with paths"""
    def __init__(self,
                 estimator: EstimationTemplate,
                 database_name: str = 'ClothesBase',
                 with_hash_indexing: bool = True,
                 metric: callable = similarity_metric):
        """
        Class constructor
        Args:
            estimator: Estimation engine
            database_name: name of created local database, if database with
                same name has already been created,
                then it is used for solution
            with_hash_indexing: preventing occurrence duplicates by image hash
        """
        self.client = pymongo.MongoClient()
        self.db_name = database_name
        self.db = self.client[database_name]
        self.collection = self.db.images
        self.with_hash_indexing = with_hash_indexing
        self.estimator = estimator
        self.metric = metric

    def _order_database(self, prediction: dict) -> list:
        """
        Find similarity elements in base by prediction results
        Args:
            prediction: system prediction

        Returns:
            List of indexes ordered by metric similarity
        """
        indexes_with_metric = []

        for elem in self.collection.find():
            indexes_with_metric.append(
                (
                    elem['_id'],
                    self.metric(prediction, elem)
                )
            )

        indexes_with_metric.sort(key=lambda x: x[1], reverse=True)

        return indexes_with_metric

    def _in_database(self, image: Image, image_hash: str) -> tuple:
        """

        Args:
            image:
            image_hash:

        Returns:

        """
        if self.collection.count_documents({'image_hash': image_hash}) > 0:
            for elem in self.collection.find(
                    {'image_hash': image_hash}):
                sample_img = read_image(elem['local_path'])
                sample_img = np.array(sample_img)
                img = np.array(image)

                if np.abs(sample_img - img).sum() == 0:
                    return True, elem

        return False, None

    def insert(self, image_object) -> pymongo.collection.ObjectId:
        """
        Insert image description to database
        Args:
            image_object: image path on local machine or URL link or Array

        Returns:
            Inserted element ID in database
        """
        image = read_image(image_object)
        img_hash = compute_image_hash(image)

        if self.with_hash_indexing:
            if self._in_database(image, img_hash)[0]:
                raise RuntimeWarning('Database has contained image already')

        results = self.estimator(image_object)

        insert_data = {
            'local_path': image_object if type(image_object) is str else '',
            'image_hash': img_hash,
            'prediction': results
        }

        return self.collection.insert_one(insert_data).inserted_id

    def search(self,
               image_object,
               top_k: int = 5,
               return_scores: bool = False) -> list:
        """
        Search top k similar samples indexes from local database
        Args:
            image_object: image path on local machine or URL link or Array
            top_k: count of found samples
            return_scores: return list of tuples with indexes and metric scores

        Returns:
            Indexes of top k similar samples from database
        """
        image = read_image(image_object)
        img_hash = compute_image_hash(image)

        need_predict = True
        prediction = None
        if self.with_hash_indexing:
            checking_result = self._in_database(image, img_hash)
            if checking_result[0]:
                prediction = checking_result[1]
                need_predict = False
                print('From base')

        if need_predict:
            prediction = {'prediction': self.estimator(image_object)}

        if prediction['prediction']['status'] != '0':
            raise RuntimeError(
                'System couldn\'t process image, error code: {}'.format(
                    prediction['prediction']['status']
                )
            )

        search_result = self._order_database(prediction)
        if not return_scores:
            search_result = [elem[0] for elem in search_result]

        if len(search_result) < top_k:
            return search_result
        return search_result[:top_k]

    def drop_collection(self):
        """
        Erase database
        Returns:
            None
        """
        return self.collection.drop()

    def get_images_by_indexes(self, indexes: list) -> list:
        """
        Return Pillow images list from base by indexes list
        Args:
            indexes: indexes list

        Returns:
            Pillow images list

        """
        return [
            read_image(
                self.collection.find_one(
                    {'_id': idx[0] if type(idx) is tuple else idx}
                )['local_path']
            )
            for idx in indexes
        ]


class SimpleLocalDatabase(object):
    """Class for local database usage"""
    def __init__(self,
                 database_name: str = 'ClothesBase',
                 metric: callable = similarity_metric):
        """
        Class constructor
        Args:
            database_name: name of created local database, if database with
                same name has already been created,
                then it is used for solution
        """
        self.client = pymongo.MongoClient()
        self.db_name = database_name
        self.db = self.client[database_name]
        self.collection = self.db.images
        self.metric = metric

    def _order_database(self, prediction: dict) -> list:
        """
        Find similarity elements in base by prediction results
        Args:
            prediction: system prediction

        Returns:
            List of indexes ordered by metric similarity
        """
        indexes_with_metric = []

        for elem in self.collection.find():
            indexes_with_metric.append(
                (
                    elem['_id'],
                    self.metric(prediction, elem)
                )
            )

        indexes_with_metric.sort(key=lambda x: x[1], reverse=True)

        return indexes_with_metric

    def insert(self, prediction: dict) -> pymongo.collection.ObjectId:
        """
        Insert image description to database
        Args:
            prediction: system prediction

        Returns:
            Inserted element ID in database
        """
        insert_data = {
            'local_path': '',
            'image_hash': '',
            'prediction': prediction
        }

        return self.collection.insert_one(insert_data).inserted_id

    def search(self,
               prediction: dict,
               top_k: int = 5,
               return_scores: bool = False) -> list:
        """
        Search top k similar samples indexes from local database
        Args:
            prediction: system prediction
            top_k: count of found samples
            return_scores: return list of tuples with indexes and metric scores

        Returns:
            Indexes of top k similar samples from database
        """
        if prediction['status'] != '0':
            raise RuntimeError(
                'System couldn\'t process image, error code: {}'.format(
                    prediction['prediction']['status']
                )
            )

        base_prediction = {'prediction': prediction}

        search_result = self._order_database(base_prediction)
        if not return_scores:
            search_result = [elem[0] for elem in search_result]

        if len(search_result) < top_k:
            return search_result
        return search_result[:top_k]

    def drop_collection(self):
        """
        Erase database
        Returns:
            None
        """
        return self.collection.drop()
