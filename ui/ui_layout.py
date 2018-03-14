from PyQt5.QtCore import QPointF, QRect
from PyQt5.QtWidgets import QPushButton, QLabel


def build_layout_dictionary(screen_width, screen_height):
    screen_pt = QPointF(screen_width, screen_height)

    border = screen_pt * 0.05
    circle_button_diameter = screen_width * 0.1875
    circle_2_button_diameter = screen_width * 0.4
    box_button_size = screen_pt * 0.2
    button_border_width = screen_height / 500
    circle_border_radius = circle_button_diameter / 2
    circle_border_radius_2 = circle_2_button_diameter / 2

    circle_stylesheet = "QPushButton{\n" \
                        "background-color:qlineargradient" \
                        "(x1: 0, y1: 0, x2: 0, y2: 2, stop: 0 white, stop: 1 grey);\n" \
                        "border-style: solid;\n" \
                        "border-color: black;\n" \
                        "border-width: " + str(button_border_width) + "px;\n" \
                        "border-radius: " + str(circle_border_radius) + "px;\n" \
                        "font-size: 30pt;\n" \
                        "font-weight: bold;\n" \
                        "}"

    big_circle_stylesheet = "QPushButton{\n" \
                        "background-color:qlineargradient" \
                        "(x1: 0, y1: 0, x2: 0, y2: 2, stop: 0 white, stop: 1 grey);\n" \
                        "border-style: solid;\n" \
                        "border-color: black;\n" \
                        "border-width: " + str(button_border_width) + "px;\n" \
                        "border-radius: " + str(circle_border_radius_2) + "px;\n" \
                        "font-size: 30pt;\n" \
                        "font-weight: bold;\n" \
                        "}"

    box_stylesheet = "QPushButton{\n" \
                     "border-style: solid;\n" \
                     "border-color: black;\n" \
                     "border-width: " + str(button_border_width) + "px;\n" \
                     "border-radius: 0px;\n" \
                     "font-size: 30pt;\n" \
                     "font-weight: bold;\n" \
                     "}"

    label_stylesheet = "QLabel{\n" \
                     "background-color: white;\n" \
                     "qproperty-alignment: AlignCenter;\n" \
                     "font-size: 30pt;\n" \
                     "font-weight: bold;\n" \
                     "}"

    eight_button_elements = {
        'pushButton_1': {
            'top_left_x': border.x(),
            'top_left_y': screen_height - 2 * (border.y() + circle_button_diameter),
            'width': circle_button_diameter,
            'height': circle_button_diameter,
            'label': 1
        },
        'pushButton_2': {
            'top_left_x': border.x() + (border.x() + circle_button_diameter),
            'top_left_y': screen_height - 2 * (border.y() + circle_button_diameter),
            'width': circle_button_diameter,
            'height': circle_button_diameter,
            'label': 2
        },
        'pushButton_3': {
            'top_left_x': border.x() + 2 * (border.x() + circle_button_diameter),
            'top_left_y': screen_height - 2 * (border.y() + circle_button_diameter),
            'width': circle_button_diameter,
            'height': circle_button_diameter,
            'label': 3
        },
        'pushButton_4': {
            'top_left_x': border.x() + 3 * (border.x() + circle_button_diameter),
            'top_left_y': screen_height - 2 * (border.y() + circle_button_diameter),
            'width': circle_button_diameter,
            'height': circle_button_diameter,
            'label': 4
        },
        'pushButton_5': {
            'top_left_x': border.x(),
            'top_left_y': screen_height - (border.y() + circle_button_diameter),
            'width': circle_button_diameter,
            'height': circle_button_diameter,
            'label': 5
        },
        'pushButton_6': {
            'top_left_x': border.x() + (border.x() + circle_button_diameter),
            'top_left_y': screen_height - (border.y() + circle_button_diameter),
            'width': circle_button_diameter,
            'height': circle_button_diameter,
            'label': 6
        },
        'pushButton_7': {
            'top_left_x': border.x() + 2 * (border.x() + circle_button_diameter),
            'top_left_y': screen_height - (border.y() + circle_button_diameter),
            'width': circle_button_diameter,
            'height': circle_button_diameter,
            'label': 7
        },
        'pushButton_8': {
            'top_left_x': border.x() + 3 * (border.x() + circle_button_diameter),
            'top_left_y': screen_height - (border.y() + circle_button_diameter),
            'width': circle_button_diameter,
            'height': circle_button_diameter,
            'label': 8
        },
        'topLeftButton': {
            'top_left_x': 0,
            'top_left_y': 0,
            'width': box_button_size.x(),
            'height': box_button_size.y(),
            'label': 9
        },
        'topRightButton': {
            'top_left_x': screen_width - box_button_size.x(),
            'top_left_y': 0,
            'width': box_button_size.x(),
            'height': box_button_size.y(),
            'label': 10
        },
        'textLabel': {
            'top_left_x': box_button_size.x(),
            'top_left_y': 0,
            'width': screen_width - 2 * box_button_size.x(),
            'height': box_button_size.y(),
            'label': 0
        }
    }

    two_button_elements = {
        'pushButton_1_big': {
            'top_left_x': border.x(),
            'top_left_y': screen_height - (border.y() + circle_2_button_diameter),
            'width': circle_2_button_diameter,
            'height': circle_2_button_diameter,
            'label': 1
        },
        'pushButton_2_big': {
            'top_left_x': screen_width - (border.x() + circle_2_button_diameter),
            'top_left_y': screen_height - (border.y() + circle_2_button_diameter),
            'width': circle_2_button_diameter,
            'height': circle_2_button_diameter,
            'label': 2
        },
        'topLeftButton': {
            'top_left_x': 0,
            'top_left_y': 0,
            'width': box_button_size.x(),
            'height': box_button_size.y(),
            'label': 9
        },
        'topRightButton': {
            'top_left_x': screen_width - box_button_size.x(),
            'top_left_y': 0,
            'width': box_button_size.x(),
            'height': box_button_size.y(),
            'label': 10
        },
        'textLabel': {
            'top_left_x': box_button_size.x(),
            'top_left_y': 0,
            'width': screen_width - 2 * box_button_size.x(),
            'height': box_button_size.y(),
            'label': 0
        }
    }

    return {
        'width': screen_width,
        'height': screen_height,
        'border': border,
        'circle_stylesheet': circle_stylesheet,
        'big_circle_stylesheet': big_circle_stylesheet,
        'box_stylesheet': box_stylesheet,
        'label_stylesheet': label_stylesheet,
        'eight_button_elements': eight_button_elements,
        'two_button_elements': two_button_elements

    }


def build_layout_element(parent, layout, element_name, num_elements=8):
    element_set = 'eight_button_elements' if num_elements == 8 else 'two_button_elements'

    elem_layout = layout[element_set][element_name]

    if 'Button' in element_name:
        button = QPushButton(parent)

        button.setGeometry(QRect(elem_layout['top_left_x'], elem_layout['top_left_y'],
                                 elem_layout['width'], elem_layout['height']))

        if 'big' in element_name:
            stylesheet = layout['big_circle_stylesheet'] if element_name.startswith('pushButton') else layout[
                'box_stylesheet']
        else:
            stylesheet = layout['circle_stylesheet'] if element_name.startswith('pushButton') else layout['box_stylesheet']
        button.setStyleSheet(stylesheet)

        button.setObjectName(element_name)

        return button

    elif element_name.startswith('text'):
        label = QLabel(parent)

        label.setGeometry(QRect(elem_layout['top_left_x'], elem_layout['top_left_y'],
                                  elem_layout['width'], elem_layout['height']))

        stylesheet = layout['label_stylesheet']
        label.setStyleSheet(stylesheet)

        label.setText("")
        label.setObjectName(element_name)

        return label

    else:
        return None
