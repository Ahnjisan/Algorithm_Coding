"""README.md의 solved.ac 현황과 풀이 통계를 갱신한다.

- Baekjoon: solved.ac API (티어, 레이팅, 스트릭, 티어별 푼 문제 수)
- Programmers / SWEA: BaekjoonHub가 올린 풀이 폴더

README.md 안의 아래 마커 사이 내용만 다시 쓴다.
    <!-- SOLVEDAC:START --> ... <!-- SOLVEDAC:END -->
    <!-- STATS:START --> ... <!-- STATS:END -->

각 풀이 폴더의 README.md 첫 줄로 플랫폼과 난이도를 판별한다.
    백준          "# [Silver III] 피보나치 함수 - 1003"
    프로그래머스  "# [level 2] 타겟 넘버 - 43165"
    SWEA          "# [D3] 숫자 배열 회전 - 1961"
"""
import json
import os
import re
import sys
import urllib.request
from collections import Counter

HANDLE = "tom401"  # solved.ac(백준) 아이디
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
README = os.path.join(ROOT, "README.md")

HEADER_RE = re.compile(r"^#\s*\[(?P<level>[^\]]+)\]")
SOLVEDAC_API = "https://solved.ac/api/v3"
ROMAN = ["V", "IV", "III", "II", "I"]
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


def fetch(path):
    req = urllib.request.Request(
        f"{SOLVEDAC_API}{path}",
        headers={"User-Agent": "Mozilla/5.0 (README updater)", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def fetch_solvedac():
    """solved.ac에서 프로필, 스트릭, 티어별 푼 문제 수를 가져온다."""
    user = fetch(f"/user/show?handle={HANDLE}")
    grass = fetch(f"/user/grass?handle={HANDLE}&topic=default")
    stats = fetch(f"/user/problem_stats?handle={HANDLE}")
    by_tier = Counter()
    for row in stats:
        if 1 <= row["level"] <= 30:
            by_tier[BOJ_TIERS[(row["level"] - 1) // 5]] += row["solved"]
    return {
        "tier": user["tier"],
        "rating": user["rating"],
        "solved": user["solvedCount"],
        "current_streak": grass.get("currentStreak", 0),
        "longest_streak": grass.get("longestStreak", user.get("maxStreak", 0)),
        "by_tier": by_tier,
    }


def tier_name(n):
    if n == 0:
        return "Unrated"
    if n >= 31:
        return "Master"
    return f"{BOJ_TIERS[(n - 1) // 5]} {ROMAN[(n - 1) % 5]}"


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


def render_solvedac(sa):
    streak = sa["current_streak"]
    fire = "🔥" if streak else "🧊"
    msg = f"{streak}일 연속 문제 해결 중!" if streak else "오늘 한 문제 풀고 스트릭을 시작해요!"
    return "\n".join([
        f"<h3>{fire} {msg}</h3>",
        "",
        table([
            ("현재 티어", f'<img src="https://static.solved.ac/tier_small/{sa["tier"]}.svg" height="18"/> **{tier_name(sa["tier"])}**'),
            ("AC Rating", f"**{sa['rating']}**"),
            ("푼 문제", f"**{sa['solved']}**"),
            ("현재 스트릭", f"**{streak}일**"),
            ("최장 스트릭", f"**{sa['longest_streak']}일**"),
        ]),
    ])


def render_stats(counts, sa):
    boj = sa["by_tier"]
    prg, swea = counts["prg"], counts["swea"]
    total = sa["solved"] + sum(prg.values()) + sum(swea.values())
    blocks = [f"**🧩 지금까지 총 {total}문제를 풀었어요!**"]
    blocks.append(
        "#### Baekjoon\n" + table(
            [("Total", f"**{sa['solved']}**")]
            + [(f'<img src="https://static.solved.ac/tier_small/{BOJ_ICON[t]}.svg" height="18"/><br>{t}',
                f"**{boj[t]}**") for t in BOJ_TIERS]
        )
    )
    blocks.append(
        "#### Programmers\n" + table(
            [("Total", f"**{sum(prg.values())}**")] + [(lv, f"**{prg[lv]}**") for lv in PRG_LEVELS]
        )
    )
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
    try:
        sa = fetch_solvedac()
    except Exception as e:  # solved.ac 응답이 없으면 기존 README를 그대로 둔다
        print(f"solved.ac 조회 실패, README를 바꾸지 않습니다: {e}", file=sys.stderr)
        return
    new = replace_block(text, "SOLVEDAC", render_solvedac(sa))
    new = replace_block(new, "STATS", render_stats(collect(), sa))
    if new != text:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new)
        print("README updated")
    else:
        print("README already up to date")


if __name__ == "__main__":
    main()
