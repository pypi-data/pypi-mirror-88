import numpy as np
import image_embeddings

from os import listdir
from PIL import Image
from tqdm import tqdm
from boxes_classifier import cfg, resize_with_padding


class Trainer:
    def __init__(self, cfg):
        self.cfg = cfg

    @staticmethod
    def normalized(a, axis=-1, order=2):
        l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
        l2[l2 == 0] = 1
        return a / np.expand_dims(l2, axis)

    @staticmethod
    def sync_images(size=(384, 384)):
        print("Process: Sync Image")

        for f in tqdm(listdir(cfg.PATH_IMAGES)):
            img = Image.open(f"{cfg.PATH_IMAGES}/{f}")
            img = resize_with_padding(img, size)
            img.save(f"{cfg.PATH_IMAGES_SYNC}/{f}")
        print(">>>> next step\n")

    def train(self):
        print('Start Training: >>> \n')
        image_embeddings.inference.write_tfrecord(image_folder=self.cfg.PATH_IMAGES_SYNC,
                                                  output_folder=self.cfg.PATH_TFRECORDS,
                                                  num_shards=self.cfg.NUM_SHARDS)
        image_embeddings.inference.run_inference(tfrecords_folder=self.cfg.PATH_TFRECORDS,
                                                 output_folder=self.cfg.PATH_EMBEDDINGS,
                                                 batch_size=self.cfg.BATCH_SIZE)
        print("Sucessful.")


if __name__ == '__main__':

    trainer = Trainer(cfg=cfg)
    trainer.sync_images()
    trainer.train()
    [id_to_name, name_to_id, embeddings] = image_embeddings.knn.read_embeddings(cfg.PATH_EMBEDDINGS)
