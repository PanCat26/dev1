import asyncio
import json
import sys

import websockets


USAGE = (
    "Usage:\n"
    '  python scripts/run_orchestration_demo.py <conv_id> "<your question>"\n'
    "\n"
    "Example:\n"
    '  python scripts/run_orchestration_demo.py 038880b3-5838-4699-a362-12703a2d431c "How does indexing work?"'
)


async def chat(conv_id: str, query: str, host: str = "localhost", port: int = 8000):
    uri = f"ws://{host}:{port}/conversations/{conv_id}/ws"
    print(f"Connecting to {uri}\n")

    async with websockets.connect(uri) as ws:
        await ws.send(query)
        print(f"> {query}\n")

        while True:
            msg = await ws.recv()
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
                name = event.get("name")
                args = event.get("arguments")
                print(f"\n[tool_call] {name}({args})")
            elif t == "done":
                print("\n\n[done]")
                return
            elif t == "error":
                print(f"\n[error] {event.get('message')}")
                return
            else:
                print(f"\n[event] {event}")


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)

    conv_id = sys.argv[1]
    query = sys.argv[2]
    asyncio.run(chat(conv_id, query))


if __name__ == "__main__":
    main()
