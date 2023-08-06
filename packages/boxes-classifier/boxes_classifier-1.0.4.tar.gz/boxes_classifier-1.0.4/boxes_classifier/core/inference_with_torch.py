import numpy as np
from PIL import Image


from efficientnet_pytorch import EfficientNet
from scipy.spatial.distance import cdist
from torchvision.transforms import transforms

from boxes_classifier.core.config import cfg
from boxes_classifier.core.embedding import Embedding
from boxes_classifier.core.sync_image import resize_with_padding


def init_model():
    model = EfficientNet.from_pretrained('efficientnet-b0')
    return model


def init_answer_embeddings():
    weights = np.load(f"{cfg.PATH_TORCH_EMBEDDING_ANSWER}/Emb.npy")
    weights = np.concatenate(weights, axis=0)
    return weights


if __name__ == '__main__':
    import os
    import torch

    transform = transforms.Compose([transforms.Resize(224), transforms.ToTensor(),
                                         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    model = init_model()
    model.eval()
    embedd = init_answer_embeddings()
    embedding = Embedding()
    print(embedd.shape)
    count = 0
    import cv2
    for i in os.listdir('/media/duongpd/Data/smart_edu/templates_2/AI/val/bad/'):
        image = Image.open(f"/media/duongpd/Data/smart_edu/templates_2/AI/val/bad /{i}").convert('RGB')
        image_cp = image.copy()
        image = resize_with_padding(image, cfg.SIZE)
        image = transform(image)
        image = torch.unsqueeze(image, dim=0)
        features = model.extract_features(image)
        emb = embedding(features)
        emb = emb.detach().numpy()
        D = sorted(cdist(embedd, emb, "cosine"))
        check = D[0:1]
        check = np.array(check)
        print(check)
        check = np.where(check < 0.62, True, False)
        check = np.squeeze(check)
        cv2.imshow('asda', np.array(image_cp))
        cv2.waitKey(0)
        cv2.destroyAllWindows()