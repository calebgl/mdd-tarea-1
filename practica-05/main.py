import pandas as pd
import json
import statsmodels.api as sm
from statsmodels.formula.api import ols


# from typing import Dict
# def read_categories(file_name: str) -> Dict[int, str]:
def read_categories(file_name: str) -> dict[int, str]:  # Python 3.9+
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def main():
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

    grp_category_and_year = df.groupby(["category", dt_year])
    total_likes_views = grp_category_and_year[["view_count", "likes"]].sum()
    total_likes_views.reset_index(inplace=True)
    total_likes_views.drop("publishedAt", inplace=True, axis=1)

    category_x_views = total_likes_views[["category", "view_count"]]

    model = ols("view_count ~ category", data=category_x_views).fit()
    df_anova = sm.stats.anova_lm(model, typ=2)

    if df_anova["PR(>F)"][0] < 0.005:
        print("Hay diferencias")
        print(df_anova)
    else:
        print("No hay diferencias")


if __name__ == "__main__":
    main()
