import json
import logging
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm

from ....common import blue_color_generator, hex_to_rgb, id2rgb
from ....pycocotools_sa.coco import COCO
from ....pycocotools_sa import mask as maskUtils

logger = logging.getLogger("superannotate-python-sdk")


def _rle_to_polygon(coco_json, annotation):
    coco = COCO(coco_json)
    binary_mask = coco.annToMask(annotation)
    contours, _ = cv2.findContours(
        binary_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    segmentation = []

    for contour in contours:
        contour = contour.flatten().tolist()
        if len(contour) > 4:
            segmentation.append(contour)
        if len(segmentation) == 0:
            continue
    return segmentation


def coco_panoptic_segmentation_to_sa_pixel(coco_path, images_path):
    coco_json = json.load(open(coco_path))
    hex_colors = blue_color_generator(len(coco_json["categories"]))
    annotate_list = coco_json["annotations"]

    cat_id_to_cat = {}
    for cat in coco_json['categories']:
        cat_id_to_cat[cat['id']] = cat['name']

    sa_jsons = {}
    for annotate in tqdm(annotate_list, "Converting annotations"):
        annot_name = Path(annotate["file_name"]).stem
        img_cv = cv2.imread(str(images_path / (annot_name + ".png")))
        if img_cv is None:
            logger.warning(
                "'{}' file dosen't exist!".format(
                    images_path / (annot_name + ".png")
                )
            )
            continue

        img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        H, W, C = img.shape
        img = img.reshape((H * W, C))
        segments = annotate["segments_info"]
        hex_colors = blue_color_generator(len(segments))

        out_json = []
        for i, seg in enumerate(segments):
            img[np.all(img == id2rgb(seg["id"]),
                       axis=1)] = hex_to_rgb(hex_colors[i])
            dd = {
                "classId": seg["category_id"],
                'className': cat_id_to_cat[seg["category_id"]],
                "probability": 100,
                "visible": True,
                "parts": [{
                    "color": hex_colors[i]
                }],
                "attributes": [],
                "attributeNames": [],
                "imageId": annotate["image_id"]
            }
            out_json.append(dd)

        img = cv2.cvtColor(img.reshape((H, W, C)), cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(images_path / (annot_name + ".jpg___save.png")), img)

        file_name = annot_name + ".jpg___pixel.json"
        sa_jsons[file_name] = out_json
        (images_path / (annot_name + ".png")).unlink()
    return sa_jsons


def coco_instance_segmentation_to_sa_pixel(coco_path, images_path):
    coco_json = json.load(open(coco_path))
    cat_id_to_cat = {}
    for cat in coco_json['categories']:
        cat_id_to_cat[cat['id']] = cat

    images_dict = {}
    for img in coco_json['images']:
        images_dict[str(img['id'])] = {
            'mask': np.zeros((img['height'], img['width'], 4)),
            'file_name': img['file_name'],
            'segments_num': 0
        }

    sa_json = {}
    hexcolors = blue_color_generator(len(coco_json['annotations']))
    for i, annot in enumerate(coco_json['annotations']):
        if str(annot['image_id']) not in images_dict:
            continue

        hexcolor = hexcolors[images_dict[str(annot['image_id'])]['segments_num']
                            ]
        color = hex_to_rgb(hexcolor)
        images_dict[str(annot['image_id'])]['segments_num'] += 1

        H, W, _ = images_dict[str(annot['image_id'])]['mask'].shape
        if isinstance(annot['segmentation'], dict):
            if isinstance(annot['segmentation']['counts'], list):
                annot['segmentation'] = _rle_to_polygon(coco_path, annot)
                for segment in annot['segmentation']:
                    bitmask = np.zeros((H, W)).astype(np.uint8)
                    pts = np.array(
                        [
                            segment[2 * i:2 * (i + 1)]
                            for i in range(len(segment) // 2)
                        ],
                        dtype=np.int32
                    )

                    cv2.fillPoly(bitmask, [pts], 1)
                    images_dict[str(
                        annot['image_id']
                    )]['mask'][bitmask == 1] = list(color)[::-1] + [255]
            else:
                images_dict[str(
                    annot['image_id']
                )]['mask'][maskUtils.decode(annot['segmentation']) == 1
                          ] = list(color)[::-1] + [255]
        else:
            for segment in annot['segmentation']:
                bitmask = np.zeros((H, W)).astype(np.uint8)
                pts = np.array(
                    [
                        segment[2 * i:2 * (i + 1)]
                        for i in range(len(segment) // 2)
                    ],
                    dtype=np.int32
                )

                cv2.fillPoly(bitmask, [pts], 1)
                images_dict[str(
                    annot['image_id']
                )]['mask'][bitmask == 1] = list(color)[::-1] + [255]

        sa_obj = {
            "classId": annot['category_id'],
            "className": cat_id_to_cat[annot['category_id']]['name'],
            'probability': 100,
            'visible': True,
            'parts': [{
                'color': hexcolor
            }],
            "attributes": [],
            "attributeNames": [],
            "imageId": annot["image_id"]
        }

        key = images_dict[str(annot['image_id'])]['file_name']
        if key not in sa_json.keys():
            sa_json[key] = []

        sa_json[key].append(sa_obj)

    for _, value in images_dict.items():
        img = cv2.imwrite(
            str(images_path / (value['file_name'] + '___save.png')),
            value['mask']
        )

    sa_jsons = {}
    for key, sa_js in sa_json.items():
        file_name = key + '___pixel.json'
        sa_jsons[file_name] = sa_js
    return sa_jsons
