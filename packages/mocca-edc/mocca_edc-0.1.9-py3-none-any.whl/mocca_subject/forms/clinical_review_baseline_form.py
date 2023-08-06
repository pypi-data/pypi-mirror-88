from django import forms
from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator

from ..models import ClinicalReviewBaseline
from .mixins import (
    EstimatedDateFromAgoFormMixin,
    CrfModelFormMixin,
    CrfFormValidatorMixin,
)


class ClinicalReviewBaselineFormValidator(
    CrfFormValidatorMixin, EstimatedDateFromAgoFormMixin, FormValidator
):
    def clean(self):
        self.estimated_date_from_ago("hiv_test_ago")
        self.when_tested_required(cond="hiv")

        for cond in ["htn", "dm", "chol"]:
            self.estimated_date_from_ago(f"{cond}_test_ago")
            self.when_tested_required(cond=cond)
            self.required_if(YES, field=f"{cond}_test", field_required=f"{cond}_dx")

    def when_tested_required(self, cond=None):
        if self.cleaned_data.get(f"{cond}_test") == YES:
            if not self.cleaned_data.get(
                f"{cond}_test_ago"
            ) and not self.cleaned_data.get(f"{cond}_test_date"):
                raise forms.ValidationError(
                    f"{cond.title()}: When was the subject tested? Either provide an "
                    "estimated time 'ago' or provide the exact date. See below."
                )


class ClinicalReviewBaselineForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = ClinicalReviewBaselineFormValidator

    class Meta:
        model = ClinicalReviewBaseline
        fields = "__all__"
