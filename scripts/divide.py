import os
import json
import shutil
import argparse

OTU_KEYS = [
    "_id",
    "name",
    "abbreviation"
]

ISOLATE_KEYS = [
    "id",
    "source_type",
    "source_name",
    "default"
]

SEQUENCE_KEYS = [
    "_id",
    "accession",
    "definition",
    "host",
    "sequence"
]

parser = argparse.ArgumentParser(description="Divide a reference.json file from a Virtool into a src tree")

parser.add_argument(
    "src",
    type=str,
    help="the path to input reference.json file",
)

parser.add_argument(
    "-o",
    type=str,
    dest="output",
    default="src",
    help="the output path for divided source directory tree"
)

args = parser.parse_args()

shutil.rmtree(args.output, ignore_errors=True)
os.mkdir(args.output)

with open(args.src, "r") as export_handle:
    data = json.load(export_handle)

    for otu in data["otus"]:

        lower_name = otu["name"].lower()
        first_letter = lower_name[0]

        try:
            os.mkdir(os.path.join(args.output, first_letter))
        except FileExistsError:
            pass

        otu_path = os.path.join(args.output, first_letter, lower_name.replace(" ", "_").replace("/", "_"))
        os.mkdir(otu_path)

        isolates = otu.pop("isolates")

        with open(os.path.join(otu_path, "otu.json"), "w") as f:
            json.dump({key: otu[key] for key in OTU_KEYS}, f, indent=4)

        for isolate in isolates:
            isolate_path = os.path.join(otu_path, isolate["id"])
            os.mkdir(isolate_path)

            sequences = isolate.pop("sequences")

            with open(os.path.join(isolate_path, "isolate.json"), "w") as f:
                json.dump({key: isolate[key] for key in ISOLATE_KEYS}, f, indent=4)

            for sequence in sequences:
                with open(os.path.join(isolate_path, "{}.json".format(sequence["_id"])), "w") as f:
                    json.dump({key: sequence[key] for key in SEQUENCE_KEYS}, f, indent=4)

    with open(os.path.join(args.output, "meta.json"), "w") as f:
        json.dump({
            "data_type": data["data_type"],
            "organism": data["organism"]
        }, f)
