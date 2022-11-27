from rest_framework import serializers

from substances.models import Dose, DoseRecord, RouteOfIngestion

class DoseRecordSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    substance_id = serializers.IntegerField()
    ROI = serializers.ChoiceField(choices=RouteOfIngestion.ROUTES)
    dosage_form_id = serializers.IntegerField(required=False, allow_null=True)
    dosage = serializers.DecimalField(decimal_places=2, max_digits=10)
    dosage_unit = serializers.ChoiceField(choices=Dose.DOSAGE_UNITS)

    def create(self, instance, validated_data):
        return DoseRecord.objects.create(**vallidated_data)

    def update(self, instance, validated_data):
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.substance_id = validated_data.get('substance_id', instance.substance_id)
        instance.ROI = validated_data.get('ROI', instance.ROI)
        instance.dosage_form_id = validated_data.get('dosage_form_id', instance.dosage_form_id)
        instance.dosage = validated_data.get('dosage', instance.dosage)
        instance.dosage_unit = validated_data.get('dosage_unit', instance.dosage_unit)

        instance.save()
        return instance

class PharmacokineticsSerializer(serializers.Serializer):
    substance_id = serializers.IntegerField()
    ROI = serializers.ChoiceField(choices=RouteOfIngestion.ROUTES)
    bioavailability = serializers.DecimalField(decimal_places=2, max_digits=10)
    tOnset = serializers.DurationField()
    tMax = serializers.DurationField()
    tHalf = serializers.DurationField()
