from typing import List, Optional, Tuple

from pydantic import BaseModel


class DriveObj(BaseModel):
    name: str
    id: str
    kind: str
    mime_type: str
    drive_id: str
    parents: str

    public: Optional[bool]
    draft: Optional[bool]
    meta: Optional[bool]
    webViewLink: Optional[str]
    pointer: Optional[str]


class DocType(DriveObj):
    title: Optional[str]
    content: Optional[dict]
    webViewLink: Optional[str]
    ast: Optional[List[Tuple[str, List]]]


class FolderType(DriveObj):
    path: Optional[List[str]]


class Drive(BaseModel):
    path: List[str] = []
