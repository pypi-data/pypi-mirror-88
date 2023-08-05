import cv2
from skimage.filters import threshold_local
from carol_pdf_generator.transform import four_point_transform
from datauri import DataURI
import numpy as np


def apply_filter(image, block_size=11, offset=10, method='gaussian'):

    # Apply the 'black and white' effect

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = (
        image > threshold_local(
            image,
            block_size,
            offset=offset,
            method=method)). astype("uint8") * 255
    return image


def scan(base64_data_uri: str, extension: str) -> str:

    image_str = DataURI(base64_data_uri).data

    npimg = np.fromstring(image_str, dtype=np.uint8)
    image = cv2.imdecode(npimg, 1)

    # Decrease height for faster processing

    # height_for_conversion = image.shape[0]
    # conversion_ratio = image.shape[0] / height_for_conversion
    # image = imutils.resize(image, height=height_for_conversion)

    # Edge Detection

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Tune parameters for better processing
    gray = cv2.bilateralFilter(gray, 3, 75, 75)
    edged = cv2.Canny(gray, 75, 200)

    # Find contours

    contours, _ = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True)[
        :min(
            3,
            len(contours))]

    flag = 0
    polygon = []

    for contour in contours:

        perimeter = cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(polygon) == 4:
            flag = 1
            break

    if flag == 1:
        warped_image = four_point_transform(
            image, polygon.reshape(
                4, 2))
    else:
        warped_image = image

    retval, buffer = cv2.imencode(f'.{extension}', warped_image)

    return str(DataURI.make(
        mimetype=f'image/{"jpeg" if extension == "jpg" else "png"}',
        charset='latin1',
        base64=True,
        data=buffer.tostring()
    ))
