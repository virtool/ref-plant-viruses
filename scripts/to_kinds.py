import os
import json
import arrow
import argparse

parser = argparse.ArgumentParser(description="Rename virus.json files to kind.json")

parser.add_argument(
    "src",
    type=str,
    help="the path to the reference src directory",
)

args = parser.parse_args()

src_path = args.src

for alpha in os.listdir(src_path):
        paths = [os.path.join(src_path, alpha, kind) for kind in os.listdir(os.path.join(src_path, alpha))]

        for path in paths:
            if "virus.json" in os.listdir(path):
                os.rename(
                    os.path.join(path, "virus.json"),
                    os.path.join(path, "kind.json")
                )
            