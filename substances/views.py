from django.shortcuts import render
# from rest_framework import authentication
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from substances.models import DoseRecord, DosageForm, DosageFormDose, Substance, Pharmacokinetics
from substances.serializers import DoseRecordSerializer, DosageFormSerializer, DosageFormDoseSerializer,\
    PharmacokineticsSerializer, SubstanceSerializer
from django.db.models import Prefetch


class SubstancesDetailView(APIView):
    http_method_name = ['get']

    def get(self, request):
        dosage_form_queryset = DosageForm.objects.prefetch_related('dosageformdose_set')
        substances_queryset = Substance.objects.prefetch_related('pharmacokinetics_set').prefetch_related(Prefetch('dosageform_set', queryset=dosage_form_queryset))
        output = []
        for substance in substances_queryset:
            substance_data = SubstanceSerializer(substance).data

            pharmacokinetics_data  = PharmacokineticsSerializer(substance.pharmacokinetics_set.all(), many=True).data
            substance_data['pharmacokinetics'] = pharmacokinetics_data


            dosage_formset = substance.dosageform_set.all()
            substance_dosage_forms = []
            for dosage_form in dosage_formset:
                doses = []
                dosage_form_data = DosageFormSerializer(dosage_form).data

                doses_set = dosage_form.dosageformdose_set.all()

                for dose in doses_set:
                    dose_data = DosageFormDoseSerializer(dose).data
                    doses.append(dose_data)
                dosage_form_data['doses'] = doses
                substance_dosage_forms.append(dosage_form_data)
            substance_data['dosage_forms'] = substance_dosage_forms
            output.append(substance_data)
        return Response(output)



class SubstancesView(APIView):
    http_method_name = ['get']

    def get(self, request):
        substances = Substance.objects.all()
        serializer = SubstanceSerializer(substances, many=True)
        return Response(serializer.data)

class DosageFormDosesView(APIView):
    http_method_names = ['get']

    def get(self, request, pk):
        doses = DosageFormDose.objects.filter(dosage_form_id=pk)
        serializer = DosageFormDoseSerializer(doses, many=True)
        return Response(serializer.data)

class SubstanceFormulationsView(APIView):
    http_method_names = ['get']

    def get(self, request, pk):
        dosage_forms = DosageForm.objects.filter(substance_id=pk)
        serializer = DosageFormSerializer(dosage_forms, many=True)
        return Response(serializer.data)


class SubstancePharmacokineticsView(APIView):
    http_method_names = ['get']

    def get(self, request, pk):
        kinetics = Pharmacokinetics.objects.filter(substance_id=pk)
        serializer = PharmacokineticsSerializer(kinetics, many=True)
        return Response(serializer.data)


class DoseRecordView(APIView):
    http_method_names  = ['get', 'post', 'put', 'delete']
    # permission_classes = []

    def get(self, request, pk=None):
        if pk:
            dose_record = get_object_or_404(DoseRecord.objects.all(), pk=pk)
            serializer = DoseRecordSerializer(dose_record)
            return Response({"dose_record": serializer.data})
        dose_records = DoseRecord.objects.all()
        serializer = DoseRecordSerializer(dose_records, many=True)
        return Response({"dose_records": serializer.data})
        pass

    def post(self, request):
        dose_record = request.data

        serializer = DoseRecordSerializer(data=dose_record)
        if serializer.is_valid(raise_exception=True):
            saved_dose_record = serializer.save()
        return Response({"success": "Dose Record {0} created successfully".format(saved_dose_record.id)})

    def put(self, request, pk):
        dose_record = get_object_or_404(DoseRecord.objects.all(), pk=pk)
        data = request.data.get('dose_record')
        serializer = DoseRecordSerializer(instance=dose_record, data=data, partial=True)

        breakpoint()
        if serializer.is_valid(raise_exception=True):
            saved_dose_record = serializer.save()
        return Response({"success": "Dose Record {0} updated successfully!".format(pk)})

    def delete(self, request, pk):
        dose_record = get_object_or_404(DoseRecord.objects.all(), pk=pk)
        dose_record.delete()
        return Response({"message": "Dose Record {0} has been deleted.".format(pk)}, status=204)

