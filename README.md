<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3776AB,100:FFD43B&height=200&section=header&text=Algorithm%20Coding&fontSize=50&fontColor=ffffff&fontAlignY=38&desc=%F0%9F%90%8D%20Python%EC%9C%BC%EB%A1%9C%20%EC%A4%80%EB%B9%84%ED%95%98%EB%8A%94%20%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8&descAlignY=60&descSize=18" width="100%"/>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Baekjoon-0076C0?style=for-the-badge&logo=baekjoon&logoColor=white"/>
  <a href="https://github.com/BaekjoonHub/BaekjoonHub"><img src="https://img.shields.io/badge/BaekjoonHub-Auto%20Push-2ea44f?style=for-the-badge&logo=github&logoColor=white"/></a>
</p>

<!-- solved.ac 프로필 배지: 아래 YOUR_HANDLE을 백준 아이디로 바꾸고 주석을 풀어주세요.
<a href="https://solved.ac/YOUR_HANDLE"><img src="http://mazassumnida.wtf/api/v2/generate_badge?boj=YOUR_HANDLE"/></a>
-->

**매일 한 문제씩, 꾸준히 🔥**

</div>

---

## 📌 About

코딩테스트 대비를 위해 알고리즘 문제를 풀고 기록하는 저장소입니다.
[BaekjoonHub](https://github.com/BaekjoonHub/BaekjoonHub)로 백준에서 맞은 풀이를 자동으로 커밋하고,
GitHub Actions가 아래 **문제 목록과 통계를 자동으로 갱신**합니다.

## 📊 Stats

<!-- STATS:START -->
| 🧩 **총 1문제** | ⚪ Silver **1** |
|:---:|:---:|
<!-- STATS:END -->

## 📚 Problems

<!-- PROBLEMS:START -->
| # | 플랫폼 | 난이도 | 문제 | 분류 | 언어 | 풀이 | 날짜 |
|:-:|:-:|:--|:--|:--|:-:|:-:|:-:|
| 1 | 백준 | <img src="https://static.solved.ac/tier_small/8.svg" height="16"/> Silver III | [1003. 피보나치 함수](https://www.acmicpc.net/problem/1003) | 다이나믹 프로그래밍 | Python | [📝](%EB%B0%B1%EC%A4%80/Silver/1003.%E2%80%85%ED%94%BC%EB%B3%B4%EB%82%98%EC%B9%98%E2%80%85%ED%95%A8%EC%88%98/%ED%94%BC%EB%B3%B4%EB%82%98%EC%B9%98%E2%80%85%ED%95%A8%EC%88%98.py) | 2026.11.20 |
<!-- PROBLEMS:END -->

## 🗂️ Structure

```
📦 Algorithm_Coding
 ┣ 📂 백준
 ┃ ┣ 📂 Bronze
 ┃ ┣ 📂 Silver
 ┃ ┃ ┗ 📂 1003. 피보나치 함수
 ┃ ┃    ┣ 📜 README.md        # 문제 설명 · 성능 요약 · 분류
 ┃ ┃    ┗ 🐍 피보나치 함수.py  # 풀이 코드
 ┃ ┗ 📂 Gold ...
 ┗ 📂 .github                  # README 자동 갱신 스크립트 & 워크플로
```

## 🧭 Roadmap

코딩테스트 빈출 유형을 기준으로 학습 진행 상황을 체크합니다.

| 유형 | 핵심 개념 | 진행 |
|:--|:--|:-:|
| 구현 / 시뮬레이션 | 조건 분기, 2차원 배열 회전 | ⬜ |
| 그리디 | 정렬 + 선택 기준 | ⬜ |
| 완전 탐색 / 백트래킹 | `itertools`, 재귀 + 가지치기 | ⬜ |
| BFS / DFS | `collections.deque`, 방문 처리 | ⬜ |
| 이분 탐색 | `bisect`, 파라메트릭 서치 | ⬜ |
| 다이나믹 프로그래밍 | 점화식, 메모이제이션 | 🟨 |
| 최단 경로 | 다익스트라(`heapq`), 플로이드-워셜 | ⬜ |
| 그래프 | 유니온 파인드, 위상 정렬, MST | ⬜ |
| 자료구조 | 스택 · 큐 · 힙 · 해시 | ⬜ |
| 문자열 / 투 포인터 | 슬라이딩 윈도우, 누적 합 | ⬜ |

> ⬜ 시작 전 · 🟨 진행 중 · ✅ 완료

## 🐍 Python Tips

```python
import sys
input = sys.stdin.readline          # 빠른 입력
sys.setrecursionlimit(10**6)        # 깊은 재귀 대비

from collections import deque, defaultdict, Counter
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from itertools import permutations, combinations, product
```

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFD43B,100:3776AB&height=100&section=footer" width="100%"/>

</div>
