import os
import json
import arrow
import argparse


DELETED_KEYS = [
    "user",
    "version",
    "imported",
    "last_indexed_version",
    "verified"
]

parser = argparse.ArgumentParser(description="Building a kinds.json file from a virtool-databse src directory")

parser.add_argument(
    "src",
    type=str,
    help="the path to the database src directory",
)

parser.add_argument(
    "-V",
    type=str,
    dest="version",
    default=None,
    help="the version string to include in the kinds.json file"
)

parser.add_argument(
    "-f",
    type=str,
    dest="output",
    default="reference.json",
    help="the output path for the kinds.json file"
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

    kinds = list()

    alpha_paths = os.listdir(src_path)

    alpha_paths.remove("meta.json")

    for alpha in alpha_paths:
        kind_paths = [os.path.join(src_path, alpha, kind) for kind in os.listdir(os.path.join(src_path, alpha))]

        for kind_path in kind_paths:

            with open(os.path.join(kind_path, "kind.json"), "r") as f:
                kind = json.load(f)

            kind["isolates"] = list()

            isolate_ids = [i for i in os.listdir(kind_path) if i != "kind.json" and i[0] != "."]

            for isolate_path in [os.path.join(kind_path, i) for i in isolate_ids]:
                with open(os.path.join(isolate_path, "isolate.json"), "r") as f:
                    isolate = json.load(f)

                with open(os.path.join(isolate_path, "sequences.json"), "r") as f:
                    isolate["sequences"] = json.load(f)

                with open(os.path.join(isolate_path, "sequences.fa"), "r") as f:
                    sid = None
                    seq = list()

                    for line in f:
                        if line[0] == ">":
                            if sid:
                                for sequence in isolate["sequences"]:
                                    if sequence["_id"] == sid:
                                        sequence["sequence"] = "".join(seq)
                                        break

                            sid = line.rstrip().replace(">", "")
                            seq = list()

                        elif line:
                            seq.append(line.rstrip())

                    if sid:
                        for sequence in isolate["sequences"]:
                            if sequence["_id"] == sid:
                                sequence["sequence"] = "".join(seq)

                kind["isolates"].append(isolate)

            kinds.append(kind)

    with open(args.output, "w") as f:
        data.update({
            "data": kinds,
            "version": args.version,
            "created_at": arrow.utcnow().isoformat()            
        })

        json.dump(data, f, indent=4)
