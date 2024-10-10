import logging
import shutil
from pathlib import Path

from textnode import TextNode, TextType


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename="logs.txt",
                    filemode="w")

LOGGER = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.resolve()
STATIC_DIR = BASE_DIR.parent / "static"
PUBLIC_DIR = BASE_DIR.parent / "public"


def main():
    copy_content(source=STATIC_DIR, destination=PUBLIC_DIR)


def copy_content(source: Path, destination:Path) -> None:
    """ Copy and write all content from a source directory 
        to a destination directory recursively
    """
    if not source.exists():
        raise Exception(f"Not found: source directory {source}")
    
    delete_content(destination)

    for content in source.iterdir():

        if content.is_file():
            new_destination = destination / content.name
            shutil.copy(src=content, dst=new_destination)
            LOGGER.info(f"FILE COPIED : FROM {content} -> TO {new_destination}")

        elif content.is_dir():
            new_destination = destination / content.name
            new_destination.mkdir(exist_ok=True)
            LOGGER.info(f"DIRECTORY CREATED : FROM {content} -> TO {new_destination}")
            copy_content(source=content, destination=new_destination)


def delete_content(destination:Path) -> None:
    """ Delete files and directories of destination directory
    """
    if not destination.exists():
        raise Exception(f"Not found: destination directory {destination}")

    for content in destination.iterdir():
        if content.is_file():
            content.unlink()
            LOGGER.info(f"FILE DELETED : {content}")
        elif content.is_dir():
            shutil.rmtree(content)
            LOGGER.info(f"DIRECTORY DELETED : {content}")


if __name__ == "__main__":
    main()



