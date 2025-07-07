import os.path
import re
import OpenImageIO as oiio
from pathlib import Path


def insert_color_space_metadata(file_path : str, color_space: str, output_dir = None ) -> str:
    try:
        image = oiio.ImageBuf(file_path)
        spec = image.spec()
        spec.attribute("oiio:ColorSpace", color_space)
        spec.attribute("ColorSpace", color_space)

        src_path = Path(file_path)
        if output_dir is None:
            output_dir = src_path.parent/ "with_metadata"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)
        clean_name = clean_exr_filename(src_path.name)
        output_file = output_dir / clean_name
        success = oiio.ImageBufAlgo.copy(image).write(str(output_file))

        if not success:
            return ""

        return str(output_file)

    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return ""


def clean_exr_filename(original_name:str) -> str:
    """
    delete sufix like _ACES, _ACEScg, _raw, _utility
    keeps udims
    """
    name, ext = os.path.splitext(original_name)
    udim_match = re.search(r"(\d{4}$)", name)
    udim = udim_match.group(1) if udim_match else ""

    name = re.sub(r"(ACEScg|ACES|raw|utility|linear|Utility)", "", name, flags=re.IGNORECASE)

    name = re.sub(r"[\s\-]+", "_", name)
    name = re.sub(r"__+", "_", name)  # dobles underscores
    name = name.strip("_")

    if udim:
        name = re.sub(r"_?" + udim + r"$", "", name)
        clean_name = f"{name}.{udim}{ext}"
    else:
        clean_name = name + ext

    clean_name = clean_name.replace("..", ".")
    clean_name = clean_name.replace("_.", ".")

    return clean_name