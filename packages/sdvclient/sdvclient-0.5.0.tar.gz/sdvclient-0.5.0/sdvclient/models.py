import copy
from dataclasses import dataclass, fields
from datetime import datetime
from typing import List, Optional

import pandas as pd
import requests
from pydantic import BaseModel, Field, root_validator

from .raw import get_data


@dataclass
class User:
    id: int
    first_name: str
    last_name: str


@dataclass
class DatasetSummary:
    id: int
    event_start: datetime
    event_end: datetime
    owner: User
    sport: Optional[str]
    tags: List[str]
    title: Optional[str]
    
    def get_data(self):
        return get_data(self.id)


@dataclass
class BaseData:
    id: int
    event_start: datetime
    event_end: datetime
    owner: User
    tags: List[str]
    title: Optional[str]
    type: str
    response: requests.Response


@dataclass
class Question:
    question: str
    answer: str


@dataclass
class Questionnaire(BaseData):
    questions: List[Question]


@dataclass
class TabularData(BaseData):
    dataframe: pd.DataFrame


@dataclass
class DailyActivity(BaseData):
    steps: int = None
    distance: float = None
    calories: int = None
    floors: int = None
    sleep_start: datetime = None
    sleep_end: datetime = None
    sleep_duration: int = None
    resting_heart_rate: int = None
    minutes_sedentary: int = None
    minutes_lightly_active: int = None
    minutes_fairly_active: int = None
    minutes_very_active: int = None


@dataclass
class UnstructuredData(BaseData):
    file_response: requests.Response


@dataclass
class GroupMember:
    user: User
    state: str
    role: str


@dataclass
class Group:
    id: int
    type: str
    name: str
    description: str
    members: List[GroupMember]
