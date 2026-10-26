from app.core.model import model
from app.prompts.shop_prompt import shop_prompt
from app.data.products import products


shop_chain = shop_prompt.partial(
    products=products,
) | model