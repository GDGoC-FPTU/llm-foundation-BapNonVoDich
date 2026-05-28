"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Estimated costs per 1M INPUT & OUTPUT tokens (USD) as of March 2026
# Vietnamese text generally consumes ~1.5x - 2.0x more tokens than English due to Unicode/diacritics.
# ---------------------------------------------------------------------------
PRICING_1M_TOKENS = {
    "gpt-4o": {"input": 5.00, "output": 20.00},
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.300},
    "gemini-2.5-pro": {"input": 1.25, "output": 5.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
}

# Standard Model Identifiers
OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"
GEMINI_MODEL = "gemini-2.5-flash"
ANTHROPIC_MODEL = "claude-3-5-haiku"


# ---------------------------------------------------------------------------
# Task 1 — Call OpenAI (GPT-4o)
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    import openai

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start_time

    response_text = response.choices[0].message.content
    usage = {
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
    }

    return response_text, latency, usage


# ---------------------------------------------------------------------------
# Task 2 — Call Google Gemini 2.5 (Standard Practical Model)
# ---------------------------------------------------------------------------
def call_gemini(
    prompt: str,
    model: str = GEMINI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    
    import google.genai as genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    start = time.time()
    response = client.models.generate_content(
        model=model,
        text=prompt,
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens,
    )
    latency = time.time() - start
    text = response.text
    usage = {
        "input_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
    }
    return text, latency, usage


# ---------------------------------------------------------------------------
# Task 3 — Call Anthropic Claude (Exploratory track)
# ---------------------------------------------------------------------------
def call_anthropic(
    prompt: str,
    model: str = ANTHROPIC_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float, dict]:
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    start_time = time.time()
    response = client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start_time

    response_text = response.content[0].text
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    return response_text, latency, usage


# ---------------------------------------------------------------------------
# Task 4 — Compare Models (OpenAI GPT-4o vs OpenAI Mini vs Gemini 2.5 Flash)
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    openai_resp = call_openai(prompt, model=OPENAI_MODEL)
    openai_mini_resp = call_openai(prompt, model=OPENAI_MINI_MODEL)
    gemini_resp = call_gemini(prompt, model=GEMINI_MODEL)

    def compute_cost(model_name: str, usage: dict) -> float:
        rates = PRICING_1M_TOKENS[model_name]
        return (usage["input_tokens"] * rates["input"] + usage["output_tokens"] * rates["output"]) / 1_000_000

    response_text, latency, usage = openai_resp
    result = {
        "gpt4o": {
            "response": response_text,
            "latency": latency,
            "cost": compute_cost("gpt-4o", usage),
            "input_tokens": usage["input_tokens"],
            "output_tokens": usage["output_tokens"],
        },
        "gpt4o_mini": {
            "response": openai_mini_resp[0],
            "latency": openai_mini_resp[1],
            "cost": compute_cost("gpt-4o-mini", openai_mini_resp[2]),
            "input_tokens": openai_mini_resp[2]["input_tokens"],
            "output_tokens": openai_mini_resp[2]["output_tokens"],
        },
        "gemini_flash": {
            "response": gemini_resp[0],
            "latency": gemini_resp[1],
            "cost": compute_cost("gemini-2.5-flash", gemini_resp[2]),
            "input_tokens": gemini_resp[2]["input_tokens"],
            "output_tokens": gemini_resp[2]["output_tokens"],
        },
    }
    return result


# ---------------------------------------------------------------------------
# Task 5 — Streaming chatbot with Gemini 2.5 (Focus Model)
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    import google.genai as genai

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            break

        history.append({"role": "user", "content": user_input})
        history = history[-6:]  # last 3 turns means at most 6 messages

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            text=user_input,
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=256,
        )

        print(response.text)


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    attempt = 0
    while True:
        try:
            return fn()
        except Exception as exc:
            attempt += 1
            if attempt > max_retries:
                raise
            time.sleep(base_delay * (2 ** (attempt - 1)))


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    results = []
    for prompt in prompts:
        comparison = compare_models(prompt)
        comparison["prompt"] = prompt
        results.append(comparison)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    lines = [
        "| Prompt | Model | Response (truncated) | Latency | Tokens (In/Out) | Cost (USD) |",
        "|---|---|---|---|---|---|",
    ]

    for item in results:
        prompt = item["prompt"]
        for model_name, model_label in [
            ("gpt4o", "GPT-4o"),
            ("gpt4o_mini", "GPT-4o-Mini"),
            ("gemini_flash", "Gemini-Flash"),
        ]:
            stats = item[model_name]
            response = stats["response"].replace("\n", " ")
            if len(response) > 50:
                response = response[:47].rstrip() + "..."
            lines.append(
                f"| {prompt} | {model_label} | {response} | {stats['latency']:.2f}s | "
                f"{stats['input_tokens']}/{stats['output_tokens']} | {stats['cost']:.8f} |"
            )
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Model Comparison Test ===")
    test_prompt = "Hãy giải thích sự khác biệt giữa temperature và top_p bằng tiếng Việt ngắn gọn trong 2 câu."
    try:
        # Note: Requires valid API keys set in environment variables
        result = compare_models(test_prompt)
        for model_name, stats in result.items():
            print(f"\n[{model_name.upper()}]")
            print(f"Latency: {stats['latency']:.2f}s | Cost: ${stats['cost']:.6f}")
            print(f"Tokens: {stats['input_tokens']} in / {stats['output_tokens']} out")
            print(f"Response: {stats['response']}")
    except Exception as e:
        print(f"Skipping live API comparison test: {e}")
        print("Set your API keys to run manual tests.")

    print("\n=== Starting Gemini 2.5 Chatbot (type 'quit' to exit) ===")
    try:
        streaming_chatbot()
    except Exception as e:
        print(f"Chatbot failed to start: {e}")
