from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from utils import http_response
from ..models import User
from rest_framework import generics
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from knox.settings import knox_settings
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import permission_classes
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated

"""View para hacer el login de un usuario"""
class LoginAPI(KnoxLoginView):
    permission_classes = () 
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # Deshabilito sesiones anteriores
        # token_limit_per_user = 1
        # if token_limit_per_user is not None:
        #     now = timezone.now()
        #     token = user.auth_token_set.filter(expiry__gt=now)
        #     if token.count() >= token_limit_per_user:
        #         for session in token:
        #             session.expiry = now
        #             session.save()

        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(user, token_ttl)
        token = self.get_post_response_data(request, token, instance)
        data = {
            "user": UserDataSerializer(user).data,
            'token': {
                **token
            }
        }

        return Response(http_response.format_response_success(data))


"""View para obtener todos los usuarios pertenecientes a un médico"""
@permission_classes([IsAuthenticated])
class UsersDoctorAPI(generics.ListAPIView):
    serializer_class = UserDataSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ["email", 'first_name', 'last_name']
    search_fields = ['$email', '$first_name', '$last_name']
    ordering_fields = ["email", 'first_name', 'last_name',]

    def get_queryset(self):  # funciona como get
        users = User.objects.filter(doctor=self.request.user.id)
        return users


"""View para obtener los datos de un paciente"""
# @permission_classes([IsAuthenticated])
class PatientDataAPI(generics.ListAPIView):
    serializer_class = PatientDataSerializer
    # filter_backends = (filters.DjangoFilterBackend,
    #                    SearchFilter, OrderingFilter)
    # filter_fields = ["email", 'first_name', 'last_name']
    # search_fields = ['$email', '$first_name', '$last_name']
    # ordering_fields = ["email", 'first_name', 'last_name',]

    def get_queryset(self):  # funciona como get
        user = User.objects.filter(cedula=self.request.query_params['cedula'])
        return user
