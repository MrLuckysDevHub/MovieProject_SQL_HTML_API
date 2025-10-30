import json

# Basic color codes
RED = "\033[91m"
RESET = "\033[0m"  # This resets the color back to default


def load_template_html(file_path: str) -> str:
    """Reads an HTML template file and returns its content as a string"""
    try:
        with open(file_path, "r") as handle:
            return handle.read()
    except IOError as e:
        print(
            f"{RED}HTML template file {file_path} could not be loaded IO error:{RESET} {e}"
        )
    except Exception as e:
        print(f"{RED}Try to load file {file_path}, system error:{RESET} {e}")
    return ""


def save_html(html_str: str, file_path: str) -> None:
    """Saves the given HTML string to a file"""
    try:
        with open(file_path, "w") as handle:
            handle.write(html_str)
    except IOError as e:
        print(f"{RED}HTML file {file_path} could not be saved IO error:{RESET} {e}")
    except Exception as e:
        print(f"{RED}Try to save file {file_path}, system error:{RESET} {e}")
