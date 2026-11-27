import sys
input = sys.stdin.readline

T = int(input())
out = []
for _ in range(T):
    n, m = map(int, input().split())
    broken = []
    for _ in range(n):
        row = input().strip()
        b = 0
        for j, ch in enumerate(row):
            if ch == 'x':
                b |= 1 << j
        broken.append(b)

    # 한 행 안에서 좌우로 붙어 앉지 않는 배치만 미리 추려 둠
    masks = [s for s in range(1 << m) if s & (s << 1) == 0]
    cnt = {s: bin(s).count('1') for s in masks}

    dp = {0: 0}                      # 0번째 행 위는 빈 행
    for r in range(n):
        ndp = {}
        for cur in masks:
            if cur & broken[r]:      # 부서진 자리에 앉으면 안 됨
                continue
            best = -1
            for prev, v in dp.items():
                if cur & (prev << 1) or cur & (prev >> 1):   # 대각선 컨닝
                    continue
                best = max(best, v)
            if best >= 0:
                ndp[cur] = best + cnt[cur]
        dp = ndp
    out.append(str(max(dp.values())))
print("\n".join(out))