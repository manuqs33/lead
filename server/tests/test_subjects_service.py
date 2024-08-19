import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from dtos import CreateSubjectFromLeadDto
from models import Subject, LeadSubject
from services.subjects_service import SubjectsService
from daos import SubjectDao, LeadSubjectDao

@pytest.fixture
def mock_session() -> Session:
    return create_autospec(Session, instance=True)

@pytest.fixture
def mock_subject_dao() -> SubjectDao:
    return create_autospec(SubjectDao, instance=True)

@pytest.fixture
def mock_lead_subject_dao() -> LeadSubjectDao:
    return create_autospec(LeadSubjectDao, instance=True)

@pytest.fixture
def subjects_service(mock_subject_dao: SubjectDao, mock_lead_subject_dao: LeadSubjectDao) -> SubjectsService:
    service = SubjectsService()
    service.subject_dao = mock_subject_dao
    service.lead_subject_dao = mock_lead_subject_dao
    return service

def test_check_or_create_subjects(subjects_service, mock_subject_dao, mock_session):
    subjects = [CreateSubjectFromLeadDto(name="Matemática", register_year=2024), CreateSubjectFromLeadDto(name="Historia", register_year=2024)]
    degree_id = 1

    existing_subjects = [Subject(name="Matemática")]
    new_subjects = [Subject(name="Historia")]

    mock_subject_dao.find_existing_subjects.return_value = existing_subjects
    mock_subject_dao.create_subjects.return_value = new_subjects

    result = subjects_service.check_or_create_subjects(subjects, degree_id, mock_session)

    assert result == existing_subjects + new_subjects
    mock_subject_dao.find_existing_subjects.assert_called_once_with(["Matemática", "Historia"], degree_id, mock_session)
    mock_subject_dao.create_subjects.assert_called_once_with([subjects[1]], degree_id, mock_session)

def test_assign_lead_to_subjects(subjects_service, mock_lead_subject_dao, mock_session):
    lead_id = 1
    lead_degree_id = 1
    subjects = [Subject(name="Matemática"), Subject(name="Historia")]
    metadata = [CreateSubjectFromLeadDto(name="Matemática", duration_in_months=6, register_year=2021, times_taken=1),
                CreateSubjectFromLeadDto(name="Historia", duration_in_months=6, register_year=2021, times_taken=1)]

    new_lead_subjects = [LeadSubject(lead_id=lead_id, subject_id=1), LeadSubject(lead_id=lead_id, subject_id=2)]

    mock_lead_subject_dao.create_lead_subjects.return_value = new_lead_subjects

    result = subjects_service.assign_lead_to_subjects(lead_id, lead_degree_id, subjects, metadata, mock_session)

    assert result == new_lead_subjects
    metadata_dict = {item.name: item for item in metadata}
    mock_lead_subject_dao.create_lead_subjects.assert_called_once_with(lead_id, lead_degree_id, subjects, metadata_dict, mock_session)