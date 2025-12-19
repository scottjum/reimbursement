from typing import Optional, Annotated
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
    
