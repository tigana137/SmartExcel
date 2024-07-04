from rest_framework.exceptions import ValidationError 




def transferElv_condition(request_data):
    if not 'prev_ecole_id' in request_data or not 'next_ecole' in request_data or not 'level' in request_data:
        raise ValidationError()
    
    try:
        prev_ecole_id = int(request_data["prev_ecole_id"])
        next_ecole_id = int(request_data["next_ecole_id"])
        level = int(request_data["level"])
    except ValueError:
        raise ValidationError()

    if not 1<=level<=6:
        raise ValidationError()
    
    return (prev_ecole_id,next_ecole_id,level)

