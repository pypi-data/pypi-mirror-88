import click
import time
from PIL import Image

from boxes_classifier import is_boxes_answer, get_types


@click.command()
@click.option('--image_file', default='',
              help='image folder fed into network')
@click.option('--type', default='answer',
              help=f'list: e.g. model_default  [{get_types().__str__()}] for Model')
def main(image_file, type):
    try:
        image = Image.open(image_file).convert("RGB")
        print("Start Process")
        t1 = time.time()
        if type not in get_types():
            raise ValueError(f"Type must be valid [{get_types().__str__()}]")
        elif type == get_types()[0]:
            check = is_boxes_answer(image, 100)
            print(f"Check {type}: {check} - Total time: {time.time() - t1}")
    except Exception as e:
        print(e)