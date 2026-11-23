import sys
from math import isqrt
input = sys.stdin.readline

T = int(input())
out = []
for _ in range(T):
    x, y = map(int, input().split())
    d = y - x
    n = isqrt(d)              # n² ≤ d 를 만족하는 가장 큰 n
    if d == n * n:
        ans = 2 * n - 1
    elif d <= n * n + n:
        ans = 2 * n
    else:
        ans = 2 * n + 1
    out.append(str(ans))
print("\n".join(out))