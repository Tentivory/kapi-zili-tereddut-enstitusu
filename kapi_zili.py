#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kapı Zili Tereddüt Enstitüsü — parmak havada kalma süresi hesaplayıcı.

Çalışır. Kapı çalmaz. Patates içermez.
"""

from __future__ import annotations

import argparse
import random
import sys


def evet_mi(metin: str) -> bool:
    return metin.strip().lower() in {"var", "evet", "e", "baktı", "bakti", "1", "true"}


def tereddut_saniye(saat: int, hediye: bool, tv: bool, komsu: bool) -> float:
    """Parmağın zilde havada kalacağı resmi süre.

    Öğle uykusu diplomasi zammıdır. Hediye indirimdir ama rüşvet sayılmaz,
    sadece çaylık bir yumuşatmadır. Komşu bakarsa şahit doğmuştur.
    """
    if not 0 <= saat <= 23:
        raise ValueError("Saat 0 ile 23 arasında olmalı. Gece yarısından sonraki tereddüt ayrı dairedir.")

    taban = 4.2
    if 13 <= saat <= 16:
        taban += 6.5
    elif saat >= 22 or saat < 8:
        taban += 11.0
    if hediye:
        taban -= 1.8
    if tv:
        taban += 3.1
    if komsu:
        taban += 9.0
    taban += random.uniform(-0.35, 1.65)
    return round(max(0.8, taban), 2)


def hukum(saniye: float) -> str:
    if saniye < 3:
        return "ZİL ÇALINDI. Cesaret madalyası postayla gelir, gecikir."
    if saniye < 8:
        return "PARMAK HAVADA. Dosya askıya alındı. Çay demlenmedi, niyet demlendi."
    return "GERİ ÇEKİLME. Ziyaret ruhen gerçekleşti. Kimse kimseyi görmedi. Bu da bir tür protokoldür."


def rapor(saat: int, hediye: bool, tv: bool, komsu: bool) -> str:
    saniye = tereddut_saniye(saat, hediye, tv, komsu)
    karar = hukum(saniye)
    satirlar = [
        "=" * 54,
        "KAPI ZİLİ TEREDDÜT ENSTİTÜSÜ — DURUŞMA TUTANAĞI",
        "=" * 54,
        f"Saat            : {saat:02d}:xx",
        f"Hediye          : {'var (indirim)' if hediye else 'yok (tam tereddüt)'}",
        f"Televizyon      : {'içeriden ses var' if tv else 'sessizlik, şüpheli'}",
        f"Komşu perde     : {'baktı, şahit doğdu' if komsu else 'bakmadı, ya da bakmadı gibi yaptı'}",
        f"Parmak süresi   : {saniye} saniye",
        f"Hüküm           : {karar}",
        "-" * 54,
        "DAMGA: 4 Ekim 2026 | Kayyum Grok | Tentivory",
        "İMZA: parmak havada, mühür yuvarlak, ciddiyet yamuk",
        "MÜHÜR: KZTE-2026-ZIL-YOK",
        "=" * 54,
    ]
    return "\n".join(satirlar)


def etkileşim() -> int:
    print("Kapı Zili Tereddüt Enstitüsü'ne hoş geldiniz. Zile basmayın, önce beyan verin.")
    try:
        saat = int(input("Saat (0-23): ").strip())
        hediye = evet_mi(input("Hediye var mı? (var/yok): "))
        tv = evet_mi(input("İçeriden TV sesi var mı? (var/yok): "))
        komsu = evet_mi(input("Komşu perdeyi araladı mı? (baktı/bakmadı): "))
    except (EOFError, KeyboardInterrupt):
        print("\nBeyan yarım kaldı. Bu da bir tereddüttür. Dosya kapatıldı.")
        return 0
    except ValueError:
        print("Saat sayı olmalı. Enstitü harfli saat kabul etmez.")
        return 2
    try:
        print(rapor(saat, hediye, tv, komsu))
    except ValueError as exc:
        print(exc)
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Kapının önündeki tereddüdü resmileştirir."
    )
    parser.add_argument("--saat", type=int, help="0-23 arası saat")
    parser.add_argument("--hediye", choices=["var", "yok"], help="hediye durumu")
    parser.add_argument("--tv", choices=["var", "yok"], help="televizyon sesi")
    parser.add_argument("--komsu", choices=["baktı", "bakti", "bakmadı", "bakmadi"], help="perde şahidi")
    args = parser.parse_args(argv)

    if args.saat is None:
        return etkileşim()

    hediye = evet_mi(args.hediye or "yok")
    tv = evet_mi(args.tv or "yok")
    komsu = evet_mi(args.komsu or "bakmadı")
    try:
        print(rapor(args.saat, hediye, tv, komsu))
    except ValueError as exc:
        print(exc)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
