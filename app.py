import json
import re
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Dumka Police BNS/BNSS Lookup Tool",
    page_icon="⚖️",
    layout="wide",
)

# Sidebar - Language Selection
st.sidebar.markdown("### 🌐 Language / भाषा")
language = st.sidebar.radio("Bhasha Chuniye / भाषा चुनें:", ("English", "Hindi"))

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

# App Header (Bilingual)
if language == "Hindi":
  header_title = "⚖️ दुमका पुलिस बीएनएस/बीएनएसएस एक्ट एंड सेक्शन लाइब्रेरी"
  header_desc = "क्राइम डिटेल्स या सेक्शन नंबर से सर्च करें और तुरंत भारतीय न्याय संहिता (BNS 2023) सेक्शन्स, सजा, और इन्वेस्टीगेशन लिमिट देखें।"
  mode_label = "🔍 सर्च मोड चुनें:"
  mode_options = [
      "क्राइम डिटेल्स / कीवर्ड्स से खोजें",
      "एक्ट और सेक्शन नंबर से खोजें",
  ]
  query_prompt = "क्राइम डिटेल्स दर्ज करें (जैसे: 'theft', 'murder', 'chori'):"
  sec_input_label = "सेक्शन नंबर दर्ज करें (जैसे: '80', '103', '303'):"
  subsec_input_label = "सब-सेक्शन दर्ज करें (वैकल्पिक, जैसे: '2', '1'):"
else:
  header_title = "⚖️ DUMKA POLICE BNS/BNSS ACT & SECTIONS LIBRARY"
  header_desc = "Search by crime details or section number to instantly view BNS 2023 sections, punishments, and investigation limits."
  mode_label = "🔍 Select Search Mode:"
  mode_options = [
      "Search by Crime Details / Keywords",
      "Search by Act & Section Number",
  ]
  query_prompt = "Enter crime details (e.g., 'theft', 'murder'):"
  sec_input_label = "Enter Section Number (e.g., '80', '103', '303'):"
  subsec_input_label = "Enter Sub-Section (optional, e.g., '2', '1'):"

st.markdown(
    f"""
<div style="background:linear-gradient(135deg, #020617, #1e3a8a); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px;">
    <h1 style="font-size: 34px; font-weight: 900;">{header_title}</h1>
    <p style="font-size: 16px; margin-top: 10px;">{header_desc}</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- QUICK REFERENCE: BNS SECTION 4 (TYPES OF PUNISHMENTS) ---
if language == "Hindi":
  with st.expander("📌 त्वरित संदर्भ (Quick Reference): BNS धारा 4 - सजा के प्रकार"):
    st.markdown("""
        **भारतीय न्याय संहिता (BNS) की धारा 4 के अनुसार, दोषियों को कुल 6 प्रकार की सजा दी जा सकती है:**
        1. **मृत्युदंड (Death Penalty):** सबसे गंभीर अपराधों के लिए फांसी की सजा।
        2. **आजीवन कारावास (Life Imprisonment):** प्राकृतिक जीवन भर का कारावास (धारा 6 के अनुसार 20 वर्ष के समतुल्य)।
        3. **कारावास (Imprisonment):** दो प्रकार का - **कठोर कारावास** (कठिन श्रम के साथ) और **साधारण कारावास**।
        4. **संपत्ति की ज़ब्ती (Forfeiture of Property):** अपराधी की संपत्ति सरकार द्वारा जब्त करना।
        5. **जुर्माना (Fine):** अदालत द्वारा निर्धारित आर्थिक दंड।
        6. **सामुदायिक सेवा (Community Service):** बीएनएस में नया प्रावधान, छोटे या गैर-हिंसक अपराधों के सुधार हेतु।
        """)
else:
  with st.expander("📌 Quick Reference: BNS Section 4 - Types of Punishments"):
    st.markdown("""
        **As per Section 4 of BNS 2023, offenders are liable to 6 types of punishments:**
        1. **Death Penalty:** Capital punishment for heinous crimes.
        2. **Life Imprisonment:** Imprisonment for the remainder of natural life.
        3. **Imprisonment:** Of two descriptions—Rigorous (with hard labor) and Simple.
        4. **Forfeiture of Property:** Confiscation of offender's property.
        5. **Fine:** Monetary penalty.
        6. **Community Service:** New provision in BNS for petty or non-violent offenses.
        """)

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
searched_flag = False

if "Crime Details" in search_mode or "क्राइम डिटेल्स" in search_mode:
  query = st.text_input(query_prompt, placeholder="Yahan type karein...")
  if query:
    searched_flag = True
    query_lower = query.lower()
    for item in bns_data:
      title_text = str(item.get("Title", "")).lower()
      def_text = str(item.get("Legal Definition", "")).lower()
      if query_lower in title_text or query_lower in def_text:
        matched_results.append(item)
else:
  col1, col2 = st.columns(2)
  with col1:
    sec_query = st.text_input(sec_input_label, placeholder="Jaise: 80, 103...")
  with col2:
    subsec_query = st.text_input(
        subsec_input_label, placeholder="Jaise: 2, 1 (optional)..."
    )

  if sec_query:
    searched_flag = True
    sec_clean = sec_query.strip().lower()
    query_digits = "".join(re.findall(r"\d+", sec_clean))
    subsec_clean = subsec_query.strip().lower() if subsec_query else ""

    for item in bns_data:
      sec_val = str(item.get("Section", "")).strip().lower()
      definition = str(item.get("Legal Definition", ""))

      if query_digits and query_digits == sec_val:
        if subsec_clean:
          pattern = (
              rf"\(\s*{re.escape(subsec_clean)}\s*\)|\b{re.escape(subsec_clean)}\)"
          )
          if re.search(pattern, definition):
            matched_results.append(item)
        else:
          matched_results.append(item)

# Display Results Cleanly
if matched_results:
  display_list = matched_results[:10]
  if language == "Hindi":
    st.markdown(
        f"<h3 style='color: #166534; font-size: 20px;'>🎯 कुल"
        f" {len(matched_results)} परिणाम मिले हैं:</h3>",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f"<h3 style='color: #166534; font-size: 20px;'>🎯 Total"
        f" {len(matched_results)} matching result(s) found:</h3>",
        unsafe_allow_html=True,
    )

  for res in display_list:
    sec_no = res.get("Section", "N/A")
    title = res.get("Title", "Section Details")
    definition = res.get(
        "Legal Definition", "As per BNS 2023 Gazette provisions"
    )

    punishment_display = (
        definition[:400] + "..."
        if len(definition) > 400
        else definition
    )
    timer_display = (
        "90 Days (SR Case)"
        if str(sec_no) in ["103", "64", "111", "113", "80"]
        else "60 Days (Non-SR Case)"
    )

    st.markdown(
        f"""
        <div style="background: white; border: 2px solid #cbd5e1; border-radius: 15px; padding: 20px; margin-bottom: 15px; box-shadow: 0 6px 12px rgba(0,0,0,0.08);">
            <h2 style="color: #1e3a8a; margin-top: 0; font-size: 22px;">📌 Section {sec_no} BNS: {title}</h2>
            <hr style="margin: 10px 0 15px 0; border:0; border-top:2px solid #e2e8f0;">
            <p style="font-size: 16px; color: #334155;"><b>Legal Definition & Provisions:</b> {punishment_display}</p>
            <p style="font-size: 16px;"><b>Investigation Limit (BNSS Timer):</b> <span style="background: #dcfce7; color: #166534; padding: 3px 10px; border-radius: 6px; font-weight: bold;">{timer_display}</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif searched_flag:
  if language == "Hindi":
    st.warning(
        "⚠️ कोई रिकॉर्ड नहीं मिला। कृपया सेक्शन नंबर या कीवर्ड जांच कर दोबारा"
        " प्रयास करें।"
    )
  else:
    st.warning("⚠️ No matching record found. Please check and try again.")

# Footer
st.markdown(
    "<br><hr><p style='text-align: center; color: #475569; font-size: 18px;"
    " font-weight: 700;'>Dumka Police CCTNS IT Cell • Built with Python &"
    " Streamlit • By Er. Bidhan Chandra Singh & Team</p>",
    unsafe_allow_html=True,
)
