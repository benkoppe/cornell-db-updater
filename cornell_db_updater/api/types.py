from pydantic import BaseModel, field_validator
from datetime import date, datetime, time
from typing import Optional

# types returned by the Cornell API


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True


# ** ROSTERS **


class RosterCatalogVersion(FrozenBaseModel):
    status: str


class RosterCatalog(FrozenBaseModel):
    descrshort: str
    descr: str
    acalogCatalogId: int
    version: RosterCatalogVersion


class RosterVersion(FrozenBaseModel):
    status: str
    referenceDttm: datetime
    catalogDttm: datetime
    descriptionSource: str
    showCatalogNote: bool
    catalog: RosterCatalog


class Roster(FrozenBaseModel):
    slug: str
    isDefaultRoster: bool
    strm: str
    descr: str
    descrshort: str
    attributeSrc: str
    defaultSessionCode: str
    defaultCampus: str
    defaultLocation: str
    defaultInstructionMode: str
    sharing: bool
    archiveMode: bool
    version: RosterVersion
    lastModifiedDttm: datetime
    classMaterialSupport: bool
    classMaterialAutoAction: str


# ** ACADEMIC CAREERS **


class AcademicCareer(FrozenBaseModel):
    value: str
    descr: str


# ** ACADEMIC GROUPS **


class AcademicGroup(FrozenBaseModel):
    value: str
    descr: str


# ** CLASS LEVELS **


class ClassLevel(FrozenBaseModel):
    value: str
    descr: int


# ** SUBJECTS **


class Subject(FrozenBaseModel):
    value: str
    descr: str
    descrformal: str


# ** CLASSES **


def american_date_format(v: str) -> date:
    return datetime.strptime(v, "%m/%d/%Y").date()


def american_time_format(v: str) -> time | None:
    try:
        return datetime.strptime(v, "%I:%M%p").time()
    except ValueError:
        return None


class ClassInstructor(FrozenBaseModel):
    instrAssignSeq: int
    netid: str
    firstName: str
    middleName: str
    lastName: str


class ClassMeeting(FrozenBaseModel):
    classMtgNbr: int
    timeStart: Optional[time]
    timeEnd: Optional[time]
    startDt: date
    endDt: date
    instructors: list[ClassInstructor]
    pattern: str
    facilityDescr: Optional[str]
    bldgDescr: Optional[str]
    facilityDescrshort: Optional[str]
    meetingTopicDescription: Optional[str]

    _fmt_timeEnd = field_validator("timeEnd", mode="before")(american_time_format)
    _fmt_timeStart = field_validator("timeStart", mode="before")(american_time_format)

    _fmt_endDt = field_validator("endDt", mode="before")(american_date_format)
    _fmt_startDt = field_validator("startDt", mode="before")(american_date_format)


class ClassNote(FrozenBaseModel):
    classNotesSeq: int
    descrlong: str


class ClassSection(FrozenBaseModel):
    ssrComponent: str
    ssrComponentLong: str
    section: str
    classNbr: int
    meetings: list[ClassMeeting]
    notes: list[ClassNote]
    campus: str
    campusDescr: str
    location: str
    locationDescr: str
    startDt: date
    endDt: date
    addConsent: str
    addConsentDescr: str
    isComponentGraded: bool
    instructionMode: Optional[str]
    instrModeDescrshort: Optional[str]
    instrModeDescr: Optional[str]
    topicDescription: str
    openStatus: Optional[str]

    _fmt_startDt = field_validator("startDt", mode="before")(american_date_format)
    _fmt_endDt = field_validator("endDt", mode="before")(american_date_format)


class SimpleCombination(FrozenBaseModel):
    subject: str
    catalogNbr: str
    type: str


class EnrollGroup(FrozenBaseModel):
    classSections: list[ClassSection]
    unitsMinimum: float
    unitsMaximum: float
    componentsOptional: list[str]
    componentsRequired: list[str]
    gradingBasis: str
    gradingBasisShort: str
    gradingBasisLong: str
    simpleCombinations: list[SimpleCombination]
    sessionCode: str
    sessionBeginDt: date
    sessionEndDt: date

    _fmt_sessionBeginDt = field_validator("sessionBeginDt", mode="before")(
        american_date_format
    )
    _fmt_sessionEndDt = field_validator("sessionEndDt", mode="before")(
        american_date_format
    )


class Class(FrozenBaseModel):
    strm: int
    crseId: int
    crseOfferNbr: int
    subject: str
    catalogNbr: str
    titleShort: str
    titleLong: str
    enrollGroups: list[EnrollGroup]
    description: Optional[str]
    catalogDistr: Optional[str]
    catalogForbiddenOverlaps: Optional[str]
    catalogAttribute: Optional[str] = None
    catalogWhenOffered: Optional[str]
    catalogComments: Optional[str]
    catalogPrereqCoreq: Optional[str]
    catalogFee: Optional[str]
    catalogSatisfiesReq: Optional[str]
    catalogPermission: Optional[str]
    catalogCourseSubfield: Optional[str]
    catalogOutcomes: Optional[list[str]]
    acadCareer: str
    acadGroup: str
