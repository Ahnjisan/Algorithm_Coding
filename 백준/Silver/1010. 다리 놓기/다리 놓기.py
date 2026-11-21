import sys
input = sys.stdin.readline

C = [[0] * 30 for _ in range(30)]
for i in range(30):
    C[i][0] = 1
    for j in range(1, i + 1):
        C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

T = int(input())
for _ in range(T):
    n, m = map(int, input().split())
    print(C[m][n])