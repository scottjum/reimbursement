import os
from supabase import create_client, Client
from dotenv import load_dotenv
from schemas import *

load_dotenv(override=True)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

