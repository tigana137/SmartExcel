

from rest_framework import serializers
from x.models import AdminEcoledata, levelstat


class levelstatSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = levelstat
        fields = ["lid","nbr_elvs", "nbr_classes", "nbr_leaving", "nbr_comming"]


class AdminEcoledataSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = AdminEcoledata
        fields = ["sid", "ministre_school_name", "principal"]


class AdminEcoledata2Serializer(serializers.ModelSerializer):
    del1_name = serializers.StringRelatedField(source='del1', read_only=True)

    class Meta(object):
        model = AdminEcoledata
        fields = ["sid", "ministre_school_name", "principal","del1_name","email","phone1","phone2"]
