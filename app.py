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

# App Header
st.markdown("""
<div style="background:linear-gradient(135deg, #020617, #1e3a8a); padding: 25px; border-radius: 25px; color: white; text-align: center; margin-bottom: 25px;">
    <h1>⚖️ DUMKA POLICE BNS/BNSS ACT & SECTIONS LIBRARY</h1>
    <p>क्राइम डिटेल्स या कीवर्ड्स एंटर करें और तुरंत भारतीय न्याय संहिता (BNS 2023)  सेक्शन्स, सजा, और इन्वेस्टीगेशन लिमिट (60/90 दिन) देखें.</p>
</div>
""", unsafe_allow_html=True)

# Search Input Box
query = st.text_input("🔍 Crime Details / Keywords enter karein (jaise: 'chori', 'hatya', 'maarpeet'):", placeholder="Yahan type karein...")

if query:
    query_lower = query.lower()
    matched_results = []
    
    # Matching logic
    for item in CRIME_DATABASE:
        if any(kw in query_lower for kw in item["keywords"]):
            matched_results.append(item)
            
    if matched_results:
        st.success(f"🎯 Total {len(matched_results)} matching result(s) mile hain:")
        for res in matched_results:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #cbd5e1; border-radius: 12px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #1e3a8a; margin-top: 0;">📌 {res['crime_name']}</h3>
                <hr style="margin: 5px 0 10px 0; border:0; border-top:1px solid #e2e8f0;">
                <p><b>Relevant BNS Section:</b> <span style="background: #e0e7ff; color: #3730a3; padding: 3px 8px; border-radius: 6px; font-weight: bold;">{res['bns_section']}</span></p>
                <p><b>Punishment (Saja):</b> {res['punishment']}</p>
                <p><b>Investigation Limit (BNSS Timer):</b> <span style="background: #dcfce7; color: #166534; padding: 3px 8px; border-radius: 6px; font-weight: bold;">{res['timer_limit']}</span></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Koi exact match nahi mila. Kripya keywords badal kar dubara koshish karein (jaise: 'chori', 'hatya', 'loot').")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #64748b; font-size: 20px;'>Dumka Police CCTNS IT Cell • Built with Python & Streamlit • By Er. Bidhan Chandra Singh & Team </p>", unsafe_allow_html=True)
