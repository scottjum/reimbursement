from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os   # environment variables
import logging
from tempfile import NamedTemporaryFile
from landingai_ade import LandingAIADE
import traceback
from pathlib import Path

load_dotenv(override=True)

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

class UploadResponse(BaseModel):
    content: str
    filename: str

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile):
    """
    Upload and process a document file.
    Supports PDF, DOCX, and TXT files.
    """
    temp_file_path = None
    try:
        # Debug: Log incoming request
        logger.debug("=" * 50)
        logger.debug("UPLOAD ROUTE CALLED")
        logger.debug("=" * 50)
        
        # Debug: Check filename
        logger.debug(f"Filename: {file.filename}")
        logger.debug(f"Content type: {file.content_type}")
        
        if not file.filename:
            logger.error("No filename provided in upload request")
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Debug: Check API key
        api_key = os.getenv("VISION_AGENT_API_KEY")
        if api_key:
            logger.debug(f"API key found: {api_key[:10]}... (length: {len(api_key)})")
        else:
            logger.error("VISION_AGENT_API_KEY environment variable not set")
            raise HTTPException(
                status_code=500, 
                detail="VISION_AGENT_API_KEY environment variable not configured"
            )
        
        # Debug: Read file content
        logger.debug("Reading file content...")
        file_content = await file.read()
        file_size = len(file_content)
        logger.debug(f"File size: {file_size} bytes")
        
        if file_size == 0:
            logger.error("Uploaded file is empty")
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Debug: Save to temporary file
        logger.debug("Saving file to temporary location...")
        with NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
            logger.debug(f"Temporary file created: {temp_file_path}")

        # Debug: Initialize client
        logger.debug("Initializing LandingAIADE client...")
        try:
            client = LandingAIADE(apikey=api_key)
            logger.debug("Client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LandingAIADE client: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize document parser: {str(e)}"
            )
        
        # Debug: Parse document
        logger.debug(f"Parsing document from path: {temp_file_path}")
        try:
            response = client.parse(document=Path(temp_file_path))
            logger.debug("Document parsed successfully")
            logger.debug(f"Response type: {type(response)}")
            logger.debug(f"Response has markdown attribute: {hasattr(response, 'markdown')}")
            
            if not hasattr(response, 'markdown'):
                logger.error(f"Response object missing 'markdown' attribute. Available attributes: {dir(response)}")
                raise HTTPException(
                    status_code=500,
                    detail="Parser response missing expected 'markdown' attribute"
                )
            
            markdown_content = response.markdown
            logger.debug(f"Markdown content length: {len(markdown_content) if markdown_content else 0}")
            
        except Exception as e:
            logger.error(f"Failed to parse document: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse document: {str(e)}"
            )
        
        # Debug: Prepare response
        logger.debug("Preparing response...")
        
        # Store the document content in memory for later use in chat requests
        # Using 'default' as the key - in production, you might want to use session IDs
        uploaded_documents['default'] = markdown_content
        logger.debug(f"Stored document content in memory (length: {len(markdown_content) if markdown_content else 0})")
        
        result = UploadResponse(content=markdown_content, filename=file.filename)
        logger.debug("Upload route completed successfully")
        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error in upload route: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}. Check server logs for details."
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.debug(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_file_path}: {str(e)}")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
