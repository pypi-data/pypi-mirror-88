from typing import Generator

from .models import DatasetSummary
from .utils import _create_session, _create_url
from .processing import DataSummaryProcessor


# TODO: host: app.sportdatavalley.nl/api/v1/dashboards/available_datasets


def my_datasets(limit: int = None) -> Generator[DatasetSummary, None, None]:
    """Generator function that returns dataset summaries s for the authenticated user.

    Args:
        limit: Maximum number of datasets to return.

    Yields:
        Yields dataset summaries as sdvclient.models.DatasetSummary
    """
    session = _create_session()
    num = 0
    page = 1
    while True:
        response = session.get(
            url=_create_url("/timeline/my_metadata"),
            params={"page": page},
            allow_redirects=False,
        )
        response.raise_for_status()

        datasets = response.json()["data"]

        if len(datasets) == 0:
            return

        for dataset in datasets:
            yield DataSummaryProcessor(dataset).process()

            num += 1
            if limit is not None and num >= limit:
                return

        page += 1


def network_datasets(limit: int = None, query: str = None) -> Generator[DatasetSummary, None, None]:
    """Generator function that returns dataset summaries s for the authenticated user.

    Args:
        limit: Maximum number of datasets to return.

    Yields:
        Yields dataset summaries as sdvclient.models.DatasetSummary
    """
    session = _create_session()
    num = 0
    page = 1
    while True:
        params= {"page": page}
        if query is not None:
            params["query"] = query

        response = session.get(
            url=_create_url("/timeline/network_metadata"),
            params=params,
            allow_redirects=False,
        )
        response.raise_for_status()

        datasets = response.json()["data"]

        if len(datasets) == 0:
            return

        for dataset in datasets:
            yield DataSummaryProcessor(dataset["metadatum"]).process()

            num += 1
            if limit is not None and num >= limit:
                return

        page += 1
