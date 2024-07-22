import imutils
import cv2

__all__ = ["create_image"]


SCALE_FACTOR = 1.1
MEAN = (103.939, 116.779, 123.680)
swapRB = False
crop = False


def create_image(model, _image, output_image=None):

    net = cv2.dnn.readNetFromTorch(model)
    image = cv2.imread(_image)
    image = imutils.resize(image, width=600)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, SCALE_FACTOR, (w, h), MEAN, swapRB=swapRB, crop=crop)
    net.setInput(blob)
    output = net.forward()
    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += MEAN[0]
    output[1] += MEAN[1]
    output[2] += MEAN[2]
    # output /= 255.0
    output = output.transpose(1, 2, 0)
    cv2.imwrite(output_image, output)
    return output_image
