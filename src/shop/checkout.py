"""Order checkout.

The rules live in `src/shop/specs/checkout.md` - read it first.
Both functions below are stubs: their signature is final, the bodies are yours.
Do not change the constants: the tests rely on them.
"""

from shop.money import percent_of

PROMO_CODES = {"WELCOME10": 10, "SUMMER15": 15, "VIP35": 35}
SUPPORTED_CITIES = ("msk", "spb")
MAX_DISCOUNT_PERCENT = 30
VAT_PERCENT = 20
SHIPPING_KOPEKS = 49_000
FREE_DELIVERY_FROM_KOPEKS = 500_000
TIER_DISCOUNTS = ((10, 5), (25, 10), (50, 15))
REQUIRED_LINE_KEYS = ("sku", "qty", "unit_price_kopecks")


def validate_order(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> str | None:
    """Return a human readable reason why the order is invalid, or None if it is fine."""
    if not lines:
        return "order has no lines"
    seen_skus: set[str] = set()
    for position in lines:
        for key in REQUIRED_LINE_KEYS:
            if key not in position:
                return f"line is missing required key {key}"
        if position.get("sku") == "":
            return "line has an empty sku"
        if not position["qty"].isdigit():
            return "line quantity must be a whole number"
        if int(position["qty"]) <= 0:
            return "line quantity must be greater than zero"
        if not position["unit_price_kopecks"].lstrip("-").isdigit():
            return "line price must be a whole number"
        if int(position["unit_price_kopecks"]) < 0:
            return "line price must not be negative"
        if position["sku"] in seen_skus:
            return "line sku is duplicated"
        seen_skus.add(position["sku"])
    if promo_code and promo_code not in PROMO_CODES:
        return "unknown promo code"
    if shipping_city and shipping_city not in SUPPORTED_CITIES:
        return "unsupported shipping city"
    return None


def calculate_order_total(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> int | None:
    """Return the order total in kopecks, or None if the order is invalid."""
    if validate_order(lines, promo_code, shipping_city) is not None:
        return None
    subtotal = sum(
        int(position["qty"]) * int(position["unit_price_kopecks"]) for position in lines
    )
    quantity = sum(int(position["qty"]) for position in lines)
    tier_percent = 0
    for threshold, percent in TIER_DISCOUNTS:
        if quantity >= threshold:
            tier_percent = percent
    promo_percent = PROMO_CODES.get(promo_code, 0)
    discount_percent = min(max(tier_percent, promo_percent), MAX_DISCOUNT_PERCENT)
    discount = percent_of(subtotal, discount_percent)
    discounted_subtotal = subtotal - discount
    vat = percent_of(discounted_subtotal, VAT_PERCENT)
    return discounted_subtotal + vat
