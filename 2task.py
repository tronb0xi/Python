a = float(input("Перше число: "))
op = input("Операція (+, -, *, /): ")
b = float(input("Друге число: "))

if op == '+':
    result = a + b
elif op == '-':
    result = a - b
elif op == '*':
    result = a * b
elif op == '/':
    result = a / b

print("Результат:", result)