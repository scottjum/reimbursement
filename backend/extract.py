import os
from io import BytesIO
from pathlib import Path

from landingai_ade import LandingAIADE
from landingai_ade.lib import pydantic_to_json_schema

from pydantic import BaseModel, Field
class InsuredInformation(BaseModel):
    lastName: str = Field(
        ..., description="The insured individual's last name.", title='Last Name'
    )
    firstName: str = Field(
        ..., description="The insured individual's first name.", title='First Name'
    )
    dateOfBirth: str = Field(
        ...,
        description="The insured individual's date of birth in MM/DD/YYYY format.",
        title='Date of Birth',
    )
    identificationNumber: str = Field(
        ...,
        description="The insured individual's identification number.",
        title='Identification Number',
    )
    address: str = Field(
        ..., description="The insured individual's street address.", title='Address'
    )
    MI: str = Field(..., description="The insured individual's middle initial.")
    city: str = Field(..., description="The insured individual's city.")
    state: str = Field(..., description="The insured individual's state.")
    zip: str = Field(..., description="The insured individual's zip code.")
    telephone: str = Field(..., description="The insured individual's telephone.")
    employerName: str = Field(..., description="The insured individual's employer.")
    insurancePlanName: str = Field(
        ..., description="The insured individual's insurance plan name."
    )
    anotherInsurancePlan: bool = Field(
        ...,
        description='Is there another insurance plan for the insured in Y/N format.',
    )
    Sex: str = Field(..., description='Sex of the insured.')
class PatientInformation(BaseModel):
    relationshipToInsured: str = Field(
        ...,
        description="The patient's relationship to the insured (e.g., Self, Spouse/DP, Child, Other).",
        title='Relationship to Insured',
    )
    status: str = Field(
        ...,
        description="The patient's marital and employment/student status.",
        title="Patient's Status",
    )
    conditionRelatedToEmployment: str = Field(
        ...,
        description="Indicates if the patient's condition is related to employment.",
        title='Condition Related to Employment',
    )
    conditionRelatedToAutoAccident: str = Field(
        ...,
        description="Indicates if the patient's condition is related to an auto accident.",
        title='Condition Related to Auto Accident',
    )
    dateOfCurrentIllness: str = Field(
        ...,
        description='The date of the current illness, injury, or pregnancy (LMP) in MM/DD/YYYY format.',
        title='Date of Current Illness',
    )
    conditionRelatedToOther: str = Field(
        ...,
        description="Indicates if the patient's condition is related to other accident.",
    )
    autoAccidentPlace: str = Field(
        ..., description='The state in which the auto accident occurred.'
    )
    patientLastName: str = Field(..., description="The patient's last name.")
    patientFirstName: str = Field(..., description="The patient's first name.")
    patientMI: str = Field(..., description="The patient's middle initial.")
    patientDateOfBirth: str = Field(
        ..., description='Date of birth of the patient in MM/DD/YYYY format.'
    )
    patientSex: str = Field(..., description='Sex of the patient.')
    patientTelephone: str = Field(..., description='The telephone of the patient.')
    patientAddress: str = Field(..., description='The street address of the patient.')
    patientCity: str = Field(..., description='The city of the patient.')
    patientState: str = Field(
        ..., description='The state in which the patient resides.'
    )
    patientZip: str = Field(..., description='The zip code of the patient.')
class OtherInsuranceInformation(BaseModel):
    policyHolderLastName: str = Field(
        ...,
        description='Last name of the other insurance policy holder.',
        title='Policy Holder Last Name',
    )
    policyHolderFirstName: str = Field(
        ...,
        description='First name of the other insurance policy holder.',
        title='Policy Holder First Name',
    )
    dateOfBirth: str = Field(
        ...,
        description='Date of birth of the other insurance policy holder in MM/DD/YYYY format.',
        title='Policy Holder Date of Birth',
    )
    identificationNumber: str = Field(
        ...,
        description='Identification number for the other insurance plan.',
        title='Other Insurance Identification Number',
    )
    insurancePlanName: str = Field(
        ...,
        description='Name of the other insurance plan or program.',
        title='Other Insurance Plan Name',
    )
    policyHolderMI: str = Field(
        ..., description='Middle Initial of the other insurance policy holder.'
    )
    policyHolderSex: str = Field(
        ..., description='Sex of other insurance policy holder.'
    )
    policyHolderTelephone: str = Field(
        ..., description='Telephone of other insurance policy holder.'
    )
    policyHolderEmployerName: str = Field(
        ..., description='Employer name of other policy holder.'
    )
class Attestation(BaseModel):
    dateOfPatient: str = Field(
        ...,
        description='Date the attestation was signed in MM/DD/YYYY format.',
        title='Date',
    )
    providerName: str = Field(
        ...,
        description='Name of the health care professional for assignment of benefits.',
        title='Provider Name',
    )
    taxNumber: str = Field(
        ..., description='Tax Number of the business of the health care professional.'
    )
    NPINumber: str = Field(
        ..., description='NPI number of the health care professional.'
    )
    dateOfInsured: str = Field(
        ..., description='Date the attestation was signed in MM/DD/YYYY format.'
    )
class HorizonMedicalHealthInsuranceClaimFormExtractionSchema(BaseModel):
    insuredInformation: InsuredInformation = Field(
        ...,
        description='Key identifying and contact information for the insured individual.',
        title="Insured's Information",
    )
    patientInformation: PatientInformation = Field(
        ...,
        description='Key identifying and contact information for the patient.',
        title="Patient's Information",
    )
    otherInsuranceInformation: OtherInsuranceInformation = Field(
        ...,
        description='Information about any other insurance plan relevant to the claim.',
        title='Other Insurance Information',
    )
    attestation: Attestation = Field(
        ...,
        description='Certification and authorization section, including signature and date.',
        title='Attestation',
    )

# Convert to JSON schema
schema = pydantic_to_json_schema(HorizonMedicalHealthInsuranceClaimFormExtractionSchema)

# Use with the SDK
client = LandingAIADE(
  # Put your API key in the environment variable VISION_AGENT_API_KEY
  apikey=os.environ.get("VISION_AGENT_API_KEY"),
)

parse_response = client.parse(
  document=Path("YOUR_PATH/TO/YOUR_PDF.pdf"),
  # The selected model defaults to its latest available version.
  # To specify an older version (e.g., 'model-name-date'), modify the model string.
  # Details on all supported model versions: [https://docs.landing.ai/ade/ade-parse-models#model-versions-and-snapshots]
  model="dpt-2",
)

extract_response = client.extract(
  schema=schema,
  markdown=BytesIO(parse_response.markdown.encode('utf-8')),
)

print(extract_response)