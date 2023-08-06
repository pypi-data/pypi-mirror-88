# AA Blueprints

This is an blueprints library app for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) (AA) that can be used to list blueprints for your corporation or alliance.

![release](https://img.shields.io/pypi/v/aa-blueprints?label=release) ![License](https://img.shields.io/badge/license-GPL-green) ![python](https://img.shields.io/badge/python-3.6-informational) ![django](https://img.shields.io/badge/django-3.1-informational) ![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white) ![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

## Overview

## Features

- Lists blueprints owned by corporation or alliance (configurable with permissions)

## Screenshots

![main-view](https://i.imgur.com/ij5j1kL.png)

# Installation

## Requirements

AA Blueprints needs the app [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to function. Please make sure it is installed before before continuing.

## Steps

### Step 1 - Install the Package

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

`pip install aa-blueprints`

### Step 2 - Configure AA

- Add 'blueprints' to `INSTALLED_APPS` in `settings/local.py`.
- Add the following automated task definition:

```python
CELERYBEAT_SCHEDULE['blueprints_update_all_blueprints'] = {
            'task': 'blueprints.tasks.update_all_blueprints',
            'schedule': crontab(minute=0, hour='*/3'),
}
CELERYBEAT_SCHEDULE['blueprints_update_all_locations'] = {
            'task': 'blueprints.tasks.update_all_locations',
            'schedule': crontab(minute=0, hour='*/12'),
}
```

### Step 3 - Finalize App installation

Run migrations & copy static files:

```bash
python manage.py migrate
python manage.py collectstatic
```

Restart your supervisor services for Auth

### Step 4 - Update EVE Online API Application

Update the Eve Online API app used for authentication in your AA installation to include the following scopes:

- `esi-corporations.read_blueprints.v1`
- `esi-universe.read_structures.v1`

### Step 5 - Data import

Load EVE Online type data from ESI:

```bash
python manage.py blueprints_load_types
```
