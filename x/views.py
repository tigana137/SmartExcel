import requests
from rest_framework.decorators import api_view,permission_classes
import base64
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from excel.functions import adjust_levelstat
from excel.models import excelsheets
from users.functions import verify_jwt
from users.models import UserProfile
from x.AnnualExcel import annualexcel
from x.UpdateStudents import UpdateStudents
from x.UpdateSchools import UpdateSchools
from x.Update_1st_grade_students import Update_1st_grade_students
from x.Update_kindergarten_students import Update_kindergarten_students
from x.excelPhoneNumberEmail import excelPhoneNumberEmail
from x.reset_dre_database import reset_dre_database
from x.UpdatesPrincipals import update_principals
from x.exportModels import exportAdminEcoledata, exportAdminElvs, exportDel1, exportDre, exportElvsprep, exportExcelSheets, exportlevelstat
from x.functions import CustomError
from x.importModels import importAdminEcoledata, importAdminElvs, importDel1, importDre, importElvsprep, importExcelSheets, importlevelstat, importlevelstat2
from x.models import AdminEcoledata, AdminElvs, Del1, DirtyNames, Dre, Elvsprep, Tuniselvs, levelstat




request2 = requests.session()


@api_view(['GET'])
@permission_classes([AllowAny])
def testSignal(request):
    # "http://localhost:80/api/x/testSignal/"

    return Response(True)  



@api_view(['GET'])
def testAuth(request):
    "http://localhost:80/api/x/testAuth/"
    return Response(True) 


 
@api_view(['GET'])
def GetCapatcha(request):
    "http://localhost:80/api/x/GetCapatcha/"


    url = "https://suivisms.cnte.tn/"
    request2.get(url=url)

    try:
        url_img = "https://suivisms.cnte.tn/inclure/img.php"
        img = request2.get(url=url_img)
    except Exception as e:
        print(e)
        raise CustomError("fama mochkla k jit te5ou fil taswira")

    # Assuming you have the binary image data in 'image_data'
    image_data_base64 = base64.b64encode(img.content).decode('utf-8')

    # Create a JSON response with the base64-encoded image
    response_data = {'image_data': image_data_base64}

    with open('capatcha_img.jpg',"wb") as w :
        w.write(img.content)

    return JsonResponse(response_data)


@api_view(['GET'])
def VerifyCapatcha(request, code):
    "http://localhost:80/api/x/VerifyCapatcha/"

    url = "https://suivisms.cnte.tn/"
    payload = {"login": "user8420",
               "pwd": "78b9adE48U",
               "secure": code,
               "auth": "",
               }

    response = request2.post(url=url, data=payload)

    # response.headers
    if not ("https://suivisms.cnte.tn/" in response.url):
        print(response.url)
        return Response(False)
    try:
        0
        # dre = reset_dre_database(request2) 
        # UpdateSchools(request2,dre)
        # UpdateStudents(request2,dre)
        # Update_1st_grade_students(request2,dre)
        # Update_kindergarten_students(request2,dre)
        # annualexcel(dre_id=dre.id)
        # print("\n✓✓✓ operation completed succesfully\n")
    finally:
        request2.close()

    return Response(True)



@api_view(['GET'])
def getMoudirins(request):
    update_principals()

    return Response(True)


@api_view(['GET'])
@permission_classes([AllowAny])
def exportDB(request):
    "http://localhost:80/api/x/exportDB"
    # exportDre()
    # exportDel1()
    # exportlevelstat()
    # exportAdminEcoledata()  
    # exportAdminElvs()
    # exportElvsprep()
    exportExcelSheets()
    return Response(True)


@api_view(['GET'])
@permission_classes([AllowAny])
def importDB(request):
    "http://localhost:80/api/x/importDB"
    # # AdminElvs.objects.all().delete()
    # # Elvsprep.objects.all().delete()
    # importDre()
    # importDel1()
    # importlevelstat()
    # importAdminEcoledata()
    # importAdminElvs()
    # importElvsprep()
    importExcelSheets()
    return Response(True)


@api_view(['GET'])
def updateLevelStat(request):
    r'''this one updates only the inital number of elves in 30 august and number of classes in case the annuel excel
    comes out late and they are transferring students already'''
    "http://localhost:80/api/x/updateLevelStat/"
    # importlevelstat2()
    return Response(True)





@api_view(['GET'])
def updateSchoolPhoneNumbers(request):
    r'''this one updates school's phone numbers and email from an excel file
    the file name should be : PhonesAndEmails.xlsx'''
    "http://localhost:80/api/x/updateSchoolPhoneNumbers/"
    # excelPhoneNumberEmail(dre_id=84)
    return Response(True)


from openpyxl import load_workbook


@api_view(['GET'])
@permission_classes([AllowAny])
def testforTransferring(request):
    "http://localhost:80/api/x/testforTransferring/" 
 
    elvs_level= 4

    levels =levelstat.objects.filter(lid__endswith=elvs_level)
    for level in levels:
        level.nbr_comming=0
        level.nbr_leaving=0
    levelstat.objects.bulk_update(levels,fields=['nbr_comming','nbr_leaving'])

    wb = load_workbook("trans.xlsx",data_only=True)
    # ws = wb.active
    ws = wb.worksheets[elvs_level-1]
    
    row_starting_point= 12 if elvs_level in [1,3,4,] else 11
    row = row_starting_point 
    charr ='L' if elvs_level!=1 else 'K'


    while ws[charr+str(row)].value or ws[charr+str(row+1)].value or ws[charr+str(row+2)].value or ws[charr+str(row+3)].value :

        del1 = str(ws[charr+str(row)].value)
        
        next_char = chr(ord(charr) + 1)
        nom_prenom = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        sid = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        prev_ecole = str(ws[next_char+str(row)].value)
      
        next_char = chr(ord(next_char) + 1)
        next_ecole = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        reason = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        decision =str(ws[next_char+str(row)].value)


        prev_ecole_instance =AdminEcoledata.objects.exclude(del1_id=8498).filter(ministre_school_name=prev_ecole).first()
        nxt_ecole_instance =AdminEcoledata.objects.exclude(del1_id=8498).filter(ministre_school_name=next_ecole).first()

        # if not prev_ecole_instance:
        #     print(f'ml9ach rzabou row={row}  ismha --{prev_ecole}--')

        if not nxt_ecole_instance:
            print(f'ml9ach rzabou row={row}  ismha --{next_ecole}--')

        adjust_levelstat(ecole_added_to_id=nxt_ecole_instance.sid if nxt_ecole_instance else 0, ecole_removed_from_id=prev_ecole_instance.sid if prev_ecole_instance else 0, level=elvs_level,dre_id=84,cancel=False)
        
        if decision!="مع الموافقة":
            # print(f'decision = --{decision}--     7arf lou houwa -{decision[0]}-')
            pass

        row+=1

    return Response(True)


dicc= {
    1:1,
    2:1,
    3:1,
    4:1,
    5:1,
    6:1,
}

def add_new_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level,problem):


    print(problem)
    workbook = load_workbook("rest.xlsx")
    sheetname = workbook.sheetnames[int(level)-1]
    sheet = workbook[sheetname]
    charr ='A'
    row = dicc[int(level)]
    
    # print(f'charr+{str(row)}   {del1}')
    sheet[charr+str(row)] = del1
            
    next_char = chr(ord(charr) + 1)
    sheet[next_char+str(row)] = nom_prenom
 
    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = uid

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = prev_ecole

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = next_ecole

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = reason

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = decision

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = problem

    dicc[int(level)]+=1

    workbook.save("rest.xlsx")




def consists_of_12_digits(s: str) -> bool:
    # Check if the string is exactly 12 characters long and contains only digits
    return len(s) == 12 and s.isdigit() or len(s) == 11 and s.isdigit() or s =="0" or s==0 or s =='0.0'


@api_view(['GET'])
@permission_classes([AllowAny])
def transferrrrr(request):
    "http://localhost:80/api/x/transferrrrr/" 

    elvs_level= 6

    levels =levelstat.objects.filter(lid__endswith=elvs_level)
    for level in levels:
        level.nbr_comming=0
        level.nbr_leaving=0
    levelstat.objects.bulk_update(levels,fields=['nbr_comming','nbr_leaving'])

    wb = load_workbook("nou9al.xlsx",data_only=True)
    # ws = wb.active
    ws = wb.worksheets[elvs_level-1]
    
    row_starting_point= 11 if elvs_level in [1,2,5,6] else 12
    row = row_starting_point 
    charr ='C' # !!!!


    while ws[charr+str(row)].value or ws[charr+str(row+1)].value or ws[charr+str(row+2)].value or ws[charr+str(row+3)].value :

        del1 = str(ws[charr+str(row)].value)
        
        next_char = chr(ord(charr) + 1)
        nom_prenom = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        uid = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        prev_ecole = str(ws[next_char+str(row)].value)
      
        next_char = chr(ord(next_char) + 1)
        next_ecole = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        reason = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        decision = str(ws[next_char+str(row)].value)


        prev_ecole_instance =AdminEcoledata.objects.exclude(del1_id=8498).filter(ministre_school_name=prev_ecole).first()
        nxt_ecole_instance =AdminEcoledata.objects.exclude(del1_id=8498).filter(ministre_school_name=next_ecole).first()

        row+=1

        if not consists_of_12_digits(uid):
            add_new_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level=elvs_level,problem='mochkla uid')
            continue

        if not prev_ecole_instance:
            add_new_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level=elvs_level,problem='mochkla f prev ecole')
            continue
            # print(f'ml9ach rzabou row={row}  ismha --{prev_ecole}--')

        if not nxt_ecole_instance:
            add_new_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level=elvs_level,problem='mochkla f next ecole')
            continue
            # print(f'ml9ach rzabou row={row}  ismha --{next_ecole}--')

        decision_ecole_instance = None

        if decision != "مع الموافقة":
            decision_ecole_instance =AdminEcoledata.objects.exclude(del1_id=8498).filter(ministre_school_name=decision).first()
            if not decision_ecole_instance:
                add_new_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level=elvs_level,problem='mouch f decision')
                continue
        print('mrgl')   
        adjust_levelstat(ecole_added_to_id=decision_ecole_instance.sid if decision_ecole_instance else nxt_ecole_instance.sid, ecole_removed_from_id=prev_ecole_instance.sid , level=elvs_level,dre_id=84,cancel=False)
        excelsheets(
            uid=uid,
            nom_prenom=nom_prenom,
            prev_ecole=prev_ecole_instance.ministre_school_name,
            prev_ecole_id=prev_ecole_instance.sid,
            Del1=del1,
            level=elvs_level,
            next_ecole=nxt_ecole_instance.ministre_school_name,
            next_ecole_id=nxt_ecole_instance.sid,
            reason=reason,
            decision=decision,
            decision_id= 0 if decision=="مع الموافقة" else decision_ecole_instance.sid,
            dre_id=84

        ).save()
        elv = AdminElvs.objects.filter(uid=uid).first()
        if not elv:
            AdminElvs(
                uid=uid,
                nom_prenom=nom_prenom,
                ecole_id=  nxt_ecole_instance.sid if decision=="مع الموافقة" else decision_ecole_instance.sid,
            ).save()




    return Response(True)




def add_new_resttt_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level,problem):


    print(problem)

    workbook = load_workbook("rest_new.xlsx")
    sheetname = workbook.sheetnames[int(level)-1]
    sheet = workbook[sheetname]
    charr ='A'
    row = dicc[int(level)]
    
    sheet[charr+str(row)] = del1
            
    next_char = chr(ord(charr) + 1)
    sheet[next_char+str(row)] = nom_prenom
 
    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = uid

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = prev_ecole

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = next_ecole

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = reason

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = decision

    next_char = chr(ord(next_char) + 1)
    sheet[next_char+str(row)] = problem

    dicc[int(level)]+=1

    workbook.save("rest_new.xlsx")

def alterstr(uid):
    if uid.endswith('.0'):
        return uid[:-2]  # Remove the last two characters '.0'
    return uid

from django.db.models import F, Func


@api_view(['GET'])
@permission_classes([AllowAny])
def transferrrrr_rest(request):
    "http://localhost:80/api/x/transferrrrr_rest/" 

    elvs_level= 'xx'
    prev_ecole_sug =  {
    "مدرسة خاصة"   :"-2" ,
    "خارج الولاية"  :"-3"  ,
    "خارج الوطن"   :"-4" ,
}

    wb = load_workbook("rest_traitee.xlsx",data_only=True)
    # ws = wb.active
    ws = wb.worksheets[elvs_level-1]
    
    row_starting_point= 1
    row = row_starting_point 
    charr ='A' # !!!!


    while ws[charr+str(row)].value or ws[charr+str(row+1)].value or ws[charr+str(row+2)].value or ws[charr+str(row+3)].value :

        del1 = str(ws[charr+str(row)].value)
        
        next_char = chr(ord(charr) + 1)
        nom_prenom = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        uid = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        prev_ecole = str(ws[next_char+str(row)].value)
      
        next_char = chr(ord(next_char) + 1)
        next_ecole = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        reason = str(ws[next_char+str(row)].value)

        next_char = chr(ord(next_char) + 1)
        decision = str(ws[next_char+str(row)].value)



        decision_ecole_instance = None 

        row+=1
        uid = alterstr(uid)
        prev_ecole=alterstr(prev_ecole)
        next_ecole=alterstr(next_ecole)
        decision=alterstr(decision)

        prev_ecole_instance =AdminEcoledata.objects.exclude(del1_id=8498).filter(sid=prev_ecole).first() if prev_ecole.isdigit() else AdminEcoledata.objects.exclude(del1_id=8498).annotate(trimmed_name=Func(F('ministre_school_name'), function='TRIM')).filter(trimmed_name__icontains=prev_ecole).first()
        nxt_ecole_instance =AdminEcoledata.objects.exclude(del1_id=8498).filter(sid=next_ecole).first() if next_ecole.isdigit() else AdminEcoledata.objects.exclude(del1_id=8498).annotate(trimmed_name=Func(F('ministre_school_name'), function='TRIM')).filter(trimmed_name__icontains=next_ecole).first()


        if decision != "مع الموافقة":
            decision_ecole_instance =AdminEcoledata.objects.exclude(del1_id=8498).filter(sid=decision).first() if decision.isdigit() else AdminEcoledata.objects.exclude(del1_id=8498).annotate(trimmed_name=Func(F('ministre_school_name'), function='TRIM')).filter(trimmed_name__icontains=decision).first()
            if not decision_ecole_instance:
                add_new_resttt_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level=elvs_level,problem='mouch f decision')
                continue

        if not consists_of_12_digits(uid):
            add_new_resttt_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level=elvs_level,problem='mochkla uid')
            continue

        if not prev_ecole_instance and prev_ecole not in prev_ecole_sug and prev_ecole!="0" and prev_ecole!='0.0':
            add_new_resttt_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level=elvs_level,problem='mochkla f prev ecole')
            continue
            # print(f'ml9ach rzabou row={row}  ismha --{prev_ecole}--')

        if not nxt_ecole_instance :
            if decision != "مع الموافقة" and not decision_ecole_instance :
                add_new_resttt_excel_row(del1,nom_prenom,uid,prev_ecole,next_ecole,reason,decision,level=elvs_level,problem='mochkla f next ecole')
                continue
            # print(f'ml9ach rzabou row={row}  ismha --{next_ecole}--')


        print('mrgl')   
        nxtecole= nxt_ecole_instance.sid if nxt_ecole_instance else 0 
        nxtecole= decision_ecole_instance.sid if decision_ecole_instance else nxtecole

        adjust_levelstat(ecole_added_to_id=nxtecole, ecole_removed_from_id=prev_ecole_instance.sid if prev_ecole_instance else 0, level=elvs_level,dre_id=84,cancel=False)
        
        prev_id=prev_ecole_instance.sid if prev_ecole_instance else 0
        if prev_ecole in prev_ecole_sug:
            prev_id = prev_ecole_sug[prev_ecole]
        excelsheets( 
            uid=uid if uid!='0.0' else 0,
            nom_prenom=nom_prenom,
            prev_ecole=prev_ecole_instance.ministre_school_name if prev_ecole_instance else prev_ecole,
            prev_ecole_id=prev_id,
            Del1=del1,
            level=elvs_level,
            next_ecole=nxt_ecole_instance.ministre_school_name if nxt_ecole_instance else "  ",
            next_ecole_id=nxt_ecole_instance.sid if nxt_ecole_instance else 0,
            reason=reason,
            decision=decision,
            decision_id= decision_ecole_instance.sid if decision_ecole_instance else 0,
            dre_id=84

        ).save()


        if uid != "0" and uid != 0 and uid!='0.0':
            elv = AdminElvs.objects.filter(uid=uid).first()
            if not elv:
                ell =AdminElvs(
                    uid=uid,
                    nom_prenom=nom_prenom,
                )
                if nxtecole !=0:
                    ell.ecole_id =nxtecole
                ell.save()




    return Response(True)



