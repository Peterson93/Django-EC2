from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Productos(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    nombreproducto=models.CharField(max_length=150)
    imagen=models.ImageField(null=True,blank=True)
    marcaproducto=models.CharField(max_length=100,null=True,blank=True)
    cagoriaproducto=models.CharField(max_length=100,null=True,blank=True)
    informacionproducto=models.TextField(null=True,blank=True)
    calificacion=models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    numeroReseñas=models.IntegerField (null=True,blank=True,default=0)
    precio=models.DecimalField(max_digits=7, decimal_places=2,null=True,blank=True)
    cantidadenstock=models.IntegerField(null=True,blank=True,default=0)
    fechadecreacion=models.DateTimeField(auto_now_add=False)
    _id=models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return self.nombreproducto

class Review(models.Model):
    producto=models.ForeignKey(Productos,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    nombre=models.CharField(max_length=200,null=True,blank=True)
    calificacion=models.IntegerField(null=True,blank=True,default=0)
    comentarios=models.TextField(null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return str(self.calificacion)


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    paymentMethod=models.CharField(max_length=200,null=True,blank=True)
    taxPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    shippingPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    totalPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    isPaid=models.BooleanField(default=False)
    paidAt=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    isDelivered=models.BooleanField(default=False)
    deliveredAt=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    createdAt=models.DateTimeField(auto_now_add=True)
    _id=models.AutoField(primary_key=True,editable=False)
    
    
    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    producto=models.ForeignKey(Productos,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    nombre=models.CharField(max_length=200,null=True,blank=True)
    cantidad=models.IntegerField(null=True,blank=True,default=0)
    precio=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    imagen=models.CharField(max_length=200,null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False)

        
    def __str__(self):
        return self.nombre

class ShippingAddress(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    city=models.CharField(max_length=200,null=True,blank=True)
    postalCode=models.CharField(max_length=200,null=True,blank=True)
    country=models.CharField(max_length=200,null=True,blank=True)
    shippingPrice=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return self.address 