import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from services import DegreesService
from dtos import CreateDegreeFromLeadDto
from models import Degree, LeadDegree
from daos import DegreeDao, LeadDegreeDao

@pytest.fixture
def mock_session() -> Session:
    return create_autospec(Session, instance=True)

@pytest.fixture
def mock_degree_dao() -> DegreeDao:
    return create_autospec(DegreeDao, instance=True)

@pytest.fixture
def mock_lead_degree_dao() -> LeadDegreeDao:
    return create_autospec(LeadDegreeDao, instance=True)

@pytest.fixture
def degrees_service(mock_degree_dao: DegreeDao, mock_lead_degree_dao: LeadDegreeDao) -> DegreesService:
    service = DegreesService()
    service.degree_dao = mock_degree_dao
    service.lead_degree_dao = mock_lead_degree_dao
    return service

def test_check_or_create_degrees(degrees_service, mock_degree_dao, mock_session):
    degrees = [CreateDegreeFromLeadDto(name="Psicología"), CreateDegreeFromLeadDto(name="Medicina")]
    existing_degrees = [Degree(name="Psicología")]
    new_degrees = [Degree(name="Medicina")]

    mock_degree_dao.find_existing_degrees.return_value = existing_degrees
    mock_degree_dao.create_degrees.return_value = new_degrees

    result = degrees_service.check_or_create_degrees(degrees, mock_session)

    assert result == existing_degrees + new_degrees
    mock_degree_dao.find_existing_degrees.assert_called_once_with(["Psicología", "Medicina"], mock_session)
    mock_degree_dao.create_degrees.assert_called_once_with(["Medicina"], mock_session)

def test_check_or_asign_lead_to_degrees(degrees_service, mock_lead_degree_dao, mock_session):
    lead_id = 1
    degrees = [Degree(id=1, name="Psicología"), Degree(id=2, name="Medicina")]
    existing_lead_degrees = [LeadDegree(degree_id=1, lead_id=lead_id)]
    new_lead_degrees = [LeadDegree(degree_id=2, lead_id=lead_id)]

    mock_lead_degree_dao.find_existing_lead_degrees.return_value = existing_lead_degrees
    mock_lead_degree_dao.create_lead_degrees.return_value = new_lead_degrees

    result = degrees_service.check_or_asign_lead_to_degrees(lead_id, degrees, mock_session)

    assert result == existing_lead_degrees + new_lead_degrees
    mock_lead_degree_dao.find_existing_lead_degrees.assert_called_once_with([1, 2], lead_id, mock_session)
    mock_lead_degree_dao.create_lead_degrees.assert_called_once_with([degrees[1]], lead_id, mock_session)