import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath) + "/code2vec"
os.chdir(dname)

from code2vec.config import Config
from code2vec.model_base import Code2VecModelBase
from code2vec.extractor import Extractor
from code2vec.common import common

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'

def load_model_dynamically(config: Config) -> Code2VecModelBase:
    assert config.DL_FRAMEWORK in {'tensorflow', 'keras'}
    if config.DL_FRAMEWORK == 'tensorflow':
        from code2vec.tensorflow_model import Code2VecModel
    elif config.DL_FRAMEWORK == 'keras':
        from code2vec.keras_model import Code2VecModel
    return Code2VecModel(config)

if __name__ == '__main__':
    config = Config(set_defaults=True, load_from_args=True)
    config.MODEL_LOAD_PATH = "models/java14_model/saved_model_iter8.release"
    config.EXPORT_CODE_VECTORS = True

    path_extractor = Extractor(config, jar_path=JAR_PATH, max_path_length=MAX_PATH_LENGTH, max_path_width=MAX_PATH_WIDTH)

    model = load_model_dynamically(config)
    config.log('Done creating code2vec model')

    input_filename = 'Input.java'
    try:
        predict_lines, hash_to_string_dict = path_extractor.extract_paths(input_filename)
    except ValueError as e:
        print(e)
        exit(1)
    print(predict_lines)
    raw_prediction_results = model.predict(predict_lines)
    method_prediction_results = common.parse_prediction_results(raw_prediction_results, hash_to_string_dict, model.vocabs.target_vocab.special_words, topk=SHOW_TOP_CONTEXTS)
    for raw_prediction, method_prediction in zip(raw_prediction_results, method_prediction_results):
        print('Original name:\t' + method_prediction.original_name)
        for name_prob_pair in method_prediction.predictions:
            print('\t(%f) predicted: %s' % (name_prob_pair['probability'], name_prob_pair['name']))
            print('Attention:')
        for attention_obj in method_prediction.attention_paths:
            print('%f\tcontext: %s,%s,%s' % (attention_obj['score'], attention_obj['token1'], attention_obj['path'], attention_obj['token2']))
        print('Code vector:')
        print(raw_prediction.code_vector.size)
        print(' '.join(map(str, raw_prediction.code_vector)))
    model.close_session()