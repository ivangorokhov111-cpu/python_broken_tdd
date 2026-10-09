"""Order checkout.

The rules live in `src/shop/specs/checkout.md` - read it first.
Both functions below are stubs: their signature is final, the bodies are yours.
Do not change the constants: the tests rely on them.
"""

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
    return None


def calculate_order_total(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> int | None:
    """Return the order total in kopecks, or None if the order is invalid."""
    ...
