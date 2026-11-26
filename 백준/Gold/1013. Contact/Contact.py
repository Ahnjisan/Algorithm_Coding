import sys, re
input = sys.stdin.readline

p = re.compile(r'(100+1+|01)+')

T = int(input())
out = []
for _ in range(T):
    s = input().strip()
    out.append("YES" if p.fullmatch(s) else "NO")
print("\n".join(out))