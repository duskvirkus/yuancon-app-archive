from pathlib import Path
import datetime
import os
from typing import Optional

def create_project_dir(
    export_dir_name: Optional[str] = None,
) -> Path:
    PROJECT_ROOT = Path(__file__).parent
    CAPTURE_DIR = PROJECT_ROOT / "capture"
    
    if not export_dir_name:
        export_dir_name = datetime.datetime.now().replace(microsecond=0).isoformat()
    export_dir: Path = CAPTURE_DIR / export_dir_name
    print(f"Creating export_dir '{export_dir}'")
    os.mkdir(export_dir)
    return export_dir

def inital_download() -> None:
    pass

def recurssive_assets() -> None:
    pass


def main() -> int:

    export_dir = create_project_dir()
    inital_download()
    recurssive_assets()

if __name__ == "__main__":
    main()
