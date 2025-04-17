# utils/packager.py
import os
import shutil
from pathlib import Path
from tempfile import mkdtemp

def package_function(function_data: dict) -> tuple[str, str]:
    language = function_data["language"]
    code = function_data["code"]
    temp_dir = mkdtemp()
    file_name = "function.py" if language == "python" else "function.js"
    file_path = os.path.join(temp_dir, file_name)
    with open(file_path, "w") as f:
        f.write(code)
    return temp_dir, file_name

def cleanup_temp_dir(temp_dir: str):
    shutil.rmtree(temp_dir, ignore_errors=True)
