from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

project_dir = Path(__file__).resolve().parents[2]


def get_pdbids():
    pdbid_list_path = project_dir / "data" / "PDBbind_v2020_pdbids.txt"
    with open(str(pdbid_list_path), "r") as f:
        pdbids = f.read().splitlines()
    return pdbids


def download_source(pdbid, download_dir):
    url = "http://www.pdbbind.org.cn/quickpdb.php?quickpdb=" + pdbid

    try:
        driver.get(url)
        with open(str(download_dir / f"{pdbid}.html"), "w") as f:
            f.write(driver.page_source)
    except:
        print(f"Failed to download {pdbid}.html")
        pass


def main():
    global driver
    pdbids = get_pdbids()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(
        service=service.Service(ChromeDriverManager().install()), options=options
    )
    driver.set_page_load_timeout(30)

    download_dir = project_dir / "data" / "sources"
    downloaded_pdbids = [p.stem for p in download_dir.glob("*.html")]
    pdbids = [pdbid for pdbid in pdbids if pdbid not in downloaded_pdbids]

    bar = tqdm(pdbids)
    for pdbid in pdbids:
        download_source(pdbid, download_dir)
        bar.update(1)
        sleep(60)


if __name__ == "__main__":
    main()
