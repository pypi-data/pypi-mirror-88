import tensorflow as tf
import image_embeddings
from efficientnet.tfkeras import EfficientNetB0
from scipy.spatial.distance import cdist
from PIL import Image, ImageOps
import numpy as np

from boxes_classifier.core.utils import resize_with_padding


def init_model():
    model = EfficientNetB0(weights="imagenet", include_top=False, pooling="avg")
    return model


def init_answer_embeddings(cfg):
    return image_embeddings.knn.read_embeddings(cfg.PATH_EMBEDDING_ANSWER)


def processing_image(image):
    image = np.array(image)
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image


def expand_dims(image, axis=0):
    return tf.expand_dims(image, axis=axis)


def is_valid(D, threshold=0.1, sub=100):
    check = D[:sub]
    check = np.array(check)
    check = np.where(check < threshold, True, False)
    check = np.squeeze(check)
    return all(check)


if __name__ == '__main__':
    import os

    model = init_model()
    path_embeddings = '/media/duongpd/Data/SF_EDU/boxes_classifier/data/model/embeddings'
    [id_to_name, name_to_id, embeddings] = image_embeddings.knn.read_embeddings(path_embeddings)
    import cv2
    for i in os.listdir('/media/duongpd/Data/smart_edu/templates_2/AI/val/images/'):
        image = Image.open(f"/media/duongpd/Data/smart_edu/templates_2/AI/val/images/{i}").convert('RGB')
        cv2.imshow('asda', np.array(image))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        image_cp = image.copy()
        image = resize_with_padding(image, (384, 384))
        image = np.array(image)
        image = processing_image(image=image)
        emb = model.predict(tf.expand_dims(image, axis=0))

        D = sorted(cdist(embeddings, emb, "cosine"))
        check = D[:100]
        check = np.array(check)
        check = np.where(check < 0.1, True, False)
        check = np.squeeze(check)
        print(check)
        # if all(check):
        #     image_cp.save(f"/media/duongpd/Data/smart_edu/templates_2/AI/val/good/{i}")
        # else:
        #     image_cp.save(f"/media/duongpd/Data/smart_edu/templates_2/AI/val/bad/{i}")
