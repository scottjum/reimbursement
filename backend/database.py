""" Database class """
from __future__ import annotations

import os
import re
from typing import Any, Dict, Optional, Tuple

from dotenv import load_dotenv
from supabase import Client, create_client
from sqlmodel import Field, SQLModel


load_dotenv(override=True)

class PatientInformationBase(SQLModel, table=True):
    """ Patient Information """
    id: Optional[int] = Field(default=None, primary_key=True, description="The patient's id.")
    insured_id: Optional[int] = Field(default=None, foreign_key="insured_information.id")
    patient_last_name: str = Field(..., description="The patient's last name.")
    patient_first_name: str = Field(..., description="The patient's first name.")
    patient_middle_initial: Optional[str] = Field(default=None, description="The patient's middle initial.")
    patient_date_of_birth: str = Field(..., description="The patient's date of birth.")
    patient_gender: str = Field(..., description="The patient's gender.")
    patient_address: str = Field(..., description="The patient's address.")
    patient_city: str = Field(..., description="The patient's city.")
    patient_state: str = Field(..., description="The patient's state.")
    patient_zip: str = Field(..., description="The patient's zip code.")
    patient_phone: str = Field(..., description="The patient's phone number.")
    status: Optional[str] = Field(default=None, description="The patient's status.")
    relationship_to_insured: str = Field(..., description="The patient's relationship to the insured.")
    condition_related_to_employment: Optional[str] = Field(default=None, description="The patient's condition related to employment.")
    condition_related_to_auto_accident: Optional[str] = Field(default=None, description="The patient's condition related to auto accident.")
    date_of_current_illness: str = Field(..., description="The patient's date of current illness.")
    condition_related_to_other: Optional[str] = Field(default=None, description="The patient's condition related to other.")
    auto_accident_place: Optional[str] = Field(default=None, description="The patient's auto accident place.")
    

class InsuredInformationBase(SQLModel, table=True):
    """ Insured Information """
    id: Optional[int] = Field(default=None, primary_key=True, description="The insured's id.")
    last_name: str = Field(..., description="The insured's last name.")
    first_name: str = Field(..., description="The insured's first name.")
    middle_initial: Optional[str] = Field(default=None, description="The insured's middle initial.")
    date_of_birth: str = Field(..., description="The insured's date of birth.")
    identification_number: int = Field(..., description="The insured's identification number.")
    gender: str = Field(..., description="The insured's gender.")
    address: str = Field(..., description="The insured's address.")
    city: str = Field(..., description="The insured's city.")
    state: str = Field(..., description="The insured's state.")
    zip: str = Field(..., description="The insured's zip code.")
    phone: str = Field(..., description="The insured's phone number.")
    employer_name: Optional[str] = Field(default=None, description="The insured's employer name.")
    insurance_plan_name: str = Field(..., description="The insured's insurance plan name.")
    another_insurance_plan: bool = Field(default=False, description="The insured's another insurance plan.")
    other_identification_number: Optional[int] = Field(default=None, description="The insured's other identification number.")

class OtherInsuranceInformationBase(SQLModel, table=True):
    """ Other Insurance Information """
    id: Optional[int] = Field(default=None, primary_key=True, description="The other insurance information's id.")
    policy_holder_insurance_last_name: str = Field(..., description="The other insurance information's policy holder insurance last name.")
    policy_holder_insurance_first_name: str = Field(..., description="The other insurance information's policy holder insurance first name.")
    policy_holder_insurance_middle_initial: Optional[str] = Field(default=None, description="The other insurance information's policy holder insurance middle initial.")
    policy_holder_insurance_date_of_birth: str = Field(..., description="The other insurance information's policy holder insurance date of birth.")
    policy_holder_identification_number: int = Field(..., description="The other insurance information's policy holder insurance identification number.")
    policy_holder_insurance_plan_name: str = Field(..., description="The other insurance information's policy holder insurance plan name.")
    policy_holder_insurance_gender: str = Field(..., description="The other insurance information's policy holder insurance gender.")
    policy_holder_telephone_number: str = Field(..., description="The other insurance information's policy holder insurance telephone number.")
    policy_holder_employer_name: Optional[str] = Field(default=None, description="The other insurance information's policy holder insurance employer name.")

class AttestationBase(SQLModel, table=True):
    """ Attestation """
    id: Optional[int] = Field(default=None, primary_key=True, description="The attestation's id.")
    date_patient: str = Field(..., description="The attestation's date of patient.")
    provider_name: str = Field(..., description="The attestation's provider name.")
    tax_number: int = Field(..., description="The attestation's tax number.")
    NPI_number: int = Field(..., description="The attestation's NPI number.")
    date_of_insured: str = Field(..., description="The attestation's date of insured.")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class Database:
    """ Database class """
    def __init__(self):
        self.supabase = supabase

    # ----------------------------
    # Internal normalization helpers
    # ----------------------------

    @staticmethod
    def _clean_str(value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            s = value.strip()
            return s if s else None
        return str(value).strip() or None

    @staticmethod
    def _parse_int(value: Any) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        s = Database._clean_str(value)
        if s is None:
            return None
        digits = re.sub(r"[^\d]", "", s)
        return int(digits) if digits else None

    @staticmethod
    def _is_effectively_empty(section: Any) -> bool:
        if not isinstance(section, dict):
            return True
        for v in section.values():
            if v is False:
                return False
            if Database._clean_str(v) is not None:
                return False
            if v is not None and not isinstance(v, (str, bool)):
                return False
        return True

    _MISSING_COLUMN_RE = re.compile(r"Could not find the '([^']+)' column", re.IGNORECASE)

    def _insert_with_unknown_column_retry(
        self,
        table: str,
        payload: Dict[str, Any],
        *,
        dry_run: bool,
    ) -> Tuple[Optional[int], Dict[str, Any]]:
        """
        Insert payload into table.
        If Supabase rejects unknown columns (PostgREST), remove the column and retry.
        Returns (id, final_payload_used).
        """
        final_payload = dict(payload)
        if dry_run:
            return None, final_payload

        while True:
            try:
                resp = self.supabase.from_(table).insert(final_payload).execute()
                inserted_id = None
                if getattr(resp, "data", None) and isinstance(resp.data, list) and resp.data:
                    inserted_id = resp.data[0].get("id")
                return inserted_id, final_payload
            except Exception as e:  # noqa: BLE001 - surface supabase errors with context
                msg = str(e)
                m = self._MISSING_COLUMN_RE.search(msg)
                if m:
                    col = m.group(1)
                    if col in final_payload:
                        final_payload.pop(col, None)
                        continue
                raise RuntimeError(f"Failed inserting into {table}: {msg}\nPayload: {final_payload}") from e

    def create_patient_information(self, patient_information: PatientInformationBase):
        """Create a new patient information."""
        return self.supabase.from_("Patient_Information").insert(patient_information.model_dump()).execute()

    # INSERT Statements

    def create_insured_information(self, insured_information: InsuredInformationBase):
        """Create a new insured information."""
        return self.supabase.from_("Insured_Information").insert(insured_information.model_dump()).execute()

    def create_other_insurance_information(self, other_insurance_information: OtherInsuranceInformationBase):
        """Create a new other insurance information."""
        return self.supabase.from_("Other_Insurance_Information").insert(other_insurance_information.model_dump()).execute()
    
    def create_attestation(self, attestation: AttestationBase):
        """Create a new attestation."""
        return self.supabase.from_("Attestation").insert(attestation.model_dump()).execute()

    # SELECT Statements

    def get_patient_information(self, patient_id: int):
        """Get a patient information by id."""
        return self.supabase.from_("Patient_Information").select("*").eq("id", patient_id).execute()

    def get_insured_information(self, insured_id: int):
        """Get an insured information by id."""
        return self.supabase.from_("Insured_Information").select("*").eq("id", insured_id).execute()

    def get_other_insurance_information(self, other_insurance_id: int):
        """Get other insurance information by id."""
        return self.supabase.from_("Other_Insurance_Information").select("*").eq("id", other_insurance_id).execute()

    def get_attestation(self, attestation_id: int):
        """Get an attestation by id."""
        return self.supabase.from_("Attestation").select("*").eq("id", attestation_id).execute()
    
    def get_all_patient_information(self):
        """ Get all patient information """
        return self.supabase.from_("Patient_Information").select("*").execute()

    def get_all_insured_information(self):
        """ Get all insured information """
        return self.supabase.from_("Insured_Information").select("*").execute()

    def get_all_other_insurance_information(self):
        """ Get all other insurance information """
        return self.supabase.from_("Other_Insurance_Information").select("*").execute()

    def get_all_attestation(self):
        """ Get all attestation """
        return self.supabase.from_("Attestation").select("*").execute()

    def get_all_patient_information_by_insured_id(self, insured_id: int):
        """ Get all patient information by insured id """
        return self.supabase.from_("Patient_Information").select("*").eq("insured_id", insured_id).execute()

    def get_all_insured_information_by_patient_id(self, patient_id: int):
        """ Get all insured information by patient id """
        return self.supabase.from_("Insured_Information").select("*").eq("patient_id", patient_id).execute()

    def get_all_other_insurance_information_by_insured_id(self, insured_id: int):
        """ Get all other insurance information by insured id """
        return self.supabase.from_("Other_Insurance_Information").select("*").eq("insured_id", insured_id).execute()

    def get_all_attestation_by_patient_id(self, patient_id: int):
        """ Get all attestation by patient id """
        return self.supabase.from_("Attestation").select("*").eq("patient_id", patient_id).execute()

    def get_all_attestation_by_insured_id(self, insured_id: int):
        """ Get all attestation by insured id """
        return self.supabase.from_("Attestation").select("*").eq("insured_id", insured_id).execute()

    def get_all_patient_information_by_patient_last_name(self, patient_last_name: str):
        """ Get all patient information by patient last name """
        return self.supabase.from_("Patient_Information").select("*").eq("patient_last_name", patient_last_name).execute()

    def get_all_insured_information_by_last_name(self, last_name: str):
        """ Get all insured information by last name """
        return self.supabase.from_("Insured_Information").select("*").eq("last_name", last_name).execute()

    def get_all_other_insurance_information_by_policy_holder_insurance_last_name(self, 
    policy_holder_insurance_last_name: str):
        """ Get all other insurance information by policy holder insurance last name """
        return self.supabase.from_("Other_Insurance_Information").select("*").eq("policy_holder_insurance_last_name", policy_holder_insurance_last_name).execute()

    def get_all_attestation_by_date_patient(self, date_patient: str):
        """ Get all attestation by date patient """
        return self.supabase.from_("Attestation").select("*").eq("date_patient", date_patient).execute()

    def get_all_attestation_by_provider_name(self, provider_name: str):
        """ Get all attestation by provider name """
        return self.supabase.from_("Attestation").select("*").eq("provider_name", provider_name).execute()

    def get_all_attestation_by_tax_number(self, tax_number: int):
        """ Get all attestation by tax number """
        return self.supabase.from_("Attestation").select("*").eq("tax_number", tax_number).execute()

    def get_all_attestation_by_npi_number(self, npi_number: int):
        """ Get all attestation by NPI number """
        return self.supabase.from_("Attestation").select("*").eq("NPI_number", npi_number).execute()

    def get_all_attestation_by_date_of_insured(self, date_of_insured: str):
        """ Get all attestation by date of insured """
        return self.supabase.from_("Attestation").select("*").eq("date_of_insured", date_of_insured).execute()

    # UPDATE Statements

    def update_patient_information(self, patient_id: int, patient_information: PatientInformationBase):
        """Update a patient information."""
        return self.supabase.from_("Patient_Information").update(patient_information.model_dump()).eq("id", patient_id).execute()

    def update_insured_information(self, insured_id: int, insured_information: InsuredInformationBase):
        """Update an insured information."""
        return self.supabase.from_("Insured_Information").update(insured_information.model_dump()).eq("id", insured_id).execute()
    
    def update_other_insurance_information(self, other_insurance_id: int, other_insurance_information: OtherInsuranceInformationBase):
        """Update other insurance information."""
        return self.supabase.from_("Other_Insurance_Information").update(other_insurance_information.model_dump()).eq("id", other_insurance_id).execute()

    def update_attestation(self, attestation_id: int, attestation: AttestationBase):
        """Update an attestation."""
        return self.supabase.from_("Attestation").update(attestation.model_dump()).eq("id", attestation_id).execute()

    # DELETE Statements
    
    def delete_patient_information(self, patient_id: int):
        """Delete a patient information."""
        return self.supabase.from_("Patient_Information").delete().eq("id", patient_id).execute()

    def delete_insured_information(self, insured_id: int):
        """ Delete an insured information """
        return self.supabase.from_("Insured_Information").delete().eq("id", insured_id).execute()

    def delete_other_insurance_information(self, other_insurance_id: int):
        """ Delete other insurance information """
        return self.supabase.from_("Other_Insurance_Information").delete().eq("id", other_insurance_id).execute()

    def delete_attestation(self, attestation_id: int):
        """ Delete an attestation """
        return self.supabase.from_("Attestation").delete().eq("id", attestation_id).execute()

    