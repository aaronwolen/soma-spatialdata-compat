import anndata as ad
from spatialdata._types import DataTree

from uv_soma_test.config import load_config
from uv_soma_test.constants import MEASUREMENT_NAME, SCENE_NAME
from uv_soma_test.workflows import spatialdata_direct, tiledbsoma_spatialdata


def test_spatialdata_direct():
    """Test spatialdata_direct workflow."""
    config = load_config()
    sdata = spatialdata_direct(config)
    assert sdata is not None
    assert sdata.table is not None
    assert len(sdata.images) > 0


def test_tiledbsoma_spatialdata():
    """Test tiledbsoma_spatialdata workflow."""
    config = load_config()
    sdata = tiledbsoma_spatialdata(config)
    assert sdata is not None

    assert MEASUREMENT_NAME in sdata.tables.keys()
    table = sdata.tables[MEASUREMENT_NAME]
    assert isinstance(table, ad.AnnData)

    assert len(sdata.images) > 0
    assert f"{SCENE_NAME}_tissue" in sdata.images.keys()

    images = sdata.images[f"{SCENE_NAME}_tissue"]
    assert isinstance(images, DataTree)
    assert len(images) == 2
