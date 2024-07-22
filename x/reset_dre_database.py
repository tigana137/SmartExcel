import re
import time
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from bidict import bidict

from django.db import IntegrityError, transaction
from requests.exceptions import ChunkedEncodingError
from rest_framework.response import Response
from excel.models import excelsheets
from x.functions import CustomError, check_if_sid_need_to_be_replaced, get_clean_name, get_clean_name_for_school_name, get_url_return_soup, post_url_return_soup


from x.models import AdminEcoledata, AdminElvs, Del1,  Dre, Elvsprep, levelstat
from pprint import pprint






def verify_select_structure_valid(options,initial_error_msg:str):
    
    

    if not options:
        raise CustomError(initial_error_msg + "medem raisa l error hedhi m3neha l options rj3t None")
    
    if len(options) != 2 :  # ~ lezmhm nrmlmnt l kol zouz loula kil ---- w b3d l weileya chouf ken le nik errur or somethn
        raise CustomError(initial_error_msg + "medem raisa l error hedhi m3neha options!=2")
    
    if options[0]['value']!="0":
        raise CustomError(initial_error_msg + "medem raisa l error hedhi m3neha l value t3 option loula != 0 ")
    
    if options[0].text.strip() !="-----------------------":
        raise CustomError(initial_error_msg + 'medem raisa l error hedhi m3neha l ism l option loula != 0  "-----------------------"')


    return



def get_dre(options,initial_error_msg:str):
    dre_id = options[1]['value']
    dre =Dre.objects.filter(id=dre_id).first()
    
    if not dre : 
        raise CustomError(initial_error_msg+ "l value t3 l wileya nrmlmnt l id t3ha ama l value l jbettou mehomch fil db :"+ str(dre_id))
    
    return dre



def get_dre_instance(request2: requests.Session):
    
    soup = get_url_return_soup(url="https://suivisms.cnte.tn/ministere/index.php?op=inscprim&act=find_etab",request=request2)
    dre_select_elm = soup.find('select', {'name': 'code_dre'})

    options = dre_select_elm.findAll('option')
    
    
    initial_error_msg ='''
        fil url : "https://suivisms.cnte.tn/ministere/index.php?op=inscprim&act=find_etab"
        tl9a select ismha "المندوبية الجهوية للتربية" nrmlmnt tl9a 7ajtin bark
        l options t3 select  feha ------- w b3d l wileya \n '''
    verify_select_structure_valid(options,initial_error_msg)
    
    dre = get_dre(options,initial_error_msg)
    
    confirmation_input = input(f'dre is {dre.name} press "y" to continue : ')

    if confirmation_input !="y":
        raise CustomError()
    
    return dre



def get_count_dre_etatiq_schools(dre:Dre):

    del1_of_private_schools = str(dre.id) + "98"

    nbr_schools_dre = AdminEcoledata.objects.filter(dre = dre).exclude(del1_id =del1_of_private_schools).count()

    return nbr_schools_dre



def reset_stats_to_0 (dre:Dre,nbr_schools_dre:int): # ~ l filtrage mouch necessaraly perfect k tfiltri lid ybda bil id t3 dre kima 84 ...

    stats_instances_of_dre_schools =  levelstat.objects.filter(lid__startswith=dre.id)

    nbr_schools_accordin_to_stats = stats_instances_of_dre_schools.count() / 6

    if nbr_schools_dre != nbr_schools_accordin_to_stats:
        confimation_input = input('''nbr t3 stats b3d me 9smthom 3ala 6 mayjiwch egal l actual nbr of schools 
              nbr 7ab stat =  {nbr_schools_accordin_to_stats}
              len of AdminEcoledata in dre =  {nbr_schools_dre} 
              press 'Y' if u want to continue : 
                ''')
        
        if confimation_input !='y':
            raise CustomError()
        
    
    for stat in stats_instances_of_dre_schools:
        stat.nbr_elvs=0
        stat.nbr_classes=0
        stat.nbr_leaving=0
        stat.nbr_comming=0

    levelstat.objects.bulk_update(stats_instances_of_dre_schools,fields=["nbr_elvs","nbr_classes","nbr_leaving","nbr_comming",])

    print('✓ stats resetted to 0')  



def delete_students(dre:Dre):

    eleves = AdminElvs.objects.filter(ecole__dre=dre)
    eleves_count = eleves.count()
    eleves.delete()

    print(f'✓ students deleted len = {eleves_count}')



def delete_prep_students(dre:Dre):

    confirmation_input = input('you want to delete preparatoire students to ? press "y" to confirm : ')
    
    if confirmation_input=='y':

        eleves_preparatoire = Elvsprep.objects.filter(ecole__dre=dre)
        eleves_preparatoire_count = eleves_preparatoire.count()
        eleves_preparatoire.delete()

        print(f'✓ prep students deleted len = {eleves_preparatoire_count}')
        return
    
    print('🗙 deleting of prep students is skipped')



def delete_excel_sheets(dre: Dre):

    sheets = excelsheets.objects.filter(dre=dre)
    sheets_count = sheets.count()
    sheets.delete()

    print(f'✓ excel sheets deleted len = {sheets_count}')



def reset_dre_database(request2: requests.Session):

    dre = get_dre_instance(request2)
    
    nbr_schools_dre = get_count_dre_etatiq_schools(dre)

    confimation_input = input(f"deleting the database of {dre.name[::-1]} including : students , resetin all stats grades to 0 , press 'y' to confirm : ")
    
    if confimation_input =='y':
        print("\n** Resetting the database ... ")

        reset_stats_to_0(dre,nbr_schools_dre)
    
        delete_students(dre)

        delete_prep_students(dre)

        delete_excel_sheets(dre)

        print(f'✓ database is reset for the dre : {dre.name[::-1]}')
        
        return dre
    

    print('🗙 resetting databse is skipped')
    return dre