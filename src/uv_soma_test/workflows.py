import tempfile
from pathlib import Path

import spatialdata_io as sdio
import tiledbsoma
import tiledbsoma.io.spatial
from scanpy.datasets._datasets import _download_visium_dataset

from uv_soma_test.config import get_data_dir, get_dataset

MEASUREMENT_NAME = "RNA"
SCENE_NAME = "scene0"


def download_visium_data(config, dataset_dir=None):
    dataset = get_dataset(config)
    if dataset_dir is None:
        data_dir = get_data_dir(config)
    else:
        data_dir = Path(dataset_dir)

    dataset_dir = _download_visium_dataset(
        sample_id=dataset["experiment_name"],  # type: ignore
        spaceranger_version=dataset["spaceranger_version"],  # type: ignore
        base_dir=data_dir,
    )
    return Path(dataset_dir)


def spatialdata_direct(config, dataset_dir=None):
    """Workflow for converting visium data directly to spatialdata."""
    if dataset_dir is None:
        dataset_dir = download_visium_data(config)
    else:
        dataset_dir = Path(dataset_dir)
    dataset = get_dataset(config)
    exp_name = dataset["experiment_name"].lower()
    sdata = sdio.visium(path=dataset_dir, dataset_id=exp_name)
    return sdata


def tiledbsoma_spatialdata(config, dataset_dir=None):
    """Workflow for visium -> tiledbsoma -> spatialdata."""
    if dataset_dir is None:
        dataset_dir = download_visium_data(config)
    else:
        dataset_dir = Path(dataset_dir)

    dataset = get_dataset(config)
    experiment_uri = tempfile.mkdtemp(prefix=f"soma-{dataset['experiment_name']}-")
    tiledbsoma.io.spatial.from_visium(
        experiment_uri=experiment_uri,
        input_path=dataset_dir,
        measurement_name=MEASUREMENT_NAME,
        scene_name=SCENE_NAME,
        image_channel_first=True,
    )
    with tiledbsoma.Experiment.open(experiment_uri) as exp:
        sdata = tiledbsoma.io.spatial.to_spatialdata(
            experiment=exp,
            measurement_names=[MEASUREMENT_NAME],
        )
    return sdata
