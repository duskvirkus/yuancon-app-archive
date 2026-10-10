from pathlib import Path
import datetime
import os
from typing import Optional
import subprocess
import re

PROJECT_ROOT = Path(__file__).parent
CAPTURE_DIR = PROJECT_ROOT / "capture"
TARGET_DOMAIN = "yuancon.app"
PRIMARY_URL = "https://yuancon.app/"


def create_project_dir(
    export_dir_name: Optional[str] = None,
) -> Path:
    if not export_dir_name:
        export_dir_name = datetime.datetime.now().replace(microsecond=0).isoformat()
    export_dir: Path = CAPTURE_DIR / export_dir_name
    print(f"Creating export_dir '{export_dir}'")
    os.mkdir(export_dir)
    return export_dir


def wget(
    target_url: str,
    export_dir: str,
    target_domain: str = TARGET_DOMAIN
) -> bool:
    wget_command = (
f"""wget \
    --recursive \
    --page-requisites \
    --adjust-extension \
    --span-hosts \
    --convert-links \
    --no-clobber \
    --restrict-file-names=windows \
    --directory-prefix {export_dir} \
    --domains {TARGET_DOMAIN} \
    --no-parent \
    {target_url}
""")
    # print(f"Running {wget_command}")
    proc = subprocess.run(wget_command, shell=True, capture_output=True)


def inital_download(
    export_dir: str
) -> None:
    wget(
        target_url=PRIMARY_URL,
        export_dir=export_dir
    )
    print("Downloaded inital capture.")


def find_all_assets(
    export_dir: str
) -> list[str]:
    """
    Here we search through website source files to find any assets that are mentioned.

    When looking at the source files I noticed that missing files are mentioned in source files. So we find them with regex.
    """

    file_list: list[Path] = []
    for root, dirs, files in os.walk(export_dir):
        for file in files:
            if file.endswith(".js") or file.endswith('.css') or file.endswith('.html'):
                file_list.append(Path(root) / file)

    possible_files: list[str] = []
    # searches for any .css .js or .html file with one or more character name.
    # "" '' or `` enclosed strings with out "'`,;&
    pattern = re.compile("[\"\`\'][^,\"\'\`&;]+(\.css|\.js|.html)[\"\`\']")
    for file_path in file_list:
        # print(f"Scaning '{file_path}' for other missed files")
        for i, line in enumerate(open(file_path)):
            for match in re.finditer(pattern, line):
                # print('Found on line %s: %s' % (i+1, match.group()))
                possible_files.append(match.group())

    results: str = []
    # clean the captures
    for x in possible_files:
        x = x.replace('"', "")
        x = x.replace("'", "")
        x = x.replace("`", "")

        if x.startswith("./"):
            x = x.replace("./", "")

        if x.startswith(PRIMARY_URL):
            x = x.replace(PRIMARY_URL, "")

        if x not in ["Node.js"] and (not x.startswith("http")):
            results.append(x)
        else:
            print(f"WARNING: Skipping {x}")

    return results


def download_if_not_local(
    export_dir: str,
    to_download: str,
) -> bool:
    local_dir = export_dir / "yuancon.app"
    if not os.path.isfile(local_dir / to_download):
        # print(f"'{to_download}' is not at '{local_dir / to_download}' attempting download.")
        finished = wget(
            target_url=PRIMARY_URL + to_download,
            export_dir=export_dir
        )
        return finished
    return False


def get_file_count(
    target_dir: str
) -> int:
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            count += 1
    return count


def download_missing(
    export_dir: str
) -> bool:
    download_list = find_all_assets(
        export_dir=export_dir
    )

    # I know it's crude but we just gonna check the file count 
    # to see if anything was downloaded cause capturing output is annoying
    before_file_count: int = get_file_count(target_dir=export_dir)

    for to_download in download_list:
        downloaded = download_if_not_local(
            export_dir=export_dir,
            to_download=to_download,
        )

    after_file_count: int = get_file_count(target_dir=export_dir)
    print(f"download_missing() file count before '{before_file_count}' after '{after_file_count}'")
    return before_file_count != after_file_count

def download_missing_recursive(
    export_dir: str,
    keep_running: bool = True,
) -> None:
    print("Recursivly checking for missing files. Will continue trying until can't find anything else to download.")
    if not keep_running:
        return

    was_something_downloaded = download_missing(
        export_dir=export_dir,
    )
    download_missing_recursive(
        export_dir=export_dir,
        keep_running=was_something_downloaded,
    )


def main() -> int:

    export_dir = create_project_dir()
    inital_download(
        export_dir=export_dir
    )
    download_missing_recursive(
        export_dir=export_dir,
    )

if __name__ == "__main__":
    main()
