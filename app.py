import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Crime Section & BNSS Timer Lookup",
    page_icon="⚖️",
    layout="wide"
)

# Predefined Crime Database (BNS Sections & BNSS Timelines)
CRIME_DATABASE = [
    {
        "keywords": ["chori", "theft", "ghar me chori", "chori karna"],
        "crime_name": "Theft (Chori)",
        "bns_section": "Section 303 BNS",
        "punishment": "Upto 3 years imprisonment or fine or both",
        "timer_limit": "60 Days (Non-SR Case)"
    },
    {
        "keywords": ["hatya", "murder", "katal", "jaan se marna", "kill"],
        "crime_name": "Murder (Hatya)",
        "bns_section": "Section 103 BNS",
        "punishment": "Death or Imprisonment for life, and fine",
        "timer_limit": "90 Days (SR Case)"
    },
    {
        "keywords": ["maarpeet", "hurt", "chot pahunchana", "marpeet", "jhagda"],
        "crime_name": "Voluntarily Causing Hurt",
        "bns_section": "Section 115 BNS",
        "punishment": "Upto 1 year imprisonment or fine upto ₹10,000 or both",
        "timer_limit": "60 Days (Non-SR Case)"
    },
    {
        "keywords": ["balatkaar", "rape", "sexual assault", "durovyavhar"],
        "crime_name": "Rape / Sexual Assault",
        "bns_section": "Section 64 BNS",
        "punishment": "Rigorous imprisonment not less than 10 years, extendable to life",
        "timer_limit": "90 Days (SR Case)"
    },
    {
        "keywords": ["fraud", "dhokhadhadi", "cheat", "paisa hadapna"],
        "crime_name": "Cheating & Dishonestly Inducing Delivery of Property",
        "bns_section": "Section 318 BNS",
        "punishment": "Upto 3 years imprisonment or fine or both",
        "timer_limit": "60 Days (Non-SR Case)"
    },
    {
        "keywords": ["loot", "dacoity", "dakaiti", "hathiyar ke dam par loot"],
        "crime_name": "Dacoity / Robbery",
        "bns_section": "Section 310 / 309 BNS",
        "punishment": "Imprisonment for life or rigorous imprisonment up to 10 years",
        "timer_limit": "90 Days (SR Case)"
    }
]

# App Header (Bigger fonts applied)
st.markdown("""
<div style="background:linear-gradient(135deg, #020617, #1e3a8a); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px;">
    <h1 style="font-size: 38px; font-weight: 900;">⚖️ DUMKA POLICE BNS/BNSS ACT & SECTIONS LIBRARY</h1>
    <p style="font-size: 18px; margin-top: 10px;">क्राइम डिटेल्स या कीवर्ड्स एंटर करें और तुरंत भारतीय न्याय संहिता (BNS 2023) सेक्शन्स, सजा, और इन्वेस्टीगेशन लिमिट (60/90 दिन) देखें.</p>
</div>
""", unsafe_allow_html=True)

# Search Input Box (Custom styling for bigger input font)
st.markdown("""
<style>
input[type="text"] {
    font-size: 18px !important;
    padding: 12px !important;
}
</style>
""", unsafe_allow_html=True)

query = st.text_input("🔍 Crime Details / Keywords enter karein (jaise: 'chori', 'hatya', 'maarpeet'):", placeholder="Yahan type karein...")

if query:
    query_lower = query.lower()
    matched_results = []
    
    # Matching logic
    for item in CRIME_DATABASE:
        if any(kw in query_lower for kw in item["keywords"]):
            matched_results.append(item)
            
    if matched_results:
        st.markdown(f"<h3 style='color: #166534; font-size: 22px;'>🎯 Total {len(matched_results)} matching result(s) mile hain:</h3>", unsafe_allow_html=True)
        for res in matched_results:
            st.markdown(f"""
            <div style="background: white; border: 2px solid #cbd5e1; border-radius: 15px; padding: 20px; margin-bottom: 15px; box-shadow: 0 6px 12px rgba(0,0,0,0.08);">
                <h2 style="color: #1e3a8a; margin-top: 0; font-size: 26px;">📌 {res['crime_name']}</h2>
                <hr style="margin: 10px 0 15px 0; border:0; border-top:2px solid #e2e8f0;">
                <p style="font-size: 18px;"><b>Relevant BNS Section:</b> <span style="background: #e0e7ff; color: #3730a3; padding: 5px 12px; border-radius: 8px; font-weight: bold; font-size: 18px;">{res['bns_section']}</span></p>
                <p style="font-size: 18px;"><b>Punishment (Saja):</b> {res['punishment']}</p>
                <p style="font-size: 18px;"><b>Investigation Limit (BNSS Timer):</b> <span style="background: #dcfce7; color: #166534; padding: 5px 12px; border-radius: 8px; font-weight: bold; font-size: 18px;">{res['timer_limit']}</span></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Koi exact match nahi mila. Kripya keywords badal kar dubara koshish karein (jaise: 'chori', 'hatya', 'loot').")

# Footer (Font size 20px as requested)
st.markdown("<br><hr><p style='text-align: center; color: #475569; font-size: 20px; font-weight: 700;'>Dumka Police CCTNS IT Cell • Built with Python & Streamlit • By Er. Bidhan Chandra Singh & Team</p>", unsafe_allow_html=True)
