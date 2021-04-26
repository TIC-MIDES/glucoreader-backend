from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from users.models import User
from ..models import Measure
from .serializer import MeasureSerializer
from rest_framework.response import Response
from utils import http_response
from rest_framework.exceptions import *
from utils import helper_functions as hf
from utils.email import Email
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime
from utils.detect_from_image import run_inference
from PIL import Image
import requests

class MeasureAPI(APIView):

    def get(self, request):
        if 'user' in request.query_params:
            measures = Measure.objects.filter(patient=request.query_params['user']).order_by('-creation_date')
            serializer = MeasureSerializer(measures, many=True)
            return Response(http_response.format_response_success(serializer.data), status=status.HTTP_200_OK)
        else: 
            measures = Measure.objects.all().order_by('-creation_date')
            serializer = MeasureSerializer(measures, many=True)
            return Response(http_response.format_response_success(serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        user = User.objects.filter(id=request.data['user_id']).first()
        if 'measure_picture' in request.data:
            image_base64 = request.data['measure_picture']
            if image_base64 is not None:
                data = hf.save_image_cloud(user, image_base64)
            else:
                return HttpResponseBadRequest('No se pudo subir la imagen')

            # image_path = "C://Users/sebac/Downloads/98.jpg"
            serializer = MeasureSerializer(data=data)
            if serializer.is_valid(): 
                measure = serializer.create(serializer.validated_data)

                measure_digits = run_inference(Image.open(requests.get(data['photo'], stream=True).raw))
                value = float((measure_digits[0] * 100) + (measure_digits[1] * 10) + measure_digits[2])
                measure.value = value
                measure.save()
        return Response(http_response.format_response_success("Ok"), status=status.HTTP_200_OK)

