import sys
input = sys.stdin.readline

zero = [1, 0] + [0] * 39
one = [0, 1] + [0] * 39

for i in range(2, 41):
    zero[i] = zero[i - 1] + zero[i - 2]
    one[i] = one[i - 1] + one[i - 2]

T = int(input())
out = []
for _ in range(T):
    n = int(input())
    out.append(f"{zero[n]} {one[n]}")
print("\n".join(out))