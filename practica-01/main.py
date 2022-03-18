from kaggle.api import kaggle_api_extended as kaggle
import zipfile
import os


def main():
    DATASET_NAME = "rsrishav/youtube-trending-video-dataset"
    FILE_NAME_ZIP = "MX_youtube_trending_data.csv.zip"
    FILE_NAME_CSV = "MX_youtube_trending_data.csv"
    FILE_NAME_JSON = "MX_category_id.json"

    api = kaggle.KaggleApi()
    api.authenticate()

    api.dataset_download_file(DATASET_NAME, FILE_NAME_CSV)
    api.dataset_download_file(DATASET_NAME, FILE_NAME_JSON)

    with zipfile.ZipFile(FILE_NAME_ZIP, "r") as zip_obj:
        zip_obj.extractall()

    os.remove(FILE_NAME_ZIP)


if __name__ == "__main__":
    main()
