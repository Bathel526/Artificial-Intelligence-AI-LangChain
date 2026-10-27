from langchain.chat_models import init_chat_model

model = init_chat_model(
    model = "qwen3:4b-instruct-2507-q4_K_M",
    model_provider="ollama",
    temperature=0,
    num_predict=1024,
)