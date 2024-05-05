from config import Config
from embeding_extractor import EmbeddingExtractor
from tensorflow_model import Code2VecModel

if __name__ == '__main__':
    config = Config(set_defaults=True, verify=True)

    model = Code2VecModel(config)

    config.log('Done creating code2vec model')

    extractor = EmbeddingExtractor(config, model)
    extractor.extract_embeddings()

    model.close_session()