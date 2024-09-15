from django.urls import path
from . import views

urlpatterns = [
    path('testAuth/',
         views.testAuth, name='testAuth'),
    path('testSignal/',
         views.testSignal, name='testSignal'),
    path('GetCapatcha/',
         views.GetCapatcha, name='GetCapatcha'),
    path('VerifyCapatcha/<str:code>',
         views.VerifyCapatcha, name='VerifyCapatcha'),
    path('getmoudirins/',
         views.getMoudirins, name='getMoudirins'),


    path('exportDB/',
         views.exportDB, name='exportDB'),
    path('importDB/',
         views.importDB, name='importDB'),
    path('updateLevelStat/',
         views.updateLevelStat, name='updateLevelStat'),
    path('updateSchoolPhoneNumbers/',
         views.updateSchoolPhoneNumbers, name='updateSchoolPhoneNumbers'),
    path('updateExcelSheets_brillant/',
         views.updateExcelSheets_brillant, name='updateExcelSheets_brillant'),




    path('transfer_rest/',
         views.transfer_rest, name='transfer_rest'),

         
]


"http://localhost:80/api/x/testSignal/"
"http://localhost:80/api/x/GetCapatcha/"
"http://localhost:80/api/x/VerifyCapatcha/84"
"http://localhost:80/api/x/getmoudirins/"

"http://localhost:80/api/x/CreateExcel"


"http://localhost:80/api/x/testAdmin/54"
