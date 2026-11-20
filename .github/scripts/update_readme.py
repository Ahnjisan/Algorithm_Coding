"""BaekjoonHub가 올린 풀이 폴더를 읽어 README.md의 풀이 통계를 갱신한다.

README.md 안의 아래 마커 사이 내용만 다시 쓴다.
    <!-- STATS:START --> ... <!-- STATS:END -->

각 풀이 폴더의 README.md 첫 줄로 플랫폼과 난이도를 판별한다.
    백준          "# [Silver III] 피보나치 함수 - 1003"
    프로그래머스  "# [level 2] 타겟 넘버 - 43165"
    SWEA          "# [D3] 숫자 배열 회전 - 1961"
"""
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
README = os.path.join(ROOT, "README.md")

HEADER_RE = re.compile(r"^#\s*\[(?P<level>[^\]]+)\]")
BOJ_TIERS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]
# solved.ac 티어 아이콘 번호 (각 티어의 I 등급)
BOJ_ICON = {t: (i + 1) * 5 for i, t in enumerate(BOJ_TIERS)}
PRG_LEVELS = [f"Lv.{i}" for i in range(6)]
SWEA_LEVELS = [f"D{i}" for i in range(1, 9)]


def classify(level):
    """'[...]' 안의 난이도 문자열 -> (플랫폼, 등급)."""
    level = level.strip()
    first = level.split()[0] if level else ""
    if first in BOJ_TIERS:
        return "boj", first
    m = re.fullmatch(r"(?i)(?:level|lv\.?)\s*(\d)", level)
    if m:
        return "prg", f"Lv.{m[1]}"
    m = re.fullmatch(r"(?i)D(\d)", level)
    if m:
        return "swea", f"D{m[1]}"
    return "etc", level


def collect():
    counts = {"boj": Counter(), "prg": Counter(), "swea": Counter(), "etc": Counter()}
    for top in os.listdir(ROOT):
        top_dir = os.path.join(ROOT, top)
        if top.startswith(".") or not os.path.isdir(top_dir):
            continue
        for dirpath, _, files in os.walk(top_dir):
            if "README.md" not in files:
                continue
            with open(os.path.join(dirpath, "README.md"), encoding="utf-8") as f:
                m = HEADER_RE.match(f.readline())
            if m:
                platform, grade = classify(m["level"])
                counts[platform][grade] += 1
    return counts


def table(cells):
    head = "| " + " | ".join(c[0] for c in cells) + " |"
    sep = "|" + ":---:|" * len(cells)
    body = "| " + " | ".join(c[1] for c in cells) + " |"
    return "\n".join([head, sep, body])


def render_stats(counts):
    total = sum(sum(c.values()) for c in counts.values())
    blocks = [f"**🧩 지금까지 총 {total}문제를 풀었어요!**"]

    boj = counts["boj"]
    blocks.append(
        "#### Baekjoon\n" + table(
            [("Total", f"**{sum(boj.values())}**")]
            + [(f'<img src="https://static.solved.ac/tier_small/{BOJ_ICON[t]}.svg" height="18"/><br>{t}',
                f"**{boj[t]}**") for t in BOJ_TIERS]
        )
    )

    prg = counts["prg"]
    blocks.append(
        "#### Programmers\n" + table(
            [("Total", f"**{sum(prg.values())}**")] + [(lv, f"**{prg[lv]}**") for lv in PRG_LEVELS]
        )
    )

    swea = counts["swea"]
    blocks.append(
        "#### SWEA\n" + table(
            [("Total", f"**{sum(swea.values())}**")] + [(d, f"**{swea[d]}**") for d in SWEA_LEVELS]
        )
    )

    return "\n\n".join(blocks)


def replace_block(text, name, body):
    pattern = re.compile(rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)", re.S)
    return pattern.sub(lambda m: f"{m[1]}\n{body}\n{m[3]}", text)


def main():
    with open(README, encoding="utf-8") as f:
        text = f.read()
    new = replace_block(text, "STATS", render_stats(collect()))
    if new != text:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new)
        print("README updated")
    else:
        print("README already up to date")


if __name__ == "__main__":
    main()
