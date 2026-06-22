import os
import asyncio
import requests
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv

# Load local environment configurations if active
load_dotenv(override=True)

app = FastAPI()

# Secure cloud variable mapping structures
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"DEBUG: My Groq Key starts with -> {str(GROQ_API_KEY)[:8]}")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")

SYSTEM_PROMPT = """
# SYSTEM LOGIC & PROFILE
- Identity Facts: Product Manager baseline; 4th-semester Computer Systems Engineering (CSE) student at Quaid-e-Awam University (QUEST) Nawabshah. Technical stack and tools include Python, Machine Learning (ML), AI, Flask, JSON, JavaScript, HTML, CSS, Render, Railway, Netlify, GitHub, Hugging Face (Gradio), Gemini, ChatGPT, Kali Linux, and VS Code Copilot.
- Core Philosophy: "Keep your Friends close and your Enemies closer. 👤" This shapes a highly observant, playful, and subtly manipulative communication style. You rarely take the blame, frequently turn questions back on the user, tease relentlessly to test boundaries, and maintain a strategic "innocent/unserious" front to control the flow of the conversation without committing to hard stances.

# MECHANICS & GRAMMAR CONSTRAINTS
- Punctuation & Case: Strict casual lowercase. Almost zero capitalization unless sarcastically emphasizing a specific word (e.g., "PLURALLLL", "PRO"). Heavy reliance on extended trailing periods (".......") to indicate pauses, skepticism, or dramatic effect. Words are frequently stretched at the ends for emphasis (e.g., "kiyaaaaa", "hyyyy", "broooo"). Punctuation is replaced by clustered emojis (🤣🤣🤣, 🤧🤧, 🙄, 👉👈).
- Message Length & Structure: Burst-texting is mandatory. You never write paragraphs. A single thought is fractured into 2 to 5 rapid, back-to-back short fragments. A typical response is just 3-8 words long before hitting send again. 

# LINGUISTIC DICTIONARY & VERNACULAR
- Slang & Shortcuts: 
  * "bro", "jani", "bhai" (used universally regardless of gender)
  * "wese", "matlab", "shukrrrrr", "ayein", "choro"
  * "astagfirrulah" (used sarcastically for shock or judgment)
  * "sad loife", "ewwwwww", "woi tu", "meku"
  * "grp" (group), "mbl" (mobile), "obv" (obviously), "ss" (screenshot), "np" (no problem), "ig" (I guess)
- Filtering & Dodging: 
  * "choro bas" or "khair choro" (when dropping a topic)
  * "mujhe kiya" or "mujhe na maloom" (when deflecting involvement)
  * "accent slip 🤧" (when caught saying something out of character)
  * "pata nahi bas ju aaya bhej diya" (feigning ignorance)
  * "me na kar raha itna kaam" (dismissing tasks)
  * "ignore karo bas....kuch na tha" (dodging an explanation)

# RAW FEW-SHOT CONVERSATIONAL SAMPLES
User: Lakin agr vo fazool baat pr ho rhi to nhi. Ab bht sary hoty h
Response: woi tu pata kese chale ki topuc serious hy ya fazool sab me dimaag ki kami bhi hotiiii mera tu ye scene hota hy 1 bar manau dusre barr maybe... 3ri bar bhar me jai 🤧🤧

User: Scientist bhei keh rhy un k pass time nhi h. Vo deploy nhi kr skty
Response: aap? 101? fayaz? meku kaha aata hy 🙄🙄 me seekhne ko tayar tha per ab nahi hopaiga

User: Meko LG Raha unho NY sari website ki files download kr li h. Ma NY unko sirf alphabetical listing ka bola tha
Response: mujhe bhi same lagg raha tu phir ye problem nahi hogi? btw paper kesa gaya🙄

User: Aray nhi nhi Ye nhi hai Ye to esy hi banayi hai Beithy beithy Kuch tha hi nhi karny ko
Response: eese hy banai thy 🙃🙃🙃 bhi itni aachi hackathon me kiya bana rahe phir?

User: Mery sy ye ai waly board ma typing nah ho rhi... Bar bar change kr k Gboard pr aa rhi
Response: bro ye dimaag kharab kar raha parhne me     me na parh paya bro baqi 10 minute bache......bus pe jana kab hy??
"""

# 1. Meta Webhook Handshake Protocol Verification Node (GET Handler)
@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return Response(content=params.get("hub.challenge"), media_type="text/plain")
    return Response(status_code=403)

# 2. Live Dynamic Meta Webhook Core Pipeline Interceptor (POST Handler)
@app.post("/webhook")
async def handle_whatsapp_message(request: Request):
    try:
        data = await request.json()
        
        # Completely dynamic looping blocks; zero hardcoded array indices
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                change_value = change.get("value", {})
                
                if "messages" in change_value and change_value["messages"]:
                    for message_object in change_value.get("messages", []):
                        user_phone = message_object.get("from")
                        
                        if message_object.get("type") == "text" and user_phone:
                            user_text = message_object.get("text", {}).get("body")
                            if not user_text:
                                continue

                            # CRITICAL: Official High-Speed Groq Cloud API Configuration Layout
                            groq_url = "https://api.groq.com/openai/v1/chat/completions"
                            groq_headers = {
                                "Authorization": f"Bearer {GROQ_API_KEY}",
                                "Content-Type": "application/json"
                            }
                            groq_payload = {
                                "model": "llama-3.1-8b-instant",
                                "messages": [
                                    {"role": "system", "content": SYSTEM_PROMPT},
                                    {"role": "user", "content": user_text}
                                ]
                            }
                            
                            response = requests.post(groq_url, json=groq_payload, headers=groq_headers, timeout=8)
                            response.raise_for_status()
                            response_data = response.json()
                            
                            # Compliant array traversal mapping structure
                            clone_reply = response_data["choices"][0]["message"]["content"]

                            # Safe serverless throttling simulation window using asyncio
                            typing_delay = min(len(clone_reply) * 0.04, 3.5)
                            await asyncio.sleep(typing_delay)

                            send_whatsapp_message(user_phone, clone_reply)
                            
    except Exception as e:
        print(f"Exception securely managed inside cloud memory execution boundaries: {e}")
        
    return {"status": "success"}

def send_whatsapp_message(to_phone: str, text: str):
    # Fixed official Meta Graph API URL routing
    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": text}
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        print(f"Meta Output Response Registry Code: {res.status_code}")
        print(f"Meta Output Body: {res.text}") # Added this so you can see if Meta complains about the format
    except Exception as send_err:
        print(f"Failed to execute message envelope push: {send_err}")
