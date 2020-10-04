from django.shortcuts import render
from rest_framework.views import APIView
from users.models import User
from .serializer import MeasureSerializer
from rest_framework.response import Response
from utils import http_response
from rest_framework.exceptions import *
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.   
class MeasureAPI(APIView):
    def post(self, request):
        user = User.objects.filter(id=request.data['user_id']).first()   #a diferencia de un get esto no devuelve error si no encuentra nada
        data = {}
        if 'measure_picture' in request.data:
            image_base64 = request.data['measure_picture']
            if image_base64 is not None:
                cloudinary_response = cloudinary.uploader.upload("data:image/png;base64," + image_base64, public_id=user.email, folder='User profile pictures')
                data['patient'] = request.data['user_id']
                data['photo'] = cloudinary_response['url']
            else:
                return HttpResponseBadRequest('No se pudo subir la imagen')
            serializer = MeasureSerializer(data=data) 
            if serializer.is_valid():
                measure = serializer.create(serializer.validated_data)
            else: 
                return Response(http_response.format_response_failure(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

            return Response(http_response.format_response_success("Se subió correctamente"), status=status.HTTP_200_OK)
        else:
            return Response(http_response.format_response_failure("No se recibió ninguna imagen"), status=status.HTTP_400_BAD_REQUEST)

