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










def is_valid_date_string(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    


def update_students_from_public_schools(request2: requests.Session,dre:Dre):


    response = request2.get("https://suivisms.cnte.tn/ministere/inscprim/getetab_choix.php?id="+str(dre.id))
    select_element = response.content.decode(encoding='utf-8', errors='ignore')
    pattern = r'value="(\d+)"'
    sids = re.findall(pattern, select_element)

    for sid in sids:
        print(f"updating students of the school : {sid}")
        elvs_array = []

        url = "https://suivisms.cnte.tn/ministere/index.php?op=inscprim&act=list_eleve"
        payload = {
            "code_dre": dre.id,
            "code_etab": sid,
            "btenv": "بحث"
        }

        soup = post_url_return_soup(url=url,payload=payload,request=request2,decode=True)

        rows = soup.find_all('tr', {'height': '30', 'bgcolor': '#a9edca'})

        for tr in rows:
            data = tr.findAll('font')

            uid = data[1].text.strip()
            if uid == "" or uid == "0" or not uid.isdigit():
                continue
            nom_prenom = data[2].text.strip()
            nom_pere = data[3].text.strip()
            date_naissance = data[4].text.strip()

            elv = AdminElvs(
                uid=uid,
                nom_prenom=get_clean_name(nom_prenom),
                nom_pere=get_clean_name(nom_pere),
                date_naissance=date_naissance if is_valid_date_string(date_naissance) else None,
                ecole_id=check_if_sid_need_to_be_replaced(sid,public_school=True)
                )
            
            elvs_array.append(elv)

        try:
            AdminElvs.objects.bulk_create(elvs_array, batch_size=100, ignore_conflicts=False, update_conflicts=True, update_fields=["nom_prenom", "nom_pere", "date_naissance", "ecole_id"])
            print(f"{sid} : updated succesfully with {len(elvs_array)} elvs\n")

        except Exception as e:
            print("------------")
            print("erreur with this : " + str(sid))
            print(f"Exception : {e}")
            print("------------")



def update_students_from_private_schools(request2: requests.Session,dre:Dre):

    sids = AdminEcoledata.objects.filter(del1_id=str(dre.id)+"98").values_list('sid', flat=True)

    for sid in sids:
        elvs_array = []
        url = "https://suivisms.cnte.tn/ministere/index.php?op=prive&act=list_eleve_prive_prim"
        payload = {
            "code_dre": dre.id,
            "code_etab": sid,
            "btenv": "بحث"
        }
        
        soup = post_url_return_soup(url=url,payload=payload,request=request2,decode=True)

        rows = soup.find_all('tr', {'height': '30', 'bgcolor': '#B9FFB9'})

        # print(rows[0].find_all('td', {'align': 'center'}))

        for tr in rows:
            data = tr.findAll('font')
          #  temp_uid = data[1].text.strip()
            uid = data[2].text.strip()
            if uid == "" or uid == "0" or not uid.isdigit():
                print('fama uid egal 0 walla "" :', end='')
                print(uid)
                continue

            nom_prenom = data[3].text.strip()
            nom_pere = data[4].text.strip()
            date_naissance = data[5].text.strip()

            elv = AdminElvs(
                uid=uid,
                nom_prenom=get_clean_name(nom_prenom),
                nom_pere=get_clean_name(nom_pere),
                date_naissance=date_naissance if is_valid_date_string(date_naissance) else None,
                ecole_id=sid,
                #   temp_uid=temp_uid
            )
            elvs_array.append(elv)

        try:
            AdminElvs.objects.bulk_create(elvs_array, batch_size=100, ignore_conflicts=False, update_conflicts=True, update_fields=["nom_prenom", "nom_pere", "date_naissance", "ecole_id"])
            print(f"{sid} : updated succesfully with {len(elvs_array)} elvs")

        except IntegrityError as e:
            print("------------")
            print("errerur with this : " + str(sid))
            print(f"IntegrityError: {e}")
            print("------------")











# ~ zid comparision bin l sids l 5dhithom welli 3ndk famch zeyed walla ne9s
# ~ les preivees in all dre 3ndhom **98 del ?
# bulkcreate lil AdminElvs2 l request 5dheha mil Verify capatcha 5atr lezmn bypass heki bch tod5al donc torbtha m3aha in case of ist3mel
def UpdateStudents(request2: requests.Session,dre:Dre):

    print('\n** Updating students ...')

    print('currently updating public school students...')
    update_students_from_public_schools(request2,dre)
    print("\n✓ public schools updated succesfully")

    print('currently updating private school students...')
    update_students_from_private_schools(request2,dre)
    print("\n✓ private schools updated succesfully")

    return Response(True)

