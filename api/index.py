import sys
import os
from mangum import Mangum

# Import the FastAPI app from the current directory
from main import app

# Create the Vercel handler using Mangum
handler = Mangum(app, lifespan="off")
