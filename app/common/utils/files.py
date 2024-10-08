import os
import glob

__all__ = ["upload_file", "model_list", "cleanup"]


def model_list(project_home_dir) -> list:
    models = []
    models_path = os.path.join(project_home_dir, 'models')
    model_files = glob.iglob(f"{models_path}/**/*.t7", recursive=True)
    for file in model_files:
        models.append("".join(file.split("/models/")[::-2]).rstrip("t7").rstrip(".").replace("/", "-"))
    return models


def upload_file(file, upload_dir):
    try:
        with open(f"{upload_dir}/{file.filename}", 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"message": "Error while uploading the file."}
    finally:
        file.file.close()


def cleanup(files: list):
    for file in files:
        os.remove(file)
