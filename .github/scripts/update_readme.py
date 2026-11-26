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
import subprocess
import os
import re
import sys
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone

HANDLE = "tom401"  # solved.ac(백준) 아이디
# 티어 아이콘은 GitHub 이미지 프록시가 solved.ac에 접속하지 못해 레포에 저장해 둔 사본(.github/assets/tier)을 쓴다.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
README = os.path.join(ROOT, "README.md")

HEADER_RE = re.compile(r"^#\s*\[(?P<level>[^\]]+)\].*?-\s*(?P<id>\d+)\s*$")
SNAPSHOT = os.path.join(ROOT, ".github", "stats", "solved.json")
SOLVEDAC_CACHE = os.path.join(ROOT, ".github", "stats", "solvedac.json")
KST = timezone(timedelta(hours=9))
SOLVEDAC_API = "https://solved.ac/api"
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
    """solved.ac 티어·레이팅·티어별 푼 문제 수.

    1) v4 API (프로필 페이지와 같은 값) → 성공하면 캐시에 저장
    2) GitHub Actions에서는 v4가 403으로 막혀 있으므로 캐시(.github/stats/solvedac.json)를 쓰고,
       v3가 캐시보다 많은 푼 문제 수를 주면(= 새 풀이가 반영되면) v3 값을 쓴다.
    """
    try:
        sa = fetch_v4()
        save_cache(sa)
        return sa
    except Exception as e:
        print(f"v4 API 실패: {e}", file=sys.stderr)
    cache = load_cache()
    try:
        v3 = fetch_v3()
        if cache is None or v3["solved"] > cache["solved"]:
            return v3
    except Exception as e:
        print(f"v3 API 실패: {e}", file=sys.stderr)
        if cache is None:
            raise
    return cache


def load_cache():
    if not os.path.exists(SOLVEDAC_CACHE):
        return None
    with open(SOLVEDAC_CACHE, encoding="utf-8") as f:
        c = json.load(f)
    return {**c, "by_tier": Counter(c["by_tier"])}


def save_cache(sa):
    data = {
        "_comment": "solved.ac v4 API에서 마지막으로 확인된 값",
        "checked": datetime.now(KST).date().isoformat(),
        "tier": sa["tier"], "rating": sa["rating"], "solved": sa["solved"],
        "by_tier": {t: sa["by_tier"][t] for t in BOJ_TIERS},
    }
    with open(SOLVEDAC_CACHE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def tiers_from_levels(counts_by_level):
    """난이도 레벨(1~30)별 개수 -> Bronze~Ruby별 개수."""
    by_tier = Counter()
    for level, n in counts_by_level:
        if 1 <= level <= 30:
            by_tier[BOJ_TIERS[(level - 1) // 5]] += n
    return by_tier


def fetch_v4():
    user = fetch(f"/v4/users/{HANDLE}")
    hist = user["ratingProblemsHistogram"]  # index = 난이도 레벨(0~30)
    return {
        "tier": user["tier"],
        "rating": user["rating"],
        "solved": user["solvedCount"],
        "by_tier": tiers_from_levels(enumerate(hist)),
    }


def fetch_v3():
    user = fetch(f"/v3/user/show?handle={HANDLE}")
    stats = fetch(f"/v3/user/problem_stats?handle={HANDLE}")
    return {
        "tier": user["tier"],
        "rating": user["rating"],
        "solved": user["solvedCount"],
        "by_tier": tiers_from_levels((r["level"], r["solved"]) for r in stats),
    }


def tier_name(n):
    if n == 0:
        return "Unrated"
    if n >= 31:
        return "Master"
    return f"{BOJ_TIERS[(n - 1) // 5]} {ROMAN[(n - 1) % 5]}"


def collect():
    """스냅샷(solved.json) + 레포에 올라온 풀이를 플랫폼별 문제 번호 기준으로 합친다.

    GitHub Actions에서는 solved.ac 최신 데이터(v4 API)를 읽을 수 없으므로,
    백준도 서비스 종료 전 solved.ac 기록(275문제)에 BaekjoonHub 업로드를 더해서 센다.
    """
    solved = {"boj": {}, "prg": {}, "swea": {}}
    if os.path.exists(SNAPSHOT):
        with open(SNAPSHOT, encoding="utf-8") as f:
            snap = json.load(f)
        solved["boj"].update(snap.get("baekjoon", {}))
        solved["prg"].update(snap.get("programmers", {}))
        solved["swea"].update(snap.get("swea", {}))
    for top in os.listdir(ROOT):
        top_dir = os.path.join(ROOT, top)
        if top.startswith(".") or not os.path.isdir(top_dir):
            continue
        for dirpath, _, files in os.walk(top_dir):
            if "README.md" not in files:
                continue
            with open(os.path.join(dirpath, "README.md"), encoding="utf-8") as f:
                m = HEADER_RE.match(f.readline().strip())
            if m:
                platform, grade = classify(m["level"])
                if platform in solved:
                    solved[platform][m["id"]] = grade
    return {k: Counter(v.values()) for k, v in solved.items()}


def table(cells):
    head = "| " + " | ".join(c[0] for c in cells) + " |"
    sep = "|" + ":---:|" * len(cells)
    body = "| " + " | ".join(c[1] for c in cells) + " |"
    return "\n".join([head, sep, body])


def solve_days():
    """BaekjoonHub 커밋 시각(KST) 기준으로 문제를 푼 날짜 집합."""
    out = subprocess.run(
        ["git", "log", "--format=%at", "--grep=-BaekjoonHub"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return {datetime.fromtimestamp(int(t), KST).date() for t in out}


def streaks(days, today):
    """(현재 스트릭, 최장 스트릭, 오늘 풀었는지). 오늘 아직 안 풀었으면 어제까지 이어진 스트릭을 유지한다."""
    longest = run = 0
    prev = None
    for d in sorted(days):
        run = run + 1 if prev and d - prev == timedelta(days=1) else 1
        longest = max(longest, run)
        prev = d
    solved_today = today in days
    d = today if solved_today else today - timedelta(days=1)
    current = 0
    while d in days:
        current += 1
        d -= timedelta(days=1)
    return current, longest, solved_today


def render_solvedac(sa, boj_solved, today=None):
    today = today or datetime.now(KST).date()
    current, longest, solved_today = streaks(solve_days(), today)
    if current and solved_today:
        head = f"🔥 {current}일 연속 문제 해결 중!"
    elif current:
        head = f"⏳ {current}일 연속! 오늘도 한 문제 풀고 이어가요"
    else:
        head = "🧊 오늘 한 문제 풀고 스트릭을 시작해요!"
    return "\n".join([
        f"<h3>{head}</h3>",
        "",
        table([
            ("현재 티어", f'<img src=".github/assets/tier/{sa["tier"]}.svg" height="18"/> **{tier_name(sa["tier"])}**'),
            ("AC Rating", f"**{sa['rating']}**"),
            ("푼 문제", f"**{boj_solved}**"),
            ("현재 스트릭", f"**{current}일**"),
            ("최장 스트릭", f"**{longest}일**"),
        ]),
        "",
        "<sub>티어 · 레이팅: solved.ac 기준 · 푼 문제: solved.ac 기록(~2026.04) + 풀이 업로드 · 스트릭: 풀이 업로드(2026.11.20~) 기준</sub>",
    ])


def render_stats(counts):
    boj, prg, swea = counts["boj"], counts["prg"], counts["swea"]
    total = sum(boj.values()) + sum(prg.values()) + sum(swea.values())
    blocks = [f"**🧩 지금까지 총 {total}문제를 풀었어요!**"]
    blocks.append(
        "#### Baekjoon\n" + table(
            [("Total", f"**{sum(boj.values())}**")]
            + [(f'<img src=".github/assets/tier/{BOJ_ICON[t]}.svg" height="18"/><br>{t}',
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
    counts = collect()
    new = replace_block(text, "SOLVEDAC", render_solvedac(sa, sum(counts["boj"].values())))
    new = replace_block(new, "STATS", render_stats(counts))
    if new != text:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new)
        print("README updated")
    else:
        print("README already up to date")


if __name__ == "__main__":
    main()
