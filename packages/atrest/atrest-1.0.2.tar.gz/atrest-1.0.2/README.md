# atrest

## About

This library is a very basic tool to submit tickets to an Autotask help desk.

---

## Usage

Initialize the `Client` class, providing the following parameters:

- Autotask Base URL (e.g. <https://webservices15.autotask.net/atservicesrest/v1.0>)
- Autotask API Integration Code
- Autotask API User
- Autotask API Secret

Here is an example implementation:

```python
from atrest import Client

def submit_ticket():
    atclient = Client(
        "https://webservices15.autotask.net/atservicesrest/v1.0",
        "<api_integration_code>,
        "<api_user>",
        "<api_secret>"
    )

    ticket_title = "Major Issue!"
    ticket_desc = """
    There was a major issue.

    You should definitely check it out!
    """

    try:
        ticket_id = atclient.create_ticket(
            ticket_title,
            ticket_desc,
            status=1,
            priority=1,
            company_id=0,
            queue_id=29682833
        )
        print(f"Ticket successfully sent. Ticket ID: {ticket_id}")
    except Exception as e:
        raise e
```

## Development (For author only - code is in private repo currently)

Initialize the environment:

```bash
git clone https://gitlab.com/jweaver-strive/atrest.git && cd atrest
pipenv install && pipenv shell
```

When running `unittest` tests, be sure to update the `.env` file with the correct environment variables.

To install the dev changes locally, run the following commands while in a virtual environment:

```bash
python setup.py bdist_wheel
pip install -e .
```

When done with development and creating a new package, change the package version in `setup.py`, then use the following commands:

```bash
python3 setup.py sdist bdist_wheel
python3 -m twine check dist/*
python3 -m twine upload dist/*
```

See here for detailed instructions on packaging for PyPi: <https://packaging.python.org/tutorials/packaging-projects/>
