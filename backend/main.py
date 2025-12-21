""" Main file for the FastAPI backend """
import os
from io import BytesIO
import logging
import traceback
from pathlib import Path
from tempfile import NamedTemporaryFile
import json

from typing import Optional

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from landingai_ade import LandingAIADE
from landingai_ade.lib import pydantic_to_json_schema
from database import (Database, InsuredInformationBase, 
PatientInformationBase, OtherInsuranceInformationBase, AttestationBase
)

load_dotenv(override=True)

database = Database()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory storage for uploaded documents
# In a production environment, you might want to use a database or session storage
uploaded_documents = {}  # Key: session_id (or 'default'), Value: document_content

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile):
    """
    Upload and process a document file.
    Supports PDF, DOCX, and TXT files.
    """
    temp_file_path = None
    try:
        if not file.filename:
            logger.error("No filename provided in upload request")
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Debug: Check API key
        api_key = os.getenv("VISION_AGENT_API_KEY")
        if api_key:
            logger.debug("API key found: %s... length: %s", api_key[:10], (len(api_key)))
        else:
            logger.error("VISION_AGENT_API_KEY environment variable not set")
            raise HTTPException(
                status_code=500, 
                detail="VISION_AGENT_API_KEY environment variable not configured"
            )
    
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size == 0:
            logger.error("Uploaded file is empty")
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        with NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        try:
            client = LandingAIADE(apikey=api_key)
        except Exception as e:
            logger.error("Failed to initialize LandingAIADE client: %s", str(e))
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize document parser: {str(e)}"
            ) from e
        
        try:
            parse_response = client.parse(document=Path(temp_file_path))
            
            if not hasattr(parse_response, 'markdown'):
                logger.error("Response object missing 'markdown' attribute. Available attributes: %s", dir(parse_response))
                raise HTTPException(
                    status_code=500,
                    detail="Parser response missing expected 'markdown' attribute"
                )
            
            markdown_content = parse_response.markdown
            # Store the document content in memory for later use in chat requests
            # Using 'default' as the key - in production, you might want to use session IDs
            uploaded_documents['default'] = markdown_content

            # Build a single extraction schema that includes ALL sections we want LandingAI to extract.
            # This mirrors the pattern in `backend/extract.py` (a top-level model with nested sections).
            class ClaimFormExtractionSchema(BaseModel):
                """ Claim Form Extraction Schema """
                insuredInformation: InsuredInformationBase = Field(..., description="The insured information.")
                patientInformation: PatientInformationBase = Field(..., description="The patient information.")
                otherInsuranceInformation: Optional[OtherInsuranceInformationBase] = Field(..., description="The other insurance information.")
                attestation: AttestationBase = Field(..., description="The attestation.")

            schema = pydantic_to_json_schema(ClaimFormExtractionSchema)
            extract_response = client.extract(schema=schema, markdown=BytesIO(markdown_content.encode('utf-8')))

            # Add extract response to the database
            database.create_insured_information(extract_response.insuredInformation)
            database.create_patient_information(extract_response.patientInformation)
            database.create_other_insurance_information(extract_response.otherInsuranceInformation)
            database.create_attestation(extract_response.attestation)


        except Exception as e:
            logger.error("Failed to parse document: %s", str(e))
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse document: {str(e)}"
            ) from e

        return {"message": "Document uploaded successfully"}

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error("Unexpected error in upload route: %s", str(e))
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}. Check server logs for details."
        ) from e
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError as e:
                logger.warning("Failed to delete temporary file %s: %s", temp_file_path, str(e))

@app.get("/database/patient_information")
async def get_all_patient_information():
    """ Get all patient information """
    return database.get_all_patient_information()

@app.get("/database/insured_information")
async def get_all_insured_information():
    """ Get all insured information """
    return database.get_all_insured_information()

@app.get("/database/other_insurance_information")
async def get_all_other_insurance_information():
    """ Get all other insurance information """
    return database.get_all_other_insurance_information()

@app.get("/database/attestation")
async def get_all_attestation():
    """ Get all attestation """
    return database.get_all_attestation()

@app.get("/database/patient_information/{patient_id}")
async def get_patient_information(patient_id: int):
    """ Get patient information by id """
    return database.get_patient_information(patient_id)

@app.get("/database/insured_information/{insured_id}")
async def get_insured_information(insured_id: int):
    """ Get insured information by id """
    return database.get_insured_information(insured_id)

@app.get("/database/other_insurance_information/{other_insurance_id}")
async def get_other_insurance_information(other_insurance_id: int):
    """ Get other insurance information by id """
    return database.get_other_insurance_information(other_insurance_id)

@app.get("/database/attestation/{attestation_id}")
async def get_attestation(attestation_id: int):
    """ Get attestation by id """
    return database.get_attestation(attestation_id)

@app.get("/database/patient_information/insured_id/{insured_id}")
async def get_all_patient_information_by_insured_id(insured_id: int):
    """ Get all patient information by insured id """
    return database.get_all_patient_information_by_insured_id(insured_id)

@app.get("/database/insured_information/patient_id/{patient_id}")
async def get_all_insured_information_by_patient_id(patient_id: int):
    """ Get all insured information by patient id """
    return database.get_all_insured_information_by_patient_id(patient_id)

@app.get("/database/other_insurance_information/insured_id/{insured_id}")
async def get_all_other_insurance_information_by_insured_id(insured_id: int):
    """ Get all other insurance information by insured id """
    return database.get_all_other_insurance_information_by_insured_id(insured_id)

    """
    Same as /database/migrate_extract but accepts a JSON file upload.
    """
    try:
        raw_bytes = await file.read()
        if not raw_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        try:
            raw = json.loads(raw_bytes.decode("utf-8"))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}") from e
        payload = ExtractResultsFile.model_validate(raw)
        return database.migrate_extract_results(payload, dry_run=dry_run)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.get("/")
async def read_root():
    """ Read root """
    return {"message": "Hello, World!"}

@app.get("/health")
async def health_check():
    """ Health check """
    return {"status": "healthy", "service": "FastAPI Backend"}
