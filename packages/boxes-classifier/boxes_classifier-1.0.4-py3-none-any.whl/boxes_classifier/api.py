from PIL import Image
from scipy.spatial.distance import cdist
from boxes_classifier.core.config import cfg


if cfg.USE_TF_MODEL:
    from boxes_classifier.core.inference import (
        init_model, resize_with_padding, init_answer_embeddings, processing_image, \
        expand_dims, is_valid
    )

    model = init_model()
    [id_to_name, name_to_id, answer_embeddings] = init_answer_embeddings(cfg)
else:
    answer_embeddings = ""


def get_types():
    types = ["answer", "hint"]
    return types


def is_boxes_answer(image, threshold, distance):
    image = Image.fromarray(image).convert("RGB")
    image = resize_with_padding(image, (384, 384))
    image = processing_image(image=image)
    emb = model.predict(expand_dims(image, axis=0))
    D = sorted(cdist(answer_embeddings, emb, "cosine"))
    return is_valid(D, threshold, distance)