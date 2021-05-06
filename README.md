# Cornershop Static Analysis

## ast

Useful classes are under `apps/patterns/analyzer.py`. For examples on how to use, check the existing notebooks.

## Configuration


### Why you need a Github token?

We are going to analyse the backend repo, which is private.
If you're in the organization, you can download it.

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


## sample_prs.ipynb

Use this notebook to:

* get a list of open PR ordered by a custom score. You must set `FROM_DATE`, `TO_DATE`, `SAMPLE_SIZE`.

## extract_services_documentation.ipynb

Use this notebook to analyse documentation on the `services.py` module of any app

Analysis is currently performed over every function inside the supplied file and the score is based on three elements:
    * argument typing
    * non-empty docstring
    * return type present
