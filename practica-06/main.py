import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import json
import numbers


# from typing import Dict
# def read_categories(file_name: str) -> Dict[int, str]:
def read_categories(file_name: str) -> dict[int, str]:  # Python 3.9+
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def transform_variable(df: pd.DataFrame, x: str) -> pd.Series:
    if isinstance(df[x][0], numbers.Number):
        return df[x]  # type: pd.Series
    else:
        return pd.Series([i for i in range(0, len(df[x]))])


def linear_regression(df: pd.DataFrame, x, y) -> None:
    fixed_x = transform_variable(df, x)
    model = sm.OLS(df[y], sm.add_constant(fixed_x)).fit()
    print(model.summary())
    html = model.summary().tables[1].as_html()
    coef = pd.read_html(html, header=0, index_col=0)[0]["coef"]
    df.plot(x=x, y=y, kind="scatter")
    plt.plot(df[x], [pd.DataFrame.mean(df[y]) for _ in fixed_x.items()], color="green")
    plt.plot(
        df[x],
        [coef.values[1] * x + coef.values[0] for _, x in fixed_x.items()],
        color="red",
    )
    plt.xticks(rotation=90)
    plt.savefig(f"./assets/lr_{y}_{x}.png")
    plt.close()


def main():
    FILE_NAME_CSV = "MX_youtube_trending_data.csv"
    FILE_NAME_JSON = "MX_category_id.json"

    categories = read_categories(FILE_NAME_JSON)
    insert_category = (
        lambda id: categories[int(id)] if int(id) in categories else "Other"
    )

    df = pd.read_csv(
        FILE_NAME_CSV,
        parse_dates=["publishedAt", "trending_date"],
        date_parser=lambda date: pd.to_datetime(date),
        converters={"categoryId": insert_category},
    )

    df.rename({"categoryId": "category"}, axis=1, inplace=True)

    dt_month = df["publishedAt"].dt.month
    after_jan_2021 = df["publishedAt"] > "2021-01"
    before_jan_2022 = df["publishedAt"] < "2022-01"

    df_2021 = df[after_jan_2021 & before_jan_2022]
    grp_month = df_2021.groupby(dt_month)
    grp_month = grp_month.mean()

    grp_month.reset_index(inplace=True)
    grp_month.drop("publishedAt", inplace=True, axis=1)

    linear_regression(grp_month, "view_count", "comments_disabled")
    linear_regression(grp_month, "likes", "dislikes")
    linear_regression(grp_month, "dislikes", "comments_disabled")
    linear_regression(grp_month, "view_count", "likes")


if __name__ == "__main__":
    main()
