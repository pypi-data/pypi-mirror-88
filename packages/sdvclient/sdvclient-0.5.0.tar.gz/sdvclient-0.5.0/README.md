# Sport Data Valley client library for Python

[![Downloads](https://pepy.tech/badge/sdvclient)](https://pepy.tech/project/sdvclient)

## Introduction
`sdvclient` is a Python client library for the Sport Data Valley platform.
It is basically a wrapper around the REST API (documented [here](https://app.sportdatavalley.nl/api-docs/index.html)).

## Installation
If you are working in the Sport Data Valley JupyterHub environment, this library is automatically installed.

If you are working in a different Python environment, this library can be installed from [PyPI](https://pypi.org/project/sdvclient/):
```bash
pip install sdvclient
```

When you have previously installed the library and want to upgrade to a newer version:
```bash
pip install --upgrade sdvclient
```

## Usage
```python
import sdvclient as sdv


for dataset in sdv.my_datasets():
    # Do something
    pass
```
The dataset summaries that are returned from `my_datasets()` have attributes like `title`, `event_start`, `event_end`, `owner`, `sport`, `tags` and more...
```python
dataset.sport
>>> "sports.riding"
```

To retrieve data from your network:

```python

import sdvclient as sdv


for dataset in sdv.network_datasets():
    # Do something
    pass
```

To retrieve data from a specific group in your network (see below for how to retrieve these groups):

```python

import sdvclient as sdv


for dataset in sdv.group_datasets():
    # Do something
    pass
```

### Limit the number of results
Both `sdv.my_datasets()`, `sdv.network_datasets()` and `sdv.group_datasets()` accept an optional `limit` argument that can be used to limit the number of dataset summaries that are returned.

```python

import sdvclient as sdv

for dataset in sdv.my_datasets(limit=10):
    # Process maximum 10 datasets
    pass
```

Please note that if there are less datasets available then the `limit` you specify, the number of returned dataset summaries is lower than `limit`.


### Filter network data
`sdv.network_datasets()` accepts an optional `query` argument that can be used to filter the returned datasets:

```python
import sdvclient as sdv

for dataset in sdv.network_datasets(query="strava"):
    # Process datasets that are matched by the "strava" query
    pass
```

Please note that the query argument filters on *all* the fields of a dataset.
This means that filtering on the name of a user does not necessarily only retrieve data for that user, as this name may also occur *anywhere* else in a different dataset.

N.B. The `query` argument is **not** available for `sdv.my_datasets()`.

### Retrieve groups and connections
To retrieve the groups in your network:

```python
import sdvclient as sdv

for group in sdv.groups():
    # Do something
    pass
```

To retrieve the connections in your network: 
```python
import sdvclient as sdv

for connection in sdv.connections():
    # Do something
    pass
```

When you found a connection that you want to retrieve data for you can retrieve those like this:
```python
import sdvclient as sdv

for dataset in sdv.connection_datasets(user=connection):
    # Do something
    pass
```

The `connection` input argument is a `User` object that can come from `sdv.connections()` or from the `dataset.owner` from a previous request.

Please be aware that this method uses `sdv.network_datasets()` under the hood and can therefore be slow when you have a lot of datasets from other connections.


### Retrieving raw/full data
After you have retrieved a dataset summary, you can then continue to download the raw/full data from this dataset by calling the `get_data()` method on this object:
```python
import sdvclient as sdv

for dataset in sdv.my_datasets():
    full_data = dataset.get_data()
```

Or you can retrieve the raw/full data directly if you know the dataset id:
```python
import sdvclient as sdv

full_data = sdv.get_data(id=1337)
```


Every object that is returned from `get_data()` has attributes like `title`, `event_start`, `event_end`, `owner`, `sport`, `type`, `tags` and more fields depending on the data_type. For example a dataset with type `strava_type` has an attribute `dataframe` that contains a [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with the data from this dataset.
```python
dataset.data_type
>>> "strava_type"
dataset.dataframe
>>> <pandas.DataFrame>
```

#### Strava data type
As mentioned above, dasets of type `strava_type` have an attribute dataframe with the corresponding data in a dataframe:
```python
dataset.data_type
>>> "strava_type"
dataset.dataframe
>>> <pandas.DataFrame>
```

#### Questionnaire data type
Datasets of type questionnaire have a `questions` attribute which contains of all the questions and answers in the questionnaire.
For each question+answer, the question and answer are available on the `question` and `answer` attributes, respectivily.
```python
dataset.questions[2].question
>>> "this is a question"

dataset.questions[2].answer
>>> "this is an answer"
```

#### Generic CSV data type
For generic tabular data like csv's the returned dataset has an attribute dataframe with the corresponding data in a dataframe:
```python
dataset.data_type
>>> "generic_csv_type"
dataset.dataframe
>>> <pandas.DataFrame>
```

#### Daily activity data type
For daily activity data that is coming from e.g. Fitbit or Polar, the returned dataset has a range of attributes:

- steps
- distance
- calories
- floors
- sleep_start
- sleep_end
- sleep_duration
- resting_heart_rate
- minutes_sedentary
- minutes_lightly_active
- minutes_fairly_active
- minutes_very_active

```python
dataset.data_type
>>> "fitbit_type"
dataset.resting_heart_rate
>>> 58
```

Please note that not all attributes are always available, this is platform and device dependent.


#### Unstructured data
Unstructured data is data (files) that Sport Data Valley does not know how to process.
These files are stored "as is" in the platform and can be download via this client library as well:
For generic tabular data like csv's the returned dataset has an attribute dataframe with the corresponding data in a dataframe:
Unstructured data has a `file_response` attribute that contains a [requests.Response](https://requests.readthedocs.io/en/latest/api/#requests.Response) object.

```python
dataset.data_type
>>> "unstructured"
dataset.file_response
>>> <Response [200]>
```

Read more about processing files downloaded with the Python requests library [here](https://requests.readthedocs.io/en/master/user/quickstart/).
E.g. to process binary response content, see [here](https://requests.readthedocs.io/en/master/user/quickstart/#binary-response-content).


#### Other data types
Although this library will be updated when new data types are added it can happen that a specific data type is not fully supported yet. In that case the returned dateset will be identical as unstructured data, with an `file_response` attribute that contains a [requests.Response](https://requests.readthedocs.io/en/latest/api/#requests.Response) object.
Unstructured data is data (files) that Sport Data Valley does not know how to process.

```python
dataset.data_type
>>> "some new data type"
dataset.file_response
>>> <Response [200]>
```


### Authentication
The library retrieves your API token from the `SDV_AUTH_TOKEN` environment variable.
If you are working in the Sport Data Valley JupyterHub, this is automatically set.
If you are working in a different environment, you can retrieve an API token from the "Advanced" page [here](https://app.sportdatavalley.nl/profile/edit) and set it like this:

```python
sdv.set_token("your API token here")
```



## Development

### Adding Python versions
The supported Python versions are specified in `pyproject.toml[tool.poetry.dependencies]#python`.
The Python versions that are tested are specified in `pyproject.toml[tool.tox]#envlist` and in `Dockerfile.test`.
If you want to add a new supported Python version, or want to test against a newer version of an existing Python version, the versions at these locations need to be updated.


## Contributors
- [Aart Goossens](https://twitter.com/aartgoossens)

## License
See [LICENSE](LICENSE) file.
