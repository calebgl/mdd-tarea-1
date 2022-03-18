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
    FILE_NAME_CSV = "MX_youtube_trending_data.csv"
    FILE_NAME_JSON = "MX_category_id.json"

    categories = read_categories(FILE_NAME_JSON)
    insert_category = (
        lambda id: categories[int(id)] if int(id) in categories else "Other"
    )

    df = pd.read_csv(
        FILE_NAME_CSV,
        index_col="video_id",
        parse_dates=["publishedAt", "trending_date"],
        date_parser=lambda date: pd.to_datetime(date),
        converters={"categoryId": insert_category},
    )

    df.rename({"categoryId": "category"}, axis=1, inplace=True)

    dt_year = df["publishedAt"].dt.year

    # Videos con más vistas en los últimos tres años por categoría
    most_viewed_videos = df[dt_year == 2020].groupby("category")[
        "view_count"].idxmax()
    most_viewed_videos = df.loc[most_viewed_videos]
    most_viewed_videos.to_csv("./data/Most_viewed_videos.csv")
    print(most_viewed_videos)

    # Total de vistas y me gustas por categoría en los últimos 3 años
    grp_category_and_year = df.groupby(["category", dt_year])
    total_likes_views = grp_category_and_year[["view_count", "likes"]].sum()
    total_likes_views.to_csv("./data/Total_likes_and_views.csv")
    print(total_likes_views)

    # Me gusta promedio en los últimos 3 años por categoría
    grp_category = df.groupby("category")
    likes_mean = grp_category["likes"].mean()
    likes_mean.to_csv("./data/Likes_mean.csv")
    print(likes_mean)


if __name__ == "__main__":
    main()
