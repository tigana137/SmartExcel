from rest_framework import status
import datetime
from rest_framework.response import Response
import jwt
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404,HttpResponseBadRequest

def create_jwtResponse(user:User):
    
    if not user.is_superuser :
        jwt_payload = {
            'dre_id': user.userprofile.dre_id,
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'exp': datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=600),
            'is_admin': user.userprofile.is_admin,

        }
    else :
        jwt_payload = {
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'exp': datetime.datetime.now(datetime.timezone.utc) +datetime.timedelta(minutes=600),
            'is_superuser': user.is_superuser,

        }
        
    token = jwt.encode(jwt_payload, 'secret', algorithm='HS256')

    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True,secure=False)
    response.data = {'success': True, }

    if not user.is_superuser :
        response.data["is_admin"]=user.userprofile.is_admin
    else:
        response.data["is_superuser"]=user.is_superuser

    return response 
 


def verify_jwt(request): 

    auth_header = request.headers.get('Authorization')
    
    try:
        token = auth_header.split(' ')[1]
        jwt_payload = jwt.decode(token, 'secret', algorithms=['HS256'], options={"verify_signature": False})

    except :
        HttpResponseBadRequest()
        
    return jwt_payload