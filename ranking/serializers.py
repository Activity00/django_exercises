from rest_framework import serializers


class RankingSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=256)
    score = serializers.IntegerField(max_value=10000000, min_value=1)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RankingGetSerializer(serializers.Serializer):
    start = serializers.IntegerField(min_value=0, default=1)
    end = serializers.IntegerField(min_value=0, default=-1)
    device_id = serializers.CharField(max_length=256)

    def validate(self, attrs):
        if attrs['start'] and attrs['end'] and attrs['start'] >= attrs['end']:
            raise serializers.ValidationError({'start': 'start can not more than end.'})
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
