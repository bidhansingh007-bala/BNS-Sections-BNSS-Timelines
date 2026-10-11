import json
import re
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

# JSON Database Load karne ka code
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
  st.sidebar.error("JSON file load nahi hui!")
  bns_data = []

# App Header
if language == "Hindi":
  header_title = "⚖️ DUMKA POLICE BNS/BNSS ACT & SECTIONS LIBRARY"
  header_desc = "क्राइम डिटेल्स या सेक्शन नंबर से सर्च करें और तुरंत भारतीय न्याय संहिता (BNS 2023) सेक्शन्स, सजा, और इन्वेस्टीगेशन लिमिट (60/90 दिन) देखें."
  mode_label = "🔍 Search Mode Chuniye:"
  mode_options = [
      "Crime Details / Keywords se Search Karein",
      "Act & Section Number se Search Karein",
  ]
  query_prompt = "Crime details enter karein (jaise: 'theft', 'murder'):"
  sec_prompt = "BNS Section Number enter karein (jaise: '303', '103', '80'):"
else:
  header_title = "⚖️ DUMKA POLICE BNS/BNSS ACT & SECTIONS LIBRARY"
  header_desc = "Search by crime details or section number to instantly view BNS 2023 sections, punishments, and investigation limits (60/90 days)."
  mode_label = "🔍 Select Search Mode:"
  mode_options = [
      "Search by Crime Details / Keywords",
      "Search by Act & Section Number",
  ]
  query_prompt = "Enter crime details (e.g., 'theft', 'murder'):"
  sec_prompt = "Enter BNS Section Number (e.g., '303', '103', '80'):"

st.markdown(
    f"""
<div style="background:linear-gradient(135deg, #020617, #1e3a8a); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px;">
    <h1 style="font-size: 38px; font-weight: 900;">{header_title}</h1>
    <p style="font-size: 18px; margin-top: 10px;">{header_desc}</p>
</div>
""",
    unsafe_allow_html=True,
)

# Custom Styling
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

search_mode = st.radio(mode_label, mode_options, horizontal=True)
matched_results = []

if "Crime Details" in search_mode:
  query = st.text_input(query_prompt, placeholder="Yahan type karein...")
  if query:
    query_lower = query.lower()
    for item in bns_data:
      # Title aur Legal Definition mein search karne ke liye
      title_text = str(item.get("Title", "")).lower()
      def_text = str(item.get("Legal Definition", "")).lower()
      if query_lower in title_text or query_lower in def_text:
        matched_results.append(item)
else:
  sec_query = st.text_input(
      sec_prompt, placeholder="Section number daalein..."
  )
  if sec_query:
    sec_clean = sec_query.strip().lower()
    query_digits = "".join(re.findall(r"\d+", sec_clean))

    for item in bns_data:
      sec_val = str(item.get("Section", "")).strip().lower()
      # Exact match for section numbers (e.g., '80', '103', '303')
      if query_digits and query_digits == sec_val:
        matched_results.append(item)
      elif sec_clean in sec_val:
        matched_results.append(item)

# Display Results Cleanly
if matched_results:
  display_list = matched_results[:10]
  st.markdown(
      f"<h3 style='color: #166534; font-size: 22px;'>🎯 Total"
      f" {len(matched_results)} matching result(s) mile hain:</h3>",
      unsafe_allow_html=True,
  )

  for res in display_list:
    sec_no = res.get("Section", "N/A")
    title = res.get("Title", "Section Details")
    definition = res.get("Legal Definition", "As per BNS 2023 Gazette provisions")

    # Punishments and BNSS timer can be parsed from Legal Definition or defaults
    punishment_display = (
        definition[:300] + "..."
        if len(definition) > 300
        else definition
    )
    timer_display = "90 Days (SR Case)" if int(sec_no) in [103, 64, 111, 113] else "60 Days (Non-SR Case)"

    st.markdown(
        f"""
        <div style="background: white; border: 2px solid #cbd5e1; border-radius: 15px; padding: 20px; margin-bottom: 15px; box-shadow: 0 6px 12px rgba(0,0,0,0.08);">
            <h2 style="color: #1e3a8a; margin-top: 0; font-size: 24px;">📌 Section {sec_no} BNS: {title}</h2>
            <hr style="margin: 10px 0 15px 0; border:0; border-top:2px solid #e2e8f0;">
            <p style="font-size: 16px; color: #334155;"><b>Legal Definition & Provisions:</b> {punishment_display}</p>
            <p style="font-size: 16px;"><b>Investigation Limit (BNSS Timer):</b> <span style="background: #dcfce7; color: #166534; padding: 3px 10px; border-radius: 6px; font-weight: bold;">{timer_display}</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif (
    ("Crime Details" in search_mode and "query" in locals() and query)
    or ("Act & Section" in search_mode and "sec_query" in locals() and sec_query)
):
  st.warning(
      "⚠️ Koi match nahi mila. Kripya keyword ya section number check karke"
      " dubara daalein."
  )

# Footer
st.markdown(
    "<br><hr><p style='text-align: center; color: #475569; font-size: 20px;"
    " font-weight: 700;'>Dumka Police CCTNS IT Cell • Built with Python &"
    " Streamlit • By Er. Bidhan Chandra Singh & Team</p>",
    unsafe_allow_html=True,
)
