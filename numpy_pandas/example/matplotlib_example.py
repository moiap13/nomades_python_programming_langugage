# import matplotlib.pyplot as plt

# x = [1, 2, 3, 4, 5]
# y = [10, 20, 30, 40, 50]
# x2 = [1, 2, 3, 4]
# y2 = [15, 23, 28, 37]
# plt.plot(x2, y2, label="Test 2")
# plt.show(block=False)

# plt.plot(x, y, label="Test")
# plt.xlabel("x - axis")
# plt.ylabel("y - axis")
# plt.legend()
# plt.title("My first graph!")
# plt.savefig("test_graph.png")
# plt.show(block=False)

# input()
# print("Done")


import numpy as np
import matplotlib.pyplot as plt


ax = plt.subplot(projection="3d")

# Prepare arrays x, y, z
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)

ax.plot(x, y, z, label="parametric curve")
ax.legend()

plt.show()
