def tokenize(expr):
    tokens = []
    num = ""
    for ch in expr:
        if ch.isdigit() or ch == '.':
            num += ch
        else:
            if num:
                tokens.append(float(num))
                num = ""
            if ch in '+-*/()':
                tokens.append(ch)
    if num:
        tokens.append(float(num))
    return tokens


tokens = []
pos = 0

def parse_expr():
    global pos
    result = parse_term()
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op = tokens[pos]
        pos += 1
        right = parse_term()
        result = result + right if op == '+' else result - right
    return result

def parse_term():
    global pos
    result = parse_factor()
    while pos < len(tokens) and tokens[pos] in ('*', '/'):
        op = tokens[pos]
        pos += 1
        right = parse_factor()
        result = result * right if op == '*' else result / right
    return result

def parse_factor():
    global pos
    if tokens[pos] == '(':
        pos += 1
        result = parse_expr()
        pos += 1
        return result
    result = tokens[pos]
    pos += 1
    return result


expr = input("Введіть вираз: ")
tokens = tokenize(expr)
pos = 0
result = parse_expr()

if result == int(result):
    result = int(result)
print("Результат:", result)