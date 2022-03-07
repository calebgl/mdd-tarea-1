import matplotlib.pyplot as plt
import pandas as pd
import json


def read_categories(file_name: str) -> dict[int, str]:
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def insert_categories(
    data_frame: pd.DataFrame, categories: dict[int, str]
) -> pd.Series:
    return data_frame["categoryId"].map(categories)


def main() -> None:
    years = {2020, 2021, 2022}
    categories = read_categories("MX_category_id.json")
    insert_category = (
        lambda id: categories[int(id)] if int(id) in categories else "Other"
    )

    df = pd.read_csv(
        "MX_youtube_trending_data.csv",
        index_col="video_id",
        parse_dates=["publishedAt", "trending_date"],
        date_parser=lambda date: pd.to_datetime(date),
        converters={"categoryId": insert_category},
    )

    df.rename({"categoryId": "category"}, axis=1, inplace=True)

    grouped_by_category = df.groupby("category")
    grouped_by_year = df.groupby(df["publishedAt"].dt.year)

    # most viewed video per category
    print("El video más visto de cada categoría: ")
    print(grouped_by_category[["title", "view_count"]].max()["title"])

    # total number of videos on each category by publication year
    print("El número total de videos en cada categoría por año")
    print(grouped_by_year["category"].value_counts())

    # ↑ plotted
    for year in years:
        grouped_by_year["category"].value_counts().loc[year].plot(kind="barh")
        plt.savefig(f"assets/views_{year}.png")

    # likes mean per category by publication year
    complex_group = df.groupby([df["publishedAt"].dt.year, "category"])
    print(complex_group["likes"].mean())

    # ↑ plotted
    for year in years:
        complex_group["likes"].mean().loc[year].plot(kind="barh")
        plt.savefig(f"assets/likes_mean_{year}.png")


if __name__ == "__main__":
    main()
