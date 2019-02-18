import os
import json
import arrow
import argparse

OTU_KEYS = [
    "_id",
    "name",
    "abbreviation",
    "schema"
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

parser = argparse.ArgumentParser(description="Build a reference.json file from a virtool reference src directory")

parser.add_argument(
    "src",
    type=str,
    help="the path to the database src directory",
)

parser.add_argument(
    "-i", "--indent",
    dest="indent",
    action="store_true",
    default=False
)

parser.add_argument(
    "-V",
    type=str,
    dest="version",
    default=None,
    help="the version string to include in the reference.json file"
)

parser.add_argument(
    "-f",
    type=str,
    dest="output",
    default="reference.json",
    help="the output path for the reference.json file"
)

args = parser.parse_args()


if __name__ == "__main__":
    src_path = args.src

    try:
        with open(os.path.join(src_path, "meta.json"), "r") as f:
            meta = json.load(f)
    except FileNotFoundError:
        meta = dict()

    data = {
        "data_type": meta.get("data_type", "genome"),
        "organism": meta.get("organism", ""),
    }

    otus = list()

    alpha_paths = os.listdir(src_path)

    try:
        alpha_paths.remove("meta.json")
    except ValueError:
        pass

    used_ids = list()

    for alpha in alpha_paths:
        otu_paths = [os.path.join(src_path, alpha, otu) for otu in os.listdir(os.path.join(src_path, alpha))]

        for otu_path in otu_paths:

            with open(os.path.join(otu_path, "otu.json"), "r") as f:
                otu = json.load(f)

            otu["isolates"] = list()

            isolate_ids = [i for i in os.listdir(otu_path) if i != "otu.json" and i[0] != "."]

            for isolate_path in [os.path.join(otu_path, i) for i in isolate_ids]:
                with open(os.path.join(isolate_path, "isolate.json"), "r") as f:
                    isolate = json.load(f)

                sequence_ids = [i for i in os.listdir(isolate_path) if i != "isolate.json" and i[0] != "."]

                isolate["sequences"] = list()

                for sequence_path in [os.path.join(isolate_path, i) for i in sequence_ids]:
                    with open(sequence_path, "r") as f:
                        sequence = json.load(f)

                    isolate["sequences"].append(sequence)

                otu["isolates"].append(isolate)

            otus.append(otu)

    with open(args.output, "w") as f:
        data.update({
            "otus": otus,
            "name": args.version,
            "created_at": arrow.utcnow().isoformat()
        })

        indent = None
        
        if args.indent:
            indent = 4

        json.dump(data, f, indent=indent, sort_keys=True)
