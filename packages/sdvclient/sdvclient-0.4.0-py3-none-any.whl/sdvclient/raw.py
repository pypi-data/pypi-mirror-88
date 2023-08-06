from .processing import DatasetProcessor
from .utils import _create_session, _create_url


def get_data(id: int):
    """Function that returns datasets by id.

    Args:
        id: De id of the dataset.

    Returns:
        Returns datasets as sdvclient.models.Dataset
    """
    session = _create_session()
    response = session.get(url=_create_url(f"/data/{id}"))
    response.raise_for_status()

    return DatasetProcessor(response).process()
