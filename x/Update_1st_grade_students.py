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



def Update_1st_grade_students(request2: requests.Session,dre:Dre):

    print('\n** Updating 1st grade students ... ')

    request2.get("https://suivisms.cnte.tn/ministere/index.php?op=primaire&act=inscrit_find")
    response = request2.get("https://suivisms.cnte.tn/ministere/primaire/getetabprint1.php?id="+str(dre.id))

    select_element = response.content.decode(encoding='utf-8', errors='ignore')
    pattern = r'value="(\d+)"'
    sids = re.findall(pattern, select_element)
    if sids[0] == '0':
        del sids[0]
        
    for sid in sids:
        elvs_array = []
        url = "https://suivisms.cnte.tn/ministere/primaire/liste_inscrit.php"
        payload = {
            "code_dre": dre.id,
            "code_etab": sid,
            "btenv": "طباعة"
        }

        response = request2.post(url=url, data=payload)

        soup = bs(response.content.decode(encoding='utf-8', errors='ignore'), 'html.parser')

        table = soup.find('table', {'id': 'datatables', }).tbody

        tr_s = [i for i in table.children if i != '\n']

        for tr in tr_s:
            tds = [i for i in tr.children if i != '\n']
            uid = tds[1].text.strip()
            nom_prenom = tds[2].text.strip() + " " + tds[3].text.strip()
            date_naissance = tds[4].text.strip()
            eleve = AdminElvs(
                uid=uid,
                nom_prenom=get_clean_name(nom_prenom),
                date_naissance=date_naissance,
                ecole_id=check_if_sid_need_to_be_replaced(sid,public_school=True),
            )
            elvs_array.append(eleve)

        try:
            AdminElvs.objects.bulk_create(elvs_array, batch_size=100, ignore_conflicts=False, update_conflicts=True, update_fields=["nom_prenom", "date_naissance", "ecole_id"])
            print(f"{sid} : updated succesfully with '{len(elvs_array)}' 1st grade students")

        except IntegrityError as e:
            print("------------")
            print("errerur with this : " + str(sid))
            print(f"IntegrityError: {e}")
            print("------------")


    print("✓ 1st grade students updated succesfully")

    return Response(True)
