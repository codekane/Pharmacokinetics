from django.shortcuts import render
# from rest_framework import authentication
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from substances.models import DoseRecord, Substance, Pharmacokinetics
from substances.serializers import DoseRecordSerializer, PharmacokineticsSerializer



class SubstanceFormulationsView(APIView):
    # http_methood_names = ['get']
    pass

class SubstancePharmacokineticsView(APIView):
    http_method_names = ['get']

    def get(self, request, pk):
        substance = get_object_or_404(Substance.objects.all(), pk=pk)
        kinetics = Pharmacokinetics.objects.filter(substance_id=pk)
        serializer = PharmacokineticsSerializer(kinetics, many=True)
        return Response({
            "pharmacokinetics": serializer.data})





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
        dose_record = request.data.get('dose_record')

        serializer = DoseRecordSerializer(data=dose_record)
        if serializer.is_valid(raise_exception=True):
            saved_dose_record = serializer.save()
        return Response({"success": "Dose Record {0} created successfully".format(pk)})

    def put(self, request, pk):
        dose_record = get_object_or_404(DoseRecord.objects.all(), pk=pk)
        data = request.data.get('dose_record')
        serializer = DoseRecordSerializer(instance=dose_record, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            saved_dose_record = serializer.save()
        return Response({"success": "Dose Record {0} updated successfully!".format(pk)})

    def delete(self, request, pk):
        dose_record = get_object_or_404(DoseRecord.objects.all(), pk=pk)
        dose_record.delete()
        return Response({"message": "Dose Record {0} has been deleted.".format(pk)}, status=204)

