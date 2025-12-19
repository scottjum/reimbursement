import os
from supabase import create_client, Client
from dotenv import load_dotenv
from schemas import PatientInformationBase, InsuredInformationBase, OtherInsuranceInformationBase, AttestationBase

load_dotenv(override=True)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def create_patient_information(patient_information: PatientInformationBase):
    """ Create a new patient information """
    return supabase.from_("patient_information").insert(patient_information.model_dump()).execute()

def create_insured_information(insured_information: InsuredInformationBase):
    """ Create a new insured information """
    return supabase.from_("insured_information").insert(insured_information.model_dump()).execute()

def create_other_insurance_information(other_insurance_information: OtherInsuranceInformationBase):
    """ Create a new other insurance information """
    return supabase.from_("other_insurance_information").insert(other_insurance_information.model_dump()).execute()

def create_attestation(attestation: AttestationBase):
    """ Create a new attestation """
    return supabase.from_("attestation").insert(attestation.model_dump()).execute()

def get_patient_information(patient_id: int):
    """ Get a patient information by id """
    return supabase.from_("patient_information").select("*").eq("id", patient_id).execute()

def get_insured_information(insured_id: int):
    """ Get an insured information by id """
    return supabase.from_("insured_information").select("*").eq("id", insured_id).execute()

def get_other_insurance_information(other_insurance_id: int):
    """ Get other insurance information by id """
    return supabase.from_("other_insurance_information").select("*").eq("id", other_insurance_id).execute()

def get_attestation(attestation_id: int):
    """ Get an attestation by id """
    return supabase.from_("attestation").select("*").eq("id", attestation_id).execute()

def update_patient_information(patient_id: int, patient_information: PatientInformationBase):
    """ Update a patient information """
    return supabase.from_("patient_information").update(patient_information.model_dump()).eq("id", patient_id).execute()

def update_insured_information(insured_id: int, insured_information: InsuredInformationBase):
    """ Update an insured information """
    return supabase.from_("insured_information").update(insured_information.model_dump()).eq("id", insured_id).execute()

def update_other_insurance_information(other_insurance_id: int, 
other_insurance_information: OtherInsuranceInformationBase):
    """ Update other insurance information """
    return supabase.from_("other_insurance_information").update(other_insurance_information.model_dump()).eq("id", other_insurance_id).execute()

def update_attestation(attestation_id: int, attestation: AttestationBase):
    """ Update an attestation """
    return supabase.from_("attestation").update(attestation.model_dump()).eq("id", attestation_id).execute()

def delete_patient_information(patient_id: int):
    """ Delete a patient information """
    return supabase.from_("patient_information").delete().eq("id", patient_id).execute()

def delete_insured_information(insured_id: int):
    """ Delete an insured information """
    return supabase.from_("insured_information").delete().eq("id", insured_id).execute()

def delete_other_insurance_information(other_insurance_id: int):
    """ Delete other insurance information """
    return supabase.from_("other_insurance_information").delete().eq("id", other_insurance_id).execute()

def delete_attestation(attestation_id: int):
    """ Delete an attestation """
    return supabase.from_("attestation").delete().eq("id", attestation_id).execute()

def get_all_patient_information():
    """ Get all patient information """
    return supabase.from_("patient_information").select("*").execute()

def get_all_insured_information():
    """ Get all insured information """
    return supabase.from_("insured_information").select("*").execute()

def get_all_other_insurance_information():
    """ Get all other insurance information """
    return supabase.from_("other_insurance_information").select("*").execute()

def get_all_attestation():
    """ Get all attestation """
    return supabase.from_("attestation").select("*").execute()

def get_all_patient_information_by_insured_id(insured_id: int):
    """ Get all patient information by insured id """
    return supabase.from_("patient_information").select("*").eq("insured_id", insured_id).execute()

def get_all_insured_information_by_patient_id(patient_id: int):
    """ Get all insured information by patient id """
    return supabase.from_("insured_information").select("*").eq("patient_id", patient_id).execute()

def get_all_other_insurance_information_by_insured_id(insured_id: int):
    """ Get all other insurance information by insured id """
    return supabase.from_("other_insurance_information").select("*").eq("insured_id", insured_id).execute()

def get_all_attestation_by_patient_id(patient_id: int):
    """ Get all attestation by patient id """
    return supabase.from_("attestation").select("*").eq("patient_id", patient_id).execute()

def get_all_attestation_by_insured_id(insured_id: int):
    """ Get all attestation by insured id """
    return supabase.from_("attestation").select("*").eq("insured_id", insured_id).execute()

def get_all_patient_information_by_patient_last_name(patient_last_name: str):
    """ Get all patient information by patient last name """
    return supabase.from_("patient_information").select("*").eq("patient_last_name", patient_last_name).execute()

def get_all_insured_information_by_last_name(last_name: str):
    """ Get all insured information by last name """
    return supabase.from_("insured_information").select("*").eq("last_name", last_name).execute()

def get_all_other_insurance_information_by_policy_holder_insurance_last_name(policy_holder_insurance_last_name: str):
    """ Get all other insurance information by policy holder insurance last name """
    return supabase.from_("other_insurance_information").select("*").eq("policy_holder_insurance_last_name", policy_holder_insurance_last_name).execute()

def get_all_attestation_by_date_patient(date_patient: str):
    """ Get all attestation by date patient """
    return supabase.from_("attestation").select("*").eq("date_patient", date_patient).execute()

def get_all_attestation_by_provider_name(provider_name: str):
    """ Get all attestation by provider name """
    return supabase.from_("attestation").select("*").eq("provider_name", provider_name).execute()

def get_all_attestation_by_tax_number(tax_number: int):
    """ Get all attestation by tax number """
    return supabase.from_("attestation").select("*").eq("tax_number", tax_number).execute()

def get_all_attestation_by_npi_number(npi_number: int):
    """ Get all attestation by NPI number """
    return supabase.from_("attestation").select("*").eq("NPI_number", npi_number).execute()

def get_all_attestation_by_date_of_insured(date_of_insured: str):
    """ Get all attestation by date of insured """
    return supabase.from_("attestation").select("*").eq("date_of_insured", date_of_insured).execute()

