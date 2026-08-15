# -*- coding: utf-8 -*-
"""Готовит фирменные шрифты GlowAroma (Manrope + Inter) для вёрстки брендбука.

Google Fonts CSS отдаёт woff2, который reportlab не читает, поэтому берём
вариативные TTF из репозитория google/fonts и нарезаем статические начертания
через fontTools.varLib.instancer.

Оба семейства содержат кириллицу. Если сети нет — сборка PDF продолжится
на DejaVu, документ от этого не сломается.
"""
import os
import sys
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
RAW = "https://raw.githubusercontent.com/google/fonts/main"

# (url вариативного шрифта, оси инстанса, имя файла на выходе)
JOBS = [
    (f"{RAW}/ofl/manrope/Manrope%5Bwght%5D.ttf", {"wght": 800}, "Manrope-ExtraBold.ttf"),
    (f"{RAW}/ofl/manrope/Manrope%5Bwght%5D.ttf", {"wght": 500}, "Manrope-Medium.ttf"),
    (f"{RAW}/ofl/inter/Inter%5Bopsz,wght%5D.ttf", {"wght": 400, "opsz": 14}, "Inter-Regular.ttf"),
    (f"{RAW}/ofl/inter/Inter%5Bopsz,wght%5D.ttf", {"wght": 700, "opsz": 14}, "Inter-Bold.ttf"),
]


def download(url, path):
    if os.path.isfile(path):
        return path
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    try:
        from fontTools.ttLib import TTFont
        from fontTools.varLib import instancer
    except ImportError:
        print("нет fontTools — установите: py -m pip install fonttools")
        sys.exit(2)

    cache = {}
    ok = 0
    for url, axes, filename in JOBS:
        target = os.path.join(OUT, filename)
        if os.path.isfile(target):
            print("уже есть:", filename)
            ok += 1
            continue
        src_name = url.rsplit("/", 1)[-1].replace("%5B", "[").replace("%5D", "]")
        src_path = os.path.join(OUT, "_var_" + src_name)
        try:
            if src_path not in cache:
                download(url, src_path)
                cache[src_path] = True
            font = TTFont(src_path)
            static = instancer.instantiateVariableFont(font, axes, inplace=False)
            static.save(target)
            print("готов:", filename, os.path.getsize(target), "байт")
            ok += 1
        except Exception as e:
            print("не удалось собрать", filename, "->", e)

    # проверим кириллицу в результате
    for _, _, filename in JOBS:
        p = os.path.join(OUT, filename)
        if os.path.isfile(p):
            cmap = TTFont(p).getBestCmap()
            has_cyr = all(ord(ch) in cmap for ch in "АаБбЁёЖжЩщЮюЯя")
            print(filename, "кириллица:", "есть" if has_cyr else "НЕТ")

    print("итог:", ok, "из", len(JOBS))
    sys.exit(0 if ok == len(JOBS) else 2)


if __name__ == "__main__":
    main()
