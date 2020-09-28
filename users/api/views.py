from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from utils import http_response

from ..models import User
from rest_framework import generics


"""View para hacer el login de un usuario"""
class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data

    data = {
        "user": UserDataSerializer(user, context=self.get_serializer_context()).data
    }

    return Response(http_response.format_response_success(data))

