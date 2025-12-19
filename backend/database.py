import os
from supabase import create_client, Client
from dotenv import load_dotenv
from schemas import PatientInformationBase, InsuredInformationBase, OtherInsuranceInformationBase, AttestationBase

load_dotenv(override=True)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class Database:
    """ Database class """
    def __init__(self):
        self.supabase = supabase

    def create_patient_information(self, patient_information: PatientInformationBase):
      """ Create a new patient information """
      return self.supabase.from_("Patient_Information").insert(patient_information.model_dump()).execute()

    """ INSERT Statements"""

    def create_insured_information(self, insured_information: InsuredInformationBase):
      """ Create a new insured information """
      return self.supabase.from_("Insured_Information").insert(insured_information.model_dump()).execute()

    def create_other_insurance_information(self, other_insurance_information: OtherInsuranceInformationBase):
      """ Create a new other insurance information """
      return self.supabase.from_("Other_Insurance_Information").insert(other_insurance_information.model_dump()).execute()
    
    def create_attestation(self, attestation: AttestationBase):
      """ Create a new attestation """
      return self.supabase.from_("Attestation").insert(attestation.model_dump()).execute()

    def get_patient_information(self, patient_id: int):
      """ Get a patient information by id """
      return self.supabase.from_("patient_information").select("*").eq("id", patient_id).execute()

    def get_insured_information(self, insured_id: int):
      """ Get an insured information by id """
      return self.supabase.from_("Insured_Information").select("*").eq("id", insured_id).execute()

    def get_other_insurance_information(self, other_insurance_id: int):
      """ Get other insurance information by id """
      return self.supabase.from_("Insured_Information").select("*").eq("id", other_insurance_id).execute()

    def get_attestation(self, attestation_id: int):
      """ Get an attestation by id """
      return self.supabase.from_("Attestation").select("*").eq("id", attestation_id).execute()

    def update_patient_information(self, patient_id: int, patient_information: PatientInformationBase):
      """ Update a patient information """
      return self.supabase.from_("Patient_Information").update(patient_information.model_dump()).eq("id", patient_id).execute()

    def update_insured_information(self, insured_id: int, insured_information: InsuredInformationBase):
      """ Update an insured information """
      return self.supabase.from_("Insured_Information").update(insured_information.model_dump()).eq("id", insured_id).execute()
    
    def update_other_insurance_information(self, other_insurance_id: int, other_insurance_information: OtherInsuranceInformationBase):
      """ Update other insurance information """
      return self.supabase.from_("Other_Insurance_Information").update(other_insurance_information.model_dump()).eq("id", other_insurance_id).execute()

    def update_attestation(self, attestation_id: int, attestation: AttestationBase):
      """ Update an attestation """
      return self.supabase.from_("Attestation").update(attestation.model_dump()).eq("id", attestation_id).execute()
    
    def delete_patient_information(self, patient_id: int):
      """ Delete a patient information """
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

