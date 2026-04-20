import asyncio
import json
import websockets
import uuid

async def test_websocket_agent(conv_id: str):
    uri = f"ws://127.0.0.1:8000/conversations/{conv_id}/ws"
    
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Type your query (or 'quit' to exit):")
            
            # Simple chat loop
            while True:
                query = input("\nUser> ")
                if query.lower() in ["quit", "exit"]:
                    break
                    
                # Send the query to the socket
                await websocket.send(query)
                print("\nAgent> ", end="", flush=True)
                
                # Receive events until the stream ends
                try:
                    while True:
                        msg = await websocket.recv()
                        
                        try:
                            event = json.loads(msg)
                            
                            if event.get("type") == "content":
                                # Stream tokens to standard output linearly
                                print(event.get("delta", ""), end="", flush=True)
                                
                            elif event.get("type") == "status":
                                # Print internal status thoughts
                                print(f"\n[Status: {event.get('message')}]", end="", flush=True)
                                
                            elif event.get("type") == "tool_call":
                                # Agent bounded tool firing
                                print(f"\n[Tool Execution: {event.get('name')} | arguments: {event.get('arguments')}]", end="", flush=True)
                                
                            elif event.get("type") == "error":
                                print(f"\n[Error: {event.get('message')}]")
                                break
                                
                            elif event.get("type") == "done":
                                break
                                
                        except json.JSONDecodeError:
                            print(msg, end="", flush=True)
                            
                except websockets.exceptions.ConnectionClosed:
                    print("\n[Stream concluded.]")
                    # If socket closes we wait for reconnect or drop.
                    break
                    
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    # Standard format: python test_client.py <CONVERSATION_UUID>
    import sys
    if len(sys.argv) < 2:
        print("Usage: python test_client.py <CONVERSATION_UUID>")
        sys.exit(1)
        
    conv_id = sys.argv[1]
    asyncio.run(test_websocket_agent(conv_id))
