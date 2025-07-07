import os
from pathlib import Path
from core.config import COLOR_SPACE_RULES
import re


def detect_map_type(filename : str) -> str:
    name = normalize_filename(filename)

    for key in COLOR_SPACE_RULES:
        if key.lower() in name:
            return key
    return "Unknown"


def scan_exr_files(folder_path : str):
    folder = Path(folder_path)
    exr_files = list(folder.glob("*.exr"))
    results = []

    for file_path in exr_files:
        map_type = detect_map_type(file_path.name)
        color_space = COLOR_SPACE_RULES.get(map_type, "ACEScg")
        results.append({
            "filename" : file_path.name,
            "fullpath" : str(file_path),
            "map_type" : map_type,
            "color_space" : color_space,
            "status" : "Pending"
        })
    return results


def normalize_filename(filename : str) -> str:
    name = Path(filename).stem
    name = re.sub(r'\d{4}$', '', name)
    name = name.replace("-", "_").replace(" ", "_").lower()
    return name
