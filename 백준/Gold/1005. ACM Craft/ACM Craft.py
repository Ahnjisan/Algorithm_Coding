import sys
from collections import deque
input = sys.stdin.readline

T = int(input())
out = []
for _ in range(T):
    n, k = map(int, input().split())
    D = [0] + list(map(int, input().split()))
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(k):
        x, y = map(int, input().split())
        graph[x].append(y)
        indeg[y] += 1
    w = int(input())

    dp = [0] * (n + 1)
    q = deque()
    for i in range(1, n + 1):
        if indeg[i] == 0:
            q.append(i)
            dp[i] = D[i]

    while q:
        cur = q.popleft()
        if cur == w:          # 목표 건물이 확정되면 바로 종료
            break
        for nxt in graph[cur]:
            dp[nxt] = max(dp[nxt], dp[cur] + D[nxt])
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)

    out.append(str(dp[w]))
print("\n".join(out))