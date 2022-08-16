"""
File: my_drawing
Name: Chin
----------------------
Title: OOOOOLAOLAOLAOLA
"""

from campy.graphics.gobjects import GOval, GRect, GLabel, GPolygon, GLine, GObject, GArc
from campy.graphics.gwindow import GWindow
from random import random, randint

window = GWindow(750, 420)


def main():
    """
    Title: JOJO said "OOOOLA x N"
    因為很想看 Jerry 學 JOJO 用很有氣勢的語氣說出： 歐歐歐歐歐拉歐拉歐拉歐拉歐拉!!!!
    """
    back_ground()
    hair()
    neck()
    face()
    left_eye_shadow()
    right_face_shadow()
    cap()
    cloth()


def back_ground():
    x_position = 0
    color_list = ("gray", "darkgray", "darkseagreen", "teal", "darkgray", "darkgray")
    while True:
        if x_position <= window.width:
            x_width = randint(1, 3)
            r = GRect(x_width, 450, x=x_position)
            r.filled = True
            r.fill_color = r.color = color_list[randint(0, 5)]
            window.add(r)
            x_position += x_width
        else:
            break

    back_ground_text("indigo", 75)


def back_ground_text(color, text_size):
    olaaa = GLabel("OOLA")
    olaaa.color = color
    olaaa.font = f"Dialog-{text_size}-bold"
    window.add(olaaa, 5, 120)

    for i in range(5):
        ola = GLabel("OLA")
        ola.color = color
        ola.font = f"Dialog-{text_size - i*10}-bold"
        window.add(ola, 5 + (i+1) * 25, 120 + (i+1) * (text_size - i*5))


def cloth():

    black_cloth_left = ((36, 420), (37, 400), (30, 391), (39, 370), (365, 275), (350, 420))
    yellow_cloth_left = ((36, 421), (37, 401), (30, 391), (39, 371), (360, 280), (361, 288), (348, 420))
    purple_cloth_left = ((36, 420), (37, 401), (56, 388), (340, 300), (345, 310), (345, 338), (330, 420))
    star = ((138, 420), (117, 402), (170, 389), (202, 350), (223, 381), (285, 375), (252, 420))

    black_cloth_right1 = ((647, 421), (679, 343), (750, 384), (750, 420))
    yellow_cloth_right1 = ((651, 421), (684, 353), (750, 387), (750, 420))
    purple_cloth_right1 = ((679, 421), (695, 388), (742, 420))

    yellow_cloth_right2 = ((750, 358), (721, 368), (730, 375), (750, 368))
    purple_cloth_right2 = ((730, 375), (750, 368), (750, 385))

    decomposed("black", black_cloth_left)
    decomposed("peru", yellow_cloth_left)
    decomposed("indigo", purple_cloth_left)
    decomposed("peru", star)
    decomposed("peru", yellow_cloth_right2)
    decomposed("indigo", purple_cloth_right2)
    decomposed("black", black_cloth_right1)
    decomposed("peru", yellow_cloth_right1)
    decomposed("indigo", purple_cloth_right1)


def neck():
    neck_right_back = ((550, 421), (582, 401), (654, 408), (646, 421))
    neck_left = ((276, 420), (277, 251), (287, 260), (305, 268), (310, 262), (317, 328), (397, 420))
    neck_right = ((521, 421), (592, 338), (577, 421))

    decomposed("saddlebrown", neck_right_back)
    decomposed("saddlebrown", neck_left)
    decomposed("saddlebrown", neck_right)


def hair():
    hair1 = ((250, 421), (250, 288), (247, 244), (234, 224), (248, 231), (242, 218),
             (247, 199), (262, 137), (244, 75), (252, 18), (257, 28), (263, 0), (390, 0),
             (337, 70), (338, 87), (344, 88), (327, 120), (322, 131), (312, 157), (317, 421))
    decomposed("indigo", hair1)


def cap():

    upper = ((343, 0), (336, 43), (520, 50), (590, 64), (678, 99), (701, 0))
    front_edge = ((313, 45), (309, 56), (417, 95), (590, 105), (682, 125),
                  (750, 153), (750, 126), (686, 110), (626, 93), (424, 70), (314, 41))
    front_edge_up = ((333, 51), (333, 41), (412, 37), (412, 44), (533, 50), (690, 90),
                     (750, 125), (750, 131), (681, 113), (613, 91), (435, 84))
    cap_link = ((342, 21), (328, 22), (322, 36), (330, 50), (347, 54))
    cap_link_inside = ((336, 29), (333, 28), (330, 40), (332, 42), (340, 46))
    cap_pic = ((391, 0), (376, 32), (429, 30), (463, 0))
    cap_pic2 = ((401, 0), (386, 32), (419, 30), (453, 0))
    cap_pic_right = ((599, -1), (589, 53), (658, 79), (675, 53), (684, -1))
    cap_pic_right2 = ((589, -1), (579, 53), (589, 53), (599, -1))
    cap_chain = ((334, 37), (334, 33), (413, 27), (534, 36), (655, 73), (695, 85), (696, 95), (649, 85), (534, 57),
                 (413, 43))
    cap_chain2 = ((413, 25), (534, 34), (663, 75), (651, 88), (547, 60), (412, 45))

    decomposed("indigo", upper)
    decomposed("teal", front_edge)
    decomposed("indigo", front_edge_up)
    decomposed("peru", cap_link)
    decomposed("black", cap_link_inside)
    decomposed("peru", cap_pic)
    decomposed("teal", cap_pic2)
    decomposed("saddlebrown", cap_pic_right, line1=True)
    decomposed("peru", cap_pic_right2, line1=True)
    decomposed("peru", cap_chain)
    decomposed("peru", cap_chain2)

    cap_circle_inside = GOval(30, 40, x=298, y=30)
    cap_circle_inside.filled = True
    cap_circle_inside.fill_color = "peru"
    window.add(cap_circle_inside)

    cap_circle_inside = GOval(20, 30, x=302, y=35)
    cap_circle_inside.filled = True
    cap_circle_inside.fill_color = "peru"
    window.add(cap_circle_inside)


def face():
    right_ear = ((646, 195), (661, 195), (659, 255), (618, 328), (598, 330))
    face1 = ((397, 421), (317, 346), (308, 267), (305, 268), (283, 258), (241, 183), (283, 116),
             (310, 139), (310, 158), (340, 89), (337, 78), (340, 60), (662, 114), (666, 125),
             (647, 169), (646, 195), (627, 249), (592, 354), (532, 421))

    lower_face = ((397, 421), (317, 346), (308, 267), (305, 268), (283, 258), (246, 220), (241, 183), (247, 164),
                  (283, 116), (310, 139), (310, 158), (329, 110), (344, 111), (393, 168), (488, 171), (520, 150),
                  (543, 158), (550, 215), (530, 225), (510, 216), (479, 239), (490, 249), (497, 270), (488, 269),
                  (468, 279), (455, 282), (435, 296), (458, 298), (487, 289), (505, 301), (524, 300), (537, 319),
                  (548, 326), (546, 310), (550, 281), (548, 271), (571, 234), (567, 204), (569, 186), (607, 209),
                  (637, 207), (619, 241), (588, 326), (572, 358), (510, 420))

    lower_lip = ((435, 296), (458, 298), (487, 289), (505, 301), (524, 300), (537, 319),
                 (548, 326), (548, 325), (537, 318), (524, 299), (505, 300), (487, 288), (458, 297), (435, 295))

    jaw = ((423, 316), (444, 310), (454, 321), (516, 336), (531, 335), (538, 329), (547, 347), (522, 365),
           (514, 350), (464, 336), (438, 338))

    jaw_1 = ((401, 420), (418, 412), (435, 410), (460, 411), (489, 420))

    left_ear = ((299, 180), (296, 162), (288, 156), (279, 130), (283, 136), (262, 172), (262, 191), (279, 218),
                (299, 237), (308, 256), (304, 214), (288, 200))

    decomposed("sienna", right_ear, line1=True)
    decomposed("sienna", face1, line1=True)
    decomposed("peachpuff", lower_face, line1=True)
    decomposed("black", lower_lip, line1=True)
    decomposed("sienna", jaw, line1=True)
    decomposed("sienna", jaw_1, line1=True)
    decomposed("sienna", left_ear, line1=True)

    left_earring = GOval(10, 10, x=285, y=242)
    left_earring.filled = True
    left_earring.fill_color = "peru"
    window.add(left_earring)


def left_eye_shadow():
    for i in range(10):
        x0 = 330
        y0 = 120
        left_eye_shadow1 = GLine(x0 - i, y0 + i * 2.5,
                                (x0 + 25) - i, (y0 + 17) + i * 2.5)
        window.add(left_eye_shadow1)

    for i in range(5):
        x0 = 320
        y0 = 145
        left_eye_shadow1 = GLine(x0 + i, y0 + i * 4,
                                (x0 + 25) + i, (y0 + 17) + i * 4)
        window.add(left_eye_shadow1)

    for i in range(10):
        x0 = 345
        y0 = 180
        left_eye_shadow1 = GLine(x0 + i, y0 + i * 4,
                                (x0 + 5) + i, (y0 + 5) + i * 4)
        window.add(left_eye_shadow1)

    for i in range(10):
        y0 = 220
        x0 = 355
        left_eye_shadow1 = GLine(x0 - i/3, y0 + i * 4,
                                (x0 + 5) + i/3, (y0 + 5) + i * 5)
        window.add(left_eye_shadow1)


def right_face_shadow():
    for i in range(10):
        x0 = 633
        y0 = 216
        right_face_shadow1 = GLine(x0 - i * 1.5, y0 + i * 2.5,
                                (x0 + 1) - i * 1.5, (y0 + 3) + i * 2.5 + i/5)
        window.add(right_face_shadow1)

    for i in range(15):
        x0 = 619
        y0 = 242
        right_face_shadow1 = GLine(x0 - i * 1.9, y0 + i * 5,
                                (x0 + 1) - i * 1.9, (y0 + 5) + i * 5 + i/2)
        window.add(right_face_shadow1)


def decomposed(color, point1, line1=False, fill=True):
    cloth_ = GPolygon()
    for i in range(0, len(point1)):
        cloth_.add_vertex(point1[i])

    cloth_.filled = fill
    cloth_.fill_color = color
    if line1:
        cloth_.color = color

    window.add(cloth_)

if __name__ == '__main__':
    main()
