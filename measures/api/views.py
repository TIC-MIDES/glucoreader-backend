from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.views import APIView
from users.models import User
from ..models import Measure
from .serializer import MeasureSerializer
from rest_framework.response import Response
from utils import http_response
from rest_framework.exceptions import *

from utils import helper_functions as hf

# Create your views here.   
class MeasureAPI(APIView):

    def get(self, request):
        if 'user' in request.query_params:
            measures = Measure.objects.filter(patient=request.query_params['user'])
            serializer = MeasureSerializer(measures, many=True)
            return Response(http_response.format_response_success(serializer.data), status=status.HTTP_200_OK)
        else: 
            measures = Measure.objects.all()
            serializer = MeasureSerializer(measures, many=True)
            return Response(http_response.format_response_success(serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        user = User.objects.filter(id=request.data['user_id']).first()
        #user = request.user PROBAR SI ESTO FUNCIONA IGUAL
        if 'measure_picture' in request.data:
            image_base64 = request.data['measure_picture']
            if image_base64 is not None:
                #Guardar en Cloudinary
                data = hf.save_image_cloud(user, image_base64)
                #Guardar en filesystem
                # hf.save_image(user.cedula, image_base64)
            else:
                return HttpResponseBadRequest('No se pudo subir la imagen')

            serializer = MeasureSerializer(data=data)
            if serializer.is_valid():
                measure = serializer.create(serializer.validated_data)
                #Reconocer valor de la medida y guardar resultado:
                digits = hf.recognize_digits(img_url=measure.photo)
                value = ''
                for digit in digits:
                    value += digit
                measure.value = float(value)
                measure.save()
            else: 
                return Response(http_response.format_response_failure(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

            return Response(http_response.format_response_success("Se subió correctamente"), status=status.HTTP_200_OK)
        else:
            return Response(http_response.format_response_failure("No se recibió ninguna imagen"), status=status.HTTP_400_BAD_REQUEST)

