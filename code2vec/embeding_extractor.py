import os
import numpy as np
import pickle

from code2vec.extractor import Extractor
from models import JavaFile, PatternPrediction, Pattern

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = 'code2vec/JavaExtractor/JPredict/JavaExtractor-0.0.1-SNAPSHOT.jar'


class EmbeddingExtractor:
    java_patterns = {
        'adapter': 'code2vec/JavaPatterns/adapter/',
        'builder': 'code2vec/JavaPatterns/builder/',
        'prototype': 'code2vec/JavaPatterns/prototype/',
        'singleton': 'code2vec/JavaPatterns/singleton/',
    }
    code_to_pattern = {
        0: Pattern.ADAPTER,
        1: Pattern.BUILDER,
        2: Pattern.PROTOTYPE,
        3: Pattern.SINGLETON
    }

    def __init__(self, config, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(config,
                                        jar_path=JAR_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)
        with open('classifier_config.pkl', 'rb') as f:
            self.classifier = pickle.load(f)

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    def extract_embeddings_from_request(self, java_file: JavaFile):
        input_filename = java_file.className
        # 1 save file on disk
        with open(input_filename, 'w') as file:
            file.write(java_file.classText)
        # 2 extract embedding
        code_vectors = []
        predicted_pattern = Pattern.NONE
        try:
            predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(input_filename)
            raw_prediction_results = self.model.predict(predict_lines)
            for raw_prediction in raw_prediction_results:
                code_vectors.append(raw_prediction.code_vector)
            mean_vector = np.mean(code_vectors, axis=0)
            mean_vector = mean_vector.reshape(1, -1)
        # 3 send embedding to classifier
            predicted_pattern = self.code_to_pattern[self.classifier.predict_proba(mean_vector).argmax(axis=1).item()]
            print(self.classifier.predict_proba(mean_vector))
            print(self.code_to_pattern[self.classifier.predict_proba(mean_vector).argmax(axis=1).item()])
        except ValueError as e:
            print(e)
        # 4 delete file
        if os.path.exists(input_filename):
            os.remove(input_filename)
            print("File deleted successfully.")
        else:
            print("File does not exist.")
        # 5 return answer
        return PatternPrediction(
            packagePath=java_file.packagePath,
            className=java_file.className,
            predictedPattern=predicted_pattern
        )
