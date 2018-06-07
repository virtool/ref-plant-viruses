# virtool-database

*An official virus reference database for Virtool*

[![Build Status](https://travis-ci.org/virtool/virtool-database.svg?branch=master)](https://travis-ci.org/virtool/virtool-database)

**This collection of virus records still requires major revision and curation. There are viral sequences that are
internal to the Centre For Plant Health and are not available in GenBank.**

## Description

This database consists of primarily of all curated plant virus genomes as
[published by NCBI](https://www.ncbi.nlm.nih.gov/genomes/GenomesGroup.cgi?taxid=10239). There are some other additions
in the form of:

- viroid sequences
- additions by the Centre for Plant Health staff as encountered during analysis
- additional isolates for NCBI-sourced viruses described above 

## Using

1. Download the ``viruses.json.gz`` file for the [latest release](https://github.com/virtool/virtool-database/releases/latest).
2. In a virgin instance of Virtool, go to the *Viruses* view and click on the *Import* link.
3. Follow the instructions to import the virus data.
4. Rebuild the index to use the virus data in analyses.

## Contributing

If you want to contribute more information to this database, please
[create an issue](https://github.com/virtool/virtool-database/issues/new) describing the addition.

We will move to a pull request-based contribution system as soon as possible.
