from __future__ import annotations

import os
import re
from typing import Any, Dict, Optional, Tuple, Union

from dotenv import load_dotenv
from supabase import Client, create_client

from schemas import (
    AttestationBase,
    ExtractPayload,
    ExtractResultsFile,
    InsuredInformationBase,
    MigrationResult,
    OtherInsuranceInformationBase,
    PatientInformationBase,
)

load_dotenv(override=True)

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

    # ----------------------------
    # Extract-results migration
    # ----------------------------

    def migrate_extract_results(
        self,
        extract_results: Union[ExtractResultsFile, Dict[str, Any]],
        *,
        dry_run: bool = False,
    ) -> MigrationResult:
        """
        Migrate a LandingAI extract-results.json payload into Supabase.

        Accepts either:
        - a parsed `ExtractResultsFile`
        - a raw dict that matches the file shape
        """
        model = extract_results if isinstance(extract_results, ExtractResultsFile) else ExtractResultsFile.model_validate(extract_results)
        extraction = model.extraction or ExtractPayload()
        return self.migrate_extraction(extraction, dry_run=dry_run)

    def migrate_extraction(
        self,
        extraction: Union[ExtractPayload, Dict[str, Any]],
        *,
        dry_run: bool = False,
    ) -> MigrationResult:
        """
        Migrate the nested `extraction` object (insured/patient/otherInsurance/attestation) into Supabase.
        """
        ex = extraction if isinstance(extraction, ExtractPayload) else ExtractPayload.model_validate(extraction)

        insured_src = (ex.insuredInformation.model_dump() if ex.insuredInformation else {})
        patient_src = (ex.patientInformation.model_dump() if ex.patientInformation else {})
        other_src = (ex.otherInsuranceInformation.model_dump() if ex.otherInsuranceInformation else {})
        attest_src = (ex.attestation.model_dump() if ex.attestation else {})

        payloads: Dict[str, Any] = {}

        insured_payload: Dict[str, Any] = {
            "last_name": self._clean_str(insured_src.get("lastName")),
            "first_name": self._clean_str(insured_src.get("firstName")),
            "middle_initial": self._clean_str(insured_src.get("MI")),
            "date_of_birth": self._clean_str(insured_src.get("dateOfBirth")),
            "identification_number": self._parse_int(insured_src.get("identificationNumber")),
            "gender": self._clean_str(insured_src.get("Sex") or insured_src.get("sex")),
            "address": self._clean_str(insured_src.get("address")),
            "city": self._clean_str(insured_src.get("city")),
            "state": self._clean_str(insured_src.get("state")),
            "zip": self._clean_str(insured_src.get("zip")),
            "phone": self._clean_str(insured_src.get("telephone")),
            "employer_name": self._clean_str(insured_src.get("employerName")),
            "insurance_plan_name": self._clean_str(insured_src.get("insurancePlanName")),
            "another_insurance_plan": insured_src.get("anotherInsurancePlan"),
            "other_identification_number": self._parse_int(insured_src.get("otherIdentificationNumber")),
        }
        insured_id, insured_used = self._insert_with_unknown_column_retry(
            "Insured_Information", insured_payload, dry_run=dry_run
        )
        payloads["Insured_Information"] = insured_used

        relationship = self._clean_str(patient_src.get("relationshipToInsured"))
        patient_is_insured = (relationship or "").lower() == "self"

        def _p(field: str) -> Optional[str]:
            return self._clean_str(patient_src.get(field))

        patient_payload: Dict[str, Any] = {
            "insured_id": insured_id,
            "patient_last_name": _p("patientLastName")
            or (self._clean_str(insured_src.get("lastName")) if patient_is_insured else None),
            "patient_first_name": _p("patientFirstName")
            or (self._clean_str(insured_src.get("firstName")) if patient_is_insured else None),
            "patient_middle_initial": _p("patientMI")
            or (self._clean_str(insured_src.get("MI")) if patient_is_insured else None),
            "patient_date_of_birth": _p("patientDateOfBirth")
            or (self._clean_str(insured_src.get("dateOfBirth")) if patient_is_insured else None),
            "patient_gender": _p("patientSex")
            or (self._clean_str(insured_src.get("Sex") or insured_src.get("sex")) if patient_is_insured else None),
            "patient_address": _p("patientAddress")
            or (self._clean_str(insured_src.get("address")) if patient_is_insured else None),
            "patient_city": _p("patientCity")
            or (self._clean_str(insured_src.get("city")) if patient_is_insured else None),
            "patient_state": _p("patientState")
            or (self._clean_str(insured_src.get("state")) if patient_is_insured else None),
            "patient_zip": _p("patientZip")
            or (self._clean_str(insured_src.get("zip")) if patient_is_insured else None),
            "patient_phone": _p("patientTelephone")
            or (self._clean_str(insured_src.get("telephone")) if patient_is_insured else None),
            "status": self._clean_str(patient_src.get("status")),
            "relationship_to_insured": relationship,
            "condition_related_to_employment": self._clean_str(patient_src.get("conditionRelatedToEmployment")),
            "condition_related_to_auto_accident": self._clean_str(patient_src.get("conditionRelatedToAutoAccident")),
            "date_of_current_illness": self._clean_str(patient_src.get("dateOfCurrentIllness")),
            "condition_related_to_other": self._clean_str(patient_src.get("conditionRelatedToOther")),
            "auto_accident_place": self._clean_str(patient_src.get("autoAccidentPlace")),
        }
        patient_id, patient_used = self._insert_with_unknown_column_retry(
            "Patient_Information", patient_payload, dry_run=dry_run
        )
        payloads["Patient_Information"] = patient_used

        other_insurance_id: Optional[int] = None
        if not self._is_effectively_empty(other_src):
            other_payload: Dict[str, Any] = {
                "insured_id": insured_id,
                "policy_holder_insurance_last_name": self._clean_str(other_src.get("policyHolderLastName")),
                "policy_holder_insurance_first_name": self._clean_str(other_src.get("policyHolderFirstName")),
                "policy_holder_insurance_middle_initial": self._clean_str(other_src.get("policyHolderMI")),
                "policy_holder_insurance_date_of_birth": self._clean_str(other_src.get("dateOfBirth")),
                "policy_holder_identification_number": self._parse_int(other_src.get("identificationNumber")),
                "policy_holder_insurance_plan_name": self._clean_str(other_src.get("insurancePlanName")),
                "policy_holder_insurance_gender": self._clean_str(other_src.get("policyHolderSex")),
                "policy_holder_telephone_number": self._clean_str(other_src.get("policyHolderTelephone")),
                "policy_holder_employer_name": self._clean_str(other_src.get("policyHolderEmployerName")),
            }
            other_insurance_id, other_used = self._insert_with_unknown_column_retry(
                "Other_Insurance_Information", other_payload, dry_run=dry_run
            )
            payloads["Other_Insurance_Information"] = other_used

        attestation_payload: Dict[str, Any] = {
            "insured_id": insured_id,
            "patient_id": patient_id,
            "date_patient": self._clean_str(attest_src.get("dateOfPatient")),
            "provider_name": self._clean_str(attest_src.get("providerName")),
            "tax_number": self._parse_int(attest_src.get("taxNumber")),
            "NPI_number": self._parse_int(attest_src.get("NPINumber")),
            "date_of_insured": self._clean_str(attest_src.get("dateOfInsured")),
        }
        attestation_id, attestation_used = self._insert_with_unknown_column_retry(
            "Attestation", attestation_payload, dry_run=dry_run
        )
        payloads["Attestation"] = attestation_used

        return MigrationResult(
            insured_id=insured_id,
            patient_id=patient_id,
            other_insurance_id=other_insurance_id,
            attestation_id=attestation_id,
            dry_run=dry_run,
            payloads=payloads if dry_run else None,
        )

