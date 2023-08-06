from dataclasses import dataclass
from io import StringIO

import pandas as pd
import requests

from . import models
from .utils import _create_session, _create_url, cast_if_not_none


@dataclass
class DataSummaryProcessor:
    dataset: dict

    def process(self):
        base_data = self._base_data()
        return models.DatasetSummary(**base_data)

    def _base_data(self):
        return {
            "id": self.dataset["versioned_data_object_id"],
            "title": self.dataset["title"],
            "event_start": self.dataset["event_start"],
            "event_end": self.dataset["event_end"],
            "owner": self._get_owner(),
            "tags": self.dataset["tags"],
            "sport": self._get_sport(),
        }

    def _get_owner(self):
        owner_data = self.dataset["owner"]
        return models.User(
            id=owner_data["id"],
            first_name=owner_data["first_name"],
            last_name=owner_data["last_name"],
        )

    def _get_sport(self):
        sport_data = self.dataset["sport"]
        if sport_data is not None:
            return sport_data["name"]


@dataclass
class DatasetProcessor:
    response: requests.Response
    
    def __post_init__(self):
        self.data = self.response.json()
        self.data_type = self.data["versioned_data_object"]["data_type"]["data_type"]
        self.id = self.data["versioned_data_object"]["id"]

    def process(self):
        try:
            response_data, response_model = getattr(self, f"_process_{self.data_type}")()
        except AttributeError:
            response_data, response_model = self._process_unstructured()

        base_data = self._base_data()
        return response_model(
            response=self.response,
            type=self.data_type,
            **response_data,
            **base_data
        )

    def _base_data(self):
        return {
            "id": self.id,
            "title": self.data["versioned_data_object"]["metadatum"]["title"],
            "event_start": self.data["versioned_data_object"]["metadatum"]["event_start"],
            "event_end": self.data["versioned_data_object"]["metadatum"]["event_end"],
            "owner": self._get_owner(),
            "tags": self.data["versioned_data_object"]["metadatum"]["tags"],
        }

    def _get_owner(self):
        owner_data = self.data["versioned_data_object"]["metadatum"]["owner"]
        return models.User(
            id=owner_data["id"],
            first_name=owner_data["first_name"],
            last_name=owner_data["last_name"],
        )
    
    def _process_questionnaire_type(self):
        data_row = self.data["versioned_data_object"]["structured_data_objects"][0]["data_rows"][0]
        actual_data = data_row.pop("values")

        questions = []
        for key, value in actual_data.items():
            if not key.startswith("v"):
                # probably not a question
                # @TODO figure out if this is really the case
                continue
            questions.append(models.Question(question=key, answer=value))

        return {"questions": questions}, models.Questionnaire

    def _process_generic_csv_type(self):
        session = _create_session()
        response = session.get(
            url=_create_url(f"/data/{self.id}/download"),
            allow_redirects=True,
        )
        response.raise_for_status()

        dataframe = pd.read_csv(StringIO(response.content.decode('utf-8')))

        return {"dataframe": dataframe}, models.TabularData

    def _process_strava_type(self):
        columns = ["hr", "speed", "power", "cadence", "elevation", "latlong", "distance"]

        session = _create_session()
        response = session.get(
            url=_create_url(f"/data/{self.id}/time_series"),
            params={"keys": ",".join(columns)},
            allow_redirects=True,
        )
        response.raise_for_status()

        data = response.json()
        dataframe = pd.DataFrame(data["time_series"], index=data["offset"])

        return {"dataframe": dataframe}, models.TabularData

    def _process_polar_type(self):
        data_row = self.data["versioned_data_object"]["structured_data_objects"][0]["data_rows"][-1]

        response_data = {
            "calories": cast_if_not_none(data_row.get("calories", None), int),
            "steps": cast_if_not_none(data_row.get("active-steps", None), int),
        }

        return response_data, models.DailyActivity

    def _process_fitbit_type(self):
        data_row = self.data["versioned_data_object"]["structured_data_objects"][0]["data_rows"][0]

        response_data = {
            "calories": cast_if_not_none(data_row.get("calories", None), int),
            "steps": cast_if_not_none(data_row.get("steps", None), int),
            "distance": cast_if_not_none(data_row.get("distance", None), float),
            "floors": cast_if_not_none(data_row.get("floors", None), int),
            "resting_heart_rate": cast_if_not_none(data_row.get("resting_heart_rate", None), int),
            "minutes_sedentary": cast_if_not_none(data_row.get("minutes_sedentary", None), int),
            "minutes_lightly_active": cast_if_not_none(data_row.get("minutes_lightly_active", None), int),
            "minutes_fairly_active": cast_if_not_none(data_row.get("minutes_fairly_active", None), int),
            "minutes_very_active": cast_if_not_none(data_row.get("minutes_very_active", None), int),
            "sleep_duration": cast_if_not_none(data_row.get("sleep_minutes", None), int),
            "sleep_start": cast_if_not_none(data_row.get("sleep_start_time", None), int),
            "sleep_end": cast_if_not_none(data_row.get("sleep_get_up_time", None), int),
        }

        return response_data, models.DailyActivity

    def _process_unstructured(self):
        session = _create_session()
        response = session.get(
            url=_create_url(f"/data/{self.id}/download"),
            allow_redirects=True,
        )
        response.raise_for_status()

        return {"file_response": response}, models.UnstructuredData
