from django.http.response import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt

from PIL import Image, ImageFilter
from tesserocr import PyTessBaseAPI


class OcrFormView(TemplateView):
    template_name = 'documents/ocr_form.html'
ocr_form_view = OcrFormView.as_view()


class OcrView(View):
    def post(self, request, *args, **kwargs):
        with PyTessBaseAPI() as api:
            with Image.open(request.FILES['image']) as image:
                sharpened_image = image.filter(ImageFilter.SHARPEN)
                api.SetImage(sharpened_image)
                utf8_text = api.GetUTF8Text()

        return JsonResponse({'utf8_text': utf8_text})
ocr_view = csrf_exempt(OcrView.as_view())
