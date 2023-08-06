"""library module"""

# standard
import json
from typing import List, Tuple, Union
# local
from matatika.catalog import Catalog
from matatika.dataset import Dataset


class MatatikaClient():
    """
    Class to handle client context

    Args:
        auth_token (str): Authentication token
        endpoint_url (str): Endpoint URL
        workspace_id (str): Workspace ID

    Example:

    ```py
    # create 'auth_token', 'endpoint_url' and 'workspace-id' variables

    client = Matatika(auth_token, endpoint_url, workspace_id)
    ```
    """

    def __init__(self, auth_token: str, endpoint_url: str, workspace_id: str):
        self._auth_token = auth_token
        self._endpoint_url = endpoint_url
        self._workspace_id = workspace_id

    # getter methods
    @property
    def auth_token(self) -> str:
        """
        Gets the client auth token

        Returns:
            str: Client auth token

        Example:

        ```py
        # create MatatikaClient object

        auth_token = client.auth_token
        print(auth_token)
        ```
        """

        return self._auth_token

    @property
    def endpoint_url(self) -> str:
        """
        Gets the client endpoint URL

        Returns:
            str: Client endpoint URL

        Example:

        ```py
        # create MatatikaClient object

        endpoint_url = client.endpoint_url
        print(endpoint_url)
        ```
        """

        return self._endpoint_url

    @property
    def workspace_id(self) -> str:
        """
        Gets the client workspace URL

        Returns:
            str: Client workspace URL

        Example:

        ```py
        # create MatatikaClient object

        workspace_id = client.workspace_id
        print(workspace_id)
        ```
        """

        return self._workspace_id

    # setter methods
    @auth_token.setter
    def auth_token(self, value: str):
        """
        Sets the client authentication token

        Args:
            value (str): Authentication token

        Example:

        ```py
        # create MatatikaClient object
        # create 'auth_token' variable

        client.auth_token = auth_token
        print(client.auth_token)
        ```
        """

        self._auth_token = value

    @endpoint_url.setter
    def endpoint_url(self, value: str):
        """
        Sets the client endpoint URL

        Args:
            value (str): Endpoint URL

        Example:

        ```py
        # create MatatikaClient object
        # create 'endpoint_url' variable

        client.endpoint_url = endpoint_url
        print(client.endpoint_url)
        ```
        """

        self._endpoint_url = value

    @workspace_id.setter
    def workspace_id(self, value: str):
        """
        Sets the client workspace ID

        Args:
            value (str): Workspace ID

        Example:

        ```py
        # create MatatikaClient object
        # create 'workspace_id' variable

        client.workspace_id = workspace_id
        print(client.workspace_id)
        ```
        """

        self._workspace_id = value

    def profile(self) -> dict:
        """
        Gets the authenticated user profile

        Returns:
            dict: Authenticated user profile

        Example:

        ```py
        # create MatatikaClient object

        profile = client.profile()

        print(profile['id'])
        print(profile['name'])
        print(profile['email'])
        ```
        """

        catalog = Catalog(self)
        return catalog.get_profile()

    def publish(self, datasets: List[Dataset]) -> List[Tuple[Dataset, int]]:
        """
        Publishes datasets

        Args:
            datasets (List[Dataset]): Datasets to publish

        Returns:
            List[Tuple[Dataset,int]]: Published datasets and status actions

        Example:

        ```py
        # create MatatikaClient object
        # create 'datasets' variable

        responses = client.publish(datasets)

        for dataset, status_code in responses:
            print(f"[{status_code}]\tSuccessfully published the dataset {dataset.dataset_id}")
        ```
        """

        catalog = Catalog(self)
        responses = catalog.post_datasets(datasets)

        published_datasets = []

        for response in responses:
            dataset = Dataset.from_dict(response.json())
            published_datasets.append((dataset, response.status_code))

        return published_datasets

    def list_resources(self, resource_type: str) -> Union[list, None]:
        """
        Lists all available resources of the specified type

        Args:
            resource_type (str): Resource type to return (workspaces/datasets)

        Returns:
            Union[list,None]: Available resources

        Examples:

        List all workspaces
        ```py
        # create MatatikaClient object

        workspaces = client.list_resources('workspaces')

        for workspace in workspaces:
            print(workspace['id'], workspace['name'], workspace['domains'])
        ```

        List all datasets in the workspace provided upon client object instantiation
        ```py
        # create MatatikaClient object

        datasets = client.list_resources('datasets')

        for dataset in datasets:
            print(dataset['id'], dataset['alias'], dataset['title'])
        ```

        List all datasets in the workspace 'c6db37fd-df5e-4ac6-8824-a4608932bda0'
        ```py
        # create MatatikaClient object

        client.workspace_id = '8566fe13-f30b-4536-aecf-b3879bd0910f'
        datasets = client.list_resources('datasets')

        for dataset in datasets:
            print(dataset['id'], dataset['alias'], dataset['title'])
        ```
        """

        catalog = Catalog(self)

        if resource_type == 'workspaces':
            return catalog.get_workspaces()

        if resource_type == 'datasets':
            return catalog.get_datasets()

        return None

    def fetch(self, dataset_id: str, raw: bool = False) -> Union[dict, str]:
        """
        Fetches the data of a dataset using the query property

        Args:
            dataset_id (str): Dataset ID in UUID format
            raw (bool, optional): Whether to return the data as a raw string or not
            (defaults to False)

        Returns:
            Union[dict,str]: Dataset data

        Examples:

        Fetch data as Python object
        ```py
        # create MatatikaClient object
        # create 'dataset_id' variable

        data = client.fetch(dataset_id)

        if data:
            print(data)
        else:
            print(f"No data was found for dataset {dataset_id}")
        ```

        Fetch data as a raw string
        ```py
        # create MatatikaClient object
        # create 'dataset_id' variable

        data = client.fetch(dataset_id, raw=True)

        if data:
            print(data)
        else:
            print(f"No data was found for dataset {dataset_id}")
        ```
        """

        catalog = Catalog(self)
        data = catalog.get_data(dataset_id)

        if raw:
            return data

        return json.loads(data)

    def get_dataset(self, dataset_id: str, raw: bool = False) -> Dataset:
        """
        Gets a dataset

        Args:
            dataset_id (str): Dataset ID in UUID format
            raw (bool, optional): Whether to return the dataset as a raw string or not
            (defaults to False)

        Returns:
            Dataset: Dataset object

        Examples:

        Fetch a dataset as a Dataset object
        ```py
        # create MatatikaClient object
        # create 'dataset_id' variable

        dataset = client.get_dataset(dataset_id)
        print(dataset)
        ```

        Fetch a dataset as a raw string
        ```py
        # create MatatikaClient object
        # create 'dataset_id' variable

        dataset = client.get_dataset(dataset_id, raw=True)
        print(dataset)
        ```
        """

        catalog = Catalog(self)
        dataset_dict = catalog.get_dataset(dataset_id)

        if raw:
            return json.dumps(dataset_dict)

        return Dataset.from_dict(dataset_dict)
