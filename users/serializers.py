from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

from users.models import UserProfile
from x.models import Dre


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = UserProfile
        fields =['id','username','password','email']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,UserProfile):

        token = super().get_token(UserProfile)
        token['dre_id']=UserProfile.dre.id
        token['isAdmin']=UserProfile.isAdmin

        return token
    


#ne9sa more fields w lktheriya mouch mrgla
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = UserProfile.objects.create(
            username=validated_data['username'],
            email=validated_data['email']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user


