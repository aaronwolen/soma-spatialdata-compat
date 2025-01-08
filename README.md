# Testing fix for SpatialData compatibility issue

## Setup

`uv` is required to run the tests. Setup the project with:

```sh
uv sync
source .venv/bin/activate
```

## Running the tests

```sh
uv-soma-test spatialdata-direct
uv-soma-test tiledbsoma-spatialdata
```
