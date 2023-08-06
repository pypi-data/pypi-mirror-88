from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_model import models as edc_models

from ..choices import CHOL_MANAGEMENT
from ..model_mixins import CrfModelMixin, InitialReviewModelMixin


class CholInitialReview(
    InitialReviewModelMixin, CrfModelMixin, edc_models.BaseUuidModel
):

    managed_by = models.CharField(
        verbose_name="How is the patient's diabetes managed?",
        max_length=25,
        choices=CHOL_MANAGEMENT,
        default=NOT_APPLICABLE,
    )

    med_start_ago = edc_models.DurationYMDField(
        verbose_name=(
            "If the patient is taking medicines for diabetes, "
            "how long have they been taking these?"
        ),
        null=True,
        blank=True,
    )

    med_start_estimated_date = models.DateField(
        verbose_name="Estimated medication start date", null=True, editable=False,
    )

    med_start_date_estimated = models.CharField(
        verbose_name="Was the medication start date estimated?",
        max_length=15,
        choices=YES_NO,
        default=YES,
        editable=False,
    )

    chol_performed = models.CharField(
        verbose_name=(
            "Has the patient had their cholesterol measured in the last few months?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    def save(self, *args, **kwargs):
        if self.med_start_ago:
            self.med_start_estimated_date = edc_models.duration_to_date(
                self.med_start_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "High Cholesterol Initial Review"
        verbose_name_plural = "High Cholesterol Initial Reviews"
