from django.db import models

# Create your models here.

class RouteOfIngestion(models.Model):
    ROUTES = [
        ("Oral", "Oral"), ("Insufflated", "Insufflated"), ("Vaporized", "Vaporized"),
        ("Rectal", "Rectal"), ("Intravenous", "Intravenous")
    ]
    class Meta:
        abstract=True
    ROI = models.CharField(max_length=30, choices=ROUTES, default="Oral")

class RouteOfIngestionMixin(RouteOfIngestion):
    class Meta:
        abstract=True

class Substance(models.Model):
    name = models.CharField(max_length=30)


class DosageForm(RouteOfIngestionMixin, models.Model):
    class Meta:
        db_table = "dosage_forms"
        verbose_name_plural = "Dosage Forms"
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)


# What's this for... Is it a base model?
class Dose(models.Model):
    DOSAGE_UNITS = [('mg', 'mg')]
    class Meta:
        abstract = True

    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    dosage = models.FloatField()
    dosage_unit = models.CharField(max_length=2, choices=DOSAGE_UNITS, default="mg")

# This is for splitting an XR into two IR doses with different offsets.
class DosageFormDose(Dose):
    class Meta:
        db_table = "dosage_form_doses"
        verbose_name_plural = "Dosage Form Doses"

    DOSAGE_UNITS = [('%', '%'), ('mg', 'mg')]
    dosage_unit = models.CharField(max_length=2, choices=DOSAGE_UNITS, default="%")
    tOffset = models.DurationField(blank=True, null=True)
    dosage_form = models.ForeignKey(DosageForm, on_delete=models.CASCADE)

class Pharmacokinetics(RouteOfIngestionMixin, models.Model):
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    bioavailability = models.FloatField()
    tOnset = models.DurationField()
    tMax = models.DurationField()
    tHalf = models.DurationField()

class DoseRecord(RouteOfIngestionMixin, Dose):
    class Meta:
        db_table = "dose_records"
        verbose_name_plural = "Dose Records"
    timestamp = models.DateTimeField()
    dosage_form = models.ForeignKey(DosageForm, on_delete=models.CASCADE, blank=True, null=True, default=None)



