import json

import zstandard as zstd
import tarfile


def desompress_from_ZST(filename):
    # Decompress the .zst file
    with open(filename + ".tar.zst", "rb") as compressed:
        dctx = zstd.ZstdDecompressor()
        with open(filename + ".tar", "wb") as decompressed:
            decompressed.write(dctx.decompress(compressed.read()))


def extract_from_tar(filename):
# Extract the .tar file
    with tarfile.open(filename + ".tar", "r") as tar:
        tar.extractall()


# Remove problematic fields recursively (if present)
def clean_data(obj):
    if isinstance(obj, dict):
        obj.pop("st_download_ok", None)
        obj.pop("report_download_ok", None)
        obj.pop("st_convert_garbage", None)
        obj.pop("report_convert_garbage", None)
        obj.pop("st_convert_ok", None)
        obj.pop("report_convert_ok", None)
        obj.pop("st_extract_ok", None)
        obj.pop("report_extract_ok", None)
        obj.pop("st_pdf_hash", None)
        obj.pop("report_pdf_hash", None)
        obj.pop("st_txt_hash", None)
        obj.pop("report_txt_hash", None)


        for key in obj:
            clean_data(obj[key])
    elif isinstance(obj, list):
        for item in obj:
            clean_data(item)

def remove_problematic_fields():
    # Load the dataset.json file
    with open("data/cc_november_23/dataset.json", "r") as file:
        data = json.load(file)

    clean_data(data)

    # Save the cleaned JSON file
    with open("data/cc_november_23/dataset_cleaned.json", "w") as file:
        json.dump(data, file, indent=4)
        



if __name__ == '__main__':
    FILE_NAME = "data/cc_november_2023"

    desompress_from_ZST(FILE_NAME)
    extract_from_tar(FILE_NAME)

    remove_problematic_fields()
