import pandas as pd
import json


def read_categories(file_name: str) -> dict[int, str]:
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def insert_categories(data_frame: pd.DataFrame, categories: dict[int, str]) -> pd.Series:
    return data_frame["categoryId"].map(categories)


def main() -> None:
    data_frame = pd.read_csv(
        "MX_youtube_trending_data.csv",
        index_col="video_id",
        parse_dates=["publishedAt", "trending_date"],
        date_parser=lambda date: pd.to_datetime(date),
    )

    categories = read_categories("MX_category_id.json")

    data_frame["category"] = insert_categories(data_frame, categories)
    data_frame.drop("categoryId", axis=1, inplace=True)

    print(data_frame)


if __name__ == "__main__":
    main()
