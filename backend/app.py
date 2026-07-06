"""
FarmWise AI — Streamlit Application
IBM Granite + RAG powered smart farming advisor
Run: streamlit run app.py  (from the backend/ directory)
"""
import sys
import os
import asyncio
import time
import streamlit as st
import plotly.graph_objects as go

# ── Path setup ───────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Page config (must be FIRST streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="FarmWise AI — Smart Farming Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Main background */
  .stApp { background-color: #f0fdf4; }

  /* Sidebar */
  [data-testid="stSidebar"] { background-color: #14532d; }
  [data-testid="stSidebar"] * { color: #dcfce7 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stTextInput label { color: #86efac !important; }

  /* Chat bubbles */
  .user-bubble {
    background: #15803d; color: white;
    padding: 12px 16px; border-radius: 18px 18px 4px 18px;
    margin: 6px 0; max-width: 80%; float: right; clear: both;
    font-size: 14px;
  }
  .bot-bubble {
    background: white; color: #1f2328;
    padding: 12px 16px; border-radius: 18px 18px 18px 4px;
    margin: 6px 0; max-width: 85%; float: left; clear: both;
    border: 1px solid #d1fae5; font-size: 14px; line-height: 1.6;
  }
  .clearfix { clear: both; }

  /* Meta badges */
  .badge {
    display: inline-block; padding: 2px 8px;
    border-radius: 12px; font-size: 11px; font-weight: 600; margin: 2px;
  }
  .badge-green  { background:#dcfce7; color:#166534; }
  .badge-blue   { background:#dbeafe; color:#1e40af; }
  .badge-yellow { background:#fef9c3; color:#854d0e; }
  .badge-red    { background:#fee2e2; color:#991b1b; }
  .badge-purple { background:#ede9fe; color:#6d28d9; }

  /* Metric cards */
  .metric-card {
    background: white; border-radius: 12px; padding: 16px;
    border: 1px solid #d1fae5; text-align: center; margin-bottom: 8px;
  }
  .metric-card h3 { font-size: 28px; color: #15803d; margin: 0; }
  .metric-card p  { font-size: 12px; color: #6b7280; margin: 4px 0 0; }

  /* Section headers */
  h2 { color: #14532d !important; }
  h3 { color: #166534 !important; }

  /* Input box */
  .stTextInput input, .stTextArea textarea {
    border: 1.5px solid #86efac !important;
    border-radius: 10px !important;
  }

  /* Buttons */
  .stButton > button {
    background: #15803d; color: white;
    border: none; border-radius: 10px;
    font-weight: 600;
  }
  .stButton > button:hover { background: #166534; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def run_async(coro):
    """Run async coroutine in sync Streamlit context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


INTENT_BADGES = {
    "crop":       ("🌾 Crop",        "badge-green"),
    "pest":       ("🪲 Pest",         "badge-red"),
    "weather":    ("🌦 Weather",      "badge-blue"),
    "irrigation": ("💧 Irrigation",   "badge-blue"),
    "fertilizer": ("🌱 Fertilizer",   "badge-yellow"),
    "market":     ("💰 Market",       "badge-yellow"),
    "schemes":    ("📢 Schemes",      "badge-purple"),
    "general":    ("💬 General",      "badge-green"),
}

LANGUAGE_OPTIONS = [
    "English", "Hindi", "Tamil", "Telugu", "Kannada",
    "Bengali", "Marathi", "Gujarati", "Punjabi", "Malayalam",
]

WMO_EMOJI = {
    "Clear sky": "☀️", "Mainly clear": "🌤️", "Partly cloudy": "⛅",
    "Overcast": "☁️", "Fog": "🌫️", "Moderate rain": "🌧️",
    "Heavy rain": "⛈️", "Thunderstorm": "⛈️", "Slight rain": "🌦️",
}

EXAMPLE_QUESTIONS = [
    "What crop should I grow in black cotton soil this kharif season?",
    "My tomato leaves have yellow spots — what is wrong?",
    "What NPK fertilizer should I use for rice?",
    "How much water does wheat need per season?",
    "What is the mandi price for onions today?",
    "Which government schemes can I apply for?",
    "How do I control stem borer in rice?",
    "What are organic alternatives to urea?",
]

CITY_COORDS = {
    "Pune": (18.52, 73.85), "Delhi": (28.61, 77.20), "Mumbai": (19.07, 72.87),
    "Bangalore": (12.97, 77.59), "Chennai": (13.08, 80.27), "Kolkata": (22.57, 88.36),
    "Hyderabad": (17.38, 78.48), "Ahmedabad": (23.02, 72.57), "Jaipur": (26.91, 75.78),
    "Lucknow": (26.84, 80.94), "Patna": (25.59, 85.13), "Bhopal": (23.25, 77.41),
    "Nagpur": (21.14, 79.08), "Indore": (22.71, 75.85), "Chandigarh": (30.73, 76.77),
}


# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = {}


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 FarmWise AI")
    st.markdown("*IBM Granite + RAG*")
    st.divider()

    st.markdown("### ⚙️ Settings")
    language = st.selectbox("🌐 Language", LANGUAGE_OPTIONS, index=0)
    season   = st.selectbox("📅 Season", ["", "kharif", "rabi", "zaid"],
                             format_func=lambda x: x.capitalize() if x else "Select season")
    soil     = st.selectbox("🌍 Soil Type", ["", "alluvial", "black", "red", "laterite", "sandy"],
                             format_func=lambda x: x.capitalize() if x else "Select soil type")
    location = st.text_input("📍 Location / District", placeholder="e.g. Pune, Maharashtra")
    crop     = st.text_input("🌱 Your Crop", placeholder="e.g. Rice, Wheat, Tomato")

    st.session_state.context = {
        "language": language,
        "season":   season   or None,
        "soil_type":soil     or None,
        "location": location or None,
        "crop":     crop     or None,
    }

    st.divider()
    st.markdown("### ⚡ Quick Ask")
    for q in EXAMPLE_QUESTIONS[:4]:
        if st.button(q[:45] + "…" if len(q) > 45 else q, use_container_width=True, key=f"qb_{q[:10]}"):
            st.session_state["quick_query"] = q

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("""
    <div style='font-size:11px; color:#86efac; text-align:center'>
    IBM Granite ibm/granite-4-h-small<br>
    RAG • ChromaDB • 58 docs
    </div>
    """, unsafe_allow_html=True)


# ── Tab layout ────────────────────────────────────────────────────────────────
tab_chat, tab_weather, tab_market, tab_schemes, tab_crops = st.tabs([
    "💬 AI Advisor", "🌦 Weather", "💰 Mandi Prices", "📢 Govt Schemes", "🌾 Crop Guide"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHAT
# ══════════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("## 💬 FarmWise AI Advisor")
    st.caption("Ask anything about crops, pests, fertilizers, irrigation, market prices, or government schemes")

    # Render chat history
    chat_box = st.container()
    with chat_box:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="user-bubble">👤 {msg["content"]}</div>'
                    '<div class="clearfix"></div>',
                    unsafe_allow_html=True
                )
            else:
                intent   = msg.get("intent", "general")
                sources  = msg.get("sources", [])
                n_docs   = msg.get("retrieved_docs", 0)
                cached   = msg.get("cached", False)
                badge_label, badge_cls = INTENT_BADGES.get(intent, ("💬", "badge-green"))

                badges_html = f'<span class="badge {badge_cls}">{badge_label}</span>'
                if cached:
                    badges_html += '<span class="badge badge-yellow">⚡ cached</span>'
                if n_docs:
                    badges_html += f'<span class="badge badge-blue">📚 {n_docs} docs</span>'
                for src in sources:
                    badges_html += f'<span class="badge badge-green">📖 {src}</span>'

                content_html = msg["content"].replace("\n", "<br>")
                st.markdown(
                    f'<div class="bot-bubble">🌾 {content_html}'
                    f'<div style="margin-top:8px">{badges_html}</div></div>'
                    '<div class="clearfix"></div>',
                    unsafe_allow_html=True
                )

    st.divider()

    # Input row
    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Ask your farming question",
            value=st.session_state.pop("quick_query", ""),
            placeholder="e.g. What crop should I grow in black soil this kharif season?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with col_send:
        send_clicked = st.button("Send 🚀", use_container_width=True)

    # More example chips
    st.markdown("**Try:**")
    ex_cols = st.columns(4)
    for i, q in enumerate(EXAMPLE_QUESTIONS[4:]):
        if ex_cols[i % 4].button(q[:30] + "…", key=f"ex_{i}"):
            st.session_state["quick_query"] = q
            st.rerun()

    # Process message
    if (send_clicked or user_input) and user_input.strip():
        query = user_input.strip()
        st.session_state.messages.append({"role": "user", "content": query})

        with st.spinner("🌾 IBM Granite thinking..."):
            try:
                from agents.farming_agent import process_farming_query
                ctx = st.session_state.context
                result = run_async(process_farming_query(
                    query=query,
                    language=ctx.get("language", "English"),
                    location=ctx.get("location"),
                    crop=ctx.get("crop"),
                    season=ctx.get("season"),
                    soil_type=ctx.get("soil_type"),
                ))
                st.session_state.messages.append({
                    "role":          "assistant",
                    "content":       result.get("answer", ""),
                    "intent":        result.get("intent", "general"),
                    "sources":       result.get("sources", []),
                    "retrieved_docs":result.get("retrieved_docs", 0),
                    "cached":        result.get("cached", False),
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role":    "assistant",
                    "content": f"⚠️ Error: {e}\n\nPlease make sure the IBM Watsonx credentials are correct.",
                })
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — WEATHER
# ══════════════════════════════════════════════════════════════════════════════
with tab_weather:
    st.markdown("## 🌦 Real-Time Weather & Farming Advisories")

    city = st.selectbox("Select City", list(CITY_COORDS.keys()), index=0)
    lat, lon = CITY_COORDS[city]

    if st.button("🔄 Fetch Weather", use_container_width=False):
        with st.spinner("Fetching live weather from Open-Meteo..."):
            try:
                from modules.weather import get_weather_summary
                data = run_async(get_weather_summary(lat, lon))
                st.session_state["weather_data"] = data
            except Exception as e:
                st.error(f"Weather fetch failed: {e}")

    # Auto-load on first visit
    if "weather_data" not in st.session_state:
        with st.spinner("Loading weather..."):
            try:
                from modules.weather import get_weather_summary
                data = run_async(get_weather_summary(lat, lon))
                st.session_state["weather_data"] = data
            except Exception as e:
                st.warning(f"Could not load weather: {e}")

    if "weather_data" in st.session_state:
        w = st.session_state["weather_data"]
        curr = w.get("current", {})

        # Current conditions
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"""<div class="metric-card">
            <h3>{curr.get('temperature_2m','--')}°C</h3>
            <p>🌡️ Temperature</p></div>""", unsafe_allow_html=True)
        c2.markdown(f"""<div class="metric-card">
            <h3>{curr.get('relative_humidity_2m','--')}%</h3>
            <p>💧 Humidity</p></div>""", unsafe_allow_html=True)
        c3.markdown(f"""<div class="metric-card">
            <h3>{curr.get('precipitation','--')}mm</h3>
            <p>🌧️ Precipitation</p></div>""", unsafe_allow_html=True)
        c4.markdown(f"""<div class="metric-card">
            <h3>{curr.get('wind_speed_10m','--')}</h3>
            <p>💨 Wind km/h</p></div>""", unsafe_allow_html=True)
        c5.markdown(f"""<div class="metric-card">
            <h3>{WMO_EMOJI.get(curr.get('condition',''), '🌡️')}</h3>
            <p>{curr.get('condition','--')}</p></div>""", unsafe_allow_html=True)

        # Farming advisories
        advisories = w.get("farming_advisory", [])
        if advisories:
            st.markdown("### 🌾 Farming Advisories")
            for adv in advisories:
                st.info(adv)

        # 7-day forecast chart
        forecast = w.get("forecast_7day", [])
        if forecast:
            st.markdown("### 📅 7-Day Forecast")
            dates  = [f["date"] for f in forecast]
            maxT   = [f["max_temp"] for f in forecast]
            minT   = [f["min_temp"] for f in forecast]
            rain   = [f["precipitation"] for f in forecast]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=maxT, mode="lines+markers",
                                     name="Max Temp (°C)", line=dict(color="#ef4444", width=2)))
            fig.add_trace(go.Scatter(x=dates, y=minT, mode="lines+markers",
                                     name="Min Temp (°C)", line=dict(color="#3b82f6", width=2)))
            fig.add_trace(go.Bar(x=dates, y=rain, name="Rain (mm)",
                                 marker_color="#22c55e", opacity=0.5, yaxis="y2"))
            fig.update_layout(
                height=320, margin=dict(l=0, r=0, t=20, b=0),
                paper_bgcolor="white", plot_bgcolor="white",
                yaxis=dict(title="Temperature (°C)"),
                yaxis2=dict(title="Rainfall (mm)", overlaying="y", side="right"),
                legend=dict(orientation="h", y=-0.2),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Forecast table
            cols = st.columns(len(forecast))
            for i, (col, day) in enumerate(zip(cols, forecast)):
                with col:
                    label = "Today" if i == 0 else day["date"][5:]
                    emoji = WMO_EMOJI.get(day["condition"], "🌡️")
                    st.markdown(f"""
                    <div style='text-align:center;padding:6px;background:white;
                                border-radius:8px;border:1px solid #d1fae5;font-size:12px'>
                        <b>{label}</b><br>{emoji}<br>
                        <span style='color:#ef4444'>{day['max_temp']}°</span> /
                        <span style='color:#3b82f6'>{day['min_temp']}°</span><br>
                        <span style='color:#22c55e'>{day['precipitation']}mm</span>
                    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MARKET PRICES
# ══════════════════════════════════════════════════════════════════════════════
with tab_market:
    st.markdown("## 💰 Live Mandi / Market Prices")
    st.caption("Source: data.gov.in (demo data when API key not configured)")

    COMMODITIES = ["wheat", "rice", "maize", "cotton", "soybean",
                   "onion", "tomato", "potato", "mustard", "arhar"]
    COMM_EMOJI  = {"wheat":"🌾","rice":"🍚","maize":"🌽","cotton":"🪻","soybean":"🫘",
                   "onion":"🧅","tomato":"🍅","potato":"🥔","mustard":"🌿","arhar":"🫘"}

    mc1, mc2 = st.columns([3, 1])
    commodity = mc1.selectbox("Select Commodity", COMMODITIES,
                               format_func=lambda x: f"{COMM_EMOJI.get(x,'')} {x.capitalize()}")
    state_filter = mc2.text_input("State (optional)", placeholder="e.g. Maharashtra")

    if st.button("🔍 Get Prices", use_container_width=False):
        with st.spinner("Fetching market prices..."):
            try:
                from modules.market import get_market_prices
                prices = run_async(get_market_prices(commodity, state_filter or None))
                st.session_state["market_prices"] = prices
                st.session_state["market_commodity"] = commodity
            except Exception as e:
                st.error(f"Market data error: {e}")

    # Auto-load
    if "market_prices" not in st.session_state:
        try:
            from modules.market import get_market_prices
            prices = run_async(get_market_prices("wheat"))
            st.session_state["market_prices"] = prices
            st.session_state["market_commodity"] = "wheat"
        except Exception:
            pass

    if "market_prices" in st.session_state:
        prices = st.session_state["market_prices"]
        comm   = st.session_state.get("market_commodity", "wheat")

        if prices:
            vals = [float(p.get("modal_price", 0) or 0) for p in prices]
            s1, s2, s3 = st.columns(3)
            s1.metric("🟢 Highest Price",  f"₹{int(max(vals)):,}/qtl")
            s2.metric("🔴 Lowest Price",   f"₹{int(min(vals)):,}/qtl")
            s3.metric("📊 Average Price",  f"₹{int(sum(vals)/len(vals)):,}/qtl")

            # Bar chart
            markets = [p.get("market", f"M{i}") for i, p in enumerate(prices)]
            fig = go.Figure(go.Bar(
                x=markets, y=vals,
                marker_color=["#15803d" if v == max(vals) else "#22c55e" for v in vals],
                text=[f"₹{int(v):,}" for v in vals],
                textposition="outside",
            ))
            fig.update_layout(
                height=300, margin=dict(l=0, r=0, t=20, b=60),
                paper_bgcolor="white", plot_bgcolor="#f9fafb",
                yaxis_title="Price ₹/quintal",
                xaxis_tickangle=-30,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Table
            st.markdown("### 📋 Detailed Prices")
            for p in prices:
                col_a, col_b, col_c = st.columns([3, 2, 2])
                col_a.markdown(f"**{p.get('market','—')}** — {p.get('state','')}")
                col_b.markdown(f"Modal: **₹{p.get('modal_price','—')}/qtl**")
                if p.get("min_price") and p.get("max_price"):
                    col_c.markdown(f"Range: ₹{p.get('min_price')}–₹{p.get('max_price')}")
                else:
                    col_c.empty()
                st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — GOVERNMENT SCHEMES
# ══════════════════════════════════════════════════════════════════════════════
with tab_schemes:
    st.markdown("## 📢 Government Schemes & Subsidies")

    from modules.schemes import get_relevant_schemes, SCHEMES_DATABASE
    CATEGORIES = ["All", "income_support", "insurance", "credit",
                  "irrigation", "organic_farming", "mechanization", "soil_health", "market"]
    cat_filter = st.selectbox("Filter by Category", CATEGORIES,
                               format_func=lambda x: x.replace("_", " ").title())

    schemes = get_relevant_schemes(None if cat_filter == "All" else cat_filter)

    SCHEME_COLORS = ["#dcfce7","#dbeafe","#fef9c3","#ede9fe",
                     "#ffedd5","#fce7f3","#f0fdf4","#e0f2fe"]

    for i, scheme in enumerate(schemes):
        bg = SCHEME_COLORS[i % len(SCHEME_COLORS)]
        with st.expander(f"**{scheme['name']}**  —  ✅ {scheme['benefit']}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📋 Eligibility:**")
                for e in scheme.get("eligibility", []):
                    st.markdown(f"• {e}")
                if scheme.get("premium"):
                    st.markdown(f"**💰 Premium:** {scheme['premium']}")
            with col2:
                st.markdown("**📍 How to Apply:**")
                st.markdown(scheme.get("apply_at", "—"))
                st.markdown("**📞 Helpline:** `1800-180-1551` (Free)")
            st.markdown(f"*Category: {scheme.get('category','').replace('_',' ').title()}*")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CROP GUIDE
# ══════════════════════════════════════════════════════════════════════════════
with tab_crops:
    st.markdown("## 🌾 Crop Recommendation Guide")

    cc1, cc2, cc3 = st.columns(3)
    soil_sel   = cc1.selectbox("Soil Type",  ["alluvial","black","red","laterite","sandy"],
                                format_func=str.capitalize)
    season_sel = cc2.selectbox("Season",     ["kharif","rabi","zaid"],
                                format_func=str.capitalize)
    rain_sel   = cc3.slider("Annual Rainfall (mm)", 200, 2000, 700, 50)

    from modules.crops import get_crop_recommendation
    rec = get_crop_recommendation(soil_type=soil_sel, season=season_sel, rainfall=rain_sel)
    crops_list = rec.get("recommended_crops", [])

    st.markdown(f"### ✅ Recommended Crops for {soil_sel.capitalize()} soil — {season_sel.capitalize()}")
    if crops_list:
        crop_cols = st.columns(min(len(crops_list), 4))
        CROP_EMOJI = {"Rice":"🍚","Wheat":"🌾","Maize":"🌽","Cotton":"🪻","Soybean":"🫘",
                      "Groundnut":"🥜","Mustard":"🌿","Chickpea":"🫘","Tomato":"🍅",
                      "Sugarcane":"🎋","Millet":"🌾","Arhar":"🫘","Barley":"🌾"}
        for i, crop_name in enumerate(crops_list):
            emoji = CROP_EMOJI.get(crop_name, "🌱")
            crop_cols[i % 4].markdown(
                f"""<div style='background:white;border:1px solid #d1fae5;border-radius:10px;
                               padding:14px;text-align:center;margin-bottom:8px'>
                    <div style='font-size:28px'>{emoji}</div>
                    <div style='font-weight:600;color:#166534'>{crop_name}</div>
                </div>""",
                unsafe_allow_html=True,
            )
    else:
        st.warning("No specific crops found for this combination. Try different filters.")

    st.markdown(f"> 💡 {rec.get('notes','')}")

    st.divider()

    # Fertilizer quick reference
    st.markdown("### 🌱 Quick Fertilizer Reference")
    from modules.fertilizer import get_fertilizer_advice
    fert_crop = st.selectbox("Crop for fertilizer guide",
                              ["rice","wheat","cotton","maize","tomato"],
                              format_func=str.capitalize, key="fert_crop")
    area = st.number_input("Area (hectares)", min_value=0.5, max_value=100.0,
                            value=1.0, step=0.5)
    fert = get_fertilizer_advice(fert_crop, area_ha=area)
    fa, fb, fc = st.columns(3)
    fa.metric("Nitrogen (N)",    f"{fert['total_fertilizer_required_kg'].get('N','--')} kg")
    fb.metric("Phosphorus (P)",  f"{fert['total_fertilizer_required_kg'].get('P','--')} kg")
    fc.metric("Potassium (K)",   f"{fert['total_fertilizer_required_kg'].get('K','--')} kg")

    with st.expander("📅 Application Schedule"):
        for step in fert.get("application_schedule", []):
            st.markdown(f"• {step}")
    with st.expander("🌿 Organic Alternatives"):
        for opt in fert.get("organic_options", []):
            st.markdown(f"• {opt}")


# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center;color:#6b7280;font-size:12px;padding:8px 0'>
  🌾 FarmWise AI &nbsp;•&nbsp; IBM Granite <code>ibm/granite-4-h-small</code> 
  &nbsp;•&nbsp; RAG + ChromaDB (58 docs) &nbsp;•&nbsp; For informational purposes only
</div>
""", unsafe_allow_html=True)
