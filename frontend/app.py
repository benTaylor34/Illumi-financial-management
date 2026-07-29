import streamlit as st
import requests

st.set_page_config(page_title="Illumi - Financial AI", page_icon="✨", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        max-width: 400px;
        margin: auto;
        border: 12px solid #1C2541;
        border-radius: 40px;
        background-color: #0B132B;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        overflow: hidden;
        color: #FFFFFF;
    }
    header {visibility: hidden;}
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #FFFFFF !important;
    }
    .stChatMessage {
        background-color: #1C2541 !important;
        border: 1px solid #3A506B;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 8px;
    }
    .stChatInputContainer input {
        background-color: #1C2541 !important;
        color: #FFFFFF !important;
        border: 1px solid #3A506B !important;
    }
    hr {
        border-color: #3A506B !important;
    }
    /* Merchant badge styling */
    .merchant-badge {
        display: inline-flex;
        align-items: center;
        background: #0B132B;
        border: 1px solid #3A506B;
        padding: 4px 8px;
        border-radius: 8px;
        margin: 2px 0;
        font-size: 13px;
    }
    .merchant-badge img {
        width: 16px;
        height: 16px;
        margin-right: 6px;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("### ✨ Illumi")
st.caption("Your Financial AI Assistant")
st.divider()

# Dictionary mapping merchants from enriched_statement to their domain logos
MERCHANT_DOMAINS = {
    "Spotify": "spotify.com",
    "McDonald's": "mcdonalds.com",
    "Asda": "asda.com",
    "Vanguard": "vanguard.com",
    "Amazon": "amazon.com",
    "Tesco": "tesco.com",
    "Trainline": "trainline.com",
    "Uber": "uber.com",
    "Google One": "google.com",
    "iD Mobile": "idmobile.co.uk",
    "Nomad eSIM": "getnomad.app",
    "Bike Share Toronto": "bikesharetoronto.com",
    "PRESTO (Toronto Transit)": "prestocard.ca"
}

def add_merchant_logos(text: str) -> str:
    """Detects merchant names in Illumi's reply and injects brand logos."""
    processed_text = text
    for merchant, domain in MERCHANT_DOMAINS.items():
        if merchant.lower() in processed_text.lower():
            logo_url = f"https://logo.clearbit.com/{domain}"
            badge_html = f"""<span class="merchant-badge"><img src="{logo_url}" onerror="this.style.display='none'"><strong>{merchant}</strong></span>"""
            # Replace merchant text with badged version safely (case-insensitive approach can be adapted)
            processed_text = processed_text.replace(merchant, badge_html)
    return processed_text

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm Illumi. Ask me anything about your spending history, subscriptions, or recent trips without any judgment! 💡"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Render HTML badges for assistant messages
        if message["role"] == "assistant":
            st.markdown(add_merchant_logos(message["content"]), unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("Ask about your spending..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Illumi is thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"message": prompt}
                )
                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data.get("reply", "I couldn't fetch an answer right now.")
                else:
                    bot_reply = f"Oops! Received an error from the server (Status {response.status_code})."
            except Exception as e:
                bot_reply = f"Unable to connect to the FastAPI backend: {e}"
            
            formatted_reply = add_merchant_logos(bot_reply)
            st.markdown(formatted_reply, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})