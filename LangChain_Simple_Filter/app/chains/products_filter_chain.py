
import json
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from app.core.model import model
from app.prompts.products_filter_prompt import products_filter_prompt
from app.filters.products_filter import filter_products

from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableLambda


PRODUCTS_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "products_structured.json"
)

with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
    products = json.load(file)


criteria_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Przeanalizuj pytanie użytkownika i rozpoznaj kryteria
wyboru laptopa.

Zwróć wyłącznie poprawny JSON z polami:
- max_price: maksymalna cena w złotych lub null
- min_ram_gb: minimalny RAM w GB lub null
- min_storage_gb: minimalna pojemność dysku w GB lub null
- max_weight_kg: maksymalna waga w kg lub null
- brand: marka lub null
- purpose: zastosowanie lub null

Zasady:
1. Użytkownik może pisać potocznym językiem.
2. „Do 3000 zł” oznacza max_price = 3000.
3. „Minimum 16 GB RAM” oznacza min_ram_gb = 16.
4. „Dysk co najmniej 512 GB” oznacza min_storage_gb = 512.
5. „Lekki laptop do 1,5 kg” oznacza max_weight_kg = 1.5.
6. Nie wymyślaj wymagań, których użytkownik nie podał.
7. Jeśli kryterium nie zostało określone, ustaw null.
8. Zwróć tylko JSON, bez komentarzy.

Przykład:
Pytanie: Laptop do 3000 zł do nauki, z 16 GB RAM.
Odpowiedź:
{{
  "max_price": 3000,
  "min_ram_gb": 16,
  "min_storage_gb": null,
  "max_weight_kg": null,
  "brand": null,
  "purpose": "nauka"
}}
"""
    ),
    ("human", "{question}"),
])

criteria_chain = criteria_prompt | model | JsonOutputParser()

class ProductsFilterInput(BaseModel):
    question: str = Field(
        ...,
        description="Opisz, jakiego laptopa szukasz",
    )

def run_products_filter(inputs: dict):
    question = inputs["question"]

    criteria = criteria_chain.invoke({
        "question": question,
    })

    allowed_keys = {
        "max_price",
        "min_ram_gb",
        "min_storage_gb",
        "max_weight_kg",
        "brand",
        "purpose",
    }

    criteria = {
        key: criteria.get(key)
        for key in allowed_keys
    }

    # 3. Odfiltruj produkty programowo.
    filtered_products = filter_products(
        products,
        **criteria,
    )

    answer = (
        products_filter_prompt
        .partial(
            products=json.dumps(
                filtered_products,
                ensure_ascii=False,
                indent=2,
            )
        )
        | model
    ).invoke({
        "question": question,
    })

    return answer.content


from langchain_core.runnables import RunnableLambda

products_filter_chain = RunnableLambda(
    run_products_filter
).with_types(input_type=ProductsFilterInput)
