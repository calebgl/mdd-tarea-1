from zipfile import ZipFile
from dotenv import load_dotenv
from json import dump
import os


def init_on_kaggle(home_directory: str, username: str, api_key: str) -> None:
    KAGGLE_CONFIG_DIR = os.path.join(home_directory, ".kaggle")
    os.makedirs(KAGGLE_CONFIG_DIR, exist_ok=True)
    api_dict = {"username": username, "key": api_key}
    with open(f"{KAGGLE_CONFIG_DIR}\kaggle.json", "w", encoding="utf-8") as f:
        dump(api_dict, f)


def main() -> None:
    load_dotenv()
    init_on_kaggle(
        os.environ.get("HOME_DIRECTORY"),
        os.environ.get("KAGGLE_USER"),
        os.environ.get("API_KEY"),
    )

    import kaggle

    api = kaggle.api
    dataset_name = "rsrishav/youtube-trending-video-dataset"

    api.dataset_download_file(dataset_name, "MX_youtube_trending_data.csv")
    api.dataset_download_file(dataset_name, "MX_category_id.json")

    with ZipFile("MX_youtube_trending_data.csv.zip", "r") as zip_obj:
        zip_obj.extractall()

    os.remove("MX_youtube_trending_data.csv.zip")


if __name__ == "__main__":
    main()
