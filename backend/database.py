import os
from supabase import create_client, Client
from dotenv import load_dotenv
from schemas import *

load_dotenv(override=True)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

AttestationTable = Table(
    name="attestations",
    schema=AttestationBase,
)
PatientInformationTable = Table(
    name="patient_information",
    schema=PatientInformationBase,
)
InsuredInformationTable = Table(
    name="insured_information",
    schema=InsuredInformationBase,
)
OtherInsuranceInformationTable = Table(
    name="other_insurance_information",
    schema=OtherInsuranceInformationBase,
)

def create_attestation(attestation: AttestationCreate) -> AttestationRead:
    return AttestationTable.create(attestation)

def create_patient_information(patient_information: PatientInformationCreate) -> PatientInformationRead:
    return PatientInformationTable.create(patient_information)

def create_insured_information(insured_information: InsuredInformationCreate) -> InsuredInformationRead:
    return InsuredInformationTable.create(insured_information)

def create_other_insurance_information(other_insurance_information: OtherInsuranceInformationCreate) -> OtherInsuranceInformationRead: