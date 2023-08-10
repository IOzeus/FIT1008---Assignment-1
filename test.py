def below(n: int) -> int:
    total = 0
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            total += i
    return total

print(below(4))