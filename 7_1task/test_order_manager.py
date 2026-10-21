import pytest
from service_body_test import Order


@pytest.fixture
def order():
    return Order(1, [
        {"price": 10.0, "quantity": 5},
        {"price": 3.0, "quantity": 2},
        {"price": 7.5, "quantity": 1},
    ])


@pytest.mark.parametrize("items, expected", [
    ([], 0),
    ([{"price": 10.5, "quantity": 3}], 31.5),
    ([
        {"price": 10.0, "quantity": 5},
        {"price": 3.0, "quantity": 2},
    ], 56.0),
    ([
        {"price": 0.1, "quantity": 1},
        {"price": 0.2, "quantity": 1},
    ], 0.3),
    ([{"price": 10.0, "quantity": 0}], 0),
])
def test_total(items, expected):
    result = Order(1, items).total()
    assert result == pytest.approx(expected)


def test_most_expensive(order):
    result = order.most_expensive()
    assert result is order.items[0]


def test_most_expensive_compares_price_not_quantity():
    cheap = {"price": 3.0, "quantity": 100}
    expensive = {"price": 10.0, "quantity": 1}
    order = Order(1, [cheap, expensive])

    result = order.most_expensive()

    assert result is expensive


def test_most_expensive_with_one_item():
    item = {"price": 5.0, "quantity": 2}
    order = Order(1, [item])

    assert order.most_expensive() is item


def test_most_expensive_returns_first_when_prices_equal():
    first = {"price": 10.0, "quantity": 1}
    second = {"price": 10.0, "quantity": 2}
    order = Order(1, [first, second])

    assert order.most_expensive() is first


def test_most_expensive_empty_order():
    with pytest.raises(ValueError):
        Order(1, []).most_expensive()


@pytest.mark.parametrize("percent, expected", [
    (0, [10.0, 3.0, 7.5]),
    (10, [9.0, 2.7, 6.75]),
    (50, [5.0, 1.5, 3.75]),
    (100, [0.0, 0.0, 0.0]),
])
def test_apply_discount_changes_all_prices(order, percent, expected):
    order.apply_discount(percent)

    prices = [item["price"] for item in order.items]
    assert prices == pytest.approx(expected)


@pytest.mark.parametrize("percent", [-5, -0.01, 100.01, 150])
def test_apply_discount_rejects_invalid_percent(order, percent):
    before = [item.copy() for item in order.items]

    with pytest.raises(ValueError, match="Invalid discount"):
        order.apply_discount(percent)

    assert order.items == before


def test_apply_discount_preserves_quantities(order):
    order.apply_discount(10)

    assert [item["quantity"] for item in order.items] == [5, 2, 1]


def test_apply_discount_empty_order():
    order = Order(1, [])

    order.apply_discount(10)

    assert order.items == []


def test_repr(order):
    assert repr(order) == "<Order 1: 3 items>"


def test_repr_empty_order():
    assert repr(Order(2, [])) == "<Order 2: 0 items>"