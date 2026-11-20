"""BaekjoonHub가 올린 풀이 폴더를 읽어 README.md의 문제 목록과 통계를 갱신한다.

README.md 안의 아래 마커 사이 내용만 다시 쓴다.
    <!-- STATS:START --> ... <!-- STATS:END -->
    <!-- PROBLEMS:START --> ... <!-- PROBLEMS:END -->
"""
import os
import re
import unicodedata
from collections import Counter
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
README = os.path.join(ROOT, "README.md")

# BaekjoonHub 문제 README 첫 줄: "# [Silver III] 피보나치 함수 - 1003"
HEADER_RE = re.compile(r"^#\s*\[(?P<level>[^\]]+)\]\s*(?P<title>.+?)\s*-\s*(?P<id>\d+)\s*$")
DATE_RE = re.compile(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일")

TIERS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]
ROMAN = {"V": 5, "IV": 4, "III": 3, "II": 2, "I": 1}
TIER_EMOJI = {"Bronze": "🟤", "Silver": "⚪", "Gold": "🟡", "Platinum": "🟢", "Diamond": "🔵", "Ruby": "🔴"}
LANG_EXT = {".py": "Python", ".cpp": "C++", ".java": "Java", ".js": "JavaScript", ".sql": "SQL"}


def nfc(s):
    return unicodedata.normalize("NFC", s)


def section(text, name):
    m = re.search(r"###\s*" + name + r"\s*\n(.*?)(?=\n###|\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def tier_icon(level):
    """'Silver III' -> solved.ac 티어 아이콘 <img>. 백준이 아니면 텍스트 그대로."""
    parts = level.split()
    if len(parts) == 2 and parts[0] in TIERS and parts[1] in ROMAN:
        n = TIERS.index(parts[0]) * 5 + (6 - ROMAN[parts[1]])
        return f'<img src="https://static.solved.ac/tier_small/{n}.svg" height="16"/> {level}'
    return level


def collect():
    problems = []
    for platform in sorted(os.listdir(ROOT)):
        p_dir = os.path.join(ROOT, platform)
        if platform.startswith(".") or not os.path.isdir(p_dir):
            continue
        for dirpath, _, files in os.walk(p_dir):
            if "README.md" not in files:
                continue
            with open(os.path.join(dirpath, "README.md"), encoding="utf-8") as f:
                text = f.read()
            m = HEADER_RE.match(nfc(text.splitlines()[0]) if text else "")
            if not m:
                continue
            code = [x for x in files if os.path.splitext(x)[1] in LANG_EXT]
            d = DATE_RE.search(section(text, "제출 일자"))
            link_target = os.path.join(dirpath, code[0]) if code else dirpath
            problems.append({
                "platform": nfc(platform),
                "level": m["level"],
                "title": nfc(m["title"]),
                "id": m["id"],
                "tags": nfc(section(text, "분류")).replace("\n", ", ") or "-",
                "date": f"{d[1]}.{int(d[2]):02d}.{int(d[3]):02d}" if d else "",
                "lang": LANG_EXT[os.path.splitext(code[0])[1]] if code else "-",
                "path": quote(os.path.relpath(link_target, ROOT)),
            })
    problems.sort(key=lambda p: (p["date"], int(p["id"])), reverse=True)
    return problems


def problem_url(p):
    if p["platform"] == "백준":
        return f"https://www.acmicpc.net/problem/{p['id']}"
    if p["platform"] == "프로그래머스":
        return f"https://school.programmers.co.kr/learn/courses/30/lessons/{p['id']}"
    return ""


def render_stats(problems):
    counts = Counter(p["level"].split()[0] for p in problems)
    cells = [f"| 🧩 **총 {len(problems)}문제** |"]
    known = [t for t in TIERS if counts[t]]
    for t in known:
        cells.append(f" {TIER_EMOJI[t]} {t} **{counts[t]}** |")
    others = len(problems) - sum(counts[t] for t in known)
    if others:
        cells.append(f" 📘 기타 **{others}** |")
    header = "".join(cells)
    sep = "|" + ":---:|" * (len(cells))
    return header + "\n" + sep


def render_table(problems):
    if not problems:
        return "_아직 푼 문제가 없어요. 첫 문제를 풀어보세요!_ 🚀"
    rows = ["| # | 플랫폼 | 난이도 | 문제 | 분류 | 언어 | 풀이 | 날짜 |",
            "|:-:|:-:|:--|:--|:--|:-:|:-:|:-:|"]
    for i, p in enumerate(problems, 1):
        url = problem_url(p)
        name = f"[{p['id']}. {p['title']}]({url})" if url else f"{p['id']}. {p['title']}"
        rows.append(
            f"| {i} | {p['platform']} | {tier_icon(p['level'])} | {name} | {p['tags']} "
            f"| {p['lang']} | [📝]({p['path']}) | {p['date']} |"
        )
    return "\n".join(rows)


def replace_block(text, name, body):
    pattern = re.compile(rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)", re.S)
    return pattern.sub(lambda m: f"{m[1]}\n{body}\n{m[3]}", text)


def main():
    problems = collect()
    with open(README, encoding="utf-8") as f:
        text = f.read()
    new = replace_block(text, "STATS", render_stats(problems))
    new = replace_block(new, "PROBLEMS", render_table(problems))
    if new != text:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"README updated: {len(problems)} problems")
    else:
        print("README already up to date")


if __name__ == "__main__":
    main()
