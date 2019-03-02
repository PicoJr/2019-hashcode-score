#!/usr/bin/env python

import argparse
import logging
from timeit import default_timer as timer


class Image(object):
    def __init__(self, image_id, orientation, tags):
        self.image_id = image_id
        self.orientation = orientation
        self.tags = set(tags)

    def __str__(self):
        return str(self.image_id)

    @staticmethod
    def score(images):
        """
        :param images: [VVVV] | [HVV] | [VVH] | [HH]
        :return: score
        """
        assert 1 < len(images) <= 4, images
        orientations = ''.join(img.orientation for img in images)
        if orientations == 'VVVV':
            tags_set = images[0].tags | images[1].tags
            other_tags_set = images[2].tags | images[3].tags
        elif orientations == 'HVV':
            tags_set = images[0].tags
            other_tags_set = images[1].tags | images[2].tags
        elif orientations == 'VVH':
            tags_set = images[0].tags | images[1].tags
            other_tags_set = images[2].tags
        else:  # 'HH'
            assert orientations == 'HH'
            tags_set = images[0].tags
            other_tags_set = images[1].tags
        return Image.score_tags(tags_set, other_tags_set)

    @staticmethod
    def score_tags(tags_set, other_tags_set):
        return min(len(tags_set - other_tags_set), len(other_tags_set - tags_set), len(tags_set & other_tags_set))

    @staticmethod
    def parse_input(input_file_path):
        """
        Parse input file
        :param input_file_path: input file path
        :return: Image list
        """
        verticals, horizontals = 0, 0
        logging.info("parsing %s", input_file_path)
        with open(input_file_path, 'r') as input_file:
            nb = int(input_file.readline())  # images nb
            images = []
            for i, img_txt in enumerate(input_file.readlines()):
                data = img_txt.rstrip().split(' ')
                orientation = data[0]
                tags = data[2:]
                images.append(Image(i, orientation, set(tags)))
                if orientation == 'V':
                    verticals += 1
                else:  # H
                    horizontals += 1
            logging.info('parsing %s done', input_file_path)
            logging.info('%d images found (%d V,%d H)', nb, verticals, horizontals)
            return images

    @staticmethod
    def parse_output(output_file_path):
        """
        Parse output file
        :param output_file_path: output file path (solution)
        :return: Image list ((Image, None)|(Image, Image)) list
        """
        logging.info("parsing %s", output_file_path)
        slides = []
        with open(output_file_path, 'r') as output_file:
            _ = output_file.readline()  # slide show size
            for line in output_file.readlines():
                image_id_tuple = tuple((int(image_id) for image_id in line.rstrip().split(' ')))
                if len(image_id_tuple) == 2:
                    img0 = Image(image_id_tuple[0], "V", [])
                    img1 = Image(image_id_tuple[1], "V", [])
                    slides.append((img0, img1))
                else:
                    img = Image(image_id_tuple[0], "H", [])
                    slides.append((img, None))
        logging.info("parsing %s: done", output_file_path)
        return slides

    @staticmethod
    def compute_score_slides(slides, images):
        previous = []
        score = 0
        for img0, img1 in slides:
            img_scored = previous + [img0]
            img0.tags = images[img0.image_id].tags
            if img1 is not None:  # VV
                img1.tags = images[img1.image_id].tags
                img_scored.append(img1)
            if previous:
                score += Image.score(img_scored)
            previous = [img0, img1] if img1 is not None else [img0]
        return score


def set_log_level(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='print score',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_file_path', type=str, help='input file path e.g. a_example.in')
    parser.add_argument('output_file_path', type=str, help='output file path e.g. a_example.out')
    parser.add_argument('--debug', action='store_true', help='for debug purpose')
    args = parser.parse_args()
    set_log_level(args)

    start = timer()
    images = Image.parse_input(args.input_file_path)
    end = timer()

    logging.debug('parsing input took %s s', end - start)

    start = timer()
    slides = Image.parse_output(args.output_file_path)
    end = timer()
    logging.debug('parsing output took %s s', end - start)

    start = timer()
    score = Image.compute_score_slides(slides, images)
    end = timer()
    logging.debug('computing score took %s s', end - start)

    print("score : {0:,}".format(score))


if __name__ == '__main__':
    main()
