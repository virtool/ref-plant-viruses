import os
import json
import arrow
import shutil
import pytest
import subprocess

TEST_PATH = "tests/files/reference.json"
TEST_NO_INDENT_PATH = "tests/files/reference_no_indent.json"
TEST_NO_SCHEMA_PATH = "tests/files/reference_no_schema.json"
TEST_WITH_INDENT_PATH = "tests/files/reference_with_indent.json"


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

    assert built_json["name"] == version


def test_created_at(tmpdir):
    """
    Test that the version field is correctly set in the viruses.json file.

    """
    json_file = tmpdir.join("viruses.json")

    subprocess.call(["python", "scripts/build.py", "-f", str(json_file), "src"])

    built_json = json.load(json_file)

    created_at = arrow.get(built_json["created_at"])

    assert (arrow.utcnow() - created_at).seconds == 0


@pytest.mark.parametrize("indent", (True, False))
@pytest.mark.parametrize("schema", (True, False))
def test_divide_build(indent, schema, tmpdir):
    
    json_path = os.path.join(str(tmpdir), "reference.json")

    if schema:
        shutil.copyfile(TEST_NO_INDENT_PATH, json_path)
    else:
        shutil.copyfile(TEST_NO_SCHEMA_PATH, json_path)    

    src_path = os.path.join(str(tmpdir), "src")

    subprocess.call(["python", "scripts/divide.py", "-o", src_path, json_path])

    out_path = os.path.join(str(tmpdir), "out.json")

    command = [
        "python",
        "scripts/build.py",
        "-f", out_path,
        src_path
    ]

    if indent:
        command.append("-i")

    subprocess.call(command)

    expected_path = TEST_NO_INDENT_PATH

    if indent:
        expected_path = TEST_WITH_INDENT_PATH

    expected_size = os.path.getsize(expected_path)
    out_size = os.path.getsize(out_path)

    print(expected_size, out_size)

    assert abs(expected_size - out_size) < 10
