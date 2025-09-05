# n: int = 0
# while n < 1e9:
#     n += 1
# print(n)

max_iter = int(1e10)
l = [0] * max_iter
for i in range(max_iter):
    l[i] += 1
print(l)
