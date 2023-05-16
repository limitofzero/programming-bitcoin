
def swap(diffs):
    pool = [1100.0, 900.0, 1000.0]
    product = pool[0] * pool[1] * pool[2]

    for i in range(3):
        if diffs[i] < 0 and abs(diffs[i]) > pool[i]:
            return False

    if (pool[0] + diffs[0]) * (pool[1] + diffs[1]) * (pool[2] + diffs[2]) < product:
        return False

    return True


min_usdb = None
for x in range(1, 901):  # Iterate over possible USDB amounts
    diffs = [-20.0, -x, 300.0]
    if swap(diffs):
        min_usdb = x
        break

result = [-20, -min_usdb, 300]
print(
    "Minimal integer USDB amount to perform a swap in form [val, val, val]:", result)
