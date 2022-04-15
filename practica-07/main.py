import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import json
import numbers
from typing import Dict, Tuple


# def read_categories(file_name: str) -> dict[int, str]:  # Python 3.9+
def read_categories(file_name: str) -> Dict[int, str]:
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def transform_variable(df: pd.DataFrame, x: str) -> pd.Series:
    if isinstance(df[x][df.index[0]], numbers.Number):
        return df[x]  # type: pd.Series
    else:
        return pd.Series([i for i in range(0, len(df[x]))])


def linear_regression(df: pd.DataFrame, x: str, y: str) -> Dict[str, float]:
    fixed_x = transform_variable(df, x)
    model = sm.OLS(list(df[y]), sm.add_constant(fixed_x), alpha=0.05).fit()
    bands = pd.read_html(model.summary().tables[1].as_html(), header=0, index_col=0)[0]
    coef = bands["coef"]
    tables_0 = model.summary().tables[0].as_html()
    r_2_t = pd.read_html(tables_0, header=None, index_col=None)[0]
    return {
        "m": coef.values[1],
        "b": coef.values[0],
        "r2": r_2_t.values[0][3],
        "r2_adj": r_2_t.values[1][3],
        "low_band": bands["[0.025"][0],
        "hi_band": bands["0.975]"][0],
    }


def plt_lr(
    df: pd.DataFrame,
    x: str,
    y: str,
    m: float,
    b: float,
    r2: float,
    r2_adj: float,
    low_band: float,
    hi_band: float,
    colors: Tuple[str, str],
):
    fixed_x = transform_variable(df, x)
    plt.plot(df[x], [m * x + b for _, x in fixed_x.items()], color=colors[0])
    plt.fill_between(
        df[x],
        [m * x + low_band for _, x in fixed_x.items()],
        [m * x + hi_band for _, x in fixed_x.items()],
        alpha=0.2,
        color=colors[1],
    )


def main():
    FILE_NAME_CSV = "MX_youtube_trending_data.csv"
    FILE_NAME_JSON = "MX_category_id.json"

    categories = read_categories(FILE_NAME_JSON)
    insert_category = (
        lambda id: categories[int(id)] if int(id) in categories else "Other"
    )

    df_music = pd.read_csv(
        FILE_NAME_CSV,
        parse_dates=["publishedAt", "trending_date"],
        date_parser=lambda date: pd.to_datetime(date),
        converters={"categoryId": insert_category},
    )

    df_music.rename({"categoryId": "category"}, axis=1, inplace=True)

    music = df_music["category"] == "Music"
    dt_date = df_music["trending_date"].dt.date
    # total stats of music videos group by day since 2020 to 2022
    df_music = df_music[music].groupby(dt_date).sum()
    df_music.reset_index(inplace=True)
    df_music = df_music[["trending_date", "view_count"]]
    df_music_last_50 = df_music.tail(50)

    x = "trending_date"
    y = "view_count"

    parse_date = lambda date: pd.to_datetime(date)
    is_thursday = lambda date: parse_date(date).dt.dayofweek == 4

    df_music_last_50.plot(x=x, y=y, kind="scatter")
    lr = linear_regression(df_music_last_50, x, y)
    plt_lr(df=df_music_last_50, x=x, y=y, colors=("red", "orange"), **lr)

    lr = linear_regression(df_music_last_50.tail(5), x, y)
    plt_lr(df=df_music_last_50.tail(5), x=x, y=y, colors=("red", "orange"), **lr)
    df_music_thursday = df_music_last_50[is_thursday(df_music_last_50[x])]
    print(df_music_thursday)

    lr = linear_regression(df_music_thursday, x, y)
    plt_lr(df=df_music_thursday, x=x, y=y, colors=("blue", "blue"), **lr)

    plt.xticks(rotation=90)
    plt.savefig(f"assets/lr_{y}_{x}_m.png")
    plt.close()

    df_music_2020_2021 = df_music.loc[
        (parse_date(df_music[x]) >= "2020-08-12")
        & (parse_date(df_music[x]) < "2021-08-13")
    ]
    print(df_music)

    dfs = [
        ("50D", df_music_last_50),
        ("10D", df_music_last_50.tail(10)),
        ("5D", df_music_last_50.tail(5)),
        (
            "jueves",
            df_music_last_50[is_thursday(df_music_last_50[x])],
        ),
        ("50D-1Y", df_music_2020_2021),
        ("10D-Y", df_music_2020_2021.tail(10)),
        ("5D-Y", df_music_2020_2021.tail(5)),
        (
            "jueves-Y",
            df_music_2020_2021[is_thursday(df_music_2020_2021[x])],
        ),
    ]
    lrs = [(title, linear_regression(_df, x=x, y=y), len(_df)) for title, _df in dfs]
    lrs_p = [
        (title, lr_dict["m"] * size + lr_dict["b"], lr_dict)
        for title, lr_dict, size in lrs
    ]
    print(lrs_p)


if __name__ == "__main__":
    main()
