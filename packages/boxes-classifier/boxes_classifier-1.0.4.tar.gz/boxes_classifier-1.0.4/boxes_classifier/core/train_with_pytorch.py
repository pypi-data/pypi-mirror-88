import numpy as np

from torch.utils.data import DataLoader
from torchvision import transforms
from efficientnet_pytorch import EfficientNet
from tqdm import tqdm
from boxes_classifier import cfg
from boxes_classifier.core.datasets import BoxesDataset
from boxes_classifier.core.embedding import Embedding


class Trainer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.transform = transforms.Compose([transforms.Resize(224), transforms.ToTensor(),
                                   transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        self.npy = []

    @staticmethod
    def init_model():
        model = EfficientNet.from_pretrained('efficientnet-b0')
        embedding = Embedding()
        return model, embedding

    def train(self):
        model, embedding = self.init_model()
        model.eval()
        train_dataset = BoxesDataset(cfg, transform=self.transform)
        train_loader = DataLoader(train_dataset, batch_size=cfg.BATCH_SIZE * len(cfg.GPUS),
                                       num_workers=6, shuffle=True, pin_memory=True, drop_last=True)
        save_npy = []
        for i_iter, batch in tqdm(enumerate(train_loader)):
            name, idx, sample = batch["name"], batch["id"], batch["sample"]
            features = model.extract_features(sample)
            features = embedding(features)
            save_npy.append(features.detach().numpy())
        self.compute_save_embeddings(save_npy)

    @staticmethod
    def compute_save_embeddings(save_npy):
        # idx = idx.detach().numpy()
        # id_to_name = np.array([*dict(zip(idx, name)).items()])
        # name_to_id = np.array([*dict(zip(name, idx)).items()])
        # embedding = embedding.detach().numpy()
        # my_data = np.concatenate([name_to_id, id_to_name, embedding], axis=1)
        np.save(f"{cfg.PATH_TORCH_EMBEDDING_ANSWER}/Emb.npy", np.array(save_npy))
        print("Save Model Sucessful")

if __name__ == '__main__':
    trainer = Trainer(cfg=cfg)
    trainer.train()

    # from numpy import genfromtxt
    # my_data = genfromtxt('/media/duongpd/Data/SF_EDU/Embeding.csv', delimiter=',')
    # np.save(f"{cfg.PATH_TORCH_EMBEDDING_ANSWER}/Emb.npy", my_data)
    # my_data = np.load("Emb.npy")
    # print(my_data.shape)
