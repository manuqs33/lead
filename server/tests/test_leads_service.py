import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from services import DegreesService, SubjectsService, LeadsService
from daos import LeadDao
from dtos import CreateLeadDto, CreateLeadResponseDto, CreateDegreeFromLeadDto, CreateSubjectFromLeadDto
from models import Lead, Degree, LeadDegree, Subject, LeadSubject


@pytest.fixture
def mock_session() -> Session:
    return create_autospec(Session, instance=True)


@pytest.fixture
def mock_degrees_service() -> DegreesService:
    response: DegreesService = create_autospec(DegreesService, instance=True)
    return response


@pytest.fixture
def mock_subjects_service() -> SubjectsService:
    return create_autospec(SubjectsService, instance=True)


@pytest.fixture
def mock_lead_dao() -> LeadDao:
    return create_autospec(LeadDao, instance=True)


@pytest.fixture
def leads_service(mock_degrees_service: DegreesService, mock_subjects_service: SubjectsService, mock_lead_dao: LeadDao) -> LeadsService:
    service = LeadsService(mock_degrees_service, mock_subjects_service)
    service.lead_dao = mock_lead_dao
    return service


def test_create_leads_and_relations(leads_service, mock_degrees_service, mock_subjects_service, mock_lead_dao, mock_session):
    lead = CreateLeadDto(
        full_name="Manuel Pérez",
        email="mock_email@hotmail.com",
        degrees=[
            CreateDegreeFromLeadDto(name="Ingeniería", subjects=[
                                    CreateSubjectFromLeadDto(name="Álgebra", register_year=2024)]),
            CreateDegreeFromLeadDto(name="Literatura", subjects=None)
        ]
    )
    db_lead = Lead(id=1, full_name="Manuel Pérez", email="mock_email@hotmail.com",)
    degrees = [Degree(name="Ingeniería", id=1), Degree(name="Literatura", id=2)]
    lead_degrees = [LeadDegree(lead_id=1, degree_id=1, id=1), LeadDegree(
        lead_id=1, degree_id=2, id=2)]
    subjects = [Subject(name="Álgebra", id=1)]
    new_lead_subjects = [LeadSubject(lead_id=1, subject_id=1)]

    mock_lead_dao.create_lead.return_value = db_lead
    mock_degrees_service.check_or_create_degrees.return_value = degrees
    mock_degrees_service.check_or_asign_lead_to_degrees.return_value = lead_degrees
    mock_subjects_service.check_or_create_subjects.return_value = subjects
    mock_subjects_service.assign_lead_to_subjects.return_value = new_lead_subjects

    result = leads_service.create_leads_and_relations(lead, mock_session)

    assert result == CreateLeadResponseDto(id=db_lead.id)
    mock_lead_dao.create_lead.assert_called_once_with(lead, mock_session)
    mock_degrees_service.check_or_create_degrees.assert_called_once_with(
        lead.degrees, mock_session)
    mock_degrees_service.check_or_asign_lead_to_degrees.assert_called_once_with(
        db_lead.id, degrees, mock_session)
    assert lead.degrees is not None
    mock_subjects_service.check_or_create_subjects.assert_called_once_with(
        lead.degrees[0].subjects, degrees[0].id, mock_session)
    mock_subjects_service.assign_lead_to_subjects.assert_called_once_with(
        db_lead.id, lead_degrees[0].id, subjects, lead.degrees[0].subjects, mock_session)


def test_create_lead(leads_service, mock_lead_dao, mock_session):
    lead = CreateLeadDto(full_name="Manuel Pérez", email="mock_email@hotmail.com")
    lead_response = CreateLeadResponseDto(id=1)
    mock_lead_dao.create_lead.return_value = lead_response
    result = leads_service.create_lead(lead, mock_session)

    assert result == lead_response
    mock_lead_dao.create_lead.assert_called_once_with(lead, mock_session)


def test_get_lead(leads_service, mock_lead_dao, mock_session):
    lead_id = 1
    lead = Lead(id=lead_id, full_name="Manuel Pérez")
    mock_lead_dao.get_lead.return_value = lead
    result = leads_service.get_lead(lead_id, mock_session)

    assert result == lead
    mock_lead_dao.get_lead.assert_called_once_with(lead_id, mock_session)


def test_get_leads(leads_service, mock_lead_dao, mock_session):
    leads = [Lead(id=1, full_name="Manuel Pérez"), Lead(id=2, full_name="María González")]
    mock_lead_dao.get_leads.return_value = leads
    result = leads_service.get_leads(mock_session)

    assert result == leads
    mock_lead_dao.get_leads.assert_called_once_with(mock_session, 10, 0)
