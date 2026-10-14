from pathlib import Path
import shutil


TEXT_FOLDER = Path(__file__).resolve().parent / "uploads" / "text"


def get_text_file_path(filename):
    if (
        not filename
        or Path(filename).name != filename
        or "/" in filename
        or "\\" in filename
        or filename in {".", ".."}
    ):
        raise ValueError("Use a filename only; folder paths are not allowed.")

    if Path(filename).suffix.lower() != ".txt":
        raise ValueError("Only .txt files are allowed for these operations.")

    TEXT_FOLDER.mkdir(parents=True, exist_ok=True)
    folder_path = TEXT_FOLDER.resolve()
    file_path = (folder_path / filename).resolve()

    if file_path.parent != folder_path:
        raise ValueError("The requested file must be inside the text folder.")

    return file_path


def create_text_file(filename):
    file_path = get_text_file_path(filename)

    with file_path.open("x", encoding="utf-8"):
        pass

    return filename


def write_text_file(filename, content):
    file_path = get_text_file_path(filename)
    file_path.write_text(content, encoding="utf-8")
    return filename


def append_text_file(filename, content):
    file_path = get_text_file_path(filename)

    with file_path.open("a", encoding="utf-8") as file:
        file.write(content)

    return filename


def read_text_file(filename):
    file_path = get_text_file_path(filename)
    return file_path.read_text(encoding="utf-8")


def read_text_file_lines(filename):
    file_path = get_text_file_path(filename)

    with file_path.open("r", encoding="utf-8") as file:
        return [line.rstrip("\r\n") for line in file]


def text_file_exists(filename):
    file_path = get_text_file_path(filename)
    return file_path.is_file()


def rename_text_file(filename, new_filename):
    source_path = get_text_file_path(filename)
    destination_path = get_text_file_path(new_filename)

    if not source_path.is_file():
        raise FileNotFoundError(filename)
    if destination_path.exists():
        raise FileExistsError(new_filename)

    source_path.rename(destination_path)
    return new_filename


def copy_text_file(filename, new_filename):
    source_path = get_text_file_path(filename)
    destination_path = get_text_file_path(new_filename)

    if not source_path.is_file():
        raise FileNotFoundError(filename)
    if destination_path.exists():
        raise FileExistsError(new_filename)

    shutil.copyfile(source_path, destination_path)
    return new_filename


def delete_text_file(filename):
    file_path = get_text_file_path(filename)

    if not file_path.is_file():
        raise FileNotFoundError(filename)

    file_path.unlink()
    return filename


def get_text_file_size(filename):
    file_path = get_text_file_path(filename)

    if not file_path.is_file():
        raise FileNotFoundError(filename)

    return file_path.stat().st_size