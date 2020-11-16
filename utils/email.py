from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Email:

    @staticmethod
    def send_email(measure):
        subject = "Alerta de valores de paciente en test de glucosa"
        destinators = [measure.patient.doctor.email]
        params = {'first_name': measure.patient.first_name, 'last_name': measure.patient.last_name, 'ci':measure.patient.cedula, 'url': "https://glucoreader.herokuapp.com/medidas/"+measure.patient.cedula, 'measure': measure.value, 'creation_date': measure.creation_date}
        html_content = render_to_string("measure.html", params)
        email = EmailMultiAlternatives(subject, from_email="Glucoreader <noreply@glucoreader.com>", to=destinators)
        email.attach_alternative(html_content, 'text/html')
        email.send()
