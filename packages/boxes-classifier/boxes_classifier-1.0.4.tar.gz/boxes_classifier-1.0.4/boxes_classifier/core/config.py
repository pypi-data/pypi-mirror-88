import os


class Config:
    ROOT = os.path.dirname(os.path.dirname(__file__))
    ROOT_DIR = '/media/duongpd/Data/smart_edu/templates_2/AI/train/images'
    SIZE = (224, 224)
    PATH_EMBEDDING_ANSWER = f'{ROOT}/data/model/embeddings'
    PATH_TORCH_EMBEDDING_ANSWER = f'{ROOT}/data/model/torch_embeddings'

    NUM_SHARDS = 10
    BATCH_SIZE = 32
    DATASET = '/media/duongpd/Data/smart_edu/templates_2/AI/train'
    PATH_IMAGES = f"{DATASET}/images"
    PATH_IMAGES_SYNC = f"{DATASET}/images_sync"
    PATH_TFRECORDS = f"{DATASET}/tfrecords"
    PATH_EMBEDDINGS = f"{DATASET}/embeddings"
    GPUS = ["0"]
    USE_TF_MODEL = True


cfg = Config()
