from openpyxl import load_workbook
from x.functions import CustomError
from x.models import AdminEcoledata


column_starting_point = 'B'
row_starting_point = 8



def check_if_sid_valid(sid:str,row:int):
    r'''check if the school id is digit with a length of 6'''

    if type(sid)!=int or len(str(sid)) !=6:
        raise CustomError(f'''fama id t3 ecole mehouch  digit walla length te3ou mouch 6 f row {row+row_starting_point}
            l valeur ta3 l cell is : "{sid}"
            ''')



def check_duplicates(sid,sids_array,ministre_school_name):
    r'''check if id is already treated b4 in the excel file'''
    if sid in sids_array:
        confirmation_msg =input(f'''l id {sid} t3 l'ecole {ministre_school_name} deja 3mltlha l traitement 9bal donc imma hedhi l id
        t3ha 8alt walla lo5ra press 'y' to break : ''')
        if confirmation_msg=='y':
            raise CustomError('')



def check_if_sid_in_db(sid,sids,ministre_school_name:str,):

    if int(sid) not in sids :
        confirmation_msg =input(f"l id {sid} t3 l'ecole {ministre_school_name} mouch mawjoud fil db press 'y' to break : ")
        if confirmation_msg=='y':
            raise CustomError('')
    return


def annualexcel(dre_id:int):
    sids = AdminEcoledata.objects.filter(dre_id=dre_id).values_list('sid',flat=True)
    wb = load_workbook("xx.xlsx")
    ws = wb.active

    row = row_starting_point
    
    ecoles = []
    sids_array = []
    
    while ws['C'+str(row)].value :
        sid = ws['C'+str(row)].value

        check_if_sid_valid(sid,row)

        ministre_school_name = ws['D'+str(row)].value
        
        check_if_sid_in_db(sid,sids,ministre_school_name)
        check_duplicates(sid,sids_array,ministre_school_name)


        premier_elvs = ws['S'+str(row)].value
        premier_classes = ws['T'+str(row)].value
        
        deuxieme_elvs = ws['X'+str(row)].value
        deuxieme_classes = ws['Y'+str(row)].value

        troisieme_elvs = ws['AC'+str(row)].value
        troisieme_classes = ws['AD'+str(row)].value

        quaterieme_elvs = ws['AH'+str(row)].value
        quaterieme_classes = ws['AI'+str(row)].value

        cinquieme_elvs = ws['AM'+str(row)].value
        cinquieme_classes = ws['AN'+str(row)].value

        sixieme_elvs = ws['AR'+str(row)].value
        sixieme_classes = ws['AS'+str(row)].value
        
        AdminEcoledata.objects.get(sid=sid).update_levelstat((premier_elvs,premier_classes),(deuxieme_elvs,deuxieme_classes),(troisieme_elvs,troisieme_classes),(quaterieme_elvs,quaterieme_classes),(cinquieme_elvs,cinquieme_classes),(sixieme_elvs,sixieme_classes))        
        
        ecole = AdminEcoledata(
            sid=sid,
            ministre_school_name=ministre_school_name
        )
        ecoles.append(ecole)
        sids_array.append(sid)
        row+=1

    AdminEcoledata.objects.bulk_update(ecoles,fields=['ministre_school_name'])
    
    return



