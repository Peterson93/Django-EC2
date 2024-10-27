#!/usr/bin/env python 2.7
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import ProductosSerializer, UserSerializer, UserSerializerWithToken
from .models import Productos
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

# for sending mails and generate token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError,force_str
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.views.generic import View


# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    return Response('hola a todos')


@api_view(['GET'])
def getProductos(request):
    productos = Productos.objects.all()
    serializer = ProductosSerializer(productos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProducto(request, pk):
    producto = Productos.objects.get(_id=pk)
    serializer = ProductosSerializer(producto, many=False)
    return Response(serializer.data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfiles(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    
    try:
         
        user = User.objects.create(first_name=data['fname'], last_name=data['lname'],
                                   username=data['email'], email=data['email'], password=make_password(data['password']), is_active=False)
        
        # generate token for sending mail
        email_subject = "Activa tu cuenta"
        message = render_to_string(
            "activate.html",
            {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            }
        )
        #print(message)
        email_message = EmailMessage(
            email_subject, message, settings.EMAIL_HOST_USER, [data['email']])
        email_message.send()
                
        serialize = UserSerializerWithToken(user, many=False)
        message = {'details':'activa tu cuenta con el enlace enviado a tu email'}
        return Response(message)
        
    except Exception as e:
        message = {'details':'ya existe un usuario con estos datos o algo salio mal'}
        return Response(message)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            return render(request,"activacionExitosa.html")
        else:
            return render(request,"activacionFallida.html")  