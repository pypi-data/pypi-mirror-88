from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from mocca_lists.models import ClinicServices

from ..model_mixins import CrfModelMixin


class ReasonForVisit(CrfModelMixin, edc_models.BaseUuidModel):

    clinic_services = models.ManyToManyField(
        ClinicServices,
        related_name="clinic_services",
        verbose_name="Why is the patient at the clinic?",
    )

    clinic_services_other = edc_models.OtherCharField()

    refill_hiv = models.CharField(
        verbose_name="Is the patient refilling HIV medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    refill_dm = models.CharField(
        verbose_name="Is the patient refilling Diabetes medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    refill_htn = models.CharField(
        verbose_name="Is the patient refilling Hypertension medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Reason for Visit"
        verbose_name_plural = "Reason for Visits"
