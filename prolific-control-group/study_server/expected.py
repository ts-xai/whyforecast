from typing import Optional

from dataclasses import dataclass


@dataclass
class ConsentGet:
    prolific_id: str


@dataclass
class StudyPost:
    prolific_id: str
    consent_for: str


@dataclass
class CompleteGet:
    check: Optional[str]

@dataclass
class TutorialGet:
    prolific_id: str


@dataclass
class TutorialPost:
    prolific_id: str
    consent_for: str


@dataclass
class TutorialGet2:
    prolific_id: str


@dataclass
class TutorialPost2:
    prolific_id: str
    consent_for: str

@dataclass
class FormPost:
    prolific_id: str
    consent_for: str