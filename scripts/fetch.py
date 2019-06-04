import collections
import json
import os
import requests

BASE_PATH = "src"
TSV_PATH = "taxid_cache.tsv"


def compare_accessions(accessions, existing):
    return strip_versions_from_accessions(accessions) - strip_versions_from_accessions(existing)


def fetch_taxids():
    if os.path.isfile(TSV_PATH):
        return

    resp = requests.get("https://www.ncbi.nlm.nih.gov/genomes/GenomesGroup.cgi?taxid=10239&cmd=download2")

    with open("taxid_cache.tsv", "w") as f:
        f.write(resp.text)


def get_existing_accessions():
    accessions = set()

    for letter in os.listdir(BASE_PATH):
        if letter == "meta.json":
            continue

        letter_path = os.path.join(BASE_PATH, letter)

        for lower_name in os.listdir(letter_path):
            if lower_name == "otu.json":
                continue

            otu_path = os.path.join(letter_path, lower_name)

            for isolate_name in os.listdir(otu_path):
                if isolate_name == "otu.json":
                    continue

                isolate_path = os.path.join(otu_path, isolate_name)

                for sequence_file_name in os.listdir(isolate_path):
                    if sequence_file_name == "isolate.json":
                        continue

                    sequence_path = os.path.join(isolate_path, sequence_file_name)

                    with open(sequence_path, "r") as json_f:
                        sequence = json.load(json_f)
                        accessions.add(sequence["accession"])

    return accessions


def parse_taxid_cache():
    accessions = set()
    complete = collections.defaultdict(dict)

    with open(TSV_PATH, "r") as f:
        for line in f:
            if line[0] == "#":
                continue

            accession, origin, host, taxonomy, name, seq_type = line.rstrip().split("\t")

            if "plant" in host:
                # print("\t".join([accession, host, name]))
                for acc in accession.split(","):
                    accessions.add(acc)

                    complete[acc] = {
                        "host": host,
                        "name": name
                    }

    return accessions, complete


def strip_versions_from_accessions(accessions):
    return {accession.split(".")[0] for accession in accessions}


def run():
    fetch_taxids()
    accessions, complete = parse_taxid_cache()
    existing = get_existing_accessions()
    missing = compare_accessions(accessions, existing)

    sortable = list()

    for acc in missing:
        com = complete[acc]
        sortable.append((acc, com["name"]))

    for com in sorted(sortable, key=lambda l: l[1]):
        print("\t".join(com))


if __name__ == "__main__":
    run()
