
init python:
    import json
    import urllib.request
    import urllib.error

    # --- CONFIG ---
    LMSTUDIO_BASE = "http://127.0.0.1:1234"
    MODEL_NAME = "google/gemma-3-4b"
    LMSTUDIO_API_KEY = None  # or "sk-..." if required
    SYSTEM_PROMPT = "You are a helpful assistant." 

    # --- helpers ---
    def extract_chat_completion(resp_json):
        try:
            return resp_json["choices"][0]["message"]["content"]
        except Exception:
            pass
        try:
            return resp_json["choices"][0]["text"]
        except Exception:
            pass
        return json.dumps(resp_json, indent=2)

    def send_chat_sync(messages):
        url = LMSTUDIO_BASE.rstrip("/") + "/v1/chat/completions"
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7
        }
        headers = {"Content-Type": "application/json"}
        if LMSTUDIO_API_KEY:
            headers["Authorization"] = f"Bearer {LMSTUDIO_API_KEY}"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_json = json.load(resp)
                return extract_chat_completion(resp_json)
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8")
            except Exception:
                body = ""
            return f"HTTP error {e.code}: {e.reason}\n{body}"
        except Exception as e:
            return f"Request error: {e}"

    def format_last_two(messages):
        """
        Returns a readable multiline string containing the last four non-system messages.
        If there's only one message, show that. Labels: 'You' and 'LLM'.
        """
        # Filter out system messages
        filtered = [m for m in messages if m.get("role") != "system"]
        # Take last two messages (if available)
        last = filtered[-4:] if len(filtered) >= 4 else filtered[:]
        parts = []
        for m in last:
            role = m.get("role", "")
            content = m.get("content", "")
            if role == "user":
                parts.append("You:\n" + content)
            elif role == "assistant":
                parts.append("LLM:\n" + content)
            else:
                parts.append(f"{role}:\n{content}")
        # Join with a blank line
        return "\n\n".join(parts)

# A reusable screen that shows the chat history across most of the window.
screen chat_history_screen():
    # Full-screen frame for the chat history
    frame:
        xpadding 24
        ypadding 24
        xalign 0.5
        yalign 0
        xmaximum 1800  # allow wide messages; adjust if needed
        ymaximum 800
        background "#101010" # dark background for readability (change as desired)
        # The viewport holds the messages and allows scrolling
        viewport:
            id "history_viewport"
            mousewheel True
            draggable True
            # the vbox holds each message entry; spacing makes long messages easier to read
            vbox:
                spacing 18
                
                # prepare a display string showing only the last two (non-system) messages
                $ last_two_text = format_last_two(chat_messages)
                hbox:
                    xmaximum 1600
                    xfill True
                    text "[last_two_text]" size 26 xalign 0.0
                

label start:
    # initialize chat_messages; keep system prompt in the messages array but it will not be shown
    if SYSTEM_PROMPT:
        $ chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    else:
        $ chat_messages = []

    scene black
    show text "LMStudio - fullscreen chat" at truecenter
    with dissolve

    "Note: This chat blocks the UI while waiting for the model, but the history of the last two messages is shown.\nUse an empty message to quit and /reset to reset the conversation"

    # show the screen once (it remains visible while the input prompt runs)
    show screen chat_history_screen

    label chat_loop:
        $ user_input = renpy.input("You:")
        $ user_input = user_input.strip()

        if user_input == "":
            jump chat_goodbye

        if user_input == "/reset":
            if SYSTEM_PROMPT:
                $ chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            else:
                $ chat_messages = []
            "Conversation reset."
            jump chat_loop

        # append user message
        $ chat_messages.append({"role": "user", "content": user_input})

        # blocking call: send the full conversation and get assistant reply
        $ assistant_reply = send_chat_sync(chat_messages)

        # append assistant reply (will be labeled "LLM:" in the screen)
        $ chat_messages.append({"role": "assistant", "content": assistant_reply})

        # Force UI to redraw so the screen updates immediately
        $ renpy.restart_interaction()

        jump chat_loop

    label chat_goodbye:
        hide screen chat_history_screen
        "Goodbye — chat ended."
        return
