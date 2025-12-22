""" Database class """
from __future__ import annotations

import os
from typing import Any, Optional

from dotenv import load_dotenv
from supabase import Client, create_client
from sqlmodel import Field, SQLModel


load_dotenv(override=True)
    
class InsuredInformationBase(SQLModel):
    """ Insured Information """
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
    another_insurance_plan: bool = Field(default=False, description="Indicates whether the insured has another insurance plan.")
    other_identification_number: Optional[int] = Field(default=None, description="The insured's other identification number.")

class PatientInformationBase(SQLModel):
    """ Patient Information """
    insured_id: Optional[int] = Field(default=None, description="Foreign key reference to the insured record, if present.")
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
    attestation_id: Optional[int] = Field(default=None, description="Foreign key reference to the attestation record.")

class OtherInsuranceInformationBase(SQLModel):
    """ Other Insurance Information """
    policy_holder_insurance_last_name: str = Field(..., description="The other insurance information's policy holder insurance last name.")
    policy_holder_insurance_first_name: str = Field(..., description="The other insurance information's policy holder insurance first name.")
    policy_holder_insurance_middle_initial: Optional[str] = Field(default=None, description="The other insurance information's policy holder insurance middle initial.")
    policy_holder_insurance_date_of_birth: str = Field(..., description="The other insurance information's policy holder insurance date of birth.")
    policy_holder_identification_number: int = Field(..., description="The other insurance information's policy holder insurance identification number.")
    policy_holder_insurance_plan_name: str = Field(..., description="The other insurance information's policy holder insurance plan name.")
    policy_holder_insurance_gender: str = Field(..., description="The other insurance information's policy holder insurance gender.")
    policy_holder_phone_number: str = Field(..., description="The other insurance information's policy holder insurance telephone number.")
    policy_holder_employer_name: Optional[str] = Field(default=None, description="The other insurance information's policy holder insurance employer name.")

class AttestationBase(SQLModel):
    """ Attestation """
    date_of_patient_signed: str = Field(..., description="The attestation's date of patient signed.")
    provider_name: str = Field(..., description="The attestation's provider name.")
    tax_number: int = Field(..., description="The attestation's tax number.")
    npi_number: int = Field(..., description="The attestation's NPI number.")
    date_of_insured_signed: str = Field(..., description="The attestation's date of insured signed.")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class Database:
    """ Database class """
    def __init__(self):
        self.supabase = supabase

    def _to_insert_payload(self, obj: Any) -> Any:
        """
        Normalize a SQLModel/Pydantic model into a plain dict for Supabase inserts.
        LandingAI extraction may already return dicts, so we keep those as-is.
        """
        if hasattr(obj, "model_dump"):
            return obj.model_dump(exclude_none=True)
        if hasattr(obj, "dict"):
            return obj.dict(exclude_none=True)  # pragma: no cover (pydantic v1 fallback)
        return obj
    
     # INSERT Statements
    def create_other_insurance_information(self, other_insurance_information: OtherInsuranceInformationBase):
        """Create a new other insurance information."""
        return self.supabase.from_("Other_Insurance_Information").insert(self._to_insert_payload(other_insurance_information)).execute()
    
    def create_attestation(self, attestation: AttestationBase):
        """Create a new attestation."""
        return self.supabase.from_("Attestation").insert(self._to_insert_payload(attestation)).execute()

    def create_insured_information(self, insured_information: InsuredInformationBase, other_insurance_id: Optional[int] = None):
        """Create a new insured information."""
        insured_information["other_identification_number"] = other_insurance_id
        return self.supabase.from_("Insured_Information").insert(self._to_insert_payload(insured_information)).execute()

    def create_patient_information(self, patient_information: PatientInformationBase, insured_id: int, attestation_id: int):
        """Create a new patient information."""
        patient_information["insured_id"] = insured_id
        patient_information["attestation_id"] = attestation_id
        return self.supabase.from_("Patient_Information").insert(self._to_insert_payload(patient_information)).execute()

    # SELECT Statements
    def get_all_patient_information(self):
        """ Get all patient information """
        return self.supabase.from_("Patient_Information").select("*").execute()

    def get_patient_information(self, patient_id: int):
        """Get a patient information by id."""
        return self.supabase.from_("Patient_Information").select("*").eq("id", patient_id).execute()
    
    def get_all_patient_information_by_patient_last_name(self, patient_last_name: str):
        """ Get all patient information by patient last name """
        return self.supabase.from_("Patient_Information").select("*").eq("patient_last_name", patient_last_name).execute()
    
    def get_all_patient_information_by_insured_id(self, insured_id: int):
        """ Get all patient information by insured id """
        return self.supabase.from_("Patient_Information").select("*").eq("insured_id", insured_id).execute()
    
    def get_all_insured_information(self):
        """ Get all insured information """
        return self.supabase.from_("Insured_Information").select("*").execute()
    
    def get_insured_information(self, insured_id: int):
        """Get an insured information by id."""
        return self.supabase.from_("Insured_Information").select("*").eq("id", insured_id).execute()
    
    def get_all_insured_information_by_last_name(self, last_name: str):
        """ Get all insured information by last name """
        return self.supabase.from_("Insured_Information").select("*").eq("last_name", last_name).execute()
    
    def get_all_insured_information_by_other_insurance_id(self, other_insurance_id: int):
        """ Get all insured information by other insurance id """
        return self.supabase.from_("Insured_Information").select("*").eq("other_identification_number", other_insurance_id).execute()
    
    def get_all_other_insurance_information(self):
        """ Get all other insurance information """
        return self.supabase.from_("Other_Insurance_Information").select("*").execute()
    
    def get_other_insurance_information(self, other_insurance_id: int):
        """Get other insurance information by id."""
        return self.supabase.from_("Other_Insurance_Information").select("*").eq("id", other_insurance_id).execute()
    
    def get_all_other_insurance_information_by_policy_holder_last_name(self, policy_holder_last_name: str):
        """ Get all other insurance information by policy holder insurance last name """
        return self.supabase.from_("Other_Insurance_Information").select("*").eq("policy_holder_last_name", policy_holder_last_name).execute()
    
    def get_all_attestation(self):
        """ Get all attestation """
        return self.supabase.from_("Attestation").select("*").execute()
    
    def get_attestation(self, attestation_id: int):
        """Get an attestation by id."""
        return self.supabase.from_("Attestation").select("*").eq("id", attestation_id).execute()

    # UPDATE Statements

    def update_patient_information(self, patient_id: int, patient_information: PatientInformationBase):
        """Update a patient information."""
        return self.supabase.from_("Patient_Information").update(patient_information).eq("id", patient_id).execute()

    def update_insured_information(self, insured_id: int, insured_information: InsuredInformationBase):
        """Update an insured information."""
        return self.supabase.from_("Insured_Information").update(insured_information).eq("id", insured_id).execute()
    
    def update_other_insurance_information(self, other_insurance_id: int, other_insurance_information: OtherInsuranceInformationBase):
        """Update other insurance information."""
        return self.supabase.from_("Other_Insurance_Information").update(other_insurance_information).eq("id", other_insurance_id).execute()

    def update_attestation(self, attestation_id: int, attestation: AttestationBase):
        """Update an attestation."""
        return self.supabase.from_("Attestation").update(attestation).eq("id", attestation_id).execute()

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

    