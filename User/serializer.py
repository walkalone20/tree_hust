from tkinter.ttk import Style
from rest_framework import serializers

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model=User
        fields=['email','username','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def save(self):
        auser=User(email=self.validated_data['email'],username=self.validated_data['username'])
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        auser.set_password(password)
        auser.save()
        return auser