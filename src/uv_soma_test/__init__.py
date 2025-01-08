import argparse

from uv_soma_test.config import load_config
from uv_soma_test.workflows import spatialdata_direct, tiledbsoma_spatialdata


def main():
    parser = argparse.ArgumentParser(
        description="Run workflows for spatial data with spatialdata and tiledbsoma"
    )
    parser.add_argument(
        "workflow",
        choices=["spatialdata-direct", "tiledbsoma-spatialdata"],
        help="Choose the workflow to execute",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to the config file.",
    )
    parser.add_argument(
        "--dataset-dir",
        type=str,
        default=None,
        help="Path to already downloaded dataset.",
    )

    args = parser.parse_args()
    config = load_config(args.config)

    if args.workflow == "spatialdata-direct":
        sdata = spatialdata_direct(config, dataset_dir=args.dataset_dir)
    elif args.workflow == "tiledbsoma-spatialdata":
        sdata = tiledbsoma_spatialdata(config, dataset_dir=args.dataset_dir)

    print("Successfully executed workflow.")
    print(f"SpatialData object: \n {sdata}")


if __name__ == "__main__":
    main()
