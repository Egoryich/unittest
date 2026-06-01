def final_price_cents(
    base_cents: int, discount_percent: int = 0, tax_percent: int = 20
) -> int:
    if type(base_cents) is not int:
        raise TypeError("base_cents must be int")
    if type(discount_percent) is not int:
        raise TypeError("discount_percent must be int")
    if type(tax_percent) is not int:
        raise TypeError("tax_percent must be int")
    if base_cents < 0:
        raise ValueError("base_cents must be >= 0")
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be in 0..100")
    if not 0 <= tax_percent <= 100:
        raise ValueError("tax_percent must be in 0..100")

    discounted = base_cents * (100 - discount_percent) / 100
    taxed = discounted * (100 + tax_percent) / 100
    return int(round(taxed))

