===============
OCR with Django
===============

The purpose of this project is to illustrate how to implement a simple OCR web form using `Django <https://www.djangoproject.com/>`_ and `tesserocr <https://github.com/sirfz/tesserocr>`_. Tesserocr is a Python wrapper for the Tesseract C++ API.

Installation
------------

Tesserocr requires a fairly recent versions of `tesseract-ocr <https://github.com/tesseract-ocr>`_ and `leptonica <http://www.leptonica.com/>`_. On Ubuntu these can be installed with: ::

    $ apt install tesseract-ocr libtesseract-dev libleptonica-dev

Depending on your environment, you might have to install these packages from the source code. Follow their respective documentations on instructions on how to do it. Next, you have to install the project's requirements: ::

    (venv) $ pip3 install Cython==0.24.1
    (venv) $ pip3 install -r ocr_with_django/requirements.txt

and run the necessary steps to set-up the Django site: ::

    (venv) $ cd ocr_with_django/
    (venv) $ python manage.py migrate
    (venv) $ python manage.py collectstatic --noinput

We've included a ``Vagrantfile`` script for you to see the site in action by yourself.

OCRView
-------

The OCR process is done in the ``OcrView`` ::

    # documents/views.py

    class OcrView(View):
        def post(self, request, *args, **kwargs):
            with PyTessBaseAPI() as api:
                with Image.open(request.FILES['image']) as image:
                    sharpened_image = image.filter(ImageFilter.SHARPEN)
                    api.SetImage(sharpened_image)
                    utf8_text = api.GetUTF8Text()

            return JsonResponse({'utf8_text': utf8_text})

We take the uploaded image, process it using a `Pillow <https://python-pillow.org/>`_ filter, and pass along the result to the Tesseract OCR API through `tesserocr <https://github.com/sirfz/tesserocr>`_.

We tried to keep the view as simple as possible (no Form, no validation) to focus only on the OCR processes. If you read `PyTessBaseAPI <https://github.com/sirfz/tesserocr/blob/master/tesserocr.pyx>`_ docstrings you'll see that there are tons of things you can do with the image and recognition result.
