import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file in current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
