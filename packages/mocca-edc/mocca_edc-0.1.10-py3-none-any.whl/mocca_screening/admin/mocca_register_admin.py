import pdb

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django_audit_fields.admin import audit_fieldset_tuple, ModelAdminAuditFieldsMixin
from edc_constants.constants import NO, YES
from edc_dashboard import url_names
from edc_model_admin import (
    ModelAdminFormInstructionsMixin,
    TemplatesModelAdminMixin,
)
from edc_model_admin.model_admin_simple_history import SimpleHistoryAdmin
from edc_sites import get_current_country
from mocca_screening.models.model_mixins import CareModelMixin

from ..admin_site import mocca_screening_admin
from ..forms import MoccaRegisterForm, MoccaRegisterContactForm
from ..mocca_original_sites import get_mocca_sites_by_country
from ..models import (
    MoccaRegister,
    MoccaRegisterContact,
    CareStatus,
    SubjectRefusal,
    SubjectRefusalScreening,
    SubjectScreening,
)
from .list_filters import ScreenedListFilter, ContactAttemptsListFilter, CallListFilter


class MoccaRegisterContactInlineMixin:
    model = MoccaRegisterContact
    form = MoccaRegisterContactForm
    extra = 0
    readonly_fields = ["report_datetime"]
    radio_fields = {
        "answered": admin.VERTICAL,
        "respondent": admin.VERTICAL,
        "survival_status": admin.VERTICAL,
        "willing_to_attend": admin.VERTICAL,
        "icc": admin.VERTICAL,
        "call_again": admin.VERTICAL,
    }


class AddMoccaRegisterContactInline(
    ModelAdminAuditFieldsMixin, MoccaRegisterContactInlineMixin, admin.StackedInline
):
    fieldsets = (
        [None, {"fields": ("report_datetime",)}],
        (
            "Details of the call",
            {
                "fields": (
                    "answered",
                    "respondent",
                    "survival_status",
                    "death_date",
                    "willing_to_attend",
                    "icc",
                    "next_appt_date",
                    "call_again",
                    "comment",
                ),
            },
        ),
    )
    verbose_name = "New Contact Attempt"
    verbose_name_plural = "New Contact Attempt"

    def has_change_permission(self, request, obj):
        return True

    def get_queryset(self, request):
        return MoccaRegisterContact.objects.none()


class ViewMoccaRegisterContactInline(
    ModelAdminAuditFieldsMixin, MoccaRegisterContactInlineMixin, admin.StackedInline
):

    fieldsets = (
        [None, {"fields": (("report_datetime", "answered"),)}],
        (
            "Details of the call",
            {
                "classes": ("collapse",),
                "fields": (
                    "respondent",
                    "survival_status",
                    "death_date",
                    "willing_to_attend",
                    "icc",
                    "next_appt_date",
                    "call_again",
                    "comment",
                ),
            },
        ),
    )
    verbose_name = "Past Contact Attempt"
    verbose_name_plural = "Past Contact Attempts"

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


@admin.register(MoccaRegister, site=mocca_screening_admin)
class MoccaRegisterAdmin(
    TemplatesModelAdminMixin, ModelAdminFormInstructionsMixin, SimpleHistoryAdmin
):
    form = MoccaRegisterForm
    show_object_tools = True
    inlines = [AddMoccaRegisterContactInline, ViewMoccaRegisterContactInline]
    ordering = ["mocca_study_identifier"]
    screening_listboard_url_name = "screening_listboard_url"
    list_per_page = 15
    fieldsets = (
        [None, {"fields": ("screening_identifier",)}],
        [
            "Original Enrollment Data",
            {
                "fields": (
                    "mocca_study_identifier",
                    "mocca_screening_identifier",
                    "mocca_site",
                    "first_name",
                    "last_name",
                    "initials",
                    "gender",
                    "dob",
                    "birth_year",
                    "age_in_years",
                )
            },
        ],
        [
            "Contact",
            {
                "fields": (
                    "notes",
                    "tel_one",
                    "tel_two",
                    "tel_three",
                    "best_tel",
                    "screen_now",
                )
            },
        ],
        audit_fieldset_tuple,
    )

    list_display = (
        "mocca_patient",
        "call_now",
        "care_status",
        "refusal",
        "screen",
        "date_last_called",
        "next_appt_date",
        "user_modified",
    )

    list_display_links = ("mocca_patient", "call_now")

    list_filter = (
        ScreenedListFilter,
        ContactAttemptsListFilter,
        CallListFilter,
        "date_last_called",
        "next_appt_date",
        "gender",
        "created",
        "modified",
    )

    radio_fields = {
        "gender": admin.VERTICAL,
        "mocca_site": admin.VERTICAL,
        "call": admin.VERTICAL,
        "screen_now": admin.VERTICAL,
    }

    search_fields = (
        "mocca_study_identifier",
        "initials",
        "mocca_screening_identifier",
        "screening_identifier",
        "user_modified",
        "user_created",
    )

    def call_now(self, obj):
        return f"{obj.call} ({obj.contact_attempts})"

    call_now.admin_order_field = "call"

    def mocca_patient(self, obj):
        return str(obj)

    mocca_patient.admin_order_field = "mocca_study_identifier"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=None)
        fields = [
            "contact_attempts",
            "screening_identifier",
            "mocca_study_identifier",
            "mocca_screening_identifier",
            "mocca_site",
        ]
        readonly_fields = list(readonly_fields)
        for f in fields:
            if f not in readonly_fields:
                readonly_fields.append(f)
        readonly_fields = tuple(readonly_fields)
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mocca_site":
            sites = get_mocca_sites_by_country(country=get_current_country())
            kwargs["queryset"] = db_field.related_model.objects.filter(
                name__in=[v.name for v in sites.values()]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def screen(self, obj=None, label=None):
        if obj.call == YES and obj.screen_now == NO:
            return self.get_empty_value_display()
        elif obj.screening_identifier:
            url = reverse(
                url_names.get(self.screening_listboard_url_name),
                kwargs=self.get_screening_listboard_url_kwargs(obj),
            )
            url = f"{url}?mocca_register={str(obj.id)}"
            label = obj.screening_identifier
            fa_icon = "fas fa-share"
            fa_icon_after = True
        else:
            add_url = reverse(
                "mocca_screening_admin:mocca_screening_subjectscreening_add"
            )
            url = (
                f"{add_url}?"
                "next=mocca_screening_admin:mocca_screening_moccaregister_changelist"
                f"&mocca_register={str(obj.id)}"
            )
            try:
                care_status = CareStatus.objects.get(mocca_register=obj)
            except ObjectDoesNotExist:
                pass
            else:
                care_status_query_string = "&".join(
                    [
                        f"{f}={getattr(care_status, f) or ''}"
                        for f in [f.name for f in CareModelMixin._meta.fields]
                    ]
                )
                url = f"{url}&{care_status_query_string}"
            label = "Add"
            fa_icon = "fas fa-plus"
            fa_icon_after = None

        context = dict(
            title=f"{SubjectScreening._meta.verbose_name}",
            url=url,
            label=label,
            fa_icon=fa_icon,
            fa_icon_after=fa_icon_after,
        )
        return render_to_string(self.button_template, context=context)

    def get_screening_listboard_url_name(self):
        return url_names.get(self.screening_listboard_url_name)

    def get_screening_listboard_url_kwargs(self, obj):
        return dict(screening_identifier=obj.screening_identifier)

    @property
    def button_template(self):
        return "mocca_screening/bootstrap3/dashboard_button.html"

    def care_status(self, obj=None, label=None):
        if not self.called_once(obj) or self.get_subject_screening_obj(
            obj=obj, label=label
        ):
            return self.get_empty_value_display()
        try:
            care_status = CareStatus.objects.get(mocca_register=obj)
        except ObjectDoesNotExist:
            url = reverse("mocca_screening_admin:mocca_screening_carestatus_add")
            url = (
                f"{url}?next=mocca_screening_admin:mocca_screening_moccaregister_changelist"
                f"&mocca_register={str(obj.id)}"
            )
            label = "Add"
            fa_icon = "fas fa-plus"
        else:
            url = reverse(
                "mocca_screening_admin:mocca_screening_carestatus_change",
                args=(care_status.id,),
            )
            url = f"{url}?next=mocca_screening_admin:mocca_screening_moccaregister_changelist"
            label = "Edit"
            fa_icon = "fas fa-pen"
        context = dict(
            title=f"{CareStatus._meta.verbose_name}",
            url=url,
            label=label,
            fa_icon=fa_icon,
        )
        return render_to_string(self.button_template, context=context)

    care_status.short_description = "Care Status"

    def refusal(self, obj=None, label=None):
        if not self.called_once(obj) or self.get_subject_screening_obj(
            obj=obj, label=label
        ):
            return self.get_empty_value_display()
        try:
            subject_refusal = SubjectRefusal.objects.get(
                screening_identifier=obj.screening_identifier
            )
        except ObjectDoesNotExist:
            url = reverse(
                "mocca_screening_admin:mocca_screening_subjectrefusalscreening_add"
            )
            url = (
                f"{url}?next=mocca_screening_admin:mocca_screening_moccaregister_changelist&"
                f"mocca_register={str(obj.id)}"
            )
            label = "Add"
            fa_icon = "fas fa-plus"
        else:
            url = reverse(
                "mocca_screening_admin:mocca_screening_subjectrefusalscreening_change",
                args=(subject_refusal.id,),
            )
            url = f"{url}?next=mocca_screening_admin:mocca_screening_moccaregister_changelist"
            label = "Edit"
            fa_icon = "fas fa-pen"
        context = dict(
            title=f"{SubjectRefusalScreening._meta.verbose_name}",
            url=url,
            label=label,
            fa_icon=fa_icon,
        )
        return render_to_string(self.button_template, context=context)

    def get_subject_screening_obj(self, obj=None, label=None):
        try:
            return SubjectScreening.objects.get(mocca_register=obj)
        except ObjectDoesNotExist:
            return None

    def called_once(self, obj=None, label=None):
        return MoccaRegisterContact.objects.filter(mocca_register=obj).exists()
