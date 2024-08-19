import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from dtos import CreateLeadDto, CreateLeadResponseDto
from services import LeadsService
from controllers import LeadController

@pytest.fixture
def mock_router() -> APIRouter:
    return create_autospec(APIRouter, instance=True)

@pytest.fixture
def mock_session() -> Session:
    return create_autospec(Session, instance=True)

@pytest.fixture
def mock_leads_service() -> LeadsService:
    return create_autospec(LeadsService, instance=True)

@pytest.fixture
def lead_controller(mock_leads_service: LeadsService, mock_router: APIRouter) -> LeadController:
    controller = LeadController(mock_router, mock_leads_service)
    controller.leads_service = mock_leads_service
    return controller

def test_create_lead_success(lead_controller, mock_leads_service, mock_session):
    lead = CreateLeadDto(full_name="Nuevo Lead", email="test@example.com")
    response_dto = CreateLeadResponseDto(id=1)

    mock_leads_service.create_leads_and_relations.return_value = response_dto

    result = lead_controller.create_lead(lead, session=mock_session)

    assert result == response_dto
    mock_leads_service.create_leads_and_relations.assert_called_once_with(lead, mock_session)

def test_create_lead_http_exception(lead_controller, mock_leads_service, mock_session):
    lead = CreateLeadDto(full_name="Nuevo Lead", email="test@example.com")
    mock_leads_service.create_leads_and_relations.side_effect = HTTPException(status_code=400, detail="Bad Request")

    with pytest.raises(HTTPException) as exc_info:
        lead_controller.create_lead(lead, session=mock_session)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Bad Request"
    mock_leads_service.create_leads_and_relations.assert_called_once_with(lead, mock_session)

def test_create_lead_general_exception(lead_controller, mock_leads_service, mock_session):
    lead = CreateLeadDto(full_name="Nuevo Lead", email="test@example.com")
    mock_leads_service.create_leads_and_relations.side_effect = Exception("Server Error")

    with pytest.raises(Exception) as exc_info:
        lead_controller.create_lead(lead, session=mock_session)
    mock_leads_service.create_leads_and_relations.assert_called_once_with(lead, mock_session)