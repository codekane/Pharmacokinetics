from django.contrib import admin
from substances.models import Substance, DosageForm, DosageFormDose, Pharmacokinetics, DoseRecord



class DosageFormInline(admin.TabularInline):
    model = DosageForm
    fk_name = 'substance'
    show_change_link = True
    extra = 0

class DosageFormDoseInline(admin.TabularInline):
    model = DosageFormDose
    fk_name = 'dosage_form'
    show_change_link = True
    extra = 0

class PharmacokineticsInline(admin.TabularInline):
    model = Pharmacokinetics
    fk_name = 'substance'
    show_change_link = True
    extra = 0

@admin.register(DosageForm)
class DosageFormAdmin(admin.ModelAdmin):
    model = DosageForm
    inlines = [ DosageFormDoseInline, ]

@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin):
    model = Substance
    inlines = [ DosageFormInline, PharmacokineticsInline ]

@admin.register(DoseRecord)
class DoseRecordAdmin(admin.ModelAdmin):
    pass
