import os
import json
import arrow
import shutil
import pytest
import subprocess

from hashlib import sha256

TEST_FILE_PATH = "tests/files/build.json"


@pytest.mark.parametrize("version", [None, "v1.0.1", "v0.8.3"])
def test_version(version, tmpdir):
    """
    Test that the version field is correctly set in the viruses.json file.

    """
    json_file = tmpdir.join("viruses.json")

    command = ["python", "scripts/build.py", "-f", str(json_file), "src"]

    if version:
        command += ["-V", version]

    subprocess.call(command)

    built_json = json.load(json_file)

    assert built_json["version"] == version


def test_created_at(tmpdir):
    """
    Test that the version field is correctly set in the viruses.json file.

    """
    json_file = tmpdir.join("viruses.json")

    subprocess.call(["python", "scripts/build.py", "-f", str(json_file), "src"])

    built_json = json.load(json_file)

    created_at = arrow.get(built_json["created_at"])

    assert (arrow.utcnow() - created_at).seconds == 0


def test_divide_build(tmpdir):
    shutil.copy(TEST_FILE_PATH, str(tmpdir))

    json_path = os.path.join(str(tmpdir), "build.json")

    src_path = os.path.join(str(tmpdir), "src")

    subprocess.call(["python", "scripts/divide.py", "-o", src_path, json_path])

    out_path = os.path.join(str(tmpdir), "out.json")

    subprocess.call(["python", "scripts/build.py", "-f", out_path, src_path])

    assert abs(os.path.getsize(json_path) - os.path.getsize(out_path)) < 10
