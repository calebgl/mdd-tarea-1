import scipy.stats as spy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json


def read_categories(file_name: str) -> dict[int, str]:
    with open(file_name, "r") as file:
        json_data = json.load(file)
        return {
            int(category["id"]): category["snippet"]["title"]
            for category in json_data["items"]
        }


def get_cmap(n, name="hsv"):
    """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name."""
    return plt.cm.get_cmap(name, n)


def scatter_group_by(
    file_path: str, df: pd.DataFrame, x_column: str, y_column: str, label_column: str
):
    _, ax = plt.subplots()
    labels = pd.unique(df[label_column])
    cmap = get_cmap(len(labels) + 1)
    for idx, label in enumerate(labels):
        filter_df = df.query(f"{label_column} == '{label}'")
        ax.scatter(
            filter_df[x_column], filter_df[y_column], label=label, color=cmap(idx)
        )
    ax.legend()
    plt.savefig(file_path)
    plt.close()


def euclidean_distance(p_1: np.array, p_2: np.array) -> float:
    return np.sqrt(np.sum((p_2 - p_1) ** 2))


def k_nearest_neightbors(
    points: list[np.array], labels: np.array, input_data: list[np.array], k: int
):
    input_distances = [
        [euclidean_distance(input_point, point) for point in points]
        for input_point in input_data
    ]
    points_k_nearest = [
        np.argsort(input_point_dist)[:k] for input_point_dist in input_distances
    ]
    return [
        spy.mode([labels[index] for index in point_nearest])
        for point_nearest in points_k_nearest
    ]


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

    comedy = df["category"] == "Comedy"
    gaming = df["category"] == "Gaming"
    sports = df["category"] == "Sports"

    feb_14_2022 = df["publishedAt"] > "2022-02-14"
    feb_15_2022 = df["publishedAt"] < "2022-02-15"

    time_range = feb_14_2022 & feb_15_2022
    categories = comedy | gaming | sports

    x = "view_count"
    y = "comment_count"
    grp = "category"

    df = df[time_range & categories]
    df = df[[x, y, grp]]

    scatter_group_by("assets/classification.png", df, x, y, grp)

    list_t = [
        (np.array(tuples[0:1]), tuples[2])
        for tuples in df.itertuples(index=False, name=None)
    ]
    points = [point for point, _ in list_t]
    labels = [label for _, label in list_t]

    kn = k_nearest_neightbors(
        points,
        labels,
        [
            np.array([6e7, 1.4e5]),
            np.array([4.5e7, 0.8e5]),
            np.array([0, 0]),
            np.array([1e7, 0.5e5]),
        ],
        5,
    )
    print(np.array(kn))


if __name__ == "__main__":
    main()
