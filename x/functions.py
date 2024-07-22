from bs4 import BeautifulSoup as bs
from bidict import bidict


class CustomError(Exception):
    def __init__(self, message="error raised without message"):
        self.message = message
        super().__init__(self.message)


# [l ids l yelzmhom ytbadlou] : actual id fil db
sids_to_replace = bidict({"842911": "842811",
                          "842913": "842813",
                          "842922": "842822",
                          "842923": "842823",
                          "842924": "842824",
                          "842912": "842812",
                          "842914": "842814"
                          })


# tna7i l repetition t3 l chadda w tfas5 l soukoun, fat7a, kasra, tajwid,dhama, kasrtin, fat7tin, dhamtin
def get_clean_name(name: str):
    soukoun = 'ْ'
    fat7a = 'َ'
    fat7tin = 'ً'
    kasra = 'ِ'
    kasrtin = 'ٍ'
    tajwid = 'ـ'
    dhama = 'ُ'
    dhamtin = 'ٌ'

    bullshit = [soukoun, fat7a, kasra, tajwid,dhama, kasrtin, fat7tin, dhamtin]

    clean_name = ''
    for i in range(len(name)):

        if name[i] == "ّ" and clean_name == '':  # e.g if awil 7rouf ybdew chadda bark
            continue
        if name[i] == "ّ" and name[i-1] == "ّ" and i > 0:
            continue

        if name[i] not in bullshit:
            clean_name += name[i]

    return clean_name



def get_url_return_soup(url:str,request,decode:bool=True):
    response = request.get(url)
    
    soup = bs(response.content.decode(encoding='utf-8', errors='ignore'), 'html.parser')
    
    return soup



def post_url_return_soup(url:str,payload,request,decode:bool=True):
    response = request.post(url=url, data=payload)

    soup = bs(response.content.decode(encoding='utf-8', errors='ignore'), 'html.parser')
    
    return soup





def check_if_sid_need_to_be_replaced(sid:str,public_school=False,private_school=False):
    if sid=="" or sid =="0":
        raise CustomError("famma sid equal null or 0 * f select t3 قائمة التلاميذ (من الثانية إلى السادسة)" + ("etatiq" if public_school else "privee") )

    if private_school and sid[2:4] !="98":
        raise CustomError(f'fama id t3 ecole fil prive metab3ch l forme t3 8498** : {sid}' )


    if sid in sids_to_replace.keys():
        return sids_to_replace[sid]
    
    return sid 








def get_clean_name_for_school_name(school_name,public_school=False,private_school=False):
    if school_name=='':
        raise CustomError("school_name je fera8 k jit te5ou fih mil options winti t updati f schools_data defq ")
    
    if public_school:
        return school_name.replace('م.إ.  ', '').replace('م.إبت. ', '').replace('م.إ. ', '').replace('المدرسة الابتدائية ', '')
    
    
    if private_school:
        return school_name.replace('المدرسة الابتدائية الخاصة  ', '').replace('المدرسة الابتدائية الخاصة ', '')













