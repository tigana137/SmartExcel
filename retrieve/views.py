# Import Django's JSON encoder
from django.db.models.functions import TruncMonth
from django.db.models import Q
from django.db.models.functions import Length
from django.shortcuts import get_object_or_404
from thefuzz import fuzz
from django.db.models import Sum
import time
from datetime import date
import json
from rest_framework.decorators import api_view
import requests
import base64
from django.http import JsonResponse
from rest_framework.response import Response
from excel.models import excelsheets
from excelpremiere.models import excelsheetsPremiere
from retrieve.functions import merge_arrays, search_by_fuzzy_algo, search_elv_by_date, search_elv_custom_sql_query, set_multiple_names


from utils.check_request_data import check_request_data
from x.functions import CustomError
from x.models import AdminEcoledata, AdminElvs, Del1, Dre, Elvsprep, levelstat
from x.serializers import AdminEcoledata2Serializer, AdminEcoledataSerializer, levelstatSerializer
from rest_framework import status

import os
from django.http import FileResponse, HttpResponse
from django.db.models import Q
from datetime import datetime

@api_view(['GET'])
def getDel1s(request):
    start_time = time.time()
    "http://localhost:80/api/retrieve/getDel1s/"
    dre_id = 84
    dre = Dre.objects.filter(id=dre_id).first()
    del1s = dre.Del1s.all()
    del1s_dic = {del1.id: del1.name for del1 in del1s}

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    return Response(del1s_dic)


@api_view(['GET'])
def getEcoles(request):
    "http://localhost:80/api/retrieve/getEcoles/"
    start_time = time.time()

    dre_id = 84
    del1s = Del1.objects.filter(dre_id=dre_id)
    ecoles_dic = {}
    for del1 in del1s:
        del1_ecoles = del1.ecoles.all()
        ecoles_serialized = AdminEcoledataSerializer(
            del1_ecoles, many=True).data
        del1_ecoles_dic = {}
        for ecole in ecoles_serialized:
            sid = ecole['sid']
            ecole['name'] = ecole['ministre_school_name']
            del1_ecoles_dic[sid] = ecole
        ecoles_dic[del1.id] = del1_ecoles_dic

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    return Response(ecoles_dic)


@api_view(['GET'])
def getLevelStat(request):
    "http://localhost:80/api/retrieve/getLevelStat/"
    dre_id = 84
    stats = levelstat.objects.filter(lid__startswith=dre_id)
    statss = {}
    start_time = time.time()

    for stat in stats:
        statss[stat.lid] = {
            "nbr_elvs": stat.nbr_elvs,
            "nbr_classes": stat.nbr_classes,
            "nbr_leaving": stat.nbr_leaving,
            "nbr_comming": stat.nbr_comming,
        }

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    return Response(statss)


@api_view(['GET'])
def getAllEcolesData(request):
    start_time = time.time()
    levels = levelstat.objects.filter(lid__startswith=84)
    levels = {level.lid: {
        "nbr_elvs": level.nbr_elvs,
        "nbr_classes": level.nbr_classes,
        "nbr_leaving": level.nbr_leaving,
        "nbr_comming": level.nbr_comming,
    }for level in levels}

    dic = {}
    dels = Del1.objects.filter(id__startswith=84).exclude(id=8498)
    for del1 in dels:
        dic[del1.id] = {"name": del1.name, }
        dic[del1.id]["ecoles"] = {}
        ecole_dic = {}
        ecoles = del1.ecoles.all().values(
            "sid", "school_name", "ministre_school_name", "principal")
        levels_str = ["premiere", "deuxieme", "troisieme",
                      "quatrieme", "cinquieme", "sixieme"]

        for ecole in ecoles:
            ecole_dic[ecole["sid"]] = {
                "school_name": ecole["school_name"],
                "name": ecole["school_name"],
                "principal": ecole["principal"],
            }
            for i in range(6):
                ecole_dic[ecole["sid"]][levels_str[i]
                                        ] = levels[int(str(ecole["sid"])+str(i+1))]

        dic[del1.id]["ecoles"] = ecole_dic

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    return Response(dic)


@api_view(['GET'])
def searchElv(request, name=None, birth_date=None):
    "http://localhost:80/api/retrieve/getElv/byname/ابتهال مريم"

    result = []

    if birth_date:
        result = search_elv_by_date(birth_date)

    if name:
        result1 = []  # na7eha ki traj3 l zouz loutanin
        # possible_names_versions = set_multiple_names(name)
        # result1 = search_elv_custom_sql_query(possible_names_versions)
        elvs_name = list(AdminElvs.objects.all().values(
            'uid',  'nom_prenom', 'nom_pere', 'date_naissance', 'ecole__school_name'))
        elvs_name = ([elv['uid'], elv['nom_prenom'], elv['nom_pere'], elv['date_naissance'],elv['ecole__school_name'],] for elv in elvs_name)
        result2 = search_by_fuzzy_algo(elvs_name, searched_name=name)
        result = merge_arrays(result1, result2)
    return Response(result)


@api_view(['POST'])
def editLevelStat(request):
    "http://localhost:80/api/retrieve/editLevelStat" 
    
    lid = request.data.get('lid')
    instance = get_object_or_404(levelstat,lid=lid) 

    serializer = levelstatSerializer(instance=instance, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()


    return Response(True)


@api_view(['GET'])
def test(request, valeur=None):
    "http://localhost:80/api/retrieve/test/"
    
 
   
    return Response(True)




@api_view(['GET'])
def getHistoriqueDates(request, valeur=None):
    "http://localhost:80/api/retrieve/getHistoriqueDates/" 

    current_date = datetime.now()

    current_month_number = current_date.month
    current_year_number = current_date.year

    if current_month_number > 7 :
        start_date = datetime(current_year_number, 7, 1).date()
    else:
        start_date = datetime(current_year_number-1, 7, 1).date()

    queryset = excelsheets.objects.filter(Q(date_downloaded__gte=start_date))
    unique_dates = queryset.values_list('date_downloaded', flat=True).distinct().order_by('-date_downloaded')

    queryset_premiere =excelsheetsPremiere.objects.filter(Q(date_downloaded__gte=start_date))
    unique_dates_premiere = queryset_premiere.values_list('date_downloaded', flat=True).distinct().order_by('-date_downloaded')
    i = 0
    i_premiere = 0
    array = []
    while i < len(unique_dates) or i_premiere < len(unique_dates_premiere):
        if  i_premiere+1 > len(unique_dates_premiere) :
            array.append((unique_dates[i],'general'))
            i+=1
            continue
        if i+1 > len(unique_dates):
            array.append((unique_dates_premiere[i],'premiere'))
            i_premiere+=1 
            continue

        if unique_dates[i] > unique_dates_premiere[i_premiere]:
            array.append((unique_dates[i],'general'))
            i+=1
        else:
            array.append((unique_dates_premiere[i_premiere],'premiere'))
            i_premiere+=1


    return Response(array)






@api_view(['GET'])
def getStats(request, valeur=None):
    # jwt_payload = verify_jwt(request)
    #
    # dre_id = jwt_payload['dre_id']
    dre_id = 84
    excelsheets_instances = excelsheets.objects.filter(dre__id=dre_id)
    total_transfers = excelsheets_instances.count()
    tranfers_from_private = excelsheets_instances.filter(prev_ecole_id=-2).count()
    tranfers_from_out_of_state = excelsheets_instances.filter(prev_ecole_id=-3).count()
    tranfers_from_out_of_country = excelsheets_instances.filter(prev_ecole_id=-4).count()
    tranfers_from_public = total_transfers-tranfers_from_private-tranfers_from_out_of_state-tranfers_from_out_of_country
    dic = {
        "total":total_transfers,
        "public":tranfers_from_public,
        "private":tranfers_from_private,
        "out_of_state":tranfers_from_out_of_state,
        "out_of_country":tranfers_from_out_of_country,
    }

    return Response(dic)


@api_view(['GET'])
def getSchoolsInfo(request, valeur=None):
    "http://localhost:80/api/retrieve/getSchoolsInfo/"
    # jwt_payload = verify_jwt(request)
    #
    # dre_id = jwt_payload['dre_id']
    dre_id = 84 
    ecoles = AdminEcoledata.objects.filter(dre_id=dre_id).exclude(del1_id=str(dre_id)+'98')
    ecoles_serialized = AdminEcoledata2Serializer(ecoles, many=True).data
    return Response(ecoles_serialized)