# Cornershop Static Analysis

## ast

Useful classes are under `apps/patterns/analyzer.py`. For examples on how to use, check the existing notebooks.

## Configuration

You must first create a `.env` file, within the `analysis` folder.
Inside complete the following values

~~~
GITHUB_TOKEN=yourtoken
~~~

You can get your personal Github API token by visiting your profile -> Developer settings -> Personal access tokens.

* Generate a new token
* Mark the `repo` scope and the `org:read` scope.
* Copy the token and add it to `.env`.


# Notebooks

## check_catalogdb_services.ipynb

Use this notebook to:

* get a list of the services only present in your branch
* get a list of name collisions between your services and every other open PR labled with "catalogdb" in the backend repo.

Read the notebook for more information.
