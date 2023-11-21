from rest_framework import serializers

from substances.models import Dose, DosageForm, DoseRecord, RouteOfIngestion, DosageFormDose, Substance, Pharmacokinetics

class DoseRecordSerializer(serializers.Serializer):
    # class Meta:
    #     model = DoseRecord
    #     fields = ['id', 'timestamp', 'substance_id', 'ROI', 'dosage_form_id', 'dosage', 'dosage_unit']
    id = serializers.IntegerField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField()
    substance_id = serializers.IntegerField()
    ROI = serializers.ChoiceField(choices=RouteOfIngestion.ROUTES)
    dosage_form_id = serializers.IntegerField(required=False, allow_null=True)
    dosage = serializers.DecimalField(decimal_places=2, max_digits=10)
    dosage_unit = serializers.ChoiceField(choices=Dose.DOSAGE_UNITS)

    def create(self, validated_data):
        return DoseRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.substance_id = validated_data.get('substance_id', instance.substance_id)
        instance.ROI = validated_data.get('ROI', instance.ROI)
        instance.dosage_form_id = validated_data.get('dosage_form_id', instance.dosage_form_id)
        instance.dosage = validated_data.get('dosage', instance.dosage)
        instance.dosage_unit = validated_data.get('dosage_unit', instance.dosage_unit)

        instance.save()
        return instance

class PharmacokineticsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pharmacokinetics
        fields = ['id', 'substance_id', 'ROI', 'bioavailability', 'tLag', 'tMax', 'tHalf', 'absorption_rate_constant', 'absorption_kinetics']
    ##substance_id = serializers.IntegerField()
    ##ROI = serializers.ChoiceField(choices=RouteOfIngestion.ROUTES)
    ##bioavailability = serializers.DecimalField(decimal_places=2, max_digits=10)
    ##tOnset = serializers.DurationField()
    ##tMax = serializers.DurationField()
    ##tHalf = serializers.DurationField()
    ##absorption_rate_constant = serializers.CharField(max_length=30)
    ##absorption_kinetics = serializers.CharField

class DosageFormDoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DosageFormDose
        fields = ['dosage', 'dosage_unit', 'tLag']

class DosageFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DosageForm
        fields = ['id', 'name', 'substance_id', 'dosage_form_dose_set']
    # name = serializers.CharField()
    # substance_id = serializers.IntegerField()
    dosage_form_dose_set = DosageFormDoseSerializer(many=True, read_only=True)

class SubstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substance
        fields = ['id', 'name', 'volume_of_distribution', 'elimination_rate_constant', 'half_life']
