import math
from functools import wraps


def _parse_amount(line):
    if not isinstance(line, str):
        return None
    parts = line.split()
    if len(parts) != 2:
        return None
    try:
        amount = float(parts[1])
    except ValueError:
        return None
    if not math.isfinite(amount):
        return None
    return amount


def shadow(limit=200):
    def decorator(gen_func):
        @wraps(gen_func)
        def wrapper(*args, **kwargs):
            gen = gen_func(*args, **kwargs)
            total = 0.0
            warned = False
            for item in gen:
                print(f"[shadow] елемент: {item!r}")
                amount = _parse_amount(item)
                if amount is not None:
                    total += amount
                    if total > limit and not warned:
                        print("Тіньовий ліміт перевищено. Активую схему.")
                        warned = True
                yield item 
            return total
        return wrapper
    return decorator


def suspicious_counter(threshold=200):
    def decorator(gen_func):
        @wraps(gen_func)
        def wrapper(*args, **kwargs):
            gen = gen_func(*args, **kwargs)
            running = 0.0
            overflow_sum = 0.0
            overflow_count = 0
            while True:
                try:
                    item = next(gen)
                except StopIteration as stop:
                    print(f"[suspicious_counter] підсумок: {overflow_count} "
                          f"підозрілих операцій на {overflow_sum:g}")
                    return stop.value
                amount = _parse_amount(item)
                if amount is not None:
                    if running + amount > threshold:
                        overflow_count += 1
                        overflow_sum += amount
                        print(f"[suspicious_counter] ПОПЕРЕДЖЕННЯ: сума {amount:g} "
                              f"не влізла в поріг {threshold} "
                              f"(таких уже {overflow_count})")
                    else:
                        running += amount
                yield item
        return wrapper
    return decorator


@suspicious_counter(threshold=200)
@shadow(limit=200)
def transactions(lines):
    for line in lines:
        yield line


def run(gen):
    try:
        while True:
            next(gen)
    except StopIteration as stop:
        return stop.value


if __name__ == "__main__":
    data = [
        "payment 120",
        "refund 50",
        "transfer 300",
        "сміття",
        "payment abc",
        "payment 10",
    ]
    final = run(transactions(data))
    print("Фінальна сума:", final)