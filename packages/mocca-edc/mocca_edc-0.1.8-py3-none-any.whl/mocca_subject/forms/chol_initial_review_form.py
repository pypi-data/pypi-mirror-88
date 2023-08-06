from django import forms
from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator
from mocca_subject.forms.mixins import InitialReviewFormValidatorMixin

from ..constants import INSULIN, DRUGS
from ..models import CholInitialReview
from .mixins import (
    EstimatedDateFromAgoFormMixin,
    CrfModelFormMixin,
    CrfFormValidatorMixin,
    raise_if_clinical_review_does_not_exist,
)


class CholInitialReviewFormValidator(
    InitialReviewFormValidatorMixin,
    EstimatedDateFromAgoFormMixin,
    CrfFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        self.raise_if_both_ago_and_actual_date()

        # TODO: How is CHOL managed? Like DM? Drugs and lifestyle?
        self.required_if(
            DRUGS, field="managed_by", field_required="med_start_ago",
        )

        if self.cleaned_data.get("dx_ago") and self.cleaned_data.get("med_start_ago"):
            if (
                self.estimated_date_from_ago("dx_ago")
                - self.estimated_date_from_ago("med_start_ago")
            ).days > 1:
                raise forms.ValidationError(
                    {"med_start_ago": "Invalid. Cannot be before diagnosis."}
                )


class CholInitialReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = CholInitialReviewFormValidator

    class Meta:
        model = CholInitialReview
        fields = "__all__"
