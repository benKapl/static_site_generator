import logging
import re
import shutil
from pathlib import Path

from page_formatter import extract_title, markdown_to_html_node


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename="logs.txt",
                    filemode="w")

LOGGER = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.resolve()
STATIC_DIR = BASE_DIR.parent / "static"
PUBLIC_DIR = BASE_DIR.parent / "public"

TEMPLATE_PATH = BASE_DIR.parent / "template.html"
CONTENT_DIR = BASE_DIR.parent / "content"


def main():
    copy_content(source=STATIC_DIR, destination=PUBLIC_DIR)
    generate_page(from_path=(CONTENT_DIR / "index.md"), 
                  template_path=TEMPLATE_PATH, 
                  dest_path=PUBLIC_DIR)


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


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    LOGGER.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = from_path.read_text()
    template_content = template_path.read_text()

    title = extract_title(md_content)
    title_placeholder = "{{ Title }}"
    html_content = markdown_to_html_node(md_content).to_html()
    content_placeholder = "{{ Content }}"

    full_html_page = template_content.replace(title_placeholder, title) \
                                     .replace(content_placeholder, html_content)
    
    # html_file = dest_path / f"{from_path.stem}.html"
    html_file = dest_path / "index.html"
    html_file.touch
    html_file.write_text(full_html_page)

    
if __name__ == "__main__":
    main()



    # print(TEMPLATE_PATH)
    # print(MARKDOWN_DIR)

