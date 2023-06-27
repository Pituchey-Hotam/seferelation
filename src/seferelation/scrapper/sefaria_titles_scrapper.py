from collections import defaultdict
from typing import List

import requests
import asyncio
import aiohttp
from tqdm.asyncio import tqdm_asyncio
import logging


def configure_logging():
    logger = logging.getLogger('error_logger')
    logger.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('error.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def err_log(task, exc):
    logger = logging.getLogger('error_logger')
    logger.error(f"Error occurred in task {task}: {exc}")


async def download_title(title):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.sefaria.org/api/index/{title}") as response:
                title_info = await response.json()
                heb_titles = title_info["heTitleVariants"]
                main_title = title_info["title"]
                return main_title, heb_titles
    except Exception as e:
        err_log(title, e)
        return "", []


async def download_titles():
    titles = requests.get("https://www.sefaria.org/api/index/titles").json()["books"]
    titles = titles[:100]
    titles_map = defaultdict(lambda: set())
    tasks = [download_title(title) for title in titles]
    for task_done in tqdm_asyncio.as_completed(tasks):
        main_title, heb_titles = await task_done
        titles_map[main_title].update(heb_titles)
    return titles_map

def main():
    configure_logging()
    titles_map = asyncio.run(download_titles())
    print(titles_map)

if __name__ == '__main__':
    main()
