from typing import Generator

from .models import DatasetSummary, Group, GroupMember, User
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


def _groups():
    session = _create_session()
    response = session.get(
        url=_create_url("/groups"),
        allow_redirects=False,
    )
    response.raise_for_status()

    groups = response.json()

    for group in groups:
        yield group


def groups():
    for group in _groups():
        if group["group_type"] not in ["group", "anonymized"]:
            continue

        group_members = []
        for member in group["group_memberships"]:
            profile = member["profile"]
            user = User(
                id=profile["id"],
                first_name=profile["first_name"],
                last_name=profile["last_name"],
            )
            group_member = GroupMember(
                user=user,
                state=member["state"],
                role=member["role"]
            )
            group_members.append(group_member)

        g = Group(
            id=group["id"],
            name=group["name"],
            type=group["group_type"],
            description=group["description"],
            members=group_members
        )

        yield g


def connections():
    session = _create_session()
    response = session.get(
        url=_create_url("/profiles/my"),
        allow_redirects=False,
    )
    response.raise_for_status()

    my_user_id = response.json()["id"]

    for group in _groups():
        if group["group_type"] == "mutual_connection":
            for member in group["group_memberships"]:
                profile = member["profile"]
                if profile["id"] != my_user_id:
                    break

            user = User(
                id=profile["id"],
                first_name=profile["first_name"],
                last_name=profile["last_name"],
            )

            yield user


def group_datasets(group_id: int, limit: int = None) -> Generator[DatasetSummary, None, None]:
    """Generator function that returns dataset summaries for the specified group.

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
            url=_create_url(f"/groups/{group_id}/recent_activity"),
            params={"page": page},
            allow_redirects=False,
        )
        response.raise_for_status()

        versioned_data_objects = response.json()["vdos"]

        if len(versioned_data_objects) == 0:
            return

        for versioned_data_object in versioned_data_objects:
            yield DataSummaryProcessor(versioned_data_object["metadatum"]).process()

            num += 1
            if limit is not None and num >= limit:
                return

        page += 1


def connection_datasets(user: User, limit: int = None) -> Generator[DatasetSummary, None, None]:
    """Generator function that returns dataset summaries for the specified connection.

    Args:
        limit: Maximum number of datasets to return.

    Yields:
        Yields dataset summaries as sdvclient.models.DatasetSummary
    """
    if user.first_name is None:
        raise AttributeError("Users with no first name are not supported")

    num = 0
    for dataset in network_datasets(query=user.first_name):
        if dataset.owner.id == user.id:
            yield dataset
            num += 1
            if limit is not None and num >= limit:
                break
