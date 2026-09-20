from argparse import ArgumentParser
from datetime import datetime
from dataclasses import dataclass
from time import sleep
import requests
import os

BASE_URL = "https://my.epitech.eu/api/"
FILES_DIR = "files"


@dataclass
class ExtractionInfo:
    year: int
    module: str
    city: str
    token: str

    def __init__(self, year: int, module: str, city: str, token: str):
        self.year = year
        self.module = module
        self.city = city
        self.token = token


def get_project_ids_from_module(info: ExtractionInfo) -> list[int]:
    url = f"{BASE_URL}/units/{info.year}/{info.module}/{info.city}?expanded=true"

    res = requests.get(url, headers={"Authorization": f"Bearer {info.token}"})

    print(res)

    if not res.ok:
        raise Exception("Project ids not found for module")

    res = res.json()

    ids = []
    for project in res["projectInstances"]:
        ids.append(project["id"])

    return ids


def get_student_resources_file_names(
    info: ExtractionInfo, project_id: int
) -> list[str]:
    url = f"{BASE_URL}/units/{info.year}/{info.module}/{info.city}/projects/{project_id}/files/students"

    res = requests.get(url, headers={"Authorization": f"Bearer {info.token}"})

    if not res.ok:
        raise Exception(f"Resources not found for project {project_id}")

    res = res.json()

    files = []
    for resource in res:
        files.append(resource["name"])

    return files


def get_link_to_resource(info: ExtractionInfo, project_id: int, file: str) -> str:
    url = f"{BASE_URL}/units/{info.year}/{info.module}/{info.city}/projects/{project_id}/files/students/{file}"

    res = requests.get(url, headers={"Authorization": f"Bearer {info.token}"})

    if not res.ok:
        raise Exception(f"Link not found for file {file}")

    return res.text


def download_link(link: str, file_name: str, files_dir: str = FILES_DIR):
    if not os.path.exists(files_dir):
        os.mkdir(files_dir)

    res = requests.get(link, stream=True)

    if not res.ok:
        raise Exception("File couldn't be downloaded")

    # TODO: could append module & project name to each directory
    with open(f"{files_dir}/{file_name}", "wb") as f:
        for chunk in res.iter_content(chunk_size=8192):
            f.write(chunk)


def main() -> None:
    args = ArgumentParser()
    _ = args.add_argument("--module", help="Module to extract", type=str, required=True)
    _ = args.add_argument(
        "--year",
        help="Get the year (default: current year)",
        type=int,
        default=datetime.now().year,
        required=False,
    )
    _ = args.add_argument(
        "--city", help="City to extract from", type=str, required=True
    )
    _ = args.add_argument(
        "--files-dir",
        help="Files dir to extract to (default: ./files/)",
        type=str,
        default=FILES_DIR,
        required=False,
    )
    args = args.parse_args()

    token = input(
        'Enter your token (enter in your console: `JSON.parse(window.localStorage.getItem("@account")).token`): '
    )

    info = ExtractionInfo(args.year, args.module, args.city, token)

    project_ids = get_project_ids_from_module(info)

    for project_id in project_ids:
        try:
            files = get_student_resources_file_names(info, project_id)

            for file in files:
                try:
                    link = get_link_to_resource(info, project_id, file)
                    download_link(link, file, args.files_dir)
                    print(f"Downloaded {file}")
                except Exception as e:
                    print(e)

                sleep(3)
        except Exception as e:
            print(e)

        sleep(5)


if __name__ == "__main__":
    main()
