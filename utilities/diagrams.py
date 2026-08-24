import matplotlib.pyplot as plt


def plot_results(df, name_suffix=""):
    attributes = [
        "Success %",
        "Average Gap %",
        "Average Time (s)"
    ]

    for attribute in attributes:
        plt.figure(figsize=(8, 5))

        plt.bar(
            df["Algorithm"],
            df[attribute],
            color="#8B0000",
            edgecolor="#5C0000",
            bottom=0
        )

        plt.title(f"{attribute} {name_suffix}")
        plt.ylabel(attribute)
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.show()

import os
import matplotlib.pyplot as plt


def save_result_plots(df, output_folder="results/plots", name_suffix=""):
    os.makedirs(output_folder, exist_ok=True)

    attributes = [
        "Success %",
        "Average Gap %",
        "Average Time (s)"
    ]

    for attribute in attributes:
        plt.figure(figsize=(8, 5))

        plt.bar(
            df["Algorithm"],
            df[attribute],
            color="#8B0000",
            edgecolor="#5C0000",
            bottom=0
        )

        plt.title(f"{attribute} {name_suffix}")
        plt.ylabel(attribute)
        plt.xticks(rotation=20)
        plt.tight_layout()

        filename = (
            attribute
            .replace("%", "percent")
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
        )

        plt.savefig(
            os.path.join(output_folder, f"{filename}.png"),
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()