
from rest_framework.exceptions import ValidationError 



def transferElv_conditionPremiere(request_data):
    if not 'prev_ecole_id' in request_data or not 'next_ecole' in request_data :
        raise ValidationError()
    
    try:
        prev_ecole_id = int(request_data["prev_ecole_id"])
        next_ecole_id = int(request_data["next_ecole_id"])
    except ValueError:
        raise ValidationError()

    
    return (prev_ecole_id,next_ecole_id)