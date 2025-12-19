""" Schemas for the API """
from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel

class PatientInformationBase(SQLModel, table=True):
    """ Patient Information """
    id: Optional[int] = Field(default=None, primary_key=True)
    insured_id: Optional[int] = Field(default=None, foreign_key="insured_information.id")
    patient_last_name: str
    patient_first_name: str
    patient_middle_initial: Optional[str] = Field(default=None)
    patient_date_of_birth: str
    patient_gender: str
    patient_address: str
    patient_city: str
    patient_state: str
    patient_zip: str
    patient_phone: str
    status: Optional[str] = Field(default=None)
    relationship_to_insured: str
    condition_related_to_employment: Optional[str] = Field(default=None)
    condition_related_to_auto_accident: Optional[str] = Field(default=None)
    date_of_current_illness: str
    condition_related_to_other: Optional[str] = Field(default=None)
    auto_accident_place: Optional[str] = Field(default=None)
    

class InsuredInformationBase(SQLModel, table=True):
    """ Insured Information """
    id: Optional[int] = Field(default=None, primary_key=True)
    last_name: str
    first_name: str
    middle_initial: Optional[str] = Field(default=None)
    date_of_birth: str
    identification_number: int
    gender: str
    address: str
    city: str
    state: str
    zip: str
    phone: str
    employer_name: Optional[str] = Field(default=None)
    insurance_plan_name: str
    another_insurance_plan: bool = Field(default=False)
    other_identification_number: Optional[int] = Field(default=None)

class OtherInsuranceInformationBase(SQLModel, table=True):
    """ Other Insurance Information """
    id: Optional[int] = Field(default=None, primary_key=True)
    policy_holder_insurance_last_name: str
    policy_holder_insurance_first_name: str
    policy_holder_insurance_middle_initial: Optional[str] = Field(default=None)
    policy_holder_insurance_date_of_birth: str
    policy_holder_identification_number: int
    policy_holder_insurance_plan_name: str
    policy_holder_insurance_gender: str
    policy_holder_telephone_number: str
    policy_holder_employer_name: Optional[str] = Field(default=None)

class AttestationBase(SQLModel, table=True):
    """ Attestation """
    id: Optional[int] = Field(default=None, primary_key=True)
    date_patient: str
    provider_name: str
    tax_number: int
    NPI_number: int
    date_of_insured: str
    

# ----------------------------
# Incoming extract JSON schemas
# ----------------------------

class ExtractInsuredInformation(BaseModel):
    """ Extract json data from Insured Information """
    model_config = ConfigDict(extra="ignore")

    lastName: Optional[str] = None
    firstName: Optional[str] = None
    MI: Optional[str] = None
    dateOfBirth: Optional[str] = None
    identificationNumber: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    telephone: Optional[str] = None
    employerName: Optional[str] = None
    insurancePlanName: Optional[str] = None
    anotherInsurancePlan: Optional[bool] = None
    sex: Optional[str] = None
    otherIdentificationNumber: Optional[str] = None


class ExtractPatientInformation(BaseModel):
    """ Extract json data from Patient Information """
    model_config = ConfigDict(extra="ignore")

    relationshipToInsured: Optional[str] = None
    status: Optional[str] = None
    conditionRelatedToEmployment: Optional[str] = None
    conditionRelatedToAutoAccident: Optional[str] = None
    dateOfCurrentIllness: Optional[str] = None
    conditionRelatedToOther: Optional[str] = None
    autoAccidentPlace: Optional[str] = None

    patientLastName: Optional[str] = None
    patientFirstName: Optional[str] = None
    patientMI: Optional[str] = None
    patientDateOfBirth: Optional[str] = None
    patientSex: Optional[str] = None
    patientTelephone: Optional[str] = None
    patientAddress: Optional[str] = None
    patientCity: Optional[str] = None
    patientState: Optional[str] = None
    patientZip: Optional[str] = None


class ExtractOtherInsuranceInformation(BaseModel):
    """ Extract json data from Other Insurance Information """
    model_config = ConfigDict(extra="ignore")

    policyHolderLastName: Optional[str] = None
    policyHolderFirstName: Optional[str] = None
    policyHolderMI: Optional[str] = None
    dateOfBirth: Optional[str] = None
    identificationNumber: Optional[str] = None
    insurancePlanName: Optional[str] = None
    policyHolderSex: Optional[str] = None
    policyHolderTelephone: Optional[str] = None
    policyHolderEmployerName: Optional[str] = None


class ExtractAttestation(BaseModel):
    """ Extract json data from Attestation """   
    model_config = ConfigDict(extra="ignore")

    dateOfPatient: Optional[str] = None
    providerName: Optional[str] = None
    taxNumber: Optional[str] = None
    NPINumber: Optional[str] = None
    dateOfInsured: Optional[str] = None


class ExtractPayload(BaseModel):
    """
    Extracted data payload from LandingAI.
    This matches the nested object at `extract_results_json["extraction"]`.
    """

    model_config = ConfigDict(extra="ignore")

    insuredInformation: Optional[ExtractInsuredInformation] = None
    patientInformation: Optional[ExtractPatientInformation] = None
    otherInsuranceInformation: Optional[ExtractOtherInsuranceInformation] = None
    attestation: Optional[ExtractAttestation] = None


class ExtractResultsFile(BaseModel):
    """
    Full extract-results.json file shape (we ignore everything except `extraction`).
    """

    model_config = ConfigDict(extra="ignore")

    extraction: Optional[ExtractPayload] = None
    extraction_metadata: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class MigrationResult(BaseModel):
    """ Migration result """
    insured_id: Optional[int] = None
    patient_id: Optional[int] = None
    other_insurance_id: Optional[int] = None
    attestation_id: Optional[int] = None
    dry_run: bool = False
    payloads: Optional[Dict[str, Any]] = None

