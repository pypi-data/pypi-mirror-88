import cv2
import numpy as np


def hex_to_rgb(hex_str: str) -> tuple:
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def draw_object_info(
        image: np.ndarray,
        render_board: np.ndarray,
        bbox: list,
        class_str: str,
        object_colors: list,
        tags: dict = None,
        color: tuple = (0, 255, 0),
        horizontal: bool = False):
    h, w = image.shape[:2]
    _bbox = np.array(bbox) * [w, h, w, h]
    _bbox = _bbox.astype(np.int32).tolist()

    image = cv2.rectangle(
        image,
        tuple(_bbox[:2]), tuple(_bbox[2:]),
        color=color, thickness=w // 200
    )

    render_board = cv2.rectangle(
        render_board,
        (0, 0), tuple(render_board.shape[:2][::-1]),
        color=color, thickness=w // 50
    )

    text = 'Name: {}'.format(class_str)
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = w / 900
    font_thickness = w // 400
    text_width, text_height = \
    cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    first_dy = 0.04 if not horizontal else 0.3

    render_board = cv2.putText(
        render_board,
        text,
        (int(render_board.shape[1] * 0.02),
         int(text_height + render_board.shape[0] * first_dy)),
        font,
        font_scale,
        (194, 24, 7),
        font_thickness,
        cv2.LINE_AA
    )

    sy = text_height + int(text_height + render_board.shape[0] * 0.08)
    if tags is not None:
        for tag_name in tags.keys():
            text = '{}: {}'.format(tag_name, tags[tag_name])
            text_width, text_height = \
            cv2.getTextSize(text, font, font_scale, font_thickness)[0]

            render_board = cv2.putText(
                render_board,
                text,
                (int(render_board.shape[1] * 0.02),
                 int(text_height + render_board.shape[0] * 0.02) + sy),
                font,
                font_scale,
                (31, 69, 252),
                font_thickness,
                cv2.LINE_AA
            )

            sy += text_height + int(text_height + render_board.shape[0] * 0.005)

    if horizontal:
        for i, ocl in enumerate(object_colors):
            colors_area_width = render_board.shape[1] // 2
            circle_d = colors_area_width // 5
            circle_r = circle_d // 2
            s = int(circle_r * 0.2)
            circle_r = int(circle_r * 0.8)

            render_board = cv2.circle(
                render_board,
                (
                    colors_area_width + s * 3 + i * (
                                colors_area_width // 5 - s) + circle_r,
                    render_board.shape[0] // 2
                ),
                circle_r - circle_r // 25,
                color=ocl,
                thickness=-1
            )

            render_board = cv2.circle(
                render_board,
                (
                    colors_area_width + s * 3 + i * (
                                colors_area_width // 5 - s) + circle_r,
                    render_board.shape[0] // 2
                ),
                circle_r,
                color=(21, 27, 31),
                thickness=circle_r // 10
            )
    else:
        for i, ocl in enumerate(object_colors):
            circle_d = int(render_board.shape[1] * 0.1)
            circle_r = circle_d // 2
            s = int(circle_r * 0.2)
            circle_r = int(circle_r * 0.8)

            render_board = cv2.circle(
                render_board,
                (
                    render_board.shape[1] - circle_r - s * 2,
                    s * 3 + i * (render_board.shape[0] // 5 - s) + circle_r
                ),
                circle_r - circle_r // 25,
                color=ocl,
                thickness=-1
            )

            render_board = cv2.circle(
                render_board,
                (
                    render_board.shape[1] - circle_r - s * 2,
                    s * 3 + i * (render_board.shape[0] // 5 - s) + circle_r
                ),
                circle_r,
                color=(21, 27, 31),
                thickness=circle_r // 10
            )


def draw_by_description(image: np.ndarray, description: dict,
                        render_size=(1200, 1000)) -> np.ndarray:
    _colors = [
        (255, 76, 148),
        (76, 255, 183),
        (76, 148, 255),
        (255, 183, 76)
    ]

    info_render = np.full((*render_size, 3), 255, dtype=np.uint8)

    rh, rw = info_render.shape[:2]

    item_window_h = rh // 5
    item_window_w = rw // 2
    item_window_x = rw - item_window_w
    item_window_y = 0

    render_image_area_width = rw - item_window_w
    render_image_area_height = rh

    image_h, image_w = image.shape[:2]
    image_resize_koeff = 1
    render_image_area_shifts = (0, 0)

    image_hw_koeff = image_h / image_w
    render_image_area_hw_koeff = render_image_area_height / render_image_area_width

    if image_hw_koeff > render_image_area_hw_koeff:
        image_resize_koeff = render_image_area_height / image_h
        new_image_width = int(image_w * image_resize_koeff)

        sx = (render_image_area_width - new_image_width) // 2

        info_render[:, sx:sx + new_image_width] = cv2.resize(
            image,
            (new_image_width, render_image_area_height),
            interpolation=cv2.INTER_AREA
        )

        render_image_area_shifts = (sx, 0)
    else:
        image_resize_koeff = render_image_area_width / image_w
        new_image_height = int(image_h * image_resize_koeff)

        sy = (render_image_area_height - new_image_height) // 2

        info_render[sy:sy + new_image_height,
        :render_image_area_width] = cv2.resize(
            image,
            (render_image_area_width, new_image_height),
            interpolation=cv2.INTER_AREA
        )

        render_image_area_shifts = (0, sy)

    render_image_shape = (
        int(image_h * image_resize_koeff),
        int(image_w * image_resize_koeff)
    )

    image_area = info_render[
                 render_image_area_shifts[1]:render_image_area_shifts[1] +
                                             render_image_shape[0],
                 render_image_area_shifts[0]:render_image_area_shifts[0] +
                                             render_image_shape[1]
                 ]

    if description['status'] != '0':
        return info_render

    for i, sample in enumerate(description['result']):
        y_shift = item_window_h
        horizontal = False
        description_render_area = info_render[
                                  item_window_y:item_window_y + item_window_h,
                                  item_window_x:
                                  ]

        if not 'tags' in sample.keys():
            y_shift = item_window_h // 4
            horizontal = True
            description_render_area = info_render[
                                      item_window_y:item_window_y + item_window_h // 4,
                                      item_window_x:
                                      ]

        draw_object_info(
            image_area,
            description_render_area,
            sample['bounding_box'],
            sample['category'],
            [hex_to_rgb(hcolor) for hcolor in sample['colors']],
            sample['tags'] if 'tags' in sample.keys() else None,
            _colors[i % len(_colors)],
            horizontal
        )

        info_render = cv2.line(
            info_render,
            (
                render_image_area_shifts[0] + int(
                    sample['bounding_box'][2] * render_image_shape[1]),
                render_image_area_shifts[1] + int(
                    sample['bounding_box'][1] * render_image_shape[0])
            ),
            (
                item_window_x,
                item_window_y
            ),
            color=_colors[i % len(_colors)],
            thickness=item_window_w // 200
        )

        item_window_y += y_shift

    return info_render
