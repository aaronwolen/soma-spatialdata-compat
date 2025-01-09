import tempfile
from pathlib import Path

import spatialdata_io as sdio
import tiledbsoma
import tiledbsoma.io.spatial
from scanpy.datasets._datasets import _download_visium_dataset
from typing_extensions import Optional

from uv_soma_test.config import get_data_dir, get_dataset
from uv_soma_test.constants import MEASUREMENT_NAME, SCENE_NAME


def download_visium_data(config: dict, dataset_dir: Optional[str] = None) -> Path:
    dataset = get_dataset(config)
    if dataset_dir is None:
        data_dir = get_data_dir(config)
    else:
        data_dir = Path(dataset_dir)

    dataset_dir: Path = _download_visium_dataset(
        sample_id=dataset["experiment_name"],  # type: ignore
        spaceranger_version=dataset["spaceranger_version"],  # type: ignore
        base_dir=data_dir,
    )
    return Path(dataset_dir)


def spatialdata_direct(config: dict, dataset_dir: Optional[str] = None):
    """Workflow for converting visium data directly to spatialdata."""
    if dataset_dir is None:
        dataset_dir = download_visium_data(config)
    else:
        dataset_dir = Path(dataset_dir)
    dataset = get_dataset(config)
    exp_name = dataset["experiment_name"].lower()
    sdata = sdio.visium(path=dataset_dir, dataset_id=exp_name)
    return sdata


def tiledbsoma_spatialdata(
    config: dict,
    dataset_dir: Optional[str] = None,
    experiment_uri: Optional[str] = None,
    obs_spatial_presence: bool = True,
):
    """Workflow for visium -> tiledbsoma -> spatialdata."""
    dataset = get_dataset(config)

    if dataset_dir is None:
        dataset_dir = download_visium_data(config)
    else:
        dataset_dir = Path(dataset_dir)
    if experiment_uri is None:
        experiment_uri = tempfile.mkdtemp(prefix=f"soma-{dataset['experiment_name']}-")

    print(f"\nIngesting into experiment uri: {experiment_uri}\n")

    tiledbsoma.io.spatial.from_visium(
        experiment_uri=experiment_uri,
        input_path=dataset_dir,
        measurement_name=MEASUREMENT_NAME,
        scene_name=SCENE_NAME,
        image_channel_first=True,
        write_obs_spatial_presence=obs_spatial_presence,
    )
    with tiledbsoma.Experiment.open(experiment_uri) as exp:
        with exp.axis_query(
            measurement_name=MEASUREMENT_NAME,
        ) as query:
            print(f"Obs scene IDs: {query.obs_scene_ids()}")
            sdata = query.to_spatialdata(X_name="data")
    return sdata
