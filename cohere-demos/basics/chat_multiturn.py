import os
import cohere


def require_env(name: str) -> str:
    """Fetch a required environment variable or raise a clear error."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is not set")
    return value


def extract_text_blocks(message_content) -> str:
    """
    Cohere Chat returns structured content blocks (a list).
    This function extracts and concatenates the text blocks.
    """
    return "".join(
        block.text
        for block in message_content
        if hasattr(block, "text") and block.text
    ).strip()


def chat_turn(co, model: str, messages: list[dict], max_tokens: int) -> str:
    """
    Send the current conversation state (messages) to Cohere and return the assistant text.
    Note: The model does not 'remember' between calls — we pass memory via `messages`.
    """
    response = co.chat(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )
    return extract_text_blocks(response.message.content)


def main() -> None:
    api_key = require_env("COHERE_API_KEY")
    co = cohere.ClientV2(api_key=api_key)

    model = "command-a-03-2025"
    max_tokens = 260

    # Conversation state: we explicitly carry memory forward by appending messages.
    messages: list[dict] = [
        {"role": "user", "content": "Explain TLS in very simple terms."}
    ]

    # Turn 1
    assistant_1 = chat_turn(co, model=model, messages=messages, max_tokens=max_tokens)
    print("Assistant (turn 1):\n")
    print(assistant_1)
    print("\n" + "-" * 60 + "\n")

    # Add the assistant reply to the conversation state
    messages.append({"role": "assistant", "content": assistant_1})

    # Turn 2 (follow-up)
    messages.append({"role": "user", "content": "Explain it again, but for a 10-year-old."})

    assistant_2 = chat_turn(co, model=model, messages=messages, max_tokens=max_tokens)
    print("Assistant (turn 2):\n")
    print(assistant_2)


if __name__ == "__main__":
    main()