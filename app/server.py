from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from app.chains.prompt_chain import prompt_chain
from app.chains.shop_chain import shop_chain
from app.chains.products_filter_chain import products_filter_chain

app = FastAPI(
    title="My Local LangChain App",
    version="1.0",
    description="LangChain with a local Ollama model",
)


@app.get("/")
async def redirect_root_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs")


add_routes(
    app,
    prompt_chain,
    path="/prompt",
)

add_routes(
    app,
    shop_chain,
    path="/shop",
)

add_routes(
    app,
    products_filter_chain,
    path="/products_filter",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)