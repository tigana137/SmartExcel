from rest_framework import serializers

from x.models import AdminElvs, levelstat




class AdminEcoledataSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = AdminElvs
        fields = ["sid", "school_name", "principal"]

