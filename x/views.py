import time
from bidict import bidict
from rest_framework.decorators import api_view
import base64
from django.http import JsonResponse
from rest_framework.response import Response

from x.UpdateDreDatabase import create_AdminEcole_data, create_AdminElvs, create_Elvpremiere, create_Elvsprep, get_dre_instance, reset_dre_database
from x.UpdatesPrincipals import update_principals
from x.exportModels import exportAdminEcoledata, exportAdminElvs, exportDel1, exportDre, exportElvsprep, exportlevelstat
from x.importModels import importAdminEcoledata, importAdminElvs, importDel1, importDre, importElvsprep, importlevelstat
from x.models import AdminEcoledata, AdminElvs, Del1, DirtyNames, Dre, Elvsprep, Tuniselvs, levelstat


sids_to_replace = bidict({"842911": "842811",
                          "842913": "842813",
                          "842922": "842822",
                          "842923": "842823",
                          "842924": "842824",
                          "842912": "842812",
                          "842914": "842814"
                          })

request2 = requests.session()


@api_view(['GET'])
def testSignal(request):
    "http://localhost:80/api/x/testSignal/"

    return Response(False)


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
        reset_dre_database(request2) 
        
        # create_AdminEcole_data(request2)
        # create_AdminElvs(request2)
        # create_Elvsprep(request2)
        # create_Elvpremiere(request2)
    finally:
        request2.close()
    return Response(True)



@api_view(['GET'])
def getMoudirins(request):
    update_principals()

    return Response(True)


@api_view(['GET'])
def exportDB(request):
    "http://localhost:80/api/x/exportDB"
    # exportDre()
    # exportDel1()
    # exportlevelstat()
    # exportAdminEcoledata() 
    # exportAdminElvs()
    # exportElvsprep()
    return Response(True)


@api_view(['GET'])
def importDB(request):
    "http://localhost:80/api/x/importDB"
    # AdminElvs.objects.all().delete()
    # Elvsprep.objects.all().delete()
    # importDre()
    # importDel1()
    # importlevelstat()
    # importAdminEcoledata()
    # importAdminElvs()
    # importElvsprep()
    return Response(True)


