
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from excel.ExcelAlgo import initiate_Excel
from excel.conditions import transferElv_condition
from excel.functions import adjust_levelstat, cancel_excelsheetRow, create_excelsheetRow
from excel.models import excelsheets
from excel.serializers import excelsheetsSerializer

from users.functions import verify_jwt
from x.models import AdminEcoledata, AdminElvs, Del1, Elvsprep, levelstat


@api_view(['GET'])
def Test(request):

    return Response(True)


@api_view(['GET'])
def GetDel1(request):
    jwt_payload = verify_jwt(request)
    dre_id = jwt_payload['dre_id']
    
    Del1s = Del1.objects.filter(id__startswith=dre_id).values_list('name', flat=True)
    return Response(Del1s)



@api_view(['GET'])
def GetEcoles(request):
    jwt_payload = verify_jwt(request)
    dre_id = jwt_payload['dre_id']

    ecoles_dic = {}
    ecoles = AdminEcoledata.objects.filter(
        sid__startswith=dre_id).order_by('sid')
    for ecole in ecoles:
        try:
            ecoles_dic[ecole.del1.name][ecole.sid] = ecole.ministre_school_name if ecole.ministre_school_name != "" else ecole.school_name
        except:
            ecoles_dic[ecole.del1.name] = {}
            ecoles_dic[ecole.del1.name][ecole.sid] = ecole.ministre_school_name if ecole.ministre_school_name != "" else ecole.school_name

    return Response(ecoles_dic)


@api_view(['GET'])
def GetExcelRows(request, page):
    jwt_payload = verify_jwt(request)
    dre_id = jwt_payload['dre_id']

    excel_rows_query = excelsheets.objects.filter(dre_id=dre_id, date_downloaded=None).all().order_by('-id')
    length = len(excel_rows_query)
    specifique_excel_rows_page = excel_rows_query[page*15:page*15+15]
    excel_rows_serialized = excelsheetsSerializer(specifique_excel_rows_page, many=True).data

    return Response({"length": length,"data": excel_rows_serialized})


@api_view(['GET'])
def GetElv(request, uid):
    verify_jwt(request)

    eleve = AdminElvs.objects.filter(uid=uid).first()

    if eleve:
        if str(eleve.ecole.sid)[2:4]  =="98":
            eleve.ecole.sid = -2
            eleve.ecole.ministre_school_name = "مدرسة خاصة"

        data = {
            'uid': '0' + str(eleve.uid),
            'nom_prenom': eleve.nom_prenom,
            'nom_pere': eleve.nom_pere,
            'date_naissance': eleve.date_naissance,
            'prev_ecole': eleve.ecole.ministre_school_name,
            'prev_ecole_id': eleve.ecole.sid,
            'decision': 'مع الموافقة',
        }
        
        return Response(data)

    eleve = Elvsprep.objects.filter(uid=uid).first()

    if not eleve:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if str(eleve.ecole.sid)[2:4]  =="98":
        eleve.ecole.sid = -2
        eleve.ecole.ministre_school_name = "مدرسة خاصة"

    data = {
        'uid': '0' + str(eleve.uid),
        'nom_prenom': eleve.nom + ' ' + eleve.prenom,
        'nom_pere': " ",
        'date_naissance': eleve.date_naissance,
        'prev_ecole': eleve.ecole.ministre_school_name,
        'prev_ecole_id': eleve.ecole.sid,
        'decision': 'مع الموافقة',
    }
    
    return Response(data)


@api_view(['POST'])
# zid l dre_id lil adjust_levelstat fil filter bch kek mayb3bsch dre o5ra
def transferElv(request):
    jwt_payload = verify_jwt(request)
    dre_id = jwt_payload['dre_id']

    try:
        (prev_ecole_id, next_ecole_id, level) = transferElv_condition(request.data)
    except ValidationError:
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    adjust_levelstat(prev_ecole_id, next_ecole_id, level, dre_id, cancel=False)

    create_excelsheetRow(request.data, dre_id)

    return Response({"response": True}, status=status.HTTP_200_OK)


@api_view(['POST'])
def cancel_transferElv(request):
    jwt_payload = verify_jwt(request)
    dre_id = jwt_payload['dre_id']

    try:
        (prev_ecole_id, next_ecole_id, level) = transferElv_condition(request.data)
    except ValidationError:
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    adjust_levelstat(prev_ecole_id, next_ecole_id, level, dre_id, cancel=True)

    cancel_excelsheetRow(request.data, dre_id)

    return Response({"response": True})


@api_view(['GET'])
def CreateExcel(request,date=None):
    jwt_payload = verify_jwt(request)
    dre_id = jwt_payload['dre_id']

    workbook, FileName = initiate_Excel(dre_id,date)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    # Save the workbook to the response
    workbook.save(response)
    response['Content-Disposition'] = 'attachment; filename='+FileName+'.xlsx'
    return response


@api_view(['POST'])
def check_nbr_elv_post_transfer(request):
    "http://localhost:80/api/excel/check_nbr_elv_post_transfer/"
    verify_jwt(request)


    if not 'sid' in request.data or not 'level' in request.data or not 'is_comming' in request.data:
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    sid = str(request.data["sid"])
    level = str(request.data["level"])
    is_comming = request.data["is_comming"]

    ecole = get_object_or_404(AdminEcoledata, sid=sid)
    lid = sid + level
    levelStat = get_object_or_404(levelstat, lid=lid)
    
   
    if is_comming  and levelStat.kethefa_after_comming() > 33:
        return Response(
            {
            "sid":sid,
            "kethefa" : levelStat.kethefa_after_comming(),
            "level":level,
            "name": ecole.school_name
        }
        )
    if not is_comming and levelStat.kethefa_after_leaving() < 16:
        return Response(False)

    return Response("null")
