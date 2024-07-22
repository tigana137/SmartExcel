import re
import time
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from bidict import bidict

from django.db import IntegrityError, transaction
from requests.exceptions import ChunkedEncodingError
from rest_framework.response import Response
from x.functions import CustomError, check_if_sid_need_to_be_replaced, get_clean_name, get_clean_name_for_school_name, get_url_return_soup, post_url_return_soup


from x.models import AdminEcoledata, AdminElvs, Del1,  Dre, Elvsprep, levelstat
from pprint import pprint




def Update_kindergarten_students(request2: requests.Session,dre:Dre):
    # request2.get(
    #     "https://suivisms.cnte.tn/ministere/index.php?op=preparatoire&act=inscrit_find")
    # response = request2.get(
    #     "https://suivisms.cnte.tn/ministere/preparatoire/getetabprint.php?id=84")

    print('\n** Updating kindergarten students ... ')

    soup = get_url_return_soup(url="https://suivisms.cnte.tn/ministere/index.php?op=preparatoire&act=inscrit_find", request=request2,decode=True)

    select_element =str( get_url_return_soup(url="https://suivisms.cnte.tn/ministere/preparatoire/getetabprint.php?id="+str(dre.id), request=request2,decode=True))

    pattern = r'value="(\d+)"'
    sids = re.findall(pattern, select_element)
    if sids[0] == '0':
        del sids[0]

    for sid in sids:
        elvs_array = []
        url = "https://suivisms.cnte.tn/ministere/preparatoire/liste_inscrit.php"
        payload = {
            "code_dre": "84",
            "code_etab": sid,
            "btenv": "طباعة"
        }
        
        soup = post_url_return_soup(url=url,payload=payload,request=request2,decode=True)

        table = soup.find('table', {'id': 'datatables', }).tbody
        tr_s = [i for i in table.children if i != '\n']

        for tr in tr_s:
            tds = [i for i in tr.children if i != '\n']
            uid = tds[1].text.strip()

            nom = tds[2].text.strip()
            nom = get_clean_name(nom)

            prenom = tds[3].text.strip()
            prenom= get_clean_name(prenom)

            date_naissance = tds[4].text.strip()

            sid = check_if_sid_need_to_be_replaced(sid, public_school=True)

            eleve = Elvsprep(
                uid=uid,
                nom=nom,
                prenom=prenom,
                date_naissance=date_naissance,
                ecole_id=sid ,
            )
            elvs_array.append(eleve)

        with transaction.atomic():
            Elvsprep.objects.bulk_create(elvs_array, ignore_conflicts=False, update_conflicts=True, update_fields=["nom", "prenom", "date_naissance", "ecole_id"])
            print(str(sid)+' : good ' + str(len(elvs_array)) + ' elvs')



    return Response(True)


