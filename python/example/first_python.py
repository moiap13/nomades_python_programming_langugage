# # using input() to take user input
# num = input("Enter a number: ")
# print("You Entered:", num)
# print("Data type of num:", type(num))

# num_int = int(input("Enter a number: "))
# print(f"You entered: {num_int}")
# print(f"Data type of num_int: {type(num_int)}")
# count = 0
# age = 32
# while age > 18:
#     print(f"You can vote {count}")
#     count += 1
num = 0

while num < 10:
    if (num % 5) == 1:
        continue
    num += 1
    print(num)
