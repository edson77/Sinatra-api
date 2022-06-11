from rest_framework.response import Response
import os
from io import BytesIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


def apiResponse(data,message,statusCode, meta = '' ):
        data = data if len(data) > 0 else []
        
        response = {
            "data":data,
            "message":message
        }
        if len(meta) > 0:
            response ={**response, **meta}
        return Response(response, status=statusCode)

def resizeUploadedImage(image, max_width, max_height):
    size = (max_width, max_height)

    # Uploaded file is in memory
    if isinstance(image, InMemoryUploadedFile):
        memory_image = BytesIO(image.read())
        pil_image = PilImage.open(memory_image)
        img_format = os.path.splitext(image.name)[1][1:].upper()
        img_format = 'JPEG' if img_format == 'JPG' else img_format

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)

        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)

        new_image = ContentFile(new_image.getvalue())
        return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)

    # Uploaded file is in disk
    elif isinstance(image, TemporaryUploadedFile):
        path = image.temporary_file_path()
        pil_image = PilImage.open(path)

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)
            pil_image.save(path)
            image.size = os.stat(path).st_size

    return image