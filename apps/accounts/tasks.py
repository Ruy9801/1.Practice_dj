from django.core.mail import send_mail 
from django.utils.html import format_html 
from celery import shared_task
 
@shared_task
def send_cust_activation_email(email, code):
    activation_url = f'http://localhost:8000/api/act_cust/?u={code}'

    send_mail(
        'Activate you account!',
        activation_url,
        'kira@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )

@shared_task
def send_auth_activation_email(email, code):
    activation_url = f'http://localhost:8000/api/act_auth/?u={code}'

    send_mail(
        'Activate you account!',
        activation_url,
        'ryudzaky@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )

