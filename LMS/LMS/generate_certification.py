import os
import cv2

list_of_names = []

# cur_path = os.getcwd()
# # print(cur_path)
# path = cur_path + "/Media/certificate/"
def delete_old_data():
    for i in os.listdir(path+"generated-certificates/"):
        os.remove(path+"generated-certificates/{}".format(i))


def cleanup_data():
    with open('name-data.txt') as f:
        for line in f:
            list_of_names.append(line.strip())


def generate_certificates(name, courseName, date, id):
    cur_path = os.getcwd()

    path = cur_path + "\Media\certificate"

    # path = "Media/certificate"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color_blue = (255, 0, 0)
    color_red = (0, 0, 255)
    color_black = (0, 0, 0)
    thickness = 2
    line_type = cv2.LINE_AA

    # Get the dimensions of the text
    text_width, text_height = cv2.getTextSize(name, font, font_scale, thickness)[0]
    print(text_width, text_height)
    # calculate the position to center the text
    text_center_x = (360 - text_width) // 2
    text_center_y = (40 - text_height) // 2

    certificate_template_image = cv2.imread(path + "certificate-template.jpeg")
    cv2.putText(certificate_template_image, name.strip(), (220 + text_center_x, 240 + text_center_y), font, font_scale, color_red, thickness, line_type)

    font_scale = 0.8
    text_width, text_height = cv2.getTextSize(courseName, font, font_scale, thickness)[0]
    print(text_width, text_height)
    # calculate the position to center the text
    text_center_x = (360 - text_width) // 2
    text_center_y = (40 - text_height) // 2
    cv2.putText(certificate_template_image, courseName.strip(), (220 + text_center_x, 330 + text_center_y), font, font_scale, color_black, thickness, line_type)

    font_scale = 0.5
    line_type = cv2.LINE_4
    thickness = 1
    text_width, text_height = cv2.getTextSize(date, font, font_scale, thickness)[0]
    print(text_width, text_height)
    # calculate the position to center the text
    text_center_x = (92 - text_width) // 2
    text_center_y = (18 - text_height) // 2
    cv2.putText(certificate_template_image, date.strip(), (288 + text_center_x, 430 + text_center_y), font, font_scale, color_blue, thickness, line_type)
    cv2.imwrite(path+"generated-certificates/{}.jpg".format(id), certificate_template_image)


def main():
    delete_old_data()
    # cleanup_data()
    generate_certificates("Pat N. Joffis", "Python for beginners", "2023-06-04", "1234")


if __name__ == '__main__':
    main()
