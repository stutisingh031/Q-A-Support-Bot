# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# # Load environment variables from .env
# load_dotenv()

# # Initialize the OpenAI client
# # It automatically looks for OPENAI_API_KEY in your environment
# client = OpenAI()

# try:
#     # Fetch the list of models
#     models = client.models.list()
    
#     print("--- Models your key can access ---")
#     # Extract and sort model IDs for readability
#     model_ids = sorted([model.id for model in models.data])
    
#     for model_id in model_ids:
#         print(f"- {model_id}")

# except Exception as e:
#     print(f"Error: {e}")
import os
from dotenv import load_dotenv

load_dotenv()
print(f"DEBUG: API Key found in env: {os.getenv('OPENAI_API_KEY') }")