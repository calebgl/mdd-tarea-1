from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
import os


def main():
    DATASET_NAME = "rsrishav/youtube-trending-video-dataset"
    FILE_NAME_ZIP = "MX_youtube_trending_data.csv.zip"
    FILE_NAME_CSV = "MX_youtube_trending_data.csv"
    FILE_NAME_JSON = "MX_category_id.json"

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_file(DATASET_NAME, FILE_NAME_CSV)
    api.dataset_download_file(DATASET_NAME, FILE_NAME_JSON)

    with ZipFile(FILE_NAME_ZIP, "r") as zip_obj:
        zip_obj.extractall()

    os.remove(FILE_NAME_ZIP)


if __name__ == "__main__":
    main()
