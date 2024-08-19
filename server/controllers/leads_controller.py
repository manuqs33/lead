import traceback
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from dtos import CreateLeadDto, CreateLeadResponseDto, LeadResponseDto
from services import LeadsService
from database import get_session
import logging


class LeadController:
    def __init__(self, router: APIRouter, leads_service: LeadsService):
        self.router = router
        self.router.add_api_route(
            "/leads/", self.create_lead, methods=["POST"], response_model=CreateLeadResponseDto)
        self.router.add_api_route(
            "/leads/{lead_id}/", self.get_lead, methods=["GET"], response_model=LeadResponseDto)
        self.router.add_api_route(
            "/leads/", self.get_leads, methods=["GET"], response_model=List[LeadResponseDto])
        self.leads_service = leads_service
        self.logger = logging.getLogger(__name__)

    def create_lead(self, lead: CreateLeadDto, session: Session = Depends(get_session)):
        try:
            response = self.leads_service.create_leads_and_relations(lead, session)
            return response
        except HTTPException as e:
            self.logger.error(f"Request error: {e}", exc_info=True)
            raise e
        except Exception as e:
            self.logger.error(f"Server error: {e}", exc_info=True)
            raise HTTPException(
                status_code=500, detail="There was an error creating the lead")

    def get_lead(self, lead_id: int, session: Session = Depends(get_session)):
        try:
            lead = self.leads_service.get_lead(lead_id, session)
            if lead is None:
                raise HTTPException(status_code=404, detail="Lead not found")
            return lead
        except HTTPException as e:
            self.logger.error(f"Request error: {e}", exc_info=True)
            raise e
        except Exception as e:
            self.logger.error(f"Server error: {e}", exc_info=True)
            raise HTTPException(
                status_code=500, detail="There was an error creating the lead")

    def get_leads(
        self,
        limit: int = Query(10, description="Number of leads to return"),
        offset: int = Query(0, description="Number of leads to skip"),
        session: Session = Depends(get_session)
    ):
        try:
            leads = self.leads_service.get_leads(session, limit, offset)
            return leads
        except HTTPException as e:
            self.logger.error(f"Request error: {e}", exc_info=True)
            raise e
        except Exception as e:
            self.logger.error(f"Server error: {e}", exc_info=True)
            raise HTTPException(
                status_code=500, detail="There was an error creating the lead")
