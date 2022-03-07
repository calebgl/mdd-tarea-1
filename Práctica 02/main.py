import pandas as pd
import json


def read_raw_data(file_name: str) -> pd.DataFrame:
    raw_data_frame = pd.read_csv(file_name)
    return raw_data_frame


def read_categories(file_name: str) -> dict[int, str]:
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def insert_categories(data_frame: pd.DataFrame, categories: dict[int, str]) -> pd.Series:
    return data_frame["categoryId"].map(categories)


def normalize_date(data_frame: pd.DataFrame, columns: list[str]) -> None:
    for column in columns:
        data_frame[column] = pd.to_datetime(data_frame[column])


def main() -> None:
    data_frame = read_raw_data("MX_youtube_trending_data.csv")
    categories = read_categories("MX_category_id.json")
    date_columns = ["publishedAt", "trending_date"]

    normalize_date(data_frame, date_columns)

    data_frame = insert_categories(data_frame, categories)
    data_frame = data_frame.drop(["categoryId"], axis=1)

    print(data_frame)


if __name__ == "__main__":
    main()
