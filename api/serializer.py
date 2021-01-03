from rest_framework import serializers


class DB(object):
    def __init__(self, column, data):
        self.column = column
        self.data = data
        self.length = len(data)


class DBConnectorSerializer(serializers.Serializer):
    column = serializers.ListField()
    data = serializers.ListField()
    length = serializers.IntegerField()
