from typing import Any, Literal

from pydantic import BaseModel, Field


class ParsedNote(BaseModel):
    summary: str = ""
    status: str = ""
    owner: str = ""
    due_date: str = ""
    risks: list[str] = Field(default_factory=list)


class ChangeOperation(BaseModel):
    operation: str
    target: str
    value: Any = None


class ChangeSet(BaseModel):
    ops: list[ChangeOperation] = Field(default_factory=list)


class GoldRecord(BaseModel):
    note_id: str
    gate_verdict: Literal["pass", "block"]
    expected_result_raw: Literal["ALLOW", "BLOCK"]
    reason: str
    parsed_note: ParsedNote = Field(default_factory=ParsedNote)
    change_set: ChangeSet = Field(default_factory=ChangeSet)
