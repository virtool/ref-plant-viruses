import copy
import json
import pytest
import tempfile
import subprocess


@pytest.fixture("session")
def built_json_file():
    with tempfile.NamedTemporaryFile(mode="r") as f:
        subprocess.call(["python", "scripts/build.py", "-V", "v1.0.1", "-f", f.name, "src"])
        data = json.load(f)

    return data


@pytest.fixture
def built_json(built_json_file):
    return copy.deepcopy(built_json_file)



