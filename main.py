from zipfile import ZipFile
import kaggle, os, json


def init_on_kaggle(home_directory: str, username: str, api_key: str) -> None:
    KAGGLE_CONFIG_DIR = os.path.join(home_directory, ".kaggle")
    os.makedirs(KAGGLE_CONFIG_DIR, exist_ok=True)
    api_dict = {"username": username, "key": api_key}
    with open(f"{KAGGLE_CONFIG_DIR}\kaggle.json", "w", encoding="utf-8") as f:
        json.dump(api_dict, f)


def main():
    # linux users home_directory "~"
    # windows users home_directory "C:\Users\user"
    init_on_kaggle(
        R"C:\Users\caleb", "calebguerrero", "b0f412283e369f5432b6d3fa6f1e30b3"
    )

    api = kaggle.api
    dataset_name = "rsrishav/youtube-trending-video-dataset"

    api.dataset_download_file(dataset_name, "MX_youtube_trending_data.csv")
    api.dataset_download_file(dataset_name, "MX_category_id.json")

    with ZipFile("MX_youtube_trending_data.csv.zip", "r") as zip_obj:
        zip_obj.extractall()

    os.remove("MX_youtube_trending_data.csv.zip")


if __name__ == "__main__":
    main()
