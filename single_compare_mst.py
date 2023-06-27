from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import Union

import batch_compare_mst
from config import ConfigSingleton

REPORT_DIR = Path(__file__).parent.joinpath("Reports")
REPORT_DIR.mkdir(exist_ok=True)
config = ConfigSingleton()


def start_checking(first_file: Union[str, Path], second_file: Union[str, Path]):
    """
    Function to compare 2 files and generate a report for the mismatching keys/values.

    Args:
        first_file (str): First file to compare.
        second_file (str): Second file to compare.
    """
    if not first_file.is_file():
        raise FileNotFoundError(f"File {first_file} not found.")
    elif not second_file.is_file():
        raise FileNotFoundError(f"File {second_file} not found.")

    match, report_str = compare_mst.compare_mst_blocks(
        desktop_file=first_file,
        mow_file=second_file,
        pre_reports=""
    )
    report_filename = f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{first_file.stem}_{second_file.stem}.txt"
    report_filepath = Path(REPORT_DIR, report_filename)
    with open(report_filepath, 'w') as writer:
        writer.write(report_str + "\n")

    print(f"Report file written to: {report_filepath}")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('first_file', help='First file to compare')
    parser.add_argument('second_file', help='Second file to compare')
    parser.add_argument('config_json_path', help='Path to config.json file', nargs='?', default=None)

    args = parser.parse_args()
    if args.config_json_path:
        config.set_config_filepath(Path(args.config_json_path))

    start_checking(Path(args.first_file), Path(args.second_file))
