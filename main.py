from pathlib import Path
import datetime
import os
from typing import Optional
import subprocess
import re
import time

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
) -> None:
    wget_command = (
f"""wget \
    --recursive \
    --page-requisites \
    --adjust-extension \
    --span-hosts \
    --convert-links \
    --restrict-file-names=windows \
    --directory-prefix {export_dir} \
    --domains {TARGET_DOMAIN} \
    --no-parent \
    {target_url}
""")
    print(f"Running {wget_command}")
    proc = subprocess.run(wget_command, shell=True, capture_output=True)
    print(proc.stdout)


def inital_download(
    export_dir: str
) -> None:
    wget(
        target_url=PRIMARY_URL,
        export_dir=export_dir
    )


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

    print(file_list)


    possible_files: list[str] = []
    # searches for any .css .js or .html file with one or more character name.
    # "" '' or `` enclosed strings with out "'`,;&
    pattern = re.compile("[\"\`\'][^,\"\'\`&;]+(\.css|\.js|.html)[\"\`\']")
    for file_path in file_list:
        print(f"Scaning '{file_path}' for other missed files")
        for i, line in enumerate(open(file_path)):
            for match in re.finditer(pattern, line):
                print('Found on line %s: %s' % (i+1, match.group()))
                possible_files.append(match.group())

    print(possible_files)

    results: str = []
    # clean the captures
    for x in possible_files:
        x = x.replace('"', "")
        x = x.replace("'", "")
        x = x.replace("`", "")
        if x not in ["Node.js"]:
            results.append(x)

    print(results)
    return results


def main() -> int:

    export_dir = create_project_dir()
    inital_download(
        export_dir=export_dir
    )
    # # seems like takes a second for files to show up
    # time.sleep(1)
    assets_list = find_all_assets(
        export_dir=export_dir
    )

if __name__ == "__main__":
    main()
