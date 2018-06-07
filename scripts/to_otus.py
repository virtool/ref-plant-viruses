import os
import json
import arrow
import argparse

parser = argparse.ArgumentParser(description="Rename kind.json files to otu.json")

parser.add_argument(
    "src",
    type=str,
    help="the path to the reference src directory",
)

args = parser.parse_args()

src_path = args.src

for alpha in os.listdir(src_path):
        if alpha == "meta.json":
            continue

        paths = [os.path.join(src_path, alpha, kind) for kind in os.listdir(os.path.join(src_path, alpha))]

        for path in paths:
            if "kind.json" in os.listdir(path):
                os.rename(
                    os.path.join(path, "kind.json"),
                    os.path.join(path, "otu.json")
                )
            