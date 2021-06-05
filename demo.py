import os
import re
import requests

from tqdm import tqdm

import arxiv


def main():
    query = "voice clone"
    max_results = 100
    out_dir = '_'.join(re.findall(r'\w+', query))
    dirpath = f"./{out_dir}"
    os.makedirs(dirpath, exist_ok=True)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
    )

    client = arxiv.Client(
        page_size=100,
        delay_seconds=3,
        num_retries=5,
    )

    for idx, paper in tqdm(enumerate(client.get(search)), total=max_results):
        filename = paper._get_default_filename()
        filename = f"{idx:06}.{filename}"
        try:
            paper.download_pdf(dirpath=dirpath, filename=filename)
        except Exception as e:
            print(f"download_pdf error: {e}")
            try:
                path = os.path.join(dirpath, filename)
                response = requests.get(paper.pdf_url, stream=True)
                with open(path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
            except Exception as e2:
                print(f"requests error: {e2}")


if __name__ == "__main__":
    main()
