EXPLORATORY_MODEL = "gpt-4"
STATIC_MODEL = "gpt-35-turbo"

LIMITS = {
    "gpt-35-turbo": {
        "max_tokens_no_chunk": 4000,
        "max_tokens_prompt": 1000,
        "max_tokens_per_chunk": 2000,
    },
    "gpt-4": {
        "max_tokens_no_chunk": 8000,
        "max_tokens_prompt": 2000,
        "max_tokens_per_chunk": 4000,
    },
}
