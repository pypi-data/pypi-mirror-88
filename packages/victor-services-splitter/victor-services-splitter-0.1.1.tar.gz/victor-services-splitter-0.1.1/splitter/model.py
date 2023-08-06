from tensorflow.keras.models import load_model

from .image_preprocessing import preprocess_image
from .prediction_utils import group_predictions, round_predictions

import splitter
import os

SPLITTER_PATH = splitter.__file__.replace('__init__.py', '')
MODELS_PATH = os.path.join(SPLITTER_PATH, 'models')
MODEL_PAGE_IMAGE_FEATURES_PATH = os.path.join(MODELS_PATH,
                                              'splitter_image_features.h5')
MODEL_PAGE_CLASSIFICATION_PATH = os.path.join(MODELS_PATH, 'splitter_image_classification.h5')


class ModelSplitter():
    def __init__(self,
                 model_page_image_features_path=MODEL_PAGE_IMAGE_FEATURES_PATH,
                 model_page_classification_path=MODEL_PAGE_CLASSIFICATION_PATH):
        self.model_page_image_features_path = model_page_image_features_path
        self.model_page_classification_path = model_page_classification_path

        self.model_page_image_features = load_model(
            self.model_page_image_features_path
            )
        self.model_page_classification = load_model(
            self.model_page_classification_path
            )
        self.num_channels = 3
        self.image_size = [224, 224]
        self.label2idx = {'FirstPage': 1, 'NextPage': 0}
        # self.idx2label = {1: 'FirstPage', 0: 'NextPage'}

    def predict_page_features(self, page_image):
        return self.model_page_image_features.predict_step(page_image)

    def predict_class_from_features(self, page_features, prev_page_features):
        return self.model_page_classification.predict_step(
            data=[page_features, prev_page_features]
            )[0][0].numpy()

    def predict_pdf_pages(self,
                          image_list,
                          has_to_group_predictions=False,
                          prediction_decimals=0):
        number_list = list(range(len(image_list)))

        page_dict = {number: {'image': image} for number, image in zip(number_list, image_list)}
        del image_list

        page_dict[number_list[0]]['prediction'] = 1

        for number, prev_number in zip(number_list[1:], number_list[:-1]):
            if 'features' not in page_dict[prev_number]:
                page_dict[prev_number]['features'] = self.predict_page_features(
                    preprocess_image(
                        page_dict[prev_number]['image'],
                        self.image_size,
                        self.num_channels
                        )
                    )
                del page_dict[prev_number]['image']

            page_dict[number]['features'] = self.predict_page_features(
                preprocess_image(
                    page_dict[number]['image'],
                    self.image_size,
                    self.num_channels
                    )
                )
            del page_dict[number]['image']

            page_dict[number]['prediction'] = self.predict_class_from_features(
                page_dict[number]['features'],
                page_dict[prev_number]['features']
                )

            del page_dict[prev_number]['features']
        if len(number_list) > 1: del page_dict[number_list[-1]]['features']

        prediction_list = [page['prediction'] for page in page_dict.values()]
        prediction_list = round_predictions(
            prediction_list,
            decimals=prediction_decimals
            )

        if has_to_group_predictions:
            return group_predictions(prediction_list)
        else:
            return prediction_list
