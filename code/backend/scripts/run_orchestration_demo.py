import asyncio
import json
import os
import sys

import websockets
from websockets.exceptions import ConnectionClosed


def _usage() -> str:
    return (
        "Usage:\n"
        '  One-shot:  python scripts/run_orchestration_demo.py <conv_id> "<question>"\n'
        "  Interactive: python scripts/run_orchestration_demo.py <conv_id>\n"
        "\n"
        "Optional env: WS_HOST (default localhost), WS_PORT (default 8000)\n"
        "\n"
        "Examples:\n"
        '  python scripts/run_orchestration_demo.py 038880b3-... "How does indexing work?"\n'
        "  python scripts/run_orchestration_demo.py 038880b3-..."
    )


def _ws_uri(conv_id: str, host: str, port: int) -> str:
    return f"ws://{host}:{port}/conversations/{conv_id}/ws"


async def _consume_turn(ws, query: str) -> None:
    """Read events for one user message until done, error, or connection closes."""
    await ws.send(query)
    print(f"\n> {query}\n")

    while True:
        try:
            msg = await ws.recv()
        except ConnectionClosed as e:
            print(f"\n[connection closed: {e}]")
            raise

        try:
            event = json.loads(msg)
        except json.JSONDecodeError:
            print(msg)
            continue

        t = event.get("type")
        if t == "content":
            print(event.get("delta", ""), end="", flush=True)
        elif t == "status":
            print(f"\n[status] {event.get('message')}")
        elif t == "tool_call":
            tid = event.get("id")
            prefix = f"{tid} " if tid else ""
            print(f"\n[tool_call] {prefix}{event.get('name')}({event.get('arguments')})")
        elif t == "done":
            print("\n\n[done]")
            return
        elif t == "error":
            print(f"\n[error] {event.get('message')}")
            return
        else:
            print(f"\n[event] {event}")


async def one_shot(conv_id: str, query: str, host: str, port: int) -> None:
    uri = _ws_uri(conv_id, host, port)
    print(f"Connecting to {uri}\n")
    async with websockets.connect(uri) as ws:
        try:
            await _consume_turn(ws, query)
        except ConnectionClosed:
            return


async def interactive(conv_id: str, host: str, port: int) -> None:
    uri = _ws_uri(conv_id, host, port)
    print(f"Connecting to {uri} … (quit or exit to stop)\n")
    async with websockets.connect(uri) as ws:
        while True:
            try:
                query = input("User> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if not query or query.lower() in ("quit", "exit"):
                return
            try:
                await _consume_turn(ws, query)
            except ConnectionClosed:
                return


def main() -> None:
    if len(sys.argv) < 2:
        print(_usage())
        sys.exit(1)

    conv_id = sys.argv[1]
    host = os.environ.get("WS_HOST", "localhost")
    port = int(os.environ.get("WS_PORT", "8000"))

    if len(sys.argv) >= 3:
        query = sys.argv[2]
        asyncio.run(one_shot(conv_id, query, host, port))
    else:
        asyncio.run(interactive(conv_id, host, port))


if __name__ == "__main__":
    main()
