import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from django import forms
from django.core.validators import EMPTY_VALUES
from django.core.validators import RegexValidator

from home.constants import card_constants
from home.constants import profile_constants

logger = logging.getLogger(__name__)


class StepEmptyForm(forms.Form):
    pass


class StepAForm(forms.Form):
    role = forms.ChoiceField(
        choices=(
            ("research_scientist", "Create and publish science"),
            ("engineer", "Engineering"),
            ("hq", "Manage and lead programs and/or people"),
            ("support", "Provide operational support services"),
            ("other", "Other"),
        ),
        required=True,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="In the heliophysics domain, what kind of work do you do most frequently?",
    )
    role_other_info = forms.CharField(
        max_length=1024,
        required=False,
        label="If other, please specify",
    )

    def clean(self):
        for fp in [
            ('role', 'role_other_info')
        ]:
            if is_empty(self.cleaned_data, fp):
                self._errors[fp[1]] = self.error_class([f'Please specify your {fp[0]} here.'])

        if self._errors:
            return self.cleaned_data

        # Creating the pretty_printed dictionary
        pretty_printed: Dict[str, Union[List[str], str]] = {}
        for field_name, field_label in self.fields['role'].choices:
            if self.cleaned_data['role'] == field_name:
                pretty_printed[profile_constants.PF_ROLE] = field_label
                if field_name == 'other':
                    pretty_printed[profile_constants.PF_ROLE] = self.cleaned_data.get('role_other_info', '')

        self.cleaned_data['pretty_printed'] = pretty_printed
        return self.cleaned_data


class StepB_ResearchScientist_Form(forms.Form):
    alphanumeric_validator = RegexValidator(
        r"^[a-zA-Z0-9_\- ]+$",
        "Only alphanumeric characters, spaces, underscores, and hyphens are allowed.",
    )
    name = forms.CharField(
        max_length=100,
        label="What is your name?",
        required=True,
        validators=[alphanumeric_validator]
    )
    student_type = forms.ChoiceField(
        choices=(
            ("undergraduate", "Undergraduate Student"),
            ("master", "Master's Student"),
            ("phd_student", "PhD Student"),
            ("post_doc", "Post Doc"),
            ("early_career", "Early Career"),
            ("mid_career", "Mid Career"),
            ("senior_career", "Senior Career"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Are you a...",
    )

    orcid_link = forms.CharField(max_length=1000, required=False, label="ORCiD link")
    zenodo_link = forms.CharField(max_length=1000, required=False)
    linkedin_link = forms.CharField(max_length=1000, required=False)
    gitlab_link = forms.CharField(max_length=1000, required=False)
    github_link = forms.CharField(max_length=1000, required=False)
    website_1_link = forms.CharField(max_length=1000, required=False)
    website_2_link = forms.CharField(max_length=1000, required=False)
    website_3_link = forms.CharField(max_length=1000, required=False)

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Union[List[str], str]] = {}

        # User name
        name = cleaned_data.get('given_name', '')
        pretty_printed[profile_constants.PF_NAME] = f"{name}".strip()

        # Career stage
        for field_name, field_label in self.fields['student_type'].choices:
            if cleaned_data['student_type'] == field_name:
                pretty_printed[profile_constants.PF_CAREER_STAGE] = field_label
                break

        # Contact links
        contact_links = []
        for field_name, value in cleaned_data.items():
            if field_name.endswith('_link') and value:
                contact_links.append(value)
        pretty_printed[profile_constants.PF_CONTACT_LINKS] = contact_links

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepB_Engineer_Form(forms.Form):
    alphanumeric_validator = RegexValidator(
        r"^[a-zA-Z0-9_\- ]+$",
        "Only alphanumeric characters, spaces, underscores, and hyphens are allowed.",
    )

    name = forms.CharField(
        max_length=100,
        label="What is your name?",
        required=True,
        validators=[alphanumeric_validator]
    )
    student_type = forms.ChoiceField(
        choices=(
            ("undergraduate", "Undergraduate Student"),
            ("master", "Master's Student"),
            ("phd_student", "PhD Student"),
            ("post_doc", "Post Doc"),
            ("early_career", "Early Career"),
            ("mid_career", "Mid Career"),
            ("senior_career", "Senior Career"),
            ("general_professional", "General Professional"),
            ("other", "Other"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Are you a...",
    )

    orcid_link = forms.CharField(max_length=1000, required=False, label="ORCiD link")
    zenodo_link = forms.CharField(max_length=1000, required=False)
    linkedin_link = forms.CharField(max_length=1000, required=False)
    gitlab_link = forms.CharField(max_length=1000, required=False)
    github_link = forms.CharField(max_length=1000, required=False)
    website_1_link = forms.CharField(max_length=1000, required=False)
    website_2_link = forms.CharField(max_length=1000, required=False)
    website_3_link = forms.CharField(max_length=1000, required=False)

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Union[List[str], str]] = {}

        # User name
        name = cleaned_data.get('given_name', '')
        pretty_printed[profile_constants.PF_NAME] = f"{name}".strip()

        # Career stage
        for field_name, field_label in self.fields['student_type'].choices:
            if cleaned_data['student_type'] == field_name:
                pretty_printed[profile_constants.PF_CAREER_STAGE] = field_label
                break

        # Contact links
        contact_links = []
        for field_name, value in cleaned_data.items():
            if field_name.endswith('_link') and value:
                contact_links.append(value)
        pretty_printed[profile_constants.PF_CONTACT_LINKS] = contact_links

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepB_HQ_Form(forms.Form):
    alphanumeric_validator = RegexValidator(
        r"^[a-zA-Z0-9_\- ]+$",
        "Only alphanumeric characters, spaces, underscores, and hyphens are allowed.",
    )

    name = forms.CharField(
        max_length=100,
        label="What is your name?",
        required=True,
        validators=[alphanumeric_validator]
    )
    student_type = forms.ChoiceField(
        choices=(
            ("administrator", "Administrator"),
            ("mid_career_researcher", "Mid Career Researcher"),
            ("senior_career_researcher", "Senior Career Researcher"),
            ("support_staff", "Support Staff"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Are you a...",
    )
    job_title = forms.CharField(
        max_length=1024,
        required=False,
        label="What is your job title?"
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Union[List[str], str]] = {}

        # User name
        name = cleaned_data.get('name', '')
        pretty_printed[profile_constants.PF_NAME] = f"{name}".strip()

        # Job title
        job_title = cleaned_data.get('job_title', '')
        pretty_printed[profile_constants.PF_JOB_TITLE] = job_title.strip()

        # Career stage
        for field_name, field_label in self.fields['student_type'].choices:
            if cleaned_data['student_type'] == field_name:
                pretty_printed[profile_constants.PF_CAREER_STAGE] = field_label
                break

        # Contact links
        contact_links = []
        for field_name, value in cleaned_data.items():
            if field_name.endswith('_link') and value:
                contact_links.append(value)
        pretty_printed[profile_constants.PF_CONTACT_LINKS] = contact_links

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepB_Support_Form(forms.Form):
    alphanumeric_validator = RegexValidator(
        r"^[a-zA-Z0-9_\- ]+$",
        "Only alphanumeric characters, spaces, underscores, and hyphens are allowed.",
    )

    name = forms.CharField(
        max_length=100,
        label="What is your name?",
        required=True,
        validators=[alphanumeric_validator]
    )
    student_type = forms.ChoiceField(
        choices=(
            ("early_career", "Early Career"),
            ("mid_career", "Mid Career"),
            ("senior_career", "Senior Career"),
            ("other", "Other"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Are you a...",
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Union[List[str], str]] = {}

        # User name
        name = cleaned_data.get('name', '')
        pretty_printed[profile_constants.PF_NAME] = f"{name}".strip()

        # Career stage
        for field_name, field_label in self.fields['student_type'].choices:
            if cleaned_data['student_type'] == field_name:
                pretty_printed[profile_constants.PF_CAREER_STAGE] = field_label
                break

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepC0Form(forms.Form):
    user_got_phd = forms.ChoiceField(
        choices=(
            ("yes", "Yes"),
            ("no", "No"),
        ),
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Did you get a PhD?",
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Union[List[str], str]] = {}

        # Career stage
        for field_name, field_label in self.fields['user_got_phd'].choices:
            if cleaned_data['user_got_phd'] == field_name:
                pretty_printed[profile_constants.PF_GOT_PHD] = field_label
                break

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepCForm(forms.Form):
    phd_received_in = forms.IntegerField(
        min_value=1920,
        max_value=2040,
        required=False,
        label="When did you receive your PhD?"
    )
    phd_discipline = forms.CharField(
        max_length=1000,
        required=False,
        label="From what discipline did you graduate?"
    )
    phd_awarded_by = forms.CharField(
        max_length=1000,
        required=False,
        label="What institution awarded your PhD?"
    )
    phd_thesis_title = forms.CharField(
        max_length=1000,
        required=False,
        label="Title of your PhD thesis"
    )
    phd_thesis_link = forms.CharField(
        max_length=1000,
        required=False,
        label="Link to your PhD thesis"
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Any] = {}

        # Thesis data
        pretty_printed[profile_constants.PF_THESIS_DATA] = {
            "phd_institution": cleaned_data.get("phd_awarded_by"),
            "phd_discipline": cleaned_data.get("phd_discipline"),
            "phd_thesis_title": cleaned_data.get("phd_thesis_title"),
            "phd_thesis_link": cleaned_data.get("phd_thesis_link"),
            "phd_received_in": cleaned_data.get("phd_received_in"),
        }

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepC_ALT_Form(forms.Form):
    degrees_received = forms.MultipleChoiceField(
        choices=(
            ("high_school", "High School"),
            ("undergrad", "Undergrad"),
            ("masters", "Masters"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="What degrees have you received?",
    )
    degree_received_in = forms.IntegerField(
        min_value=1920,
        max_value=2040,
        required=False,
        label="When did you graduate from your last degree?"
    )
    currently_in_school = forms.MultipleChoiceField(
        choices=(
            ("still_in_school", "I am still in school"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="",
    )
    degree_institution = forms.CharField(
        max_length=1000,
        required=False,
        label="What was the institution you last graduated from?"
    )
    degree_discipline = forms.CharField(
        max_length=1000,
        required=False,
        label="What did you receive your degree in?"
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Any] = {}

        # Degree data
        pretty_printed[profile_constants.PF_DEGREE_DATA] = {
            "degree_institution": cleaned_data.get("degree_institution"),
            "degree_discipline": cleaned_data.get("degree_discipline"),
            "phd_thesis_title": cleaned_data.get("phd_thesis_title"),
            "degree_received_in": cleaned_data.get("degree_received_in"),
            "currently_in_school": cleaned_data.get("currently_in_school"),
        }

        pretty_printed[profile_constants.PF_DEGREES_RECEIVED] = []
        for field_name, field_label in self.fields['degrees_received'].choices:
            if cleaned_data['degrees_received'] == field_name:
                pretty_printed[profile_constants.PF_DEGREES_RECEIVED].append(field_label)

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepC_HQ_Form(forms.Form):
    phd_received_in = forms.IntegerField(
        min_value=1920,
        max_value=2040,
        required=False,
        label="When did you receive your PhD?"
    )
    phd_discipline = forms.CharField(
        max_length=1000,
        required=False,
        label="From what discipline did you graduate?"
    )
    phd_awarded_by = forms.CharField(
        max_length=1000,
        required=False,
        label="What institution awarded your PhD?"
    )
    phd_thesis_title = forms.CharField(
        max_length=1000,
        required=False,
        label="Title of your PhD thesis"
    )
    phd_thesis_link = forms.CharField(
        max_length=1000,
        required=False,
        label="Link to your PhD thesis"
    )

    orcid_link = forms.CharField(max_length=1000, required=False, label="ORCiD link")
    zenodo_link = forms.CharField(max_length=1000, required=False)
    linkedin_link = forms.CharField(max_length=1000, required=False)
    gitlab_link = forms.CharField(max_length=1000, required=False)
    github_link = forms.CharField(max_length=1000, required=False)
    website_1_link = forms.CharField(max_length=1000, required=False)
    website_2_link = forms.CharField(max_length=1000, required=False)
    website_3_link = forms.CharField(max_length=1000, required=False)

    actively_researching = forms.ChoiceField(
        choices=(
            ("yes", "Yes"),
            ("no", "No"),
        ),
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Are you still actively researching and publishing in this field?",
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Any] = {}

        # Thesis data
        pretty_printed[profile_constants.PF_THESIS_DATA] = {
            "phd_institution": cleaned_data.get("phd_awarded_by"),
            "phd_discipline": cleaned_data.get("phd_discipline"),
            "phd_thesis_title": cleaned_data.get("phd_thesis_title"),
            "phd_thesis_link": cleaned_data.get("phd_thesis_link"),
            "phd_received_in": cleaned_data.get("phd_received_in"),
        }

        # Contact links
        contact_links = []
        for field_name, value in cleaned_data.items():
            if field_name.endswith('_link') and value:
                contact_links.append(value)
        pretty_printed[profile_constants.PF_CONTACT_LINKS] = contact_links

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepDForm(forms.Form):
    user_works_for_nasa = forms.ChoiceField(
        choices=(
            ("yes", "Yes"),
            ("no", "No"),
        ),
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Do you work for NASA?",
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Union[List[str], str]] = {}

        # Career stage
        for field_name, field_label in self.fields['user_works_for_nasa'].choices:
            if cleaned_data['user_works_for_nasa'] == field_name:
                pretty_printed[profile_constants.PF_WORKS_FOR_NASA] = field_label
                break

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepD1Form(forms.Form):
    job_title = forms.CharField(
        max_length=1024,
        required=False,
        label="What is your job title?"
    )
    nasa_center = forms.MultipleChoiceField(
        choices=(
            ("nasa_headquarters", "NASA Headquarters"),
            ("mission_support", "Mission Support"),
            ("ames_research_center", "Ames Research Center"),
            ("armstrong_flight_research_center", "Armstrong Flight Research Center"),
            ("glenn_research_center", "Glenn Research Center"),
            ("goddard_space_flight_center", "Goddard Space Flight Center"),
            ("goddard_institute_for_space_studies", "Goddard Institute for Space Studies"),
            ("jet_propulsion_laboratory", "Jet Propulsion Laboratory"),
            ("johnson_space_center", "Johnson Space Center"),
            ("katherine_johnson_ivv_facility", "Katherine Johnson IV&V Facility"),
            ("kennedy_space_center", "Kennedy Space Center"),
            ("langley_research_center", "Langley Research Center"),
            ("marshall_space_flight_center", "Marshall Space Flight Center"),
            ("michoud_assembly_facility", "Michoud Assembly Facility"),
            ("nasa_engineering_and_safety_center", "NASA Engineering and Safety Center"),
            ("nasa_safety_center", "NASA Safety Center"),
            ("nasa_shared_services_center", "NASA Shared Services Center"),
            ("neil_armstrong_test_facility", "Neil Armstrong Test Facility"),
            ("stennis_space_center", "Stennis Space Center"),
            ("wallops_flight_center", "Wallops Flight Center"),
            ("white_sands_test_facility", "White Sands Test Facility"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="Are you associated with a NASA center?",
    )
    what_kind_of_work_does_user = forms.CharField(
        max_length=1024,
        required=False,
        label="What kind of work do you do?"
    )
    nasa_missions = forms.MultipleChoiceField(
        choices=(
            ("aeronomy_of_ice_in_the_mesosphere", "Aeronomy of Ice in the Mesosphere (AIM)"),
            ("cluster", "Cluster"),
            ("deep_space_climate_observatory", "Deep Space Climate Observatory (DSCVOR)"),
            ("hinode", "HINODE"),
            ("interface_region_imaging_spectrograph", "Interface Region Imaging Spectrograph (IRIS)"),
            ("interstellar_boundary_explorer", "Interstellar Boundary Explorer (IBEX)"),
            ("ionospheric_connection_explorer", "Ionospheric Connection Explorer (ICON)"),
            ("juno", "Juno"),
            ("magnetospheric_multiscale_satellites", "Magnetospheric Multiscale Satellites (MMS)"),
            ("solar_dynamics_observatory", "Solar Dynamics Observatory (SDO)"),
            ("solar_orbiter", "Solar Orbiter"),
            ("solar_terrestrial_relations_observatory", "Solar Terrestrial Relations Observatory (STERO)"),
            ("thermosphere_ionosphere_mesosphere_energetics_and_dynamics", "Thermosphere Ionosphere Mesosphere Energetics and Dynamics (TIMED)"),
            ("time_history_of_events_and_macroscale_interactions_during_substorms", "Time History of Events and Macroscale Interactions during Substorms (THEMIS)"),
            ("two-wide_angle_imaging_neutral-atom_spectrometers", "Two-Wide Angle Imaging Neutral-Atom Spectrometers (TWINS)"),
            ("van_alen_probes", "Van Allen Probes (formerly RBSP)"),
            ("wind", "Wind"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="Are you currently working on any NASA missions?",
    )
    nasa_former_missions = forms.CharField(
        max_length=1024,
        required=False,
        label="Have you previously worked on any NASA missions?",
    )
    nasa_infrastructure = forms.MultipleChoiceField(
        choices=(
            ("cdaweb", "CDAWeb"),
            ("spase_metadata", "SPASE Metadata"),
            ("heliophysics_digital_resource_library", "Heliophysics Digital Resource Library"),
            ("community_coordinated_modeling_center", "Community Coordinated Modeling Center"),
            ("solar_data_analysis_center", "Solar Data Analysis Center"),
            ("helionauts", "Helionauts"),
            ("chianti", "CHIANTI"),
            ("other", "Other (please specify)"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="Are you a POC for any NASA infrastructure?",
    )
    nasa_infrastructure_other = forms.CharField(
        max_length=1024,
        required=False,
        label="If other, please specify"
    )
    nasa_initiatives = forms.MultipleChoiceField(
        choices=(
            ("open_science_tops", "Open Science/TOPS"),
            ("sound_rockets_programs", "Sound Rockets Programs"),
            ("cubesats", "Cubesats"),
            ("other", "Other"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="Are you affiliated with any of these NASA initiatives?",
    )
    nasa_initiatives_other = forms.CharField(
        max_length=1024,
        required=False,
        label="If other, please specify"
    )
    nasa_programs = forms.CharField(
        max_length=1024,
        required=False,
        label="Are you affiliated with any NASA programs? If yes, what is your affiliation?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Participating Scientist, Heliophysics Supporting Research; Program Director, Living With a Star'})
    )
    nasa_funding_arms = forms.CharField(
        max_length=1024,
        required=False,
        label="Are you affiliated with any NASA funding arms? If yes, what is your affiliation?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Grant Recipient, NASA Roses; Funder, NASA Roses'})
    )
    nasa_internal_groups = forms.MultipleChoiceField(
        choices=(
            ("center_for_helioanalytics", "Center for HelioAnalytics"),
            ("moon_to_mars_office", "Moon to Mars Office"),
            ("integrated_space_weather_analysis_team", "Integrated Space Weather Analysis Team"),
            ("other", "Other"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="Are you affiliated with any internal groups?",
    )
    nasa_internal_groups_other = forms.CharField(
        max_length=1024,
        required=False,
        label="If other, please specify"
    )

    def clean(self):
        cleaned_data = super().clean()

        # Check if all required fields are filled
        for fp in [
            ('nasa_initiatives', 'nasa_initiatives_other'),
            ('nasa_infrastructure', 'nasa_infrastructure_other'),
            ('nasa_internal_groups', 'nasa_internal_groups_other'),
        ]:
            if is_empty(cleaned_data, fp):
                self._errors[fp[1]] = self.error_class(['Please specify the details here.'])

        if self._errors:
            return cleaned_data

        # Prepare pretty_printed data
        pretty_printed: Dict[str, Any] = {}

        # Process multiple choice fields
        for field, label in [
            ('nasa_center', "NASA Centers"),
            ('nasa_missions', "NASA Missions"),
            ('nasa_infrastructure', "NASA Infrastructure"),
            ('nasa_initiatives', "NASA Initiatives"),
            ('nasa_internal_groups', "groups"),
        ]:
            choices_dict = dict(self.fields[field].choices)
            selected = cleaned_data.get(field, [])
            if selected:
                pretty_printed[label] = [choices_dict.get(choice) for choice in selected]

            if other_info := cleaned_data.get(f"{field}_other", None):
                pretty_printed[label].append(other_info)

        # Process text fields
        text_fields = [
            ('nasa_programs', "NASA Programs"),
            ('nasa_funding_arms', "NASA Funding Arms")
        ]
        for field, label in text_fields:
            value = cleaned_data.get(field)
            if value:
                pretty_printed[label] = [val.strip() for val in value.split(';') if val.strip()]

        groups = pretty_printed.get("groups")
        pretty_printed.pop("groups", None)

        cleaned_data['pretty_printed'] = {
            profile_constants.PF_JOB_TITLE: cleaned_data.get('job_title'),
            profile_constants.PF_JOB_DESCRIPTION: cleaned_data.get('what_kind_of_work_does_user'),
            profile_constants.PF_GROUPS: groups,
            profile_constants.PF_AFFILIATIONS: pretty_printed,
        }
        return cleaned_data


class StepD1_HQ_Form(forms.Form):
    nasa_center = forms.MultipleChoiceField(
        choices=(
            ("nasa_headquarters", "NASA Headquarters"),
            ("mission_support", "Mission Support"),
            ("ames_research_center", "Ames Research Center"),
            ("armstrong_flight_research_center", "Armstrong Flight Research Center"),
            ("glenn_research_center", "Glenn Research Center"),
            ("goddard_space_flight_center", "Goddard Space Flight Center"),
            ("goddard_institute_for_space_studies", "Goddard Institute for Space Studies"),
            ("jet_propulsion_laboratory", "Jet Propulsion Laboratory"),
            ("johnson_space_center", "Johnson Space Center"),
            ("katherine_johnson_ivv_facility", "Katherine Johnson IV&V Facility"),
            ("kennedy_space_center", "Kennedy Space Center"),
            ("langley_research_center", "Langley Research Center"),
            ("marshall_space_flight_center", "Marshall Space Flight Center"),
            ("michoud_assembly_facility", "Michoud Assembly Facility"),
            ("nasa_engineering_and_safety_center", "NASA Engineering and Safety Center"),
            ("nasa_safety_center", "NASA Safety Center"),
            ("nasa_shared_services_center", "NASA Shared Services Center"),
            ("neil_armstrong_test_facility", "Neil Armstrong Test Facility"),
            ("stennis_space_center", "Stennis Space Center"),
            ("wallops_flight_center", "Wallops Flight Center"),
            ("white_sands_test_facility", "White Sands Test Facility"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="What NASA Center do you work at?",
    )

    def clean(self):
        cleaned_data = super().clean()

        pretty_printed: Dict[str, Any] = {}

        for field, label in [
            ('nasa_center', profile_constants.PF_AFFILIATIONS_NASA_CENTERS),
        ]:
            choices_dict = dict(self.fields[field].choices)
            selected = cleaned_data.get(field, [])
            if selected:
                pretty_printed[label] = [choices_dict.get(choice) for choice in selected]

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepD2_HQ_Form(forms.Form):
    programs_currently_managing = forms.CharField(
        max_length=1024,
        required=False,
        label="What programs are you currently managing?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Program name, from year'})
    )
    programs_previously_managing = forms.CharField(
        max_length=1024,
        required=False,
        label="What programs have you previously managed?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Program name, from year to year'})
    )
    notable_achievements = forms.CharField(
        max_length=1024,
        required=False,
        label="What notable achievements, initiatives have you made?",
        widget=forms.TextInput(attrs={'placeholder': ''})
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed: Dict[str, Any] = {}

        # Continue from here!
        pretty_printed[profile_constants.PF_HQ_PROGRAMS] = {
            'Programs Currently Managing': cleaned_data.get('programs_currently_managing'),
            'Programs Previously Managing': cleaned_data.get('programs_previously_managing'),
            'Notable Achievements': cleaned_data.get('notable_achievements'),
        }

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepD3_HQ_Form(forms.Form):
    nasa_missions = forms.MultipleChoiceField(
        choices=(
            ("aeronomy_of_ice_in_the_mesosphere", "Aeronomy of Ice in the Mesosphere (AIM)"),
            ("cluster", "Cluster"),
            ("deep_space_climate_observatory", "Deep Space Climate Observatory (DSCVOR)"),
            ("hinode", "HINODE"),
            ("interface_region_imaging_spectrograph", "Interface Region Imaging Spectrograph (IRIS)"),
            ("interstellar_boundary_explorer", "Interstellar Boundary Explorer (IBEX)"),
            ("ionospheric_connection_explorer", "Ionospheric Connection Explorer (ICON)"),
            ("juno", "Juno"),
            ("magnetospheric_multiscale_satellites", "Magnetospheric Multiscale Satellites (MMS)"),
            ("solar_dynamics_observatory", "Solar Dynamics Observatory (SDO)"),
            ("solar_orbiter", "Solar Orbiter"),
            ("solar_terrestrial_relations_observatory", "Solar Terrestrial Relations Observatory (STERO)"),
            ("thermosphere_ionosphere_mesosphere_energetics_and_dynamics", "Thermosphere Ionosphere Mesosphere Energetics and Dynamics (TIMED)"),
            ("time_history_of_events_and_macroscale_interactions_during_substorms", "Time History of Events and Macroscale Interactions during Substorms (THEMIS)"),
            ("two-wide_angle_imaging_neutral-atom_spectrometers", "Two-Wide Angle Imaging Neutral-Atom Spectrometers (TWINS)"),
            ("van_alen_probes", "Van Allen Probes (formerly RBSP)"),
            ("wind", "Wind"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="Are you currently working on any NASA missions?",
    )
    nasa_initiatives = forms.MultipleChoiceField(
        choices=(
            ("open_science_tops", "Open Science/TOPS"),
            ("sound_rockets_programs", "Sound Rockets Programs"),
            ("cubesats", "Cubesats"),
            ("other", "Other"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="Are you affiliated with any of these NASA initiatives?",
    )
    nasa_initiatives_other = forms.CharField(
        max_length=1024,
        required=False,
        label="If other, please specify"
    )
    nasa_programs = forms.CharField(
        max_length=1024,
        required=False,
        label="Are you affiliated with any NASA programs? If yes, what is your affiliation?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Participating Scientist, Heliophysics Supporting Research; Program Director, Living With a Star'})
    )
    nasa_funding_arms = forms.CharField(
        max_length=1024,
        required=False,
        label="Are you affiliated with any NASA funding arms? If yes, what is your affiliation?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Grant Recipient, NASA Roses; Funder, NASA Roses'})
    )
    nasa_internal_groups = forms.MultipleChoiceField(
        choices=(
            ("center_for_helioanalytics", "Center for HelioAnalytics"),
            ("moon_to_mars_office", "Moon to Mars Office"),
            ("integrated_space_weather_analysis_team", "Integrated Space Weather Analysis Team"),
            ("other", "Other"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="Are you affiliated with any internal groups?",
    )
    nasa_internal_groups_other = forms.CharField(
        max_length=1024,
        required=False,
        label="If other, please specify"
    )

    def clean(self):
        cleaned_data = super().clean()

        # Check if all required fields are filled
        for fp in [
            ('nasa_initiatives', 'nasa_initiatives_other'),
            ('nasa_internal_groups', 'nasa_internal_groups_other'),
        ]:
            if is_empty(cleaned_data, fp):
                self._errors[fp[1]] = self.error_class([f'Please specify your {fp[0]} here.'])

        if self._errors:
            return cleaned_data

        # Prepare pretty_printed data
        pretty_printed: Dict[str, Any] = {}

        # Process multiple choice fields
        for field, label in [
            ('nasa_missions', "NASA Missions"),
            ('nasa_initiatives', "NASA Initiatives"),
            ('nasa_internal_groups', "groups"),
        ]:
            choices_dict = dict(self.fields[field].choices)
            selected = cleaned_data.get(field, [])
            if selected:
                pretty_printed[label] = [choices_dict.get(choice) for choice in selected]

            if other_info := cleaned_data.get(f"{field}_other_info", None):
                pretty_printed[label].append(other_info)

        # Process text fields
        text_fields = [
            ('nasa_programs', "NASA Programs"),
            ('nasa_funding_arms', "NASA Funding Arms"),
        ]
        for field, label in text_fields:
            value = cleaned_data.get(field)
            if value:
                pretty_printed[label] = [val.strip() for val in value.split(';') if val.strip()]

        groups = pretty_printed.get("groups")
        pretty_printed.pop("groups", None)

        cleaned_data['pretty_printed'] = {
            profile_constants.PF_GROUPS: groups,
            profile_constants.PF_AFFILIATIONS: pretty_printed,
        }
        return cleaned_data


class StepD2Form(forms.Form):
    employer = forms.CharField(
        max_length=1024,
        required=False,
        label="Who is your employer?"
    )
    place_of_work = forms.CharField(
        max_length=1024,
        required=False,
        label="Where are you located?"
    )
    job_title = forms.CharField(
        max_length=1024,
        required=False,
        label="What is your job title?"
    )
    what_kind_of_work_does_user = forms.CharField(
        max_length=1024,
        required=False,
        label="What kind of work do you do?"
    )
    non_nasa_groups_affiliated_with = forms.CharField(
        max_length=1000,
        required=False,
        label="At your place of work, what departments, labs, or groups are you affiliated with?",
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    non_nasa_infrastructure_affiliated_with = forms.CharField(
        max_length=1000,
        required=False,
        label="Are you affiliated with any notable materials, initiatives, or other infrastructure (models, programs, etc.) hosted at your place of work?",
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    non_nasa_other_affiliation_info = forms.CharField(
        max_length=1000,
        required=False,
        label="Is there any other information you would like to share about your affiliations at your place of work?",
        widget=forms.TextInput(attrs={'placeholder': ''})
    )

    def clean(self):
        cleaned_data = super().clean()

        pretty_printed = dict()

        pretty_printed[profile_constants.PF_EMPLOYER] = cleaned_data.get('employer')
        pretty_printed[profile_constants.PF_PLACE_OF_WORK] = cleaned_data.get('place_of_work')
        pretty_printed[profile_constants.PF_JOB_TITLE] = cleaned_data.get('job_title')
        pretty_printed[profile_constants.PF_JOB_DESCRIPTION] = cleaned_data.get('what_kind_of_work_does_user')
        pretty_printed[profile_constants.PF_GROUPS] = cleaned_data.get('non_nasa_groups_affiliated_with')
        pretty_printed[profile_constants.PF_NON_NASA_INFRASTRUCTURE] = cleaned_data.get('non_nasa_infrastructure_affiliated_with')
        pretty_printed[profile_constants.PF_NON_NASA_OTHER_AFFILIATION_INFO] = cleaned_data.get('non_nasa_other_affiliation_info')

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepE_ResearchScientist_Form(forms.Form):
    solar_system_area = forms.MultipleChoiceField(
        choices=(
            ("ionosphere", "Ionosphere"),
            ("magnetosphere", "Magnetosphere"),
            ("solar", "Solar"),
            ("solar_wind", "Solar Wind"),
            ("neutral_atmosphere", "Neutral Atmosphere"),
            ("theoretical", "Theoretical"),
            ("space_weather", "Space Weather"),
            ("heliophysics", "Heliophysics"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="What area of the solar system do you study?",
    )

    def clean(self):
        cleaned_data = super().clean()
        studies = cleaned_data.get('solar_system_area', [])

        pretty_printed = {
            profile_constants.PF_STUDIES: [label for value, label in self.fields['solar_system_area'].choices if value in studies],
        }

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepF_ResearchScientist_Form(forms.Form):
    solar_system_area_study_type = forms.MultipleChoiceField(
        choices=(
            ("build_models", "Build Models"),
            ("make_instruments", "Make Instruments"),
            ("develop_theory", "Develop Theory"),
            ("data_analysis", "Data Analysis"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="How do you study that?",
    )
    solar_system_area_study_type_others = forms.CharField(
        max_length=500,
        required=False,
        label="Other (please specify)"
    )

    def clean(self):
        cleaned_data = super().clean()

        methods = cleaned_data.get('solar_system_area_study_type', [])
        pretty_printed = {
            profile_constants.PF_METHODS: [label for value, label in self.fields['solar_system_area_study_type'].choices if value in methods],
        }
        if other_study := cleaned_data.get('solar_system_area_study_type_others'):
            pretty_printed[profile_constants.PF_METHODS].append(other_study)

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepG_ResearchScientist_Form(forms.Form):
    study_topics = forms.MultipleChoiceField(
        choices=(
            ("archival_tools", "Archival Tools"),
            ("arms", "ARMS"),
            ("atomic_physics", "Atomic Physics"),
            ("chromosphere", "Chromosphere"),
            ("cmes", "CMEs"),
            ("coronagraphs", "Coronagraphs"),
            ("coronal_heating", "Coronal Heating"),
            ("coronal_mass_ejection", "Coronal Mass Ejection"),
            ("data_analysis", "Data Analysis"),
            ("enas", "ENAs"),
            ("euv", "EUV"),
            ("flares", "Flares"),
            ("flux_ropes", "Flux Ropes"),
            ("heliophysics_infrastructure", "Heliophysics Infrastructure"),
            ("high_performance_computing", "High Performance Computing"),
            ("high_energy", "High-energy (X-Rays/Gamma-rays)"),
            ("in_situ_observations", "In Situ Observations"),
            ("interplanetary_shocks", "Interplanetary Shocks"),
            ("lare", "LARE"),
            ("magnetic_connectivity", "Magnetic Connectivity"),
            ("magnetic_reconnection", "Magnetic Reconnection"),
            ("magnetohydrodynamics", "Magnetohydrodynamics (MHD)"),
            ("mission_development", "Mission Development"),
            ("numerical_modeling", "Numerical Modeling"),
            ("optics", "Optics"),
            ("particle_acceleration", "Particle Acceleration"),
            ("particle_in_cell", "Particle-in-cell (PIC) Modeling"),
            ("prominences_filaments", "Prominences/Filaments"),
            ("radiative_transport", "Radiative Transport"),
            ("radio", "Radio"),
            ("solar", "Solar"),
            ("solar_convection_zone", "Solar Convection Zone"),
            ("solar_corona", "Solar Corona"),
            ("solar_cycle", "Solar Cycle"),
            ("solar_energetic_particles", "Solar Energetic Particles (SEPs)"),
            ("solar_flares", "Solar Flares"),
            ("solar_instrumentation", "Solar Instrumentation"),
            ("solar_magnetic_fields", "Solar Magnetic Fields"),
            ("solar_modeling", "Solar Modeling"),
            ("solar_photosphere", "Solar Photosphere"),
            ("solar_remote_sensing", "Solar Remote Sensing"),
            ("solar_wind", "Solar Wind"),
            ("solar_wind_acceleration", "Solar Wind Acceleration"),
            ("solar_wind_formation", "Solar Wind Formation"),
            ("sounding_rockets", "Sounding Rockets"),
            ("space_weather_forecasting", "Space Weather Forecasting"),
            ("spectroscopy", "Spectroscopy"),
            ("transition_region", "Transition Region"),
            ("turbulence", "Turbulence"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="What topics do you study?",
    )
    study_topics_others = forms.CharField(max_length=500, required=False, label="Other (please specify)")

    def clean(self):
        cleaned_data = super().clean()
        topics = cleaned_data.get('study_topics', [])

        pretty_printed = {
            profile_constants.PF_TOPICS: [label for value, label in self.fields['study_topics'].choices if value in topics],
        }
        if other_study := cleaned_data.get('study_topics_others'):
            pretty_printed[profile_constants.PF_TOPICS].append(other_study)

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepH_ResearchScientist_Form(forms.Form):
    user_extra_occupations = forms.MultipleChoiceField(
        choices=(
            ("engineering", "Engineering"),
            ("administration", "Administration"),
            ("policy", "Policy"),
            ("program_management", "Program Management"),
            ("people_management", "People Management"),
            ("software_development", "Software Development"),
            ("community_organization", "Community Organization"),
            ("event_organization", "Event Organization"),
            ("knowledge_management", "Knowledge Management"),
        ),
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
        label="What else do you do?",
    )
    user_extra_occupations_others = forms.CharField(max_length=500, required=False, label="Other (please specify)")

    def clean(self):
        cleaned_data = super().clean()
        occupations = cleaned_data.get('user_extra_occupations', [])

        pretty_printed = {
            profile_constants.PF_OCCUPATIONS: [label for value, label in self.fields['user_extra_occupations'].choices if value in occupations],
        }
        if other_occupation := cleaned_data.get('user_extra_occupations_others'):
            pretty_printed[profile_constants.PF_OCCUPATIONS].append(other_occupation)

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepI_ResearchScientist_Form(forms.Form):
    primary_skillset = forms.CharField(
        max_length=1000,
        required=False,
        label="What is your primary skillset?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Research Programmer, Theoretical Scientist, Research Scientist'})
    )
    instruments_worked_with = forms.CharField(
        max_length=1000,
        required=False,
        label="Have you worked with particular instruments?",
    )
    models_worked_with = forms.CharField(
        max_length=1000,
        required=False,
        label="What models have you previously worked with?",
    )
    tools_used = forms.CharField(
        max_length=1000,
        required=False,
        label="What tools do you use?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Python, Fortran, Ontologies, 3D Printer, 3D Printer Software Languages'})
    )
    techniques_used = forms.CharField(
        max_length=1000,
        required=False,
        label="What techniques do you use?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Fourier Analysis, Flux Corrective Transport'})
    )

    def clean(self):
        cleaned_data = super().clean()

        pretty_printed: Dict[str, List[str]] = {}

        fields_mapping = {
            "primary_skillset": "Skillset",
            "instruments_worked_with": "Instruments",
            "models_worked_with": "Models",
            "tools_used": "Tools",
            "techniques_used": "Techniques"
        }

        for field, label in fields_mapping.items():
            value = cleaned_data.get(field)
            if value:
                pretty_printed[label] = [val.strip() for val in value.split(',') if val.strip()]

        cleaned_data['pretty_printed'] = {
            profile_constants.PF_SKILLSET: pretty_printed
        }
        return cleaned_data


class StepI_Engineer_Form(forms.Form):
    engineering_kind = forms.CharField(
        max_length=1000,
        required=False,
        label="What kind of engineering do you do?",
    )
    primary_skillset = forms.CharField(
        max_length=1000,
        required=False,
        label="What is your primary skillset?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Software Engineer'})
    )
    other_skillset = forms.CharField(
        max_length=1000,
        required=False,
        label="What other skills do you have?",
    )
    areas_worked_in = forms.CharField(
        max_length=1000,
        required=False,
        label="What areas do you work in?",
    )
    approaches_used = forms.CharField(
        max_length=1000,
        required=False,
        label="What approaches do you use?",
    )
    tools_used = forms.CharField(
        max_length=1000,
        required=False,
        label="What tools do you use?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Python, CATIA, Steel Structures'})
    )
    techniques_used = forms.CharField(
        max_length=1000,
        required=False,
        label="What techniques do you use?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Fourier Analysis, Flux Corrective Transport'})
    )
    instruments_worked_with = forms.CharField(
        max_length=1000,
        required=False,
        label="Have you worked with particular instruments?",
    )

    def clean(self):
        cleaned_data = super().clean()

        pretty_printed: Dict[str, List[str]] = {}

        fields_mapping = {
            "primary_skillset": "Skillset",
            "areas_worked_in": "Areas Worked In",
            "approaches_used": "Approaches",
            "other_skillset": "Other Skills",
            "instruments_worked_with": "Instruments",
            "tools_used": "Tools",
            "techniques_used": "Techniques"
        }

        for field, label in fields_mapping.items():
            value = cleaned_data.get(field)
            if value:
                pretty_printed[label] = [val.strip() for val in value.split(',') if val.strip()]

        cleaned_data['pretty_printed'] = {
            profile_constants.PF_JOB_DESCRIPTION: cleaned_data.get('engineering_kind'),
            profile_constants.PF_SKILLSET: pretty_printed
        }

        return cleaned_data


class StepJForm(forms.Form):
    questions_being_investigated = forms.CharField(
        max_length=1000,
        required=False,
        label="What current science questions are you investigating?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: What heats the solar corona?'})
    )
    # This will only be shown in the engineering flow
    engineering_topics = forms.CharField(
        max_length=1000,
        required=False,
        label="What current engineering topics are you working on?",
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    personal_initiatives = forms.CharField(
        max_length=250,
        required=False,
        label="What personal initiatives are you pursuing, in general or related to specific roles?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Pursuing a PhD, writing a proposal for <RFP>, writing a paper about <topic>'})
    )
    programs_affiliated_to = forms.CharField(
        max_length=250,
        required=False,
        label="What formal roles do you have? Are you affiliated with any programs?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Principal Investigator, Mission Science;  Co-Investigator, Project Science; Lab Chief, Program Science; Director, Program Science'})
    )
    projects_working_on = forms.CharField(
        max_length=250,
        required=False,
        label="Are you working on any projects?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Helioweb, Martian S-Web, Mesoscale dynamics in the solar wind, GPS Anomalies Caused by Space Weather'})
    )
    events_as_speaker = forms.CharField(
        max_length=250,
        required=False,
        label="Are you speaking or presenting at any upcoming events?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Event name, style of presentation, date'})
    )
    events_as_organizer = forms.CharField(
        max_length=250,
        required=False,
        label="Are you organizing any upcoming events?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Role title at event name'})
    )
    community_initiatives = forms.CharField(
        max_length=250,
        required=False,
        label="Are you involved in any community or outreach initiatives?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Activity, role title, organization'})
    )
    other_scientific_activities = forms.CharField(
        max_length=250,
        required=False,
        label="Is there anything else you'd like to share?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Activity, role type'})
    )

    def clean(self):
        cleaned_data = super().clean()

        # The profile_constants.PF_TOPICS field is only shown in the engineering flow
        # So it should never overwrite the one in the StepG_ResearchScientist_Form
        pretty_printed: Dict[str, List[str]] = {}
        pretty_printed_mapping = {
            "questions_being_investigated": "Science Questions",
            "engineering_topics": "Topics",
            "personal_initiatives": "Initiatives",
            "programs_affiliated_to": "Programs",
            "projects_working_on": "Projects",
            "events_as_speaker": "Events as Speaker",
            "events_as_organizer": "Events as Organizer",
            "community_initiatives": "Community Outreach",
            "other_scientific_activities": "Other Scientific Activities"
        }
        for field, label in pretty_printed_mapping.items():
            if value := cleaned_data.get(field):
                pretty_printed[label] = [val.strip() for val in value.split(',') if val.strip()]

        stub_cards: List[Dict[str, str]] = []
        stubs_mapping = {
            "questions_being_investigated": card_constants.GraphTypes.SCIENCE_QUESTION.value,
            "personal_initiatives": card_constants.INITIATIVE,
            "projects_working_on": card_constants.PROJECT,
            "events_as_speaker": card_constants.GraphTypes.EVENT.value,
            "events_as_organizer": card_constants.GraphTypes.EVENT.value,
        }
        for field, label in stubs_mapping.items():
            if value := cleaned_data.get(field):
                stubs = [val.strip() for val in value.split(',') if val.strip()]
                stub_cards.extend([{"type": label, "name": s} for s in stubs])

        cleaned_data['pretty_printed'] = {
            profile_constants.PF_WORKING_ON: pretty_printed
        }
        cleaned_data['stub_cards'] = stub_cards
        return cleaned_data


class StepKForm(forms.Form):
    aas_spd_society = forms.ChoiceField(
        choices=(
            ("leader", "Leader"),
            ("contributor", "Contributor"),
            ("general_member", "General Member"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="AAS/SPD",
    )
    agu_society = forms.ChoiceField(
        choices=(
            ("leader", "Leader"),
            ("contributor", "Contributor"),
            ("general_member", "General Member"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="AGU",
    )
    ams_society = forms.ChoiceField(
        choices=(
            ("leader", "Leader"),
            ("contributor", "Contributor"),
            ("general_member", "General Member"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="AMS",
    )
    aps_society = forms.ChoiceField(
        choices=(
            ("leader", "Leader"),
            ("contributor", "Contributor"),
            ("general_member", "General Member"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="APS",
    )
    aiaa_society = forms.ChoiceField(
        choices=(
            ("leader", "Leader"),
            ("contributor", "Contributor"),
            ("general_member", "General Member"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="AIAA",
    )
    affiliated_research_groups = forms.CharField(
        max_length=1000,
        required=False,
        label="Are you affiliated with any research groups?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Director at Lab Group'})
    )
    affiliated_programs_outside_work = forms.CharField(
        max_length=1000,
        required=False,
        label="Are you affiliated with any programs outside of your place of work?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: XYZ at University of Michigan'})
    )
    affiliated_groups_outside_work = forms.CharField(
        max_length=1000,
        required=False,
        label="Are you affiliated with any other formal groups outside of your place of work?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Liaison with Google, Partnership with HP, Visiting Scholar at SFI'})
    )
    affiliated_journals = forms.CharField(
        max_length=1000,
        required=False,
        label="Are you affiliated with any journals?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Editor/Organizer/Staff/Peer Reviewer at Journal Name'})
    )
    affiliated_conferences = forms.CharField(
        max_length=1000,
        required=False,
        label="Are you affiliated with any conferences or events?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Program Committee at KGC'})
    )
    list_previous_affiliations = forms.ChoiceField(
        choices=(
            ("yes", "Yes"),
            ("no", "No"),
        ),
        required=True,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Would you like to list your previous affiliations? ",
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed = {}

        affiliations = {}
        society_fields = [
            'aas_spd_society',
            'agu_society',
            'ams_society',
            'aps_society',
            'aiaa_society'
        ]

        for field in society_fields:
            if field in cleaned_data and cleaned_data[field]:
                label = self.fields[field].label
                choice_label = dict(self.fields[field].choices)[cleaned_data[field]]
                affiliations[label] = choice_label

        text_fields = [
            'affiliated_research_groups',
            'affiliated_programs_outside_work',
            'affiliated_groups_outside_work',
            'affiliated_journals',
            'affiliated_conferences',
        ]

        for field in text_fields:
            if field in cleaned_data and cleaned_data[field]:
                label = self.fields[field].label
                affiliations[label] = [val.strip() for val in cleaned_data[field].split(';') if val.strip()]

        pretty_printed[profile_constants.PF_OTHER_AFFILIATIONS] = affiliations
        cleaned_data['pretty_printed'] = pretty_printed

        return cleaned_data


class StepK1Form(forms.Form):
    previously_affiliated_research_groups = forms.CharField(
        max_length=1000,
        required=False,
        label="Have you been previously affiliated with any research groups?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Director at Lab Group, ...'})
    )
    previously_affiliated_programs_outside_work = forms.CharField(
        max_length=1000,
        required=False,
        label="Have you been affiliated previously with particular programs?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Role at TOPS, ...'})
    )
    previously_affiliated_groups_outside_work = forms.CharField(
        max_length=1000,
        required=False,
        label="Have you been previously affiliated with any other formal groups, at your place of work or via collaboration?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Admin at Center for HelioAnalytics, ...'})
    )
    previously_affiliated_journals = forms.CharField(
        max_length=1000,
        required=False,
        label="Have you previously been affiliated with any journals?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Editor/Organizer/Staff/Peer Reviewer at Journal Name, ...'})
    )
    previously_affiliated_conferences = forms.CharField(
        max_length=1000,
        required=False,
        label="Have you been affiliated with any conferences or events?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Organizer at Event, ...'})
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed = {}

        previous_affiliations = {}
        text_fields = [
            'affiliated_research_groups',
            'affiliated_programs_outside_work',
            'affiliated_groups_outside_work',
            'affiliated_journals',
            'affiliated_conferences',
        ]

        for field in text_fields:
            if field in cleaned_data and cleaned_data[field]:
                label = self.fields[field].label
                previous_affiliations[label] = [val.strip() for val in cleaned_data[field].split(';') if val.strip()]

        pretty_printed[profile_constants.PF_OTHER_AFFILIATIONS] = previous_affiliations
        cleaned_data['pretty_printed'] = pretty_printed

        return cleaned_data


class StepLForm(forms.Form):
    primary_contact_for = forms.CharField(
        max_length=1024,
        required=False,
        label="Are you the primary contact for any scientific resources?",
    )

    def clean(self):
        cleaned_data = super().clean()
        raw_primary_contact_form = cleaned_data.get("primary_contact_for", "")
        pocs = [item.strip() for item in raw_primary_contact_form.split(',') if item.strip()]
        cleaned_data['pretty_printed'] = {
            profile_constants.PF_PRIMARY_CONTACT_FOR: pocs
        }

        return cleaned_data


class StepMForm(forms.Form):
    orgs_received_funding_from = forms.CharField(
        max_length=1000,
        required=False,
        label="From what organizations have you received funding?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: NASA Roses, year(s); NSF, year(s)'})
    )
    journals_published_in = forms.CharField(
        max_length=1000,
        required=False,
        label="In what journals have you published?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: The Astrophysics Journal,  2024; Journal of Geophysical Research, 2023; Nature, 2021; Science, 2021; Solar Physics, 2024'})
    )
    events_spoken_at = forms.CharField(
        max_length=1000,
        required=False,
        label="At what events have you spoken?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: AGU 2024, ESIP 2022'})
    )
    awards_received = forms.CharField(
        max_length=1000,
        required=False,
        label="Have you received any awards?",
        widget=forms.TextInput(attrs={'placeholder': 'Example: Award, granting organization'})
    )

    def clean(self):
        cleaned_data = super().clean()

        # Prepare pretty_printed data
        pretty_printed: Dict[str, List[str]] = {}

        field_mappings = {
            "orgs_received_funding_from": 'Received Funding From',
            "journals_published_in": 'Journals Published In',
            "events_spoken_at": 'Events Spoken At',
            "awards_received": 'Awards Received',
        }

        for field_name, pretty_label in field_mappings.items():
            field_value = cleaned_data.get(field_name)
            if field_value:
                pretty_printed[pretty_label] = [item.strip() for item in field_value.split(';') if item.strip()]

        cleaned_data['pretty_printed'] = {
            profile_constants.PF_HAVE_DONE: pretty_printed
        }
        return cleaned_data


class StepNForm(forms.Form):
    collaborators = forms.CharField(
        max_length=1000,
        required=False,
        label="Who is in your “lab group” - people who you commonly work with and interact with about developments in the field? Please identify collaborators by sharing their email addresses, separated by commas - these addresses will not be made public, but will be used to link your colleagues with the right profile if they have not yet joined the Helioweb network.",
        widget=forms.TextInput(attrs={'placeholder': 'Example: email@example.com, email2@example.com, ...'})
    )

    def clean(self):
        cleaned_data = super().clean()
        pretty_printed = {
            profile_constants.PF_COLLABORATORS: [v.strip() for v in cleaned_data.get('collaborators', '').split(',') if v.strip()]
        }

        cleaned_data['pretty_printed'] = pretty_printed
        return cleaned_data


class StepOForm(forms.Form):
    collaboration_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming collaboration opportunities?",
    )
    job_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming job opportunities?",
    )
    post_doc_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming post doc opportunities?",
    )
    rfp_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming RFP opportunities?",
    )
    journal_call_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming journal call opportunities?",
    )
    event_call_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming conference or event call opportunities?",
    )
    community_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming community opportunities?",
    )
    mentorship_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming mentorship opportunities?",
    )
    internship_opportunities = forms.CharField(
        max_length=1024,
        required=False,
        label="Do you have any current or upcoming internship opportunities?",
    )

    def clean(self):
        cleaned_data = super().clean()

        pretty_printed: Dict[str, List[str]] = {}
        fields_mapping = {
            'collaboration_opportunities': "Collaborations",
            'job_opportunities': "Jobs",
            'post_doc_opportunities': "Post Docs",
            'rfp_opportunities': "RFPs",
            'journal_call_opportunities': "Journal Calls",
            'event_call_opportunities': "Conference or Event Calls",
            'community_opportunities': "Community",
            'mentorship_opportunities': "Mentorships",
            'internship_opportunities': "Internships",
        }

        for field, label in fields_mapping.items():
            if value := cleaned_data.get(field):
                pretty_printed[label] = [val.strip() for val in value.split(',') if val.strip()]

        stub_cards: List[Dict[str, str]] = []
        stubs_mapping = {
            "collaboration_opportunities": card_constants.COLLABORATION,
            'job_opportunities': card_constants.JOB,
            'post_doc_opportunities': card_constants.POST_DOC,
            'rfp_opportunities': card_constants.RFP,
            'journal_call_opportunities': card_constants.JOURNAL_CALL,
            'event_call_opportunities': card_constants.EVENT_CALL,
            'community_opportunities': card_constants.COMMUNITY_OPPORTUNITY,
            'mentorship_opportunities': card_constants.MENTOR,
            'internship_opportunities': card_constants.INTERNSHIP,
        }
        for field, label in stubs_mapping.items():
            if value := cleaned_data.get(field):
                stubs = [val.strip() for val in value.split(',') if val.strip()]
                stub_cards.extend([{"type": label, "name": s} for s in stubs])

        cleaned_data['pretty_printed'] = {
            profile_constants.PF_UPCOMING_OPPORTUNITIES: pretty_printed
        }
        cleaned_data['stub_cards'] = stub_cards
        return cleaned_data


class StepPForm(forms.Form):
    job_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Jobs",
    )
    post_doc_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Post Docs",
    )
    community_engagement_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Community Opportunities",
    )
    rfp_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="RFPs",
    )
    journal_call_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Journal Calls",
    )
    conference_event_call_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Conference/Event Calls",
    )
    collaboration_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Collaborations",
    )
    mentor_menteeship_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Mentor/Menteeship",
    )
    internship_opportunities = forms.ChoiceField(
        choices=(
            ("now", "Now"),
            ("in_general", "In General"),
        ),
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Internship",
    )


def is_empty(data: dict, field_pair: tuple[str, str]) -> bool:
    """Check if a secondary field is empty based on the value of a primary field.

    This function is used to determine if a secondary field (`other_info_field_name`)
    should be considered empty. It checks the value of a primary field (`main_field_name`),
    and if the primary field's value is 'other', it then checks if the secondary field's
    value is empty. The function returns True if the secondary field is empty when the
    primary field's value is 'other', otherwise, it returns False.

    This is used to determine if the user has inputted wrong data: if they have checked
    the 'other' option for the primary field, the should specify what "other" really is.

    Args:
        data (dict): The form data containing the fields to check.
        field_pair (tuple[str, str]): A tuple containing the names of the primary field
                                      and the secondary field to check.

    Returns:
        bool: True if the secondary field is empty when the primary field's value is 'other',
              otherwise False.
    """
    main_field_name, other_info_field_name = field_pair
    if data.get(main_field_name, '') == 'other' or 'other' in data.get(main_field_name, []):
        other_info = data.get(other_info_field_name, None)
        if other_info in EMPTY_VALUES:
            return True
    return False
