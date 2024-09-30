from rest_framework import serializers

from excel.models import excelsheets, excelsheets_brillant


class excelsheetsSerializer(serializers.ModelSerializer):

    next_ecole = serializers.CharField(trim_whitespace=False)  # Adjust the field

    class Meta(object):
        model = excelsheets
        fields = ["uid", "nom_prenom", "nom_pere", "date_naissance", "level", "prev_ecole", "prev_ecole_id",
                  "Del1", "next_ecole", "next_ecole_id", "reason", "decision","decision_id", "comments", "dre_id","user_id"]




class excelsheetsSerializerSearchTransferElvs(serializers.ModelSerializer):

    class Meta(object):
        model = excelsheets
        fields = ["uid", "nom_prenom",  "level", "prev_ecole",  "next_ecole", "reason", "decision","decision_id", "comments", "dre_id","date_downloaded"]




class excelsheets_brillantSerializerSearchTransferElvs(serializers.ModelSerializer):

    class Meta(object):
        model = excelsheets_brillant
        fields = ["uid", "nom_prenom",  "level", "prev_ecole",  "next_ecole", "reason", "decision","date_downloaded"]  


