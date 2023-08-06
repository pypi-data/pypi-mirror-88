from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_utils import get_utcnow
from mocca_screening.models.model_mixins import CareModelMixin


class CareStatus(UniqueSubjectIdentifierFieldMixin, CareModelMixin, BaseUuidModel):
    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
        help_text="Date and time of report.",
    )

    mocca_register = models.OneToOneField(
        "mocca_screening.moccaregister",
        on_delete=models.PROTECT,
        null=True,
        verbose_name="MOCCA (original) register details",
    )

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Care Status"
        verbose_name_plural = "Care Status"
