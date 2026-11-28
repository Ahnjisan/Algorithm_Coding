import sys
from collections import deque
input = sys.stdin.readline

n, m = map(int, input().split())
targets = list(map(int, input().split()))

dq = deque(range(1, n + 1))
ans = 0
for t in targets:
    idx = dq.index(t)
    if idx <= len(dq) - idx:       # 왼쪽 회전이 더 짧음
        dq.rotate(-idx)
        ans += idx
    else:                          # 오른쪽 회전이 더 짧음
        dq.rotate(len(dq) - idx)
        ans += len(dq) - idx
    dq.popleft()
print(ans)