import logging
import shutil
from pathlib import Path

from page_formatter import extract_title, markdown_to_html_node


BASE_DIR = Path(__file__).parent.parent.resolve()
STATIC_DIR = BASE_DIR / "static"
PUBLIC_DIR = BASE_DIR / "public"
CONTENT_DIR = BASE_DIR / "content"

TEMPLATE_PATH = BASE_DIR / "template.html"
LOG_PATH = BASE_DIR / "logs.txt"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=LOG_PATH,
                    filemode="w")

LOGGER = logging.getLogger(__name__)


def main():
    copy_content(source=STATIC_DIR, destination=PUBLIC_DIR)
    generate_pages_recursive(dir_path_content=CONTENT_DIR, 
                             template_path=TEMPLATE_PATH, 
                             dest_dir_path=PUBLIC_DIR)


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
            LOGGER.info(f"DIRECTORY COPIED : FROM {content} -> TO {new_destination}")
            copy_content(source=content, destination=new_destination)

        else:
            raise Exception(f"invalid content: {content}")


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
    """ Create a html document from a markdown document.
    Takes as input : 
    - from_path: path of the markdown document
    - template_path: html template used to create the html document
    - dest_path: path of the newly created html document
    """
    LOGGER.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = from_path.read_text()
    template_content = template_path.read_text()

    title = extract_title(md_content)
    title_placeholder = "{{ Title }}"
    html_content = markdown_to_html_node(md_content).to_html()
    content_placeholder = "{{ Content }}"

    full_html_page = template_content.replace(title_placeholder, title) \
                                     .replace(content_placeholder, html_content)
    
    html_file = dest_path / f"{from_path.stem}.html" # defined path of document
    html_file.touch                                  # create document
    html_file.write_text(full_html_page)             # add content
    LOGGER.info(f"FILE CREATED : {html_file}")


def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path) -> None:
    """Generate all html documents from directory tree containing markdown files.
    Takes as input : 
    - dir_path_content: path of markdown content directory
    - template_path: html template used to create the html documents
    - dest_dir_path: path of the newly created html documents
    """
    for content in dir_path_content.iterdir():
        
        if content.is_file():
            generate_page(from_path=content, template_path=template_path, 
                          dest_path=dest_dir_path)

        elif content.is_dir():
            # Create destination directory
            new_dest_dir_path = dest_dir_path / content.name
            new_dest_dir_path.mkdir(exist_ok=True)
            LOGGER.info(f"DIRECTORY CREATED : FROM {content} -> TO {new_dest_dir_path}")
            # Generate pages in new directory
            generate_pages_recursive(dir_path_content=content, 
                                     template_path=template_path,
                                     dest_dir_path=new_dest_dir_path)

        else:
            raise Exception(f"invalid content: {content}")
        

if __name__ == "__main__":
    main()
    


