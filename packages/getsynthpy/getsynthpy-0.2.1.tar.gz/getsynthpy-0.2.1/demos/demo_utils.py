import pandas as pd

import random
import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from faker import Faker

fake = Faker()


overrides = {
    "users.job": {
        "type": "string",
        "faker": {
            "generator": "job"
        }
    },
    "users.address": {
        "type": "string",
        "faker": {
            "generator": "address"
        }
    },
    "users.birthdate": {
        "type": "string",
        "date_time": {
            "type": "naive_date",
            "format": "%Y-%m-%d",
            "begin": "1945-1-11",
            "end": "2002-6-25",
        }
    },
    "users.mail": {
        "type": "string",
        "faker": {
            "generator": "ascii_email"
        }
    },
    "users.ssn": {
        "type": "string",
        "faker": {
            "generator": "ssn"
        }
    },
    "users.sex": {
        "type": "string",
        "categorical": {
            "M": 506,
            "F": 491
        }
    },
    "users.created_at": {
        "type": "string",
        "date_time": {
            "format": "%Y-%m-%dT%H:%M:%S",
            "begin": "2016-3-12T6:34:42",
        }
    },
    "users.last_logged_in_ip": {
        "type": "string",
        "faker": {
            "generator": "ipv4"
        }
    },
    "users.num_logins": {
        "type": "number",
        "subtype": "u64",
        "range": {
            "low": 1,
            "high": 42,
            "step": 1
        }
    },
    "users.name": {
        "type": "string",
        "faker": {
            "generator": "name"
        }
    },
}


async def apply_overrides(client, ns):
    for field, override in overrides.items():
        await client.override.put_override(field=field, override=override, namespace=ns, replace=True)


def restrict(profile):
    return {
        key: value
        for key, value in profile.items()
        if any(key in k for k in overrides.keys())
    }


def augment(profile):
    profile.update(
        {
            "birthdate": fake.date_between(start_date="-40y", end_date="-18y"),
            "created_at": fake.date_time_between(start_date="-4y", end_date="now"),
            "last_logged_in_ip": fake.ipv4(),
            "num_logins": random.randint(1, 25),
        }
    )
    return profile


def get_profiles():
    profiles = []
    for _ in range(1000):
        profiles.append(augment(restrict(fake.profile())))
    import pickle

    with open("users_data.pickle", "wb") as f:
        pickle.dump(profiles, f)


async def load_users_data():
    import pickle

    with open("users_data.pickle", "rb") as f:
        data = pickle.load(f)

    from synthpy import Synth

    client = Synth()
    await client.ingest.put_documents(collection="users", document=data[0], namespace="dev")
    await apply_overrides(client, "dev")

    return data


async def clean_up():
    from synthpy import Synth

    client = Synth()
    await client.namespace.delete_collection(namespace="dev", collection="users")
    await client.namespace.delete_namespace(namespace="dev", erase=True)


columns = [
    "job",
    "ssn",
    "name",
    "sex",
    "address",
    "mail",
    "birthdate",
    "created_at",
    "last_logged_in_ip",
    "num_logins",
]


def fancy_dataframe(data):
    return pd.DataFrame.from_dict(data)[columns]


def pretty_print(json_object):
    json_str = json.dumps(json_object, indent=4, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))


class Tracker:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        print(self.msg)

    def __exit__(self, type, value, traceback):
        print("Done!")
