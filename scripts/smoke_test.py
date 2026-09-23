"""Smoke-test a served North Mini Code endpoint.

Checks three things the research plan depends on, in order of how badly a
failure would corrupt results:
  1. the server answers at all
  2. tool calls parse (a parser bug here reads as a model failure)
  3. reasoning is returned separately from content
"""
import json
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8100"

TOOL = {
    "type": "function",
    "function": {
        "name": "run_tests",
        "description": "Run the test suite and return failures.",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
}


def post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())


def main() -> int:
    with urllib.request.urlopen(f"{BASE}/v1/models", timeout=30) as r:
        model = json.loads(r.read())["data"][0]["id"]
    print(f"[1/3] served model: {model}")

    out = post("/v1/chat/completions", {
        "model": model,
        "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
        "max_tokens": 32, "temperature": 0,
    })
    print(f"[2/3] plain completion: {out['choices'][0]['message']['content']!r}")

    out = post("/v1/chat/completions", {
        "model": model,
        "messages": [{"role": "user", "content": "Run the tests in tests/test_cart.py"}],
        "tools": [TOOL], "tool_choice": "auto",
        "max_tokens": 256, "temperature": 0,
    })
    msg = out["choices"][0]["message"]
    calls = msg.get("tool_calls") or []
    if calls:
        fn = calls[0]["function"]
        print(f"[3/3] tool call parsed: {fn['name']}({fn['arguments']})")
    else:
        print(f"[3/3] NO TOOL CALL — parser suspect. content={msg.get('content')!r}")
    # vLLM calls it "reasoning"; llama.cpp calls it "reasoning_content".
    # Code that checks only one silently sees no reasoning on the other stack.
    reasoning = msg.get("reasoning") or msg.get("reasoning_content") or ""
    if reasoning:
        field = "reasoning" if msg.get("reasoning") else "reasoning_content"
        print(f"      reasoning returned separately: {len(reasoning)} chars "
              f"(field: {field})")
    else:
        print("      NO REASONING RETURNED — check both field names")
    return 0 if calls else 1


if __name__ == "__main__":
    raise SystemExit(main())
