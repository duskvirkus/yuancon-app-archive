from pathlib import Path
import datetime
import os
from typing import Optional
import subprocess


PROJECT_ROOT = Path(__file__).parent
CAPTURE_DIR = PROJECT_ROOT / "capture"
TARGET_DOMAIN = "yuancon.app"


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


def inital_download(export_dir: str) -> None:
    wget(
        target_url="https://yuancon.app/",
        export_dir=export_dir
    )


def recurssive_assets() -> None:
    pass


def main() -> int:

    export_dir = create_project_dir()
    inital_download(
        export_dir=export_dir
    )
    recurssive_assets()

if __name__ == "__main__":
    main()
