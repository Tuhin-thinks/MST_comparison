from pathlib import Path
from typing import Union

from MST import MST
from config import ConfigSingleton

config = ConfigSingleton()
config.set_config_filepath(Path(__file__).parent.joinpath("config.json"))


def compare_mst_blocks(desktop_file: Union[Path, str], mow_file: [str, Path], pre_reports: str = ""):
    """Compare two MST_DATA blocks."""

    mst_string_1 = read_mst_string(desktop_file)
    mst_string_2 = read_mst_string(mow_file)

    mst_desktop = MST(mst_string_1, name="desktop")
    mst_web = MST(mst_string_2, name="web")

    match, report_str = mst_desktop.compare(mst_web)
    display_str = f"{pre_reports}\n" \
                  f"{report_str}\n" \
                  f"{'__' * 40}\n"
    return match, display_str


def read_mst_string(file_path: Union[str, Path]):
    """Read MST_DATA string from file."""
    with open(file_path, "r") as f:
        mst_string = f.read()

    return mst_string


def execute_all_cases(cases_dir: Union[str, Path]):
    """Execute all cases in the given directory."""
    cases_dir = Path(cases_dir)
    cases_file_mapping = {}
    pre_reports = ""

    for case_file in cases_dir.iterdir():
        if case_file.is_file() and case_file.name.endswith(".mst"):
            name_parts = case_file.name.split("__")
            case_name = name_parts[0]
            cases_file_mapping.setdefault(case_name, {}).update({name_parts[1]: case_file})

    for case, file_mapping in cases_file_mapping.items():
        writer = open(f"Report_{case}", 'w')
        pre_reports += f"\nCase: {case}"
        desktop_file = file_mapping.get("desktop")
        web_file = file_mapping.get("MOW")

        if not desktop_file:
            pre_reports += "\nDesktop file not found"
            continue

        if not web_file:
            pre_reports += "\nWeb file not found"
            continue

        match, report_str = compare_mst_blocks(desktop_file, web_file, pre_reports)
        pre_reports = ""
        print(report_str, file=writer)
        writer.close()


def execute_single_case(case_dir: Union[str, Path], required_case_name: str):
    """Execute a single case."""
    case_dir = Path(case_dir)

    case_file_mapping = {}
    for case_file in case_dir.iterdir():
        if case_file.is_file() and case_file.name.endswith(".mst") and case_file.name.startswith(required_case_name):
            name_parts = case_file.name.split("__")
            case_name = name_parts[0]
            case_file_mapping.setdefault(case_name, {}).update({name_parts[1]: case_file})

    if not case_file_mapping:
        raise FileNotFoundError(f"Case {required_case_name} not found in {case_dir}")

    writer = open(f"Report_{required_case_name}", 'w')
    for case, file_mapping in case_file_mapping.items():
        print(f"Case: {case}", file=writer)
        desktop_file = file_mapping.get("desktop")
        web_file = file_mapping.get("MOW")

        if not desktop_file:
            print("Desktop file not found")
            continue

        if not web_file:
            print("Web file not found")
            continue

        match, report_str = compare_mst_blocks(desktop_file, web_file)
        writer = open(f"Report_{case}", 'w')
        print(report_str, file=writer)
    writer.close()


if __name__ == '__main__':
    DATA_DIR = "MST_DATA"
    # execute_single_case(DATA_DIR, "HB_Test6")
    execute_all_cases(DATA_DIR)
