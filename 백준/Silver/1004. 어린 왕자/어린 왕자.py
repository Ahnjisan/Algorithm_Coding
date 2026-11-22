import sys
input = sys.stdin.readline

def inside(x, y, cx, cy, r):
    return (x - cx) ** 2 + (y - cy) ** 2 < r * r

T = int(input())
out = []
for _ in range(T):
    x1, y1, x2, y2 = map(int, input().split())
    n = int(input())
    count = 0
    for _ in range(n):
        cx, cy, r = map(int, input().split())
        if inside(x1, y1, cx, cy, r) != inside(x2, y2, cx, cy, r):
            count += 1
    out.append(str(count))
print("\n".join(out))