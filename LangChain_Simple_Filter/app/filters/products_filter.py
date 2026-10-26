def filter_products(
        products: list[dict],
        max_price: int | None = None,
        min_ram_gb: int | None = None,
        min_storage_gb: int | None = None,
        max_weight_kg: float | None = None,
        brand: str | None = None,
        purpose: str | None = None,
) -> list[dict]:
    filtered = products

    if max_price is not None:
        filtered = [
            p for p in filtered
            if p["price"] <= max_price
        ]

    if min_ram_gb is not None:
        filtered = [
            p for p in filtered
            if p["ram_gb"] >= min_ram_gb
        ]

    if min_storage_gb is not None:
        filtered = [
            p for p in filtered
            if p["storage_gb"] >= min_storage_gb
        ]

    if max_weight_kg is not None:
        filtered = [
            p for p in filtered
            if p["weight_kg"] <= max_weight_kg
        ]

    if brand is not None:
        filtered = [
            p for p in filtered
            if p["brand"].casefold() == brand.casefold()
        ]

    if purpose is not None:
        filtered = [
            p for p in filtered
            if any(
                purpose.casefold() in item.casefold()
                for item in p["purpose"]
            )
        ]

    return filtered 