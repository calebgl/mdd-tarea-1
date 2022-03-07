import pandas as pd
import json


def read_categories(file_name: str) -> dict[int, str]:
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def main() -> None:
    categories = read_categories("MX_category_id.json")
    insert_category = lambda id: categories[int(id)] if int(id) in categories else "Other"

    data_frame = pd.read_csv(
        "MX_youtube_trending_data.csv",
        index_col="video_id",
        parse_dates=["publishedAt", "trending_date"],
        date_parser=lambda date: pd.to_datetime(date),
        converters={"categoryId": insert_category}
    )

    data_frame.rename(columns={"categoryId": "category"}, inplace=True)

    print(data_frame)


if __name__ == "__main__":
    main()
