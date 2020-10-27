from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from users.models import User
from ..models import Measure
from .serializer import MeasureSerializer
from rest_framework.response import Response
from utils import http_response
from rest_framework.exceptions import *
from utils import helper_functions as hf


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
                results_list = hf.recognize_digits(img_url=measure.photo)
                values_dict = {} # La medida es la key y el numero de coincidencias es el value
                for digit_list in results_list:
                    value = ''
                    for digit in digit_list:
                        value += str(digit)
                    try:
                        float_value = float(value)
                        if float_value in values_dict:
                            values_dict[float_value] += 1
                        else:
                            values_dict[float_value] = 0
                    except:
                        print(value)

                print(values_dict)

                if len(values_dict) > 1:    # Se reconocieron digitos distintos
                    ordered_values_dict = {k: v for k, v in sorted(values_dict.items(), key=lambda item: item[1])}
                    items_list = list(ordered_values_dict.items())
                    if items_list[0][1] > items_list[1][1]: # Si hay un unico valor con numero de coincidencias max
                        measure.value = items_list[0][0]
                        measure.save()
                    else:
                        return Response(http_response.format_response_failure('Error al reconocer los digitos'),
                                        status=status.HTTP_400_BAD_REQUEST)
                elif len(values_dict) == 1:
                    measure.value = list(values_dict.keys())[0] # Se guarda el unico valor reconocido
                else:
                    return Response(http_response.format_response_failure('Error al reconocer los digitos'),
                                    status=status.HTTP_400_BAD_REQUEST)
            else: 
                return Response(http_response.format_response_failure(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

            response_data = MeasureSerializer(measure).data
            return Response(http_response.format_response_success(response_data), status=status.HTTP_200_OK)
        else:
            return Response(http_response.format_response_failure("No se recibió ninguna imagen"), status=status.HTTP_400_BAD_REQUEST)

