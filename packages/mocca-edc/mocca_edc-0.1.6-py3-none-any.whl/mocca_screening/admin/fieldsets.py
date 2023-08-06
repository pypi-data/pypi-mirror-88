from edc_fieldsets import Fieldset

care_status_fieldset = Fieldset(
    "care",
    "care_not_in_reason",
    "icc",
    "icc_not_in_reason",
    "icc_since_mocca",
    "icc_since_mocca_comment",
    "care_facility_location",
    "care_comment",
    section="Care status",
).fieldset
