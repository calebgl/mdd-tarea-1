import matplotlib.pyplot as plt
import pandas as pd
import json


# from typing import Dict
# def read_categories(file_name: str) -> Dict[int, str]:
def read_categories(file_name: str) -> dict[int, str]:  # Python 3.9+
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def main() -> None:
    FILE_NAME_CSV = "MX_youtube_trending_data.csv"
    FILE_NAME_JSON = "MX_category_id.json"
    YEARS = {2020, 2021, 2022}
    IMG_FOLDER = "./assets"

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

    df_2022 = df[dt_year == 2022]
    df_2022["view_count"].plot(
        kind="hist", bins=50, figsize=(15, 10), title="Distribución de vistas en 2022"
    )
    plt.savefig(f"{IMG_FOLDER}/views_distribution.png")
    plt.close()

    df.plot(
        kind="scatter",
        x="view_count",
        y="likes",
        xlabel="Vistas",
        ylabel="Me gustas",
        title="Vistas vs Me gustas",
    )
    plt.savefig(f"{IMG_FOLDER}/views_vs_likes.png")
    plt.close()

    df.plot(
        kind="scatter",
        x="likes",
        y="dislikes",
        xlabel="Me gustas",
        ylabel="No me gustas",
        title="Me gustas vs No me gustas",
    )
    plt.savefig(f"{IMG_FOLDER}/likes_vs_dislikes.png")
    plt.close()

    grp_year = df.groupby(dt_year)
    pct_years = grp_year["category"].value_counts(normalize=True)
    for year in YEARS:
        pct_year = pct_years.loc[year]
        labels = [f"{l}, {s*100:.2f}%" for l, s in zip(categories.values(), pct_year)]
        ax = pct_year.plot(
            kind="pie",
            normalize=True,
            ylabel="",
            labels=None,
            figsize=(10, 10),
            title=f"Porcentaje de videos por categoría en {year}",
        )
        ax.legend(loc=3, labels=labels)
        plt.savefig(f"{IMG_FOLDER}/percentage_category_{year}.png")
        plt.close()

    grp_category_and_year = df.groupby(["category", dt_year])
    total_likes_views = grp_category_and_year[["view_count", "likes"]].sum()

    total_likes_views.reset_index(inplace=True)
    total_likes_views.drop("publishedAt", inplace=True, axis=1)
    total_likes_views.boxplot("likes", by="category", figsize=(18, 9))
    plt.xticks(rotation=90)
    plt.savefig("assets/boxplot_likes.png")
    plt.close()

    total_likes_views.boxplot("view_count", by="category", figsize=(18, 9))
    plt.xticks(rotation=90)
    plt.savefig("assets/boxplot_views.png")
    plt.close()


if __name__ == "__main__":
    main()
