import requests
from multiprocessing import Pool

from pathlib import Path
import pickle
from tqdm import tqdm


INTERVAL_SIZE = 500


def download_range(start, end):
    target_path = f"downloads/sheets_dump_{start:07}_{end:07}.pickle"
    if Path(target_path).exists():
        print(f"already done: {target_path}")
        return
    res_list = []
    for i in tqdm(range(start, end)):
        url = f"https://www.sefaria.org/api/sheets/{i}"
        response = requests.get(url)
        res_list.append(response.json())

    with open(target_path, "wb") as f:
        pickle.dump(res_list, f)
    # with open(f"sheets_dump_{start}_{end}.json", "w") as f:
    #     json.dump(res_list, f)


def main():
    with Pool(40) as p:
        intervals = [(i, i + INTERVAL_SIZE) for i in range(200*1000, 400*1000, INTERVAL_SIZE)]
        p.starmap(download_range, intervals)


if __name__ == '__main__':
    main()


