from django.utils.safestring import mark_safe
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_screening.screening_eligibility import ScreeningEligibility


class MoccaScreeningEligibility(ScreeningEligibility):
    @property
    def eligible(self):
        """Returns True or False.
        """
        eligible = False
        if self.model_obj.unsuitable_for_study == YES:
            eligible = False
        elif (
            self.model_obj.mocca_register
            and self.model_obj.care == YES
            and self.model_obj.pregnant in [NO, NOT_APPLICABLE]
            and self.model_obj.requires_acute_care == NO
        ):
            eligible = True
        return eligible

    @property
    def reasons_ineligible(self):
        """Returns a dictionary of reasons ineligible.
        """
        reasons_ineligible = {}
        if not self.model_obj.eligible:
            if self.model_obj.unsuitable_for_study == YES:
                reasons_ineligible.update(unsuitable_for_study="Subject unsuitable")
            if not self.model_obj.mocca_register:
                reasons_ineligible.update(
                    not_mocca_patient="Unable to link to MOCCA (original) participant"
                )
            if self.model_obj.care != YES:
                reasons_ineligible.update(not_in_care="Not in care")
            if self.model_obj.pregnant == YES:
                reasons_ineligible.update(pregnant="Pregnant (unconfirmed)")
            if self.model_obj.requires_acute_care == YES:
                reasons_ineligible.update(requires_acute_care="Requires acute care")
            if self.model_obj.willing_to_consent != YES:
                reasons_ineligible.update(unwilling_to_consent="Not willing to consent")
        return reasons_ineligible

    def format_reasons_ineligible(*str_values):
        reasons = None
        str_values = [x for x in str_values if x is not None]
        if str_values:
            str_values = "".join(str_values)
            reasons = mark_safe(str_values.replace("|", "<BR>"))
        return reasons

    def eligibility_display_label(obj):
        return "ELIGIBLE" if obj.eligible else "not eligible"
