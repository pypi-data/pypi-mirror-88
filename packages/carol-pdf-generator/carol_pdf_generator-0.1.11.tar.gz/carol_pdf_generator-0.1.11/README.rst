carol\_pdf\_generator
=====================

carol\_pdf\_generator is a Python library for creating PDF Files from
images (png, jpg) file. Base64 encoded is also supported.

Installation
------------

Use the package manager `pip <https://pip.pypa.io/en/stable/>`__ to
install foobar.

.. code:: bash

    pip install carol_pdf_generator

Usage
-----

.. code:: python

    from carol_pdf_generator import get_from_file_list, get_from_base64_list
    from urllib import request

    file_list = [
        'jpgfile.jpg',
        'pngfile.png'
    ]

    base64_images.append(request.urlopen('https://pastebin.com/raw/k3VZeNHW').read().decode('latin1'))
    base64_images.append(request.urlopen('https://pastebin.com/raw/CaZJ7n6s').read().decode('latin1'))
    base64_images.append(request.urlopen('https://pastebin.com/raw/7Asb2iMJ').read().decode('latin1'))

    from_file = get_from_file_list(file_list)

    base64 = get_from_base64_list(base64_images, 'test.pdf')  # Returns the PDF base64 encoded data uri and saves the PDF to test.pdf

Document Scan and auto rotation
-------------------------------

This library can automatic try to identify paper documents and rotate the image to better fits the PDF Document.

.. code:: python

    base64_jpg = str(DataURI.make(
            mimetype='image/jpeg',
            charset='latin1',
            base64=True,
            data=request.urlopen('https://raw.githubusercontent.com/danielgatis/docscan/master/examples/doc-1.jpg').read().decode('latin-1')
        ))

    base64_png_2 = str(DataURI.make(
            mimetype='image/png',
            charset='latin1',
            base64=True,
            data=request.urlopen('https://raw.githubusercontent.com/danielgatis/docscan/master/examples/doc-2.png').read().decode('latin-1')
        ))

    base64_jpg_3 = str(DataURI.make(
        mimetype='image/jpeg',
        charset='latin1',
        base64=True,
        data=request.urlopen('https://raw.githubusercontent.com/danielgatis/docscan/master/examples/doc-3.jpg').read().decode('latin-1')
    ))

    base64_images = [
        base64_jpg,
        base64_png_2,
        base64_jpg_3
    ]

    # Returns the PDF base64 encoded data uri and saves the PDF to test.pdf, correcting the document geometry and auto rotating the images
    pdf = get_from_base64_list(base64_images, auto_rotate=True, scan_docs=True, output_file="test.pdf")

Merging PDF and images
----------------------

This library you can create a PDF file merging PDF, JPEG and PNG files. Just use merge_pdfs() function using a List() of base64 encoded files as parameter.

.. code:: python

    from carol_pdf_generator.carol_pdf_generator import merge_pdfs
    files = [
        base64_jpg,
        DataURI.from_file("test.pdf"),
        base64_jpg1,
        DataURI.from_file("test2.pdf"),
        base64_jpg2,
        DataURI.from_file("test3.pdf")
    ]

    data = DataURI(merge_pdfs(files))
    b = BytesIO(data.data) ## Some random BytesIO Object
    with open("test333.pdf", "wb") as f:
        f.write(b.getbuffer())

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
