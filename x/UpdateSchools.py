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










def get_public_schools_from_select_elements(request2: requests.Session,dre:Dre):
    r'''tnavigi l url fih select t3 l meders l kol w traj3 l options i.e l mederes'''
    soup = get_url_return_soup(url="https://suivisms.cnte.tn/ministere/index.php?op=inscprim&act=find_etab", request=request2,decode=True)

    existing_sids_in_db = set(AdminEcoledata.objects.filter(dre=dre).values_list('sid', flat=True))

    soup = get_url_return_soup(url=f'https://suivisms.cnte.tn/ministere/inscprim/getetab_choix.php?id={dre.id}', request=request2,decode=True)

    options = soup.find_all('option')

    return options



def get_private_schools_from_select_elements(request2: requests.Session,dre:Dre):

    soup = get_url_return_soup(url=f'https://suivisms.cnte.tn/ministere/prive/getetab_prive_prim.php?id={dre.id}', request=request2,decode=True)

    options = soup.find_all('option')

    return options



def check_private_school_id_structure(sid:str,dre:Dre):
    r'''the ids of private schools has to be the id of dre + 98 i.e sousse : 8498
        if other dres doesnt have the same structure it s a problem when excluding the private schools
        in extraction and api calls
    '''

    if str(dre.id)+"98" != sid[:4]:
        raise CustomError(f'''
            the ids of private schools has to be the id of dre + 98 i.e sousse : 8498
            if other dres doesnt have the same structure it s a problem when excluding the private schools
            in extraction and api calls , l id l found : {sid}
        ''')
    return



def modify_incorrect_sid(ecole:AdminEcoledata,):
    prev_sid = ecole.sid
    modified_sid = input('write the actual id to the school : ')
    if not modified_sid.isdigit() and len(modified_sid) != 6 :
        raise CustomError('')
    
    ecole.sid = modified_sid
    ecole.create_levelstats()
    print('✓ school {school_name} and levels are created in the db')
    raise CustomError(f'''got to array "sids_to_replace" and hardcode it to replace the sid with the appropriate one 
                to save students next to the right school s id 
                replace '{prev_sid}' with '{ecole.sid}'
                ''')



def delete_old_private_schools(options,dre:Dre):
    r'''deletes the old private schools from the database '''

    del1_id=str(dre.id) +"98"
    setof_existing_private_schools_in_db = set(AdminEcoledata.objects.filter(dre=dre).filter(del1_id=del1_id).values_list('sid', flat=True)) 
    
    setof_current_sids = {int(option['value']) for option in options}
    
    old_sids = setof_existing_private_schools_in_db - setof_current_sids 

    AdminEcoledata.objects.filter(dre=dre).filter(sid__in =old_sids).delete()



def bulk_update_schools(options,dre:Dre,public=False,private=False):
    if (not private) and (not public) or public and private :
        raise CustomError('3ndk 8alta fil code l function bulk_update_schools lezm feha ima public walla prive True')
    
    
    existing_sids_in_db = set(AdminEcoledata.objects.filter(dre=dre).values_list('sid', flat=True)) if public else []

    instances = []
    for option in options:
        sid = option['value']

        if public:
            sid = check_if_sid_need_to_be_replaced(sid, public_school=public,private_school=private)
        if private:
            check_private_school_id_structure(sid,dre)
            
        school_name = option.get_text()
        school_name = get_clean_name_for_school_name(school_name, public_school=public,private_school=private)

        ecole = AdminEcoledata(
            sid=sid,
            school_name=school_name,
            dre=dre,
            del1_id=sid[:4],
        )

        if  public and int(sid) not in existing_sids_in_db:  # create Levelstat instances for the levels
            print(f'New school found : {school_name} with an id of {sid}')
            confimation_input = input("if the school's id is correct press 'y' to continue : ")

            if confimation_input =='y' :
                ecole.ministre_school_name=school_name
                ecole.create_levelstats()
                print(f'✓ school {school_name} and levels are created in the db')
                continue
            
            modify_incorrect_sid(ecole)

        instances.append(ecole)


    with transaction.atomic():
        
        AdminEcoledata.objects.bulk_create(instances, batch_size=100, ignore_conflicts=False, update_conflicts=True, update_fields=["school_name"])

    if private:
        delete_old_private_schools(options,dre)
    



# bulkcreate l data t3 mders f admin ecole data prive w etatik
def UpdateSchools(request2: requests.Session,dre:Dre):

    print('\n** Updating Schools information ')

    # public
    print('currently updating public schools ...')
    options = get_public_schools_from_select_elements(request2,dre)
    bulk_update_schools(options,dre,public=True)
    print("✓ public schools updated succesfully")
  
    # private
    print('currently updating private schools ...')
    options=get_private_schools_from_select_elements(request2,dre)
    bulk_update_schools(options,dre,private=True)
    print("✓ private schools updated succesfully")
   

    return Response(True)