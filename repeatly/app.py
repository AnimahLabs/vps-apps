"""
Repeatly — Restaurant Review Response Agent
MVP: Basic restaurant info + review → contextual response options
"""

import streamlit as st
import os
import json
import re
import requests
from datetime import datetime

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Repeatly",
    page_icon="🍽️",
    layout="centered"
)

# MiniMax API
API_URL = "https://api.minimax.io/anthropic/v1/messages"
MODEL = "MiniMax-M2.7"
DEFAULT_API_KEY = "sk-cp-86PdTVq7y2U3xsmeIaf26pC7_HCiGA-hpBx_dFTEQB9fwfeTfl0yAQlvpIj_-m2EkTIjiWvb4dL2NLzoMH8-JwM91GLQvM36wbezNRVPUFjCCNjfDUb3w8o"

# ─────────────────────────────────────────────
# Initialize session state
# ─────────────────────────────────────────────
if "api_key_configured" not in st.session_state:
    st.session_state.api_key_configured=True
if "api_key" not in st.session_state:
    st.session_state.api_key=DEFAULT_API_KEY

# ─────────────────────────────────────────────
# Prompt Engineering (the core product)
# ─────────────────────────────────────────────

def build_prompt(restaurant_info: dict, review_text: str, brand_voice: str, response_length: str) -> str:
    """Build the agent prompt — this is where the magic happens."""

    length_instruction = {
        "short": "Keep it under 50 words. Concise and warm.",
        "medium": "Keep it under 100 words. Friendly and personal.",
        "long": "Keep it under 150 words. Detailed and thoughtful."
    }.get(response_length, "Keep it under 100 words.")

    review_lower = review_text.lower()
    negative_indicators = ["terrible", "awful", "worst", "horrible", "disgusting", "rude", "cold", "slow", "burnt", "raw", "undercooked", "overcooked", "salty", "bland", "dirty", "never", "disappointed", "disappointing", "bad", "poor", "mediocre", "noisy", "expensive", "overpriced"]
    positive_indicators = ["amazing", "delicious", "best", "great", "fantastic", "wonderful", "perfect", "love", "loved", "fresh", "incredible", "outstanding", "friendly", "recommend", "favorite", "gem"]

    negative_count = sum(1 for w in negative_indicators if w in review_lower)
    positive_count = sum(1 for w in positive_indicators if w in review_lower)

    if negative_count > positive_count:
        sentiment_instruction = """This is a NEGATIVE review. Your response must:
1. Apologize sincerely — acknowledge their specific complaint
2. Show genuine empathy — they had a bad experience and that matters
3. Offer to make it right — invite them to contact you directly
4. NEVER be defensive, dismissive, or excuse-making
5. Keep it professional but warm"""
    elif positive_count > negative_count:
        sentiment_instruction = """This is a POSITIVE review. Your response must:
1. Express genuine, specific gratitude — reference what they loved
2. Mention a specific dish, staff name, or detail they referenced
3. Invite them to return — make them feel valued
4. Sound like you mean it, not like a template"""
    else:
        sentiment_instruction = """This is a NEUTRAL review. Your response should:
1. Thank them for their feedback
2. Address any specific points they mentioned
3. Invite them to return or offer to hear more"""

    # Extract mentioned items
    mentioned_items = []
    dish_list = restaurant_info.get("popular_dishes", "").lower()
    if dish_list:
        dishes = [d.strip() for d in dish_list.split(",")]
        for dish in dishes:
            if dish and len(dish) > 2 and dish in review_lower:
                mentioned_items.append(dish.title())

    staff_mentioned = []
    staff_list = restaurant_info.get("staff_names", "")
    if staff_list:
        staff_names = [s.strip() for s in staff_list.split(",")]
        for staff in staff_names:
            if staff and len(staff) > 2:
                parts = staff.lower().split()
                for part in parts:
                    if part in review_lower and part not in ["the", "was", "and", "for", "with"]:
                        mentioned_items.append(staff.title())
                        staff_mentioned.append(staff.title())
                        break

    context_additions = ""
    if mentioned_items:
        unique_items = list(set(mentioned_items))[:3]
        context_additions = f"\nSpecifically mentioned by customer: {', '.join(unique_items)}"

    if staff_mentioned:
        unique_staff = list(set(staff_mentioned))[:2]
        context_additions += f"\nStaff member(s) to recognize: {', '.join(unique_staff)}"

    brand_notes = ""
    if restaurant_info.get("recent_context"):
        brand_notes = f"\nRecent context to be aware of: {restaurant_info.get('recent_context')}"

    return f"""You are a restaurant manager. Write one response to this review:

{restaurant_info.get('restaurant_name', 'The restaurant')} - {restaurant_info.get('vibe', 'casual')} vibe, {restaurant_info.get('cuisine_type', 'American')} cuisine.

Review: "{review_text}"

Write one response that:
- Matches the sentiment of the review (negative, positive, mixed, or neutral)
- References specific details mentioned in the review
- Sounds like a real restaurant manager, not generic corporate language

Write only the response. Nothing else."""


# ─────────────────────────────────────────────
# LLM Call
# ─────────────────────────────────────────────

def get_api_key() -> str:
    """Get API key from session state (user-configured)."""
    return st.session_state.get("api_key", "")


def generate_responses(prompt: str) -> str:
    """Call MiniMax API to generate response options."""

    api_key = st.session_state.get("api_key", "")
    if not api_key:
        return "Error: No API key found. Please configure your MiniMax API key."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": MODEL,
        "max_tokens": 800,
        "temperature": 0.8,
        "thinking": {
            "type": "off"
        },
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        # If error, include the actual error message
        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", response.text)
            except:
                error_msg = response.text
            return f"Error {response.status_code}: {error_msg}"

        data = response.json()

        # MiniMax/M2.7 returns content as a list of blocks
        # Blocks can have type="text" with actual response, type="thinking" with reasoning
        if "content" in data and isinstance(data["content"], list):
            # First, try to find a text block with the actual response
            for block in data["content"]:
                if block.get("type") == "text" and block.get("text"):
                    return block["text"]

            # Fall back to thinking block if no text found
            for block in data["content"]:
                if block.get("thinking"):
                    return block["thinking"]

        return f"Error: Unexpected response format: {str(data)[:2000]}"

    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def parse_single_response(text: str) -> str:
    """Parse the LLM output to extract the single response.

    Since we now ask for one response, this is simpler than parse_responses.
    """
    if text.startswith("Error"):
        return text

    # Clean up the text - remove any label prefixes like "Response 1:" or "Option A:"
    cleaned = re.sub(r'^(?:Response\s+\d+|Option\s+[ABC])[\s:\]]+', '', text, flags=re.IGNORECASE | re.MULTILINE)

    # Remove any remaining label-like prefixes on subsequent lines
    lines = cleaned.split('\n')
    real_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip meta-text lines
        if re.match(r'^(?:Let\'s?|I\'ll|I will|We\'ll|First|Second|Third|The |Write |Need |Response |Option )', stripped, re.IGNORECASE):
            if len(stripped) < 80:
                continue
        if stripped.startswith('[') and stripped.endswith(']'):
            continue
        if re.match(r'^(?:\d+\.|\-|•)', stripped):
            continue
        real_lines.append(stripped)

    result = ' '.join(real_lines).strip()
    result = re.sub(r"Let's count[^.]*\.?", "", result, flags=re.IGNORECASE)
    result = re.sub(r"Word count[^.]*\.?", "", result, flags=re.IGNORECASE)
    result = re.sub(r"Approximate[^.]*\.?", "", result, flags=re.IGNORECASE)
    result = re.sub(r"\s{2,}", " ", result)

    return result if result else text.strip()


def parse_responses(text: str) -> list:
    """Parse the LLM output into individual response options.

    Handles cases where the thinking block contains both instructions
    and actual response text mixed together, or outputs [response N] placeholders.
    """

    if text.startswith("Error"):
        return [text]

    responses = []

    # Strategy: Find each "Option X:" or "Response N:" then extract text until the next label or end
    # Look for various label patterns
    option_pattern = re.compile(
        r'(?:Option\s+([ABC])|Response\s+(\d))[\s:\]]+(.*?)(?=(?:(?:Option\s+[ABC])|(?:Response\s+\d))|$)',
        re.IGNORECASE | re.DOTALL
    )

    matches = option_pattern.findall(text)

    for match in matches:
        # Group 1 = Option letter, Group 2 = Response number, Group 3 = content
        label = match[0] or match[1]  # letter or number
        content = match[2]
        # Clean up the content
        text_block = content.strip()

        # Remove any [response N] placeholder lines
        text_block = re.sub(r'\[response\s*\d+\]', '', text_block, flags=re.IGNORECASE)

        # Remove lines that are just planning/instructions (short lines that look like notes)
        lines = text_block.split('\n')
        real_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip lines that look like meta-text
            if re.match(r'^(?:Let\'s?|I\'ll|I will|We\'ll|First|Second|Third|The |Write |Need |Response )', stripped, re.IGNORECASE):
                if len(stripped) < 80:  # Short instruction lines
                    continue
            if stripped.startswith('[') and stripped.endswith(']'):
                continue  # Placeholder brackets
            if re.match(r'^(?:\d+\.|\-|•)', stripped):
                continue  # List markers
            real_lines.append(stripped)

        cleaned = ' '.join(real_lines).strip()
        # Further clean: remove any remaining "Let's count" or word counting
        cleaned = re.sub(r"Let's count[^.]*\.?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"Word count[^.]*\.?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"Approximate[^.]*\.?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s{2,}", " ", cleaned)  # collapse multiple spaces

        if len(cleaned) > 30 and len(responses) < 3:
            responses.append(cleaned)

    if len(responses) >= 3:
        return responses[:3]

    # Fallback: if we still don't have 3, just return what we have or the whole text
    if responses:
        return responses[:3]

    return [text.strip()] if text.strip() else ["Failed to generate responses. Please try again."]


# ─────────────────────────────────────────────
# UI Components
# ─────────────────────────────────────────────

def render_header():
    """App header."""
    st.html("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a2e; margin: 0;">
            Repeatly 🍽️
        </h1>
        <p style="color: #6b7280; font-size: 1rem; margin: 0.25rem 0 0 0;">
            Turn every review into a chance to bring them back
        </p>
    </div>
    """)


def render_api_key_input():
    """Render API key input if not configured."""
    if not st.session_state.get("api_key_configured", False):
        st.warning("⚠️ To use Repeatly, you need a MiniMax API key. Get one free at https://www.minimaxi.com/")

        with st.container():
            st.markdown("**Enter your MiniMax API Key**")
            api_key_input = st.text_input(
                "API Key",
                type="password",
                placeholder="Enter your MiniMax API key...",
                label_visibility="collapsed",
                key="api_key_input_field"
            )

            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("Save API Key", type="primary", use_container_width=True):
                    if api_key_input.strip():
                        st.session_state.api_key = api_key_input.strip()
                        st.session_state.api_key_configured = True
                        st.rerun()
                    else:
                        st.error("Please enter an API key")
            with col2:
                st.caption("Your key is stored only in this browser session. [Get a free key](https://www.minimaxi.com/)")
                if st.button("Reset key", key="reset_api_key"):
                    st.session_state.api_key=DEFAULT_API_KEY
                    st.session_state.api_key_configured=True
                    st.rerun()

        st.divider()
        return False
    return True


def render_restaurant_form():
    """Render the restaurant profile form."""
    st.subheader("1. Tell us about your restaurant")

    col1, col2 = st.columns(2)
    with col1:
        restaurant_name = st.text_input(
            "Restaurant name",
            placeholder="Luigi's Trattoria",
            help="The name customers would see in reviews"
        )
    with col2:
        location = st.text_input(
            "Location / neighborhood",
            placeholder="Chicago's Lincoln Park"
        )

    cuisine_type = st.text_input(
        "Cuisine type",
        placeholder="Italian — handmade pasta, wood-fired pizza"
    )

    vibe = st.text_input(
        "Vibe / atmosphere",
        placeholder="Cozy candlelit space, date night favorite, family-friendly"
    )

    popular_dishes = st.text_input(
        "Popular dishes",
        placeholder="Cacio e Pepe, Truffle Pasta, Margherita Pizza, Tiramisu",
        help="Comma-separated list of your signature dishes"
    )

    staff_names = st.text_input(
        "Staff names to personalize with",
        placeholder="Maria, Tony, Chef Marco, Sarah",
        help="Comma-separated. Agent will mention staff by name when reviewers reference them."
    )

    recent_context = st.text_input(
        "Recent context (optional)",
        placeholder="Just opened, new menu, under renovation, short-staffed, seasonal specials",
        help="Any context that might affect how you want to respond"
    )

    return {
        "restaurant_name": restaurant_name,
        "location": location,
        "cuisine_type": cuisine_type,
        "vibe": vibe,
        "popular_dishes": popular_dishes,
        "staff_names": staff_names,
        "recent_context": recent_context
    }


def render_review_input():
    """Render the review input section."""
    st.subheader("2. Paste the review")

    review_text = st.text_area(
        "Review text",
        placeholder="The pasta was amazing but the service was a bit slow...",
        height=120,
        help="Paste the full review text here"
    )

    return review_text


def render_settings():
    """Render generation settings."""
    st.subheader("3. Generation settings")

    col1, col2 = st.columns(2)

    with col1:
        brand_voice = st.selectbox(
            "Brand voice",
            options=["warm", "casual", "formal", "witty"],
            index=0,
            help="The tone the response should have"
        )

    with col2:
        response_length = st.selectbox(
            "Response length",
            options=["short", "medium", "long"],
            index=1,
            help="How detailed should the response be"
        )

    return brand_voice, response_length


def render_response(response: str):
    """Render the single generated response."""
    st.subheader("4. Your response")

    col1, col2 = st.columns([4, 1])

    with col1:
        st.success(response)

    with col2:
        st.write("")
        st.write("")
        st.button(
            "📋 Copy",
            key="copy_response",
            use_container_width=True
        )


def render_review_analysis(review_text: str, restaurant_info: dict):
    """Show detected sentiment and mentioned items."""
    st.subheader("Review analysis")

    review_lower = review_text.lower()

    negative_indicators = ["terrible", "awful", "worst", "horrible", "disgusting", "rude", "cold", "slow", "burnt", "raw", "undercooked", "overcooked", "salty", "bland", "dirty", "never", "disappointed", "mediocre", "noisy", "expensive"]
    positive_indicators = ["amazing", "delicious", "best", "great", "fantastic", "wonderful", "perfect", "love", "loved", "fresh", "incredible", "friendly", "recommend", "favorite", "gem"]

    negative_count = sum(1 for w in negative_indicators if w in review_lower)
    positive_count = sum(1 for w in positive_indicators if w in review_lower)

    if negative_count > positive_count:
        sentiment = "⚠️ Negative"
        emoji = "😞"
    elif positive_count > negative_count:
        sentiment = "✓ Positive"
        emoji = "😊"
    else:
        sentiment = "~ Neutral"
        emoji = "😐"

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Detected sentiment", f"{emoji} {sentiment}")
    with col2:
        word_count = len(review_text.split())
        st.metric("Review length", f"{word_count} words")

    # Check for mentioned items
    mentioned = []
    dish_list = restaurant_info.get("popular_dishes", "").lower()
    if dish_list:
        dishes = [d.strip() for d in dish_list.split(",")]
        for dish in dishes:
            if dish and len(dish) > 2 and dish in review_lower:
                mentioned.append(dish.title())

    if mentioned:
        st.info(f"📌 Detected mentions: {', '.join(set(mentioned))}")


# ─────────────────────────────────────────────
# Main App
# ─────────────────────────────────────────────

def main():
    # Initialize session state
    if "response" not in st.session_state:
        st.session_state.response = None
    if "restaurant_info" not in st.session_state:
        st.session_state.restaurant_info = None
    if "review_text" not in st.session_state:
        st.session_state.review_text = ""
    if "last_review" not in st.session_state:
        st.session_state.last_review = ""

    render_header()

    # Check API key
    if not render_api_key_input():
        st.stop()

    st.divider()

    # Restaurant Profile
    restaurant_info = render_restaurant_form()

    st.divider()

    # Review Input
    review_text = render_review_input()

    # Settings
    brand_voice, response_length = render_settings()

    st.divider()

    # Generate Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_disabled = not (restaurant_info.get("restaurant_name") and review_text.strip())
        clicked = st.button(
            "✨ Generate Response",
            type="primary",
            disabled=generate_disabled,
            use_container_width=True
        )

    # When Generate is clicked OR we have a new review with existing response
    if clicked and review_text.strip():
        with st.spinner("Crafting your response..."):
            prompt = build_prompt(restaurant_info, review_text.strip(), brand_voice, response_length)
            raw_response = generate_responses(prompt)
            response = parse_single_response(raw_response) if not raw_response.startswith("Error") else raw_response
            st.session_state.response = response
            st.session_state.restaurant_info = restaurant_info
            st.session_state.review_text = review_text
            st.session_state.last_review = review_text

    # Show analysis and response
    if review_text.strip():
        render_review_analysis(review_text, restaurant_info)

    if st.session_state.response:
        render_response(st.session_state.response)

    # Footer
    st.divider()
    st.caption("Built with Repeatly · Turn reviews into repeat customers")


if __name__ == "__main__":
    main()
