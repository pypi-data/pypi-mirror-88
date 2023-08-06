# pylint: disable=attribute-defined-outside-init, no-member, no-self-use

##########################
# Imports
##########################


import os
from typing import Dict
from typing import List

import pickle
import numpy as np
from annoy import AnnoyIndex
from easydict import EasyDict as edict

from few_shots_clf import utils
from few_shots_clf.fm_classifier import utils as fm_utils
from few_shots_clf.fm_classifier import constants


##########################
# FMClassifier
##########################


class FMClassifier:
    """Class implementing the Features Matching Classifier (FMClassifier)

    Args:
        catalog_path (string): [description]
        params (dict): [description]
    """

    ##########################
    # Init
    ##########################

    def __init__(self, catalog_path: str, params: Dict = {}):
        self.catalog_path = catalog_path
        self._config_classifier(catalog_path, params)

    ##########################
    # Config
    ##########################

    def _config_classifier(self, catalog_path, params):
        self._get_classifier_config(params)
        self._get_catalog_images(catalog_path)
        self._get_catalog_labels(catalog_path)
        self._get_catalog_images2labels()
        self._load_fingerprints()

    def _get_classifier_config(self, params):
        self.config = edict({
            "verbose": params.get("verbose", constants.VERBOSE),
            "feature_descriptor": params.get("feature_descriptor", constants.FEATURE_DESCRIPTOR),
            "feature_dimension": params.get("feature_dimension", constants.FEATURE_DIMENSION),
            "image_size": params.get("image_size", constants.IMAGE_SIZE),
            "keypoint_stride": params.get("keypoint_stride", constants.KEYPOINT_STRIDE),
            "keypoint_sizes": params.get("keypoint_sizes", constants.KEYPOINT_SIZES),
            "matcher_path": params.get("matcher_path", constants.MATCHER_PATH),
            "matcher_distance": params.get("matcher_distance", constants.MATCHER_DISTANCE),
            "matcher_n_trees": params.get("matcher_n_trees", constants.MATCHER_N_TREES),
            "scoring": params.get("scoring", constants.SCORING),
            "k_nn": params.get("k_nn", constants.K_NN),
            "fingerprint_path": params.get("fingerprint_path",
                                           constants.FINGERPRINT_PATH),
        })

    def _get_catalog_images(self, catalog_path):
        self.catalog_images = utils.get_all_images_from_folder(catalog_path)

    def _get_catalog_labels(self, catalog_path):
        self.catalog_labels = utils.get_labels_from_catalog(catalog_path)

    def _get_catalog_images2labels(self):
        self.catalog_images2labels = utils.compute_images2labels(self.catalog_images,
                                                                 self.catalog_labels)

    def _load_fingerprints(self):
        # Previous fingerprint
        if os.path.exists(self.config.fingerprint_path):
            with open(self.config.fingerprint_path, "rb") as pickle_file:
                self.config.fingerprint = pickle.load(pickle_file)
        else:
            self.config.fingerprint = ""

        # Current fingerprint
        self.fingerprint = fm_utils.compute_fingerprint(self.catalog_path,
                                                        self.config)

    ##########################
    # Train
    ##########################

    def train(self):
        """Method used to train the classifier.
        """
        # Init matcher
        self.matcher = AnnoyIndex(self.config.feature_dimension,
                                  self.config.matcher_distance)

        # Create or load matcher
        if self._should_create_index():
            self._create_matcher_index()
            self._save_matcher_index()
            self._save_fingerprint()
        else:
            self._load_matcher_index()

    def _should_create_index(self):
        fingerprint_changed = self.config.fingerprint != self.fingerprint
        matcher_file_exists = os.path.isfile(self.config.matcher_path)
        return fingerprint_changed or (not matcher_file_exists)

    def _create_matcher_index(self):
        # Get descriptors
        catalog_descriptors = self._get_catalog_descriptors()

        # Get iterator
        descriptors_iterator = utils.get_iterator(catalog_descriptors,
                                                  verbose=self.config.verbose,
                                                  description="Creating Index...")

        # Config matcher
        for k, descriptor in enumerate(descriptors_iterator):
            self.matcher.add_item(k, descriptor)
        self.matcher.build(self.config.matcher_n_trees)

    def _get_catalog_descriptors(self):
        # Init descriptors list
        catalog_descriptors = []

        # Init iterator
        iterator = utils.get_iterator(
            utils.get_all_images_from_folder(self.catalog_path),
            verbose=self.config.verbose,
            description="Computing catalog descriptors")

        # Compute all descriptors
        for path in iterator:
            # Read image
            img = utils.read_image(path, size=self.config.image_size)

            # Compute keypoints
            keypoints = utils.compute_keypoints(
                img,
                self.config.keypoint_stride,
                self.config.keypoint_sizes)

            # Compute descriptors
            descriptors = utils.compute_descriptors(
                img,
                keypoints,
                self.config.feature_descriptor)

            # Update descriptors list
            catalog_descriptors.append(descriptors)

        # Reshape descriptors list
        catalog_descriptors = np.array(catalog_descriptors)
        catalog_descriptors = catalog_descriptors.reshape(-1,
                                                          catalog_descriptors.shape[-1])

        return catalog_descriptors

    def _save_matcher_index(self):
        matcher_folder = "/".join(self.config.matcher_path.split("/")[:-1])
        if not os.path.exists(matcher_folder):
            os.makedirs(matcher_folder)
        if self.config.verbose:
            print("Saving Index...")
        self.matcher.save(self.config.matcher_path)

    def _load_matcher_index(self):
        if self.config.verbose:
            print("Loading Index...")
        self.matcher.load(self.config.matcher_path)

    def _save_fingerprint(self):
        fingerprint_folder = "/".join(
            self.config.fingerprint_path.split("/")[:-1])
        if not os.path.exists(fingerprint_folder):
            os.makedirs(fingerprint_folder)
        with open(self.config.fingerprint_path, "wb") as pickle_file:
            pickle.dump(self.fingerprint, pickle_file)

    ##########################
    # Predict
    ##########################

    def predict(self, query_path: str) -> np.array:
        """Method used to predict a score per class for a given query.

        Args:
            query_path (str): The local path of the query.

        Returns:
            np.array: The list of scores per class.
        """
        # Read img
        query_img = utils.read_image(query_path, size=self.config.image_size)

        # Get keypoints
        query_keypoints = utils.compute_keypoints(query_img,
                                                  self.config.keypoint_stride,
                                                  self.config.keypoint_sizes)

        # Get descriptors
        query_descriptors = utils.compute_descriptors(query_img,
                                                      query_keypoints,
                                                      self.config.feature_descriptor)

        # Get scores
        scores = self._get_query_scores(query_descriptors)

        # To numpy
        scores = np.array(scores)

        return scores

    def predict_batch(self, query_paths: List[str]) -> np.array:
        """Method used to predict a class for a batch of queries.

        Args:
            query_paths (List[str]): The list of all query paths.

        Returns:
            np.array: The scores per class for each query.
        """
        # Init scores
        scores = []

        # Get iterator
        iterator = utils.get_iterator(query_paths,
                                      verbose=self.config.verbose,
                                      description="Prediction of all queries")

        # Loop over all queries
        for query_path in iterator:
            # Predict score of query
            query_scores = self.predict(query_path)

            # Update scores
            scores.append(query_scores)

        # To numpy
        scores = np.array(scores)

        return scores

    def _get_query_scores(self, query_descriptors):
        # Init scores variables
        scores = np.zeros((len(self.catalog_labels)))
        n_desc = query_descriptors.shape[0]

        # Compute matches
        train_idx, distances = self._compute_query_matches(query_descriptors)

        # Compute score matrix
        scores_matrix = self._compute_scores_matrix(distances)

        # Compute final scores
        for ind, nn_train_idx in enumerate(train_idx):
            for k, idx in enumerate(nn_train_idx):
                # Get image_path
                image_path = self.catalog_images[int(idx // n_desc)]

                # Get image_label
                image_label = self.catalog_images2labels[image_path]

                # Get label_idx
                label_idx = self.catalog_labels.index(image_label)

                # Update score
                scores[label_idx] += scores_matrix[ind, k]

        return scores

    def _compute_query_matches(self, query_descriptors):
        # Init matches variables
        n_matches = query_descriptors.shape[0]
        train_idx = np.zeros((n_matches, self.config.k_nn))
        distances = np.zeros((n_matches, self.config.k_nn))

        # Compute matches
        for i, descriptor in enumerate(query_descriptors):
            idx, dist = self.matcher.get_nns_by_vector(
                descriptor,
                self.config.k_nn,
                include_distances=True)
            train_idx[i] = idx
            distances[i] = dist

        return train_idx, distances

    def _compute_scores_matrix(self, distances):
        if self.config.scoring == "distance":
            return self._compute_scores_matrix_distance(distances)
        if self.config.scoring == "count":
            return self._compute_scores_matrix_count(distances)
        return self._compute_scores_matrix_distance(distances)

    def _compute_scores_matrix_distance(self, distances):
        return np.exp(-distances ** 2)

    def _compute_scores_matrix_count(self, distances):
        scores_matrix = np.zeros(distances.shape)
        for k in range(self.config.k_nn):
            scores_matrix[:, k] = 1 - k / self.config.k_nn
        return scores_matrix

    ##########################
    # Utils
    ##########################

    def label_id2str(self, label_id: int) -> str:
        """Gets the label_str given the label_id.

        Args:
            label_id (int): The given label_id.

        Returns:
            str: The label_str of the given label_id.
        """
        return self.catalog_labels[label_id]

    def label_str2id(self, label_str: str) -> int:
        """Gets the label_id given the label_str.

        Args:
            label_str (str): The given label_str.

        Returns:
            int: The label_id of the given label_id.
        """
        if label_str in self.catalog_labels:
            return self.catalog_labels.index(label_str)
        return -1
