from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()

class UserSignUpSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    password2=serializers.CharField(write_only=True,required=True)

    class Meta:
        model=User
        fields=(
            'username',
            'email',
            'password',
            'password2'
        )
    def validate(self,data):
            if data.get('password') != data.get('password2'):
                raise serializers.ValidationError("Password does not match")
            return data
    def create(self,validated_data):
            password = validated_data.pop('password')
            validated_data.pop('password2',None)
            user=User(**validated_data)
            user.set_password(password)
            user.save()
            return user
