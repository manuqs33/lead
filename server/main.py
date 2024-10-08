from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Degree, Lead, LeadDegree, LeadSubject, Subject
import database
from dependencies import router as leads_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", database.create_metadata)
app.include_router(leads_router, prefix="/api")