"""
main.py

The main entry point for the HackLens backend application.
It loads environment variables, initializes the FastAPI application, sets up CORS middleware,
and mounts all available API routers.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="HackLens API",
    description="A lightweight AI-powered backend system to review and evaluate CS-related content.",
    version="1.0.0"
)

# Set up CORS middleware to support potential frontend interfaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed in production settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes under the standard v1 prefix
app.include_router(analyze_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint serving as a simple health check.
    """
    return {
        "status": "online",
        "service": "HackLens Backend API",
        "version": "1.0.0"
    }
