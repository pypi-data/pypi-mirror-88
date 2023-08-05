from typing import List
from urllib import request
from carol_pdf_generator.docscan import scan
import hashlib
from io import BytesIO
from PyPDF2 import PdfFileMerger
from datauri import DataURI
from fpdf import FPDF

from PIL import Image

from copy import copy


def get_image_data(base64_data_uri: str) -> BytesIO:
    """Get the image data from a base64 data uri

    Args:
        base64_data_uri (str): Base64 encoded image

    Returns:
        bytes: decoded image
    """
    return BytesIO(DataURI(base64_data_uri).data)


def image_supported(base64_data: str) -> bool:
    """Check if the image is supported by this lib

    Args:
        base64_data (str): base64 data uri image

    Returns:
        bool: true if base64 data type is jpeg or png
    """
    return get_image_type(base64_data) in ['png', 'jpeg', 'jpg']


def get_image_type(base64_data: str) -> str:
    """Returns the image file type

    Args:
        base64_data (str): base64 data uri image

    Returns:
        str: the current file type
    """
    uri = DataURI(base64_data)
    return uri.mimetype.replace('image/', '')


def get_image_size(image_fp: BytesIO) -> list:
    """Return the image size

    Args:
        image_fp (BytesIO): Byte array of image

    Returns:
        list: a list with image weight and height
    """
    im = Image.open(image_fp)
    return im.size


def auto_rotate_image(
        image_fp: BytesIO,
        counter_clockwise: bool = False) -> BytesIO:
    """Auto rotate the image to better use of PDF Document

    Args:
        image_fp (BytesIO): Byte array of image

    Returns:
        BytesIO: Byte array of rotated image
    """
    im = Image.open(image_fp)
    w, h = im.size
    if w > h:
        im_rotate = im.rotate(
            90 * (-1 if counter_clockwise else 1), expand=True)
    else:
        im_rotate = im
    img_byte_arr = BytesIO()
    im_rotate.save(img_byte_arr, format=im.format)
    img_byte_arr.seek(0)
    return img_byte_arr


def get_from_base64_list(
        image_list: list,
        output_file: str = None,
        auto_rotate: bool = True,
        scan_docs: bool = False,
        remove_encoding: bool = True) -> str:
    """Creates PDF from a list of base64 images

    Args:
        image_list (list): List of base64 images data:image/[jpeg|png]
        output_file (str, optional): Path of output PDF. Defaults to None.
        remove_encoding (boot, optional): Removes the encoding information

    Returns:
        str: data uri with base64 PDF file
    """

    pdf = FPDF(unit='pt')
    pdf.set_compression(True)

    for image in image_list:
        if image_supported(image):
            result = hashlib.md5(image.encode())
            image_type = get_image_type(image)
            extension = 'jpg' if image_type.lower() in [
                'jpeg', 'jpg'] else 'png'
            filename = f'{result.hexdigest()}.{extension}'
            if scan_docs:
                image = scan(copy(image), extension)

            img_data = get_image_data(image)
            if auto_rotate:
                img_data = auto_rotate_image(img_data)
            pdf.add_page()
            image_copy = copy(img_data)
            image_weight, image_height = get_image_size(image_fp=image_copy)

            image_ratio = image_weight / image_height
            page_ratio = pdf.w / pdf.h

            if image_weight < pdf.w and image_height < pdf.h:
                pdf.image(
                    name=filename,
                    image_fp=img_data,
                    x=0,
                    y=0,
                    valign='C')
            else:
                if page_ratio <= image_ratio:
                    pdf.image(
                        name=filename,
                        image_fp=img_data,
                        x=0,
                        y=0,
                        w=pdf.w,
                        valign='C')
                else:
                    pdf.image(
                        name=filename,
                        image_fp=img_data,
                        x=0,
                        y=0,
                        h=pdf.h,
                        valign='C')

    if output_file is not None:
        pdf.output(output_file, 'F')

    pdf_data = pdf.output(dest='S')

    data_uri = DataURI.make(
        mimetype='application/pdf',
        charset='latin1',
        base64=True,
        data=pdf_data
    )
    return str(data_uri).replace('charset=latin1;',
                                 '' if remove_encoding else 'charset=latin1;')


def get_from_file_list(
        images: list,
        output_file: str = None,
        remove_encoding: bool = False) -> str:
    """Creates PDF from a list of images paths

    Args:
        image_list (list): List of images paths
        output_file (str, optional): Path of output PDF. Defaults to None.
        remove_encoding (boot, optional): Removes the encoding information

    Returns:
        str: data uri with base64 PDF file
    """
    data_uri_list = []

    for image_path in images:
        data_uri = DataURI.from_file(image_path)
        if image_supported(data_uri):
            data_uri_list.append(data_uri)

    return get_from_base64_list(
        data_uri_list,
        output_file=output_file,
        remove_encoding=remove_encoding)


def merge_pdfs(files_data: List[str],
               remove_encoding: bool = False) -> DataURI:
    """merge various PDF and image files in a single PDF

    Args:
        files_data (List[DataURI]): List of base64 encoded
        PDF and image (PNG or JPEG)

    Returns:
        DataURI: Base64 encoded merged PDF
    """
    merger = PdfFileMerger()
    for file_data in files_data:
        fileobj = BytesIO()
        uri = DataURI(file_data)
        if image_supported(uri):
            uri = DataURI(get_from_base64_list([uri]))
        fileobj = BytesIO(uri.data)
        merger.append(fileobj)
    output_file = BytesIO()
    merger.write(output_file)
    merger.close()
    output_file.seek(0)
    data_uri = DataURI.make(
        mimetype='application/pdf',
        charset='latin1',
        base64=True,
        data=output_file.read()
    )
    return str(data_uri).replace('charset=latin1;',
                                 '' if remove_encoding else 'charset=latin1;')
