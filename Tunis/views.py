# Import Django's JSON encoder
from django.db.models import Max
from django.db.models import Min
import time
from rest_framework.decorators import api_view
import requests

from rest_framework.response import Response
from Tunis.bulkCreate_classes_elves import bulkcreate_Classes_of_1ecole, bulkcreate_Eleves_of_1ecole, get_nbr_classes_and_elvs
from Tunis.functions import extract_cnte_id, extract_ecoles_of_dre_info
from Tunis.models import ClassTunis, DreTunis, EcolesTunis, ElvsTunis, ElvsTunis
from Tunis.strict_conditions import Verify_Dre_exits, Verify_both_cnte_ids_same, Verify_len_dres_same, Verify_number_of_classes_matches, Verify_number_of_elvs_matches
from Tunis.utils import send_get_request
from django.db import transaction
from bs4 import BeautifulSoup as bs

import re

from excel.models import excelsheets
from excelpremiere.models import excelsheetsPremiere
from retrieve.functions import search_by_fuzzy_algo, search_elv_by_date
from x.functions import CustomError, get_clean_name


def check_dre_db_good():
    print('checking if all dres exists with the same name and cnte_id (exp : sousse= 7 ) ')

    request = requests.session()
    cnte_url = "http://www.ent.cnte.tn/ent/"

    soup = send_get_request(url=cnte_url, request=request, decode=False)

    request.close()
    list_element = soup.find('ul', {'id': 'menu-accordeon'})
    links = list_element.find_all('a', {'id': 'Servs'})

    Verify_len_dres_same(dres_count_in_soup=len(links))

    for link in links:
        dre_name = link.text.strip()
        db_dre_id_in_cnte = Verify_Dre_exits(dre_name)

        dre_cnte_id_in_function = link["onclick"]
        dre_cnte_id = extract_cnte_id(dre_cnte_id_in_function)

        Verify_both_cnte_ids_same(db_dre_id_in_cnte, dre_cnte_id)

    print('Done ')


def update_ecoles_info():   # tmchi l cnte w extracti l name,principal w slug
    "http://localhost:80/api/Tunis/test/"
    print('updating all ecoles : name , slug')
    print('ps : w8 5s after each iteration of wileya')

    request = requests.session()
    dres = DreTunis.objects.all().values('id', 'name', 'dre_id_in_cnte')
    try:
        for dre in dres:
            print('traitment de dre : ', dre['name'])

            url = "http://www.ent.cnte.tn/ent/lireJson.php?gov=" + \
                str(dre['dre_id_in_cnte'])
            soup = send_get_request(url=url, request=request, decode=False)

            ecoles = extract_ecoles_of_dre_info(soup=soup, dre=dre)

            with transaction.atomic():
                EcolesTunis.objects.bulk_create(
                    ecoles, batch_size=100, ignore_conflicts=False, update_conflicts=True, update_fields=["school_name", "school_name", "principal", "slug"])

            print('✓ extraction of dre succefuly now sleeping for 5')
            time.sleep(5)

    finally:
        request.close()

    return Response(True)


@api_view(['GET'])
def mine_ElvTunis(request, valeur=None):
    r'te5ou les donnes t3 tlemtha min kol class in a loop of  50 random ecoles '

    "http://localhost:80/api/Tunis/test/"
    # print(EcolesTunis.objects.filter(extracted_from=True).count());return Response(True)
    # elvs_name = list(ElvsTunis.objects.filter(uid = "016297063461"))
    # return Response(len(elvs_name))

    request = requests.session()
    prev = 4066+100
    for i in range(50):
        ecoles = EcolesTunis.objects.exclude(sid__in=[641822,431128,843102,433101,431404,137531, 
                                                      521411, 432610, 722509,531610, 124018, 100318,210328,432604,101621]).filter(extracted_from=False).order_by('?')
        
        ecole = ecoles.first()
 
        # ecole = EcolesTunis.objects.get(sid=914024)

        try:
            print('traitment of Ecole sid :', str(ecole.sid))
            (nbr_class, nbr_elvs) = get_nbr_classes_and_elvs(
                ecole_slang=ecole.slug, request=request)

            bulkcreate_Classes_of_1ecole(ecole, request, nbr_class)

            # ! u sleep for 1 sec in each class extract
            bulkcreate_Eleves_of_1ecole(ecole, request, nbr_elvs)

            ecole.extracted_from = True
            ecole.save()
            print('\ntraitment of Ecole ran smoothly ✓ ✓ ✓ ✓ ✓ ✓\n')
        except KeyboardInterrupt:
            request.close()
        finally:
            request.close()

        allecoles_treated = EcolesTunis.objects.filter(extracted_from=True).count()
        print('ecoles treated today = ', str(allecoles_treated-prev), '\n\n')
        time.sleep(10)

    return Response(True)


@api_view(['GET'])
def test(request, valeur=None):
    "http://localhost:80/api/Tunis/test/"
    # check_dre_db_good()
    # update_ecoles_info()

    elv = ElvsTunis.objects.filter(uid = "16371038388").values('uid',  'nom_prenom', 'classe__class_name', 'ecole__dre__name', 'ecole__school_name')
    return Response(elv[0]['nom_prenom'])

 

@api_view(['GET'])
def searchElv(request, name=None):
    "http://localhost:80/api/Tunis/searchElv/مريم هلالي"

    result = []
    # نورسين ابن سالم
    # جنة الاندلسي
    # رماس قباع
    start_time = time.time()
    elvs_name = list(ElvsTunis.objects.all().values('uid',  'nom_prenom', 'classe__class_name', 'ecole__dre__name', 'ecole__school_name'))
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    start_time = time.time()
    elvs_name = ([elv['uid'], elv['nom_prenom'], elv['classe__class_name'], elv['ecole__dre__name'], elv['ecole__school_name'],] for elv in elvs_name)
    print(elvs_name)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    result = search_by_fuzzy_algo(elvs_name, searched_name=name)

    return Response(result)  



@api_view(['GET'])
def searchElv(request, name=None):
    "http://localhost:80/api/Tunis/searchElv/نورسين ابن سالم"

    result = []
    # نورسين ابن سالم  
    # 2 paget + 4 tlemtha  ama l elvtunis 1 page and 3 tlemtha
    # جنة الاندلسي
    # رماس قباع

    elvs_name = list(ElvsTunis.objects.filter().values('uid',  'nom_prenom', 'classe__class_name', 'ecole__dre__name', 'ecole__school_name'))
    elvs_name = ([elv['uid'], elv['nom_prenom'], elv['classe__class_name'], elv['ecole__dre__name'], elv['ecole__school_name'],] for elv in elvs_name)
    result = search_by_fuzzy_algo(elvs_name, searched_name=name)
    return Response(result)
 
    dres = DreTunis.objects.all()
    for dre in dres : 
        print('traitment of : ',str(dre))
        elvs_name = list(ElvsTunis.objects.filter(ecole_id__in = dre.ecoles.all()).values('uid',  'nom_prenom', 'classe__class_name', 'ecole__dre__name', 'ecole__school_name'))
        elvs_name = ([elv['uid'], elv['nom_prenom'], elv['classe__class_name'], elv['ecole__dre__name'], elv['ecole__school_name'],] for elv in elvs_name)
        result.extend( search_by_fuzzy_algo(elvs_name, searched_name=name))

    # elvs_name = list(ElvsTunis.objects.all().values('uid',  'nom_prenom', 'classe__class_name', 'ecole__dre__name', 'ecole__school_name'))

    # elvs_name = ([elv['uid'], elv['nom_prenom'], elv['classe__class_name'], elv['ecole__dre__name'], elv['ecole__school_name'],] for elv in elvs_name)

    # result = search_by_fuzzy_algo(elvs_name, searched_name=name)

    return Response(result)  






import mammoth

import os
from django.http import FileResponse, HttpResponse
from django.db.models import Q

import mishkal.tashkeel
import adawat.adaat
from datetime import datetime

@api_view(['GET'])
def download_document(request):
    "http://localhost:80/api/Tunis/download_document"

    # with open("xx2.docx", "rb") as docx_file:
    #     result = mammoth.extract_raw_text(docx_file)
    #     text = result.value # The generated HTML
    #     messages = result.messages # Any messages, such as warnings during conversion
    #     a = mammoth.convert_to_html(docx_file)
    #     # print(a.value)
    #     with open("xx2.txt", "w",encoding='utf-8') as w:
    #         w.write(a.value)
#     vocalizer = mishkal.tashkeel.TashkeelClass()
#     text = "كان من حسن تدبير القائمين على مدرستنا أنهم خصصوا لنا ساعة في الأسبوع للأشغال اليدوية  وكانت تلك الساعة من أمتع الساعات عندي. فقد كان لنا مشغل مجهز بأحدث أدوات النجارة  والحفر في الخشب وتجليد الكتب"
#     # print(text)
#     r"""
    
# اُلشَّمْسُ سَاطِعَة ٌوَاُلسَّمَاءُ صَافِيَة ٌ. غَانِمٌ يَتَنَزَّهُ  فِي اُلْحَقْلِ بَيْنَ اُلْوُرُودِ الُفَوَّاحَةِ وَاُلْأَشْجَارِ اُلْمُثْمِرَةِ وَاُلْفَرَاشَاتُ تَطِيرُ فِي اُلْفَضَاءِ الشّاسِعِ.
# فَجْأَةً لَمَحَ غَانِمٌ عُشًّا بِهِ فِرَاخًا صَغِيرَةً تَشْدُو فَوْقَ شَجَرَةِ اُلْخَوْخِ . وَعَلَى عَجَلَةٍ تَسَلَّقَ غَانِمٌ اُلشَّجَرَةَ وَأَخَذَ فَرْخًا صَغِيرًا ثُمَّ اُسْتَلْقَى عَلَى اُلْعُشْبِ اُلْأَخْضَرِ وَأَخَذَ يَمْسَحُ عَلَى رِيشِهِ اُلْأَصْفَرِ اُلنَّاعِمِ بِلُطْفٍ.نَظَرَ غَانِمٌ إِلَى أَعْلَى فَرَأَى الأُمُّ قَدْ عَادَتْ إِلَى صِغِارِهَا. فَكَّرَ غَانِمُ  قَلِيلاً ثُمَّ أَعَادَ الْعُصْفُورَ إِلَى أُمّهِ

#     """
#     a= get_clean_name(r"""
    
# اُلشَّمْسُ سَاطِعَة ٌوَاُلسَّمَاءُ صَافِيَة ٌ. غَانِمٌ يَتَنَزَّهُ  فِي اُلْحَقْلِ بَيْنَ اُلْوُرُودِ الُفَوَّاحَةِ وَاُلْأَشْجَارِ اُلْمُثْمِرَةِ وَاُلْفَرَاشَاتُ تَطِيرُ فِي اُلْفَضَاءِ الشّاسِعِ.
# فَجْأَةً لَمَحَ غَانِمٌ عُشًّا بِهِ فِرَاخًا صَغِيرَةً تَشْدُو فَوْقَ شَجَرَةِ اُلْخَوْخِ . وَعَلَى عَجَلَةٍ تَسَلَّقَ غَانِمٌ اُلشَّجَرَةَ وَأَخَذَ فَرْخًا صَغِيرًا ثُمَّ اُسْتَلْقَى عَلَى اُلْعُشْبِ اُلْأَخْضَرِ وَأَخَذَ يَمْسَحُ عَلَى رِيشِهِ اُلْأَصْفَرِ اُلنَّاعِمِ بِلُطْفٍ.نَظَرَ غَانِمٌ إِلَى أَعْلَى فَرَأَى الأُمُّ قَدْ عَادَتْ إِلَى صِغِارِهَا. فَكَّرَ غَانِمُ  قَلِيلاً ثُمَّ أَعَادَ الْعُصْفُورَ إِلَى أُمّهِ

#     """)
#     # a = vocalizer.tashkeel(text)

# Get the current date and time
    current_date = datetime.now()

    # Extract the month number from the current date
    month_number = current_date.month
    year_number = current_date.year
    print("Current month number:", month_number)
    if month_number > 7 :
        start_date = datetime(year_number, 7, 1).date()
    else:
        start_date = datetime(year_number-1, 7, 1).date()

    end_date = datetime.now().date()

    queryset = excelsheets.objects.filter(
        Q(date_downloaded__gte=start_date) & Q(date_downloaded__lte=end_date)
    )

    unique_dates = queryset.values_list('date_downloaded', flat=True).distinct().order_by('-date_downloaded')


    queryset_premiere =excelsheetsPremiere.objects.filter(
        Q(date_downloaded__gte=start_date) & Q(date_downloaded__lte=end_date)
    )
    unique_dates_premiere = queryset_premiere.values_list('date_downloaded', flat=True).distinct().order_by('-date_downloaded')

    return Response(unique_dates)
    
