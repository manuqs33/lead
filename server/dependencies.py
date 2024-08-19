from fastapi import APIRouter
from services import DegreesService, SubjectsService, LeadsService
from controllers import LeadController

router = APIRouter()


degrees_service = DegreesService()
subjects_service = SubjectsService()
leads_service = LeadsService(
    degrees_service=degrees_service, subjects_service=subjects_service)
lead_controller = LeadController(router, leads_service)
