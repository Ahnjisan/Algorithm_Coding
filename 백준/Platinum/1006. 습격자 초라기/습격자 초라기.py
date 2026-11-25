import sys
input = sys.stdin.readline
INF = float('inf')

def linear(r0, r1, n, W):
    a = [INF] * (n + 1); b = [INF] * (n + 1); c = [INF] * (n + 1)
    c[0] = 0
    a[1] = b[1] = 1
    c[1] = 1 if r0[0] + r1[0] <= W else 2
    for k in range(1, n):
        # k열 안쪽만 남기기: 단독 or (k-1열 바깥만 있던 상태에서) 안쪽 가로 묶기
        a[k+1] = c[k] + 1
        if r0[k-1] + r0[k] <= W:
            a[k+1] = min(a[k+1], b[k] + 1)
        # k열 바깥쪽만 남기기
        b[k+1] = c[k] + 1
        if r1[k-1] + r1[k] <= W:
            b[k+1] = min(b[k+1], a[k] + 1)
        # k열 전부 채우기
        c[k+1] = min(c[k] + (1 if r0[k] + r1[k] <= W else 2),
                     a[k+1] + 1, b[k+1] + 1)
        if r0[k-1] + r0[k] <= W and r1[k-1] + r1[k] <= W:
            c[k+1] = min(c[k+1], c[k-1] + 2)   # 두 줄 모두 가로 묶기
    return c[n]

T = int(input())
out = []
for _ in range(T):
    n, W = map(int, input().split())
    r0 = list(map(int, input().split()))   # 안쪽
    r1 = list(map(int, input().split()))   # 바깥쪽

    ans = linear(r0, r1, n, W)             # 1) 원형 연결 X
    if n > 1:
        B = W + 1
        w0 = r0[0] + r0[-1] <= W
        w1 = r1[0] + r1[-1] <= W
        if w0:                             # 2) 안쪽 원형 연결
            t0 = r0[:]; t0[0] = t0[-1] = B
            ans = min(ans, linear(t0, r1, n, W) - 1)
        if w1:                             # 3) 바깥쪽 원형 연결
            t1 = r1[:]; t1[0] = t1[-1] = B
            ans = min(ans, linear(r0, t1, n, W) - 1)
        if w0 and w1:                      # 4) 둘 다
            ans = min(ans, linear(t0, t1, n, W) - 2)
    out.append(str(ans))
print("\n".join(out))