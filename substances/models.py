from django.db import models

# Create your models here.

class RouteOfIngestion(models.Model):
    ROUTES = [
        ("Oral", "Oral"), ("Insufflated", "Insufflated"), ("Vaporized", "Vaporized"),
        ("Sublingual", "Sublingual"), ("Rectal", "Rectal"), ("Intravenous", "Intravenous")
    ]
    class Meta:
        abstract=True
    ROI = models.CharField(max_length=30, choices=ROUTES, default="Oral")

class RouteOfIngestionMixin(RouteOfIngestion):
    class Meta:
        abstract=True


class Substance(models.Model):
    name = models.CharField(max_length=30)
    volume_of_distribution = models.CharField(max_length=30, blank=True, null=True) # L/KG
    elimination_rate_constant = models.CharField(max_length=30, blank=True, null=True) # /1h
    half_life = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Hours

    def __str__(self):
        return "{0}".format(self.name)


class DosageForm(models.Model):
    class Meta:
        db_table = "dosage_forms"
        verbose_name_plural = "Dosage Forms"
    name = models.CharField(max_length=30)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.substance.name, self.name)

# What's this for... Is it a base model?
class Dose(models.Model):
    DOSAGE_UNITS = [('mg', 'mg')]
    class Meta:
        abstract = True

    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    dosage = models.DecimalField(decimal_places=2, max_digits=10)
    dosage_unit = models.CharField(max_length=2, choices=DOSAGE_UNITS, default="mg")

    def __str__(self):
        return "{0} {1} {2}".format(self.dosage, self.dosage_unit, self.substance.name)

# This is for splitting an XR into two IR doses with different offsets.
class DosageFormDose(Dose):
    class Meta:
        db_table = "dosage_form_doses"
        verbose_name_plural = "Dosage Form Doses"

    DOSAGE_UNITS = [('%', '%'), ('mg', 'mg')]
    dosage_unit = models.CharField(max_length=2, choices=DOSAGE_UNITS, default="%")
    tOffset = models.DurationField(blank=True, null=True)
    tLag = models.DecimalField(decimal_places=2, max_digits=10)
    dosage_form = models.ForeignKey(DosageForm, on_delete=models.CASCADE)

class Pharmacokinetics(RouteOfIngestionMixin, models.Model):
    KINETICS = [('Instantaneous', 'Instantaneous'), ('Zero Order', 'Zero Order'), ('First Order', 'First Order')]
    class Meta:
        verbose_name_plural = "Pharmacokinetics"
        unique_together = ('ROI', 'substance')
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    bioavailability = models.DecimalField(decimal_places=2, max_digits=10)
    tLag = models.DecimalField(decimal_places=2, max_digits=10)
    tOnset = models.DurationField()
    tMax = models.DurationField()
    tHalf = models.DurationField()
    absorption_rate_constant = models.CharField(max_length=30, null=True, blank=True) # /1h
    absorption_kinetics = models.CharField(max_length=30, choices=KINETICS, null=True, blank=True)

class DoseRecord(RouteOfIngestionMixin, Dose):
    class Meta:
        db_table = "dose_records"
        verbose_name_plural = "Dose Records"
    timestamp = models.DateTimeField()
    dosage_form = models.ForeignKey(DosageForm, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return "{0} {1} {2}{3}".format(self.timestamp, self.substance.name, self.dosage, self.dosage_unit )



