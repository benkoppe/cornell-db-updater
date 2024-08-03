from pydantic import BaseModel
from datetime import datetime

# types returned by the Cornell API


class RosterCatalogVersion(BaseModel):
    status: str


class RosterCatalog(BaseModel):
    descrshort: str
    descr: str
    acalogCatalogId: int
    version: RosterCatalogVersion


class RosterVersion(BaseModel):
    status: str
    referenceDttm: datetime
    catalogDttm: datetime
    descriptionSource: str
    showCatalogNote: bool
    catalog: RosterCatalog


class Roster(BaseModel):
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
