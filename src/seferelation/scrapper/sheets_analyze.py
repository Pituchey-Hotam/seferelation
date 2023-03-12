from typing import List
import os
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
import pickle
from tqdm import tqdm


def _load_fields_from_file(path: Path, fields) -> List:
    with open(path, 'rb') as f:
        interval = pickle.load(f)
    return [{k: v for k,v in e.items() if k in fields} for e in interval]


def _load_fields_from_dir(path: Path, fields):
    path = Path(path)
    loaded_fields = []
    i = 0
    for name in tqdm(os.listdir(path)):
        file_path = path / name
        loaded_fields += _load_fields_from_file(file_path, fields)
        i += 1
        if i > 1:
            break
    return loaded_fields


def load_fields_from_path(path: Path, fields):
    path = Path(path)
    if path.is_dir():
        return _load_fields_from_dir(path, fields)
    else:
        return _load_fields_from_file(path, fields)


def plot_histogram_by_fields(field, savefig):
    # fields = {field, "id"}
    # all_db_fields = _load_fields_from_file("downloads/sheets_dump_0197500_0198000.pickle", field)
    all_db_fields = load_fields_from_path("sheets_sample_5percent.pickle", field)
    only_field = [e[field] for e in all_db_fields if field in e]
    print(len(only_field))
    plt.hist(only_field, bins=100)
    plt.savefig(savefig)


def _sample_file_by_percent(path: Path, percent: float) -> List:
    with open(path, 'rb') as f:
        interval = pickle.load(f)
    return list(np.random.choice(interval, int(len(interval) * percent)))


def sample_dir_by_percent(path: Path, percent: float):
    path = Path(path)
    sampled_intervals = []
    for name in tqdm(os.listdir(path)):
        file_path = path / name
        sampled_intervals += _sample_file_by_percent(file_path, percent)
    with open("sheets_sample_5percent.pickle", "wb") as f:
        pickle.dump(sampled_intervals, f)


# with open("sheets_sample_5percent.pickle", "rb") as f:
#     sample5p = pickle.load(f)
# with open("sheets_sample_100.pickle", "wb") as f:
#     pickle.dump(sample5p[:100], f)

# plot_histogram_by_fields("views", "views_histogram_sample.png")
# ls = _sample_file_by_percent("downloads/sheets_dump_0197500_0198000.pickle", 0.05)
# sample_dir_by_percent("downloads", 0.05)

# lf = _load_fields_from_dir("downloads", {"views", "status", "id"})
# print(lf)
