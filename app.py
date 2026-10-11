import json
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Crime Section & BNSS Timer Lookup",
    page_icon="⚖️",
    layout="wide",
)

# Sidebar - Language Selection
st.sidebar.markdown("### 🌐 Language / Bhasha")
language = st.sidebar.radio("Bhasha Chuniye:", ("English", "Hindi"))

# JSON Database Load karne ka code (Language ke anusaar)
try:
  if language == "Hindi":
    with open("bns_database_hindi.json", "r", encoding="utf-8") as f:
      bns_data = json.load(f)
  else:
    with open("bns_database_auto.json", "r", encoding="utf-8") as f:
      bns_data = json.load(f)

  st.sidebar.success(
      f"Total Sections Loaded ({language}): {len(bns_data)}"
  )
except Exception as e:
  # Agar file load hone mein error aaye toh fallback ke liye hardcoded CRIME_DATABASE use karein
  st.sidebar.error(
      "JSON file load nahi hui, default database use ho raha hai."
  )
  bns_data = [
      {
          "keywords": ["chori", "theft", "ghar me chori", "chori karna"],
          "crime_name": "Theft (Chori)",
          "bns_section": "Section 303 BNS",
          "section_num": "303",
          "punishment": "Upto 3 years imprisonment or fine or both",
          "timer_limit": "60 Days (Non-SR Case)",
      },
      {
          "keywords": ["hatya", "murder", "katal", "jaan se marna", "kill"],
          "crime_name": "Murder (Hatya)",
          "bns_section": "Section 103 BNS",
          "section_num": "103",
          "punishment": "Death or Imprisonment for life, and fine",
          "timer_limit": "90 Days (SR Case)",
      },
  ]

# App Header (Bigger fonts)
if language == "Hindi":
  header_title = "⚖️ DUMKA POLICE BNS/BNSS ACT & SECTIONS LIBRARY"
  header_desc = "क्राइम डिटेल्स या सेक्शन नंबर से सर्च करें और तुरंत भारतीय न्याय संहिता (BNS 2023) सेक्शन्स, सजा, और इन्वेस्टीगेशन लिमिट (60/90 दिन) देखें."
  mode_label = "🔍 Search Mode Chuniye:"
  mode_options = ["Crime Details / Keywords se Search Karein", "Act & Section Number se Search Karein"]
  query_prompt = "Crime details enter karein (jaise: 'theft', 'murder'):"
  sec_prompt = "BNS Section Number enter karein (jaise: '303', '103', '64'):"
else:
  header_title = "⚖️ DUMKA POLICE BNS/BNSS ACT & SECTIONS LIBRARY"
  header_desc = "Search by crime details or section number to instantly view BNS 2023 sections, punishments, and investigation limits (60/90 days)."
  mode_label = "🔍 Select Search Mode:"
  mode_options = ["Search by Crime Details / Keywords", "Search by Act & Section Number"]
  query_prompt = "Enter crime details (e.g., 'theft', 'murder'):"
  sec_prompt = "Enter BNS Section Number (e.g., '303', '103', '64'):"

st.markdown(
    f"""
<div style="background:linear-gradient(135deg, #020617, #1e3a8a); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px;">
    <h1 style="font-size: 38px; font-weight: 900;">{header_title}</h1>
    <p style="font-size: 18px; margin-top: 10px;">{header_desc}</p>
</div>
""",
    unsafe_allow_html=True,
)

# Custom Styling for bigger input font
st.markdown(
    """
<style>
input[type="text"] {
    font-size: 18px !important;
    padding: 12px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# Search Mode Selection
search_mode = st.radio(mode_label, mode_options, horizontal=True)

matched_results = []

if "Crime Details" in search_mode:
  query = st.text_input(query_prompt, placeholder="Yahan type karein...")
  if query:
    query_lower = query.lower()
    for item in bns_data:
      # Keywords ya crime name mein search karna
      crime_title = item.get("crime_name", "") or item.get(
          "crime_name_hi", ""
      )
      keywords = item.get("keywords", [])
      if any(
          query_lower in kw.lower() for kw in keywords
      ) or query_lower in crime_title.lower():
        matched_results.append(item)
else:
  sec_query = st.text_input(sec_prompt, placeholder="Section number daalein...")
  if sec_query:
    sec_clean = sec_query.strip().lower()
    for item in bns_data:
      sec_num = str(item.get("section_num", ""))
      bns_sec = str(item.get("bns_section", ""))
      if sec_clean in sec_num.lower() or sec_clean in bns_sec.lower():
        matched_results.append(item)

# Display Results
if "Crime Details" in search_mode and "query" in locals() and query:
  if matched_results:
    st.markdown(
        f"<h3 style='color: #166534; font-size: 22px;'>🎯 Total"
        f" {len(matched_results)} matching result(s) mile hain:</h3>",
        unsafe_allow_html=True,
    )
    for res in matched_results:
      title_display = (
          res.get("crime_name_hi")
          if language == "Hindi" and res.get("crime_name_hi")
          else res.get("crime_name", "N/A")
      )
      bns_sec_display = res.get("bns_section", "N/A")
      punishment_display = res.get(
          "punishment", "As per BNS 2023 Gazette provisions"
      )
      timer_display = res.get("timer_limit", "60 Days (Non SR Case)")

      st.markdown(
          f"""
            <div style="background: white; border: 2px solid #cbd5e1; border-radius: 15px; padding: 20px; margin-bottom: 15px; box-shadow: 0 6px 12px rgba(0,0,0,0.08);">
                <h2 style="color: #1e3a8a; margin-top: 0; font-size: 26px;">📌 {title_display}</h2>
                <hr style="margin: 10px 0 15px 0; border:0; border-top:2px solid #e2e8f0;">
                <p style="font-size: 18px;"><b>Relevant BNS Section:</b> <span style="background: #e0e7ff; color: #3730a3; padding: 5px 12px; border-radius: 8px; font-weight: bold; font-size: 18px;">{bns_sec_display}</span></p>
                <p style="font-size: 18px;"><b>Punishment (Saja):</b> {punishment_display}</p>
                <p style="font-size: 18px;"><b>Investigation Limit (BNSS Timer):</b> <span style="background: #dcfce7; color: #166534; padding: 5px 12px; border-radius: 8px; font-weight: bold; font-size: 18px;">{timer_display}</span></p>
            </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.warning(
        "⚠️ Koi exact match nahi mila. Kripya keywords badal kar dubara koshish"
        " karein."
    )

elif "Act & Section" in search_mode and "sec_query" in locals() and sec_query:
  if matched_results:
    st.markdown(
        f"<h3 style='color: #166534; font-size: 22px;'>🎯 Section {sec_query}"
        " ke liye details:</h3>",
        unsafe_allow_html=True,
    )
    for res in matched_results:
      title_display = (
          res.get("crime_name_hi")
          if language == "Hindi" and res.get("crime_name_hi")
          else res.get("crime_name", "N/A")
      )
      bns_sec_display = res.get("bns_section", "N/A")
      punishment_display = res.get(
          "punishment", "As per BNS 2023 Gazette provisions"
      )
      timer_display = res.get("timer_limit", "60 Days (Non SR Case)")

      st.markdown(
          f"""
            <div style="background: white; border: 2px solid #cbd5e1; border-radius: 15px; padding: 20px; margin-bottom: 15px; box-shadow: 0 6px 12px rgba(0,0,0,0.08);">
                <h2 style="color: #1e3a8a; margin-top: 0; font-size: 26px;">📌 {title_display}</h2>
                <hr style="margin: 10px 0 15px 0; border:0; border-top:2px solid #e2e8f0;">
                <p style="font-size: 18px;"><b>Relevant BNS Section:</b> <span style="background: #e0e7ff; color: #3730a3; padding: 5px 12px; border-radius: 8px; font-weight: bold; font-size: 18px;">{bns_sec_display}</span></p>
                <p style="font-size: 18px;"><b>Punishment (Saja):</b> {punishment_display}</p>
                <p style="font-size: 18px;"><b>Investigation Limit (BNSS Timer):</b> <span style="background: #dcfce7; color: #166534; padding: 5px 12px; border-radius: 8px; font-weight: bold; font-size: 18px;">{timer_display}</span></p>
            </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.warning(
        f"⚠️ Section '{sec_query}' ke anusaar database mein koi record nahi"
        " mila."
    )

# Footer
st.markdown(
    "<br><hr><p style='text-align: center; color: #475569; font-size: 20px;"
    " font-weight: 700;'>Dumka Police CCTNS IT Cell • Built with Python &"
    " Streamlit • By Er. Bidhan Chandra Singh & Team</p>",
    unsafe_allow_html=True,
)
