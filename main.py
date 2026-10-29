import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import httpx
import requests
from bs4 import BeautifulSoup
from rich import print
from tqdm import tqdm

from tools import check_internet, delete_dir, find_files, format_bytes, unroll_vars

URL_RUSTORE = "https://www.rustore.ru/catalog/app/ru.oneme.app"
URL_APK = "https://download.cdn.oneme.ru/android/release/google/MAX.apk"

if not check_internet():
    print("[bold red]No internet[/bold red]")
    sys.exit(1)

def rustore_info() -> None:
    r = requests.get(URL_RUSTORE, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    for script in soup.find_all("script", type="application/ld+json"):
        if not script.string:
            continue

        try:
            data = json.loads(script.string)
        except json.JSONDecodeError:
            continue

        items = data.get("@graph", [data]) if isinstance(data, dict) else data

        if not isinstance(items, list):
            items = [items]

        for item in items:
            if isinstance(item, dict) and item.get("@type") == "SoftwareApplication":
                version = item.get("softwareVersion")

                if version:
                    print(f"Version: {version}")

                    date_raw = item.get("dateModified")
                    if date_raw:
                        date = datetime.fromisoformat(date_raw)
                        print(f"Last modification: {date.astimezone().strftime('%d.%m.%Y %H:%M:%S')}")
                    file_size = item.get("fileSize")
                    if file_size is not None:
                        print(f"File size: {format_bytes(int(file_size))}")

                    return

        print("[bold red]Can not load rustore[/bold red]")

def download_apk(url: str = URL_APK, output_path: str = "max.apk") -> None:
    with httpx.stream("GET", url, follow_redirects=True) as response:
        response.raise_for_status()
        
        total_size = int(response.headers.get("content-length", 0))
        
        with open(output_path, "wb") as file, tqdm(total=total_size, unit="B", unit_scale=True, desc=output_path) as progress_bar:
            for chunk in response.iter_bytes(chunk_size=8192):
                file.write(chunk)
                progress_bar.update(len(chunk))

def decompile_apk(apk_path: str = "max.apk") -> None:
    delete_dir("resources")
    delete_dir("sources")
    cmd = ["jadx", "--comments-level", "none", "-d", ".", "-j", "8", apk_path, "--deobf"]
    process = subprocess.Popen(cmd)
    process.wait()
    delete_dir("resources")

def finalise() -> None:
    results = find_files("sources/defpackage", ["PING", "DEBUG"])
    for file_path in results:
        print(f"[blue]File: {file_path}[/blue]")
        unroll_vars(file_path)
        for i in get_result(file_path):
            print(f"{i[1]} = {i[0]}")

def get_result(p: Path) -> list[tuple[int, str]]:
    text = p.read_text(encoding="utf-8")
    cls = re.search(r'\bclass\s+(\w+)', text)
    if cls:
        pat = re.compile(rf'new {cls.group(1)}\(\s*"(\w+)"\s*,\s*(\d+)\s*,\s*(?:\(short\)\s*)?(-?\d+|0x[0-9a-fA-F]+)')
        return [
            (int(m.group(3), 0), m.group(1))
            for m in sorted(pat.finditer(text), key=lambda m: int(m.group(2)))
        ]
    else:
        print("[red]Class not found[/red]")
        return []

def main() -> None:
    try:
        print("[green][1] info[/green]")
        rustore_info()
        print("[green][2] download apk[/green]")
        download_apk()
        print("[green][3] decompile apk[/green]")
        decompile_apk()
        print("[green][4] look for files[/green]")
        finalise()
        
    except KeyboardInterrupt:
        print("[red]Cancelled[/red]")

if __name__ == "__main__":
    main()
