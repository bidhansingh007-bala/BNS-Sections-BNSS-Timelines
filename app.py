
import json
import re
import html
import calendar
from pathlib import Path
from datetime import date, timedelta

import streamlit as st


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Dumka Police BNS/BNSS Sections Library",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATABASE SETTINGS
# Keep both JSON files in the same folder as app.py
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASES = {
    "English": {
        "filename": "bns_database_auto.json",
        "url": (
            "https://raw.githubusercontent.com/"
            "bidhansingh007-bala/BNS-Sections-BNSS-Timelines/"
            "main/bns_database_auto.json"
        ),
    },
    "Hindi": {
        "filename": "bns_database_hindi.json",
        "url": (
            "https://raw.githubusercontent.com/"
            "bidhansingh007-bala/BNS-Sections-BNSS-Timelines/"
            "main/bns_database_hindi.json"
        ),
    },
}

# Original app's operational classification.
# These are configurable tracking defaults, not a legal determination.
DEFAULT_SR_SECTIONS = "103, 64, 80, 111, 113"
DEFAULT_SR_DAYS = 90
DEFAULT_NON_SR_DAYS = 60

# BNSS Section 193(2): investigation completion period
# of two months for the listed BNS sections.
BNSS_TWO_MONTH_SECTIONS = {
    "64", "65", "66", "67", "68", "70", "71"
}


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f3f6fb;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    .main-header {
        background: linear-gradient(120deg, #102a56, #174a83);
        color: white;
        padding: 24px 26px;
        border-radius: 15px;
        margin-bottom: 18px;
        box-shadow: 0 5px 16px rgba(16, 42, 86, 0.16);
    }

    .main-header h1 {
        color: white;
        font-size: clamp(22px, 3vw, 34px);
        margin: 0 0 8px 0;
        line-height: 1.25;
    }

    .main-header p {
        color: #e3edff;
        font-size: 16px;
        margin: 0;
        line-height: 1.5;
    }

    .section-card {
        background: white;
        border: 1px solid #dce5f0;
        border-radius: 13px;
        padding: 17px;
        margin-bottom: 14px;
        box-shadow: 0 3px 10px rgba(15, 35, 65, 0.045);
        overflow-wrap: anywhere;
    }

    .section-number {
        color: #174a83;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .section-title {
        color: #172b4d;
        font-size: 18px;
        font-weight: 700;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .definition {
        color: #334155;
        font-size: 15px;
        line-height: 1.75;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }

    .small-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }

    .timer-box {
        background: #eef5ff;
        border-left: 4px solid #2459a9;
        border-radius: 7px;
        padding: 11px 13px;
        margin-top: 13px;
        color: #17345f;
        line-height: 1.6;
        font-size: 14px;
    }

    .legal-box {
        background: #fff8e8;
        border-left: 4px solid #d69a17;
        border-radius: 7px;
        padding: 11px 13px;
        margin-top: 10px;
        color: #674b10;
        line-height: 1.6;
        font-size: 14px;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding: 20px 5px 5px 5px;
        line-height: 1.8;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #dce5f0;
        border-radius: 10px;
        padding: 12px;
    }

    @media (max-width: 700px) {
        .block-container {
            padding: 0.8rem 0.7rem 1.5rem 0.7rem;
        }

        .main-header {
            padding: 18px 16px;
        }

        .section-card {
            padding: 14px;
        }

        .section-title {
            font-size: 17px;
        }

        .definition {
            font-size: 15px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA LOADING
# Local JSON is preferred; GitHub raw URL is the fallback.
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def load_database(language):
    config = DATABASES[language]
    local_path = BASE_DIR / config["filename"]

    # 1. Try local repository file
    if local_path.exists():
        try:
            with open(local_path, "r", encoding="utf-8-sig") as file:
                raw_data = json.load(file)
            return normalize_database(raw_data), (
                f"Local file: {config['filename']}"
            )
        except (OSError, json.JSONDecodeError) as exc:
            local_error = str(exc)
    else:
        local_error = "Local JSON file not found."

    # 2. Fallback: fetch the raw GitHub JSON file
    try:
        from urllib.request import Request, urlopen

        request = Request(
            config["url"],
            headers={"User-Agent": "Dumka-Police-Sections-Library"},
        )

        with urlopen(request, timeout=10) as response:
            raw_bytes = response.read()

        raw_text = raw_bytes.decode("utf-8-sig")
        raw_data = json.loads(raw_text)

        return normalize_database(raw_data), (
            f"Loaded from GitHub: {config['filename']}"
        )

    except Exception as exc:
        raise RuntimeError(
            f"Could not load {config['filename']}. "
            f"Local file status: {local_error} "
            f"GitHub status: {exc}"
        ) from exc


def normalize_database(raw_data):
    """
    Accept a JSON list or a dictionary containing a list of records.
    Keep the source fields and do not invent missing legal content.
    """
    if isinstance(raw_data, list):
        records = raw_data

    elif isinstance(raw_data, dict):
        records = None

        for key in ("data", "sections", "records", "results"):
            if isinstance(raw_data.get(key), list):
                records = raw_data[key]
                break

        if records is None:
            # A single section object is also accepted.
            if any(
                key in raw_data
                for key in ("Section", "section", "section_number")
            ):
                records = [raw_data]
            else:
                raise ValueError(
                    "JSON dictionary does not contain a recognized "
                    "list of section records."
                )
    else:
        raise ValueError("Unsupported JSON format.")

    cleaned = []

    for item in records:
        if not isinstance(item, dict):
            continue

        section = get_field(
            item,
            "Section",
            "section",
            "section_number",
            "section_no",
        )

        title = get_field(
            item,
            "Title",
            "title",
            "Title_hi",
            "title_hi",
            "Title Hindi",
            "शीर्षक",
        )

        definition = get_field(
            item,
            "Legal Definition",
            "legal_definition",
            "definition",
            "Legal Definition Hindi",
            "definition_hi",
            "विवरण",
        )

        hindi_name = get_field(
            item,
            "crime_name_hi",
            "Crime Name Hindi",
            "crime_name_hindi",
            "हिंदी नाम",
        )

        if section is None:
            continue

        title = html.unescape(str(title or "")).strip()
        definition = html.unescape(str(definition or "")).strip()
        hindi_name = html.unescape(str(hindi_name or "")).strip()

        cleaned.append({
            "Section": str(section).strip(),
            "Title": str(title or "").strip(),
            "Legal Definition": str(definition or "").strip(),
            "crime_name_hi": str(hindi_name or "").strip(),
            "_original": item,
        })

    return cleaned


def get_field(record, *names):
    """Find a field using any of the supplied key names."""
    for name in names:
        if name in record and record[name] is not None:
            return record[name]
    return None


# =========================================================
# SECTION MATCHING
# Examples: 80, 80(2), 80 (2), Section 80(2)
# Do not concatenate subsection digits into 802.
# =========================================================

def normalize_section(value):
    value = str(value or "").strip().lower()
    value = re.sub(r"^\s*(section|sec\.?)\s*", "", value)
    value = re.sub(r"\s+", "", value)
    return value


def get_base_section(value):
    """
    Returns the main section number:
    80(2) -> 80
    103 -> 103
    80A -> 80a
    """
    normalized = normalize_section(value)
    match = re.match(r"^(\d+[a-z]?)", normalized)
    return match.group(1) if match else normalized


def section_match_rank(record_section, query_section):
    """
    2 = exact section/subsection match
    1 = base-section match
    0 = no match
    """
    record_normalized = normalize_section(record_section)
    query_normalized = normalize_section(query_section)

    if not query_normalized:
        return 0

    if record_normalized == query_normalized:
        return 2

    if (
        get_base_section(record_normalized)
        == get_base_section(query_normalized)
    ):
        return 1

    return 0


# =========================================================
# SEARCH HELPERS
# =========================================================

def searchable_text(record):
    values = [
        record.get("Section", ""),
        record.get("Title", ""),
        record.get("Legal Definition", ""),
        record.get("crime_name_hi", ""),
    ]

    # Include extra source fields, if present, for bilingual search.
    for key, value in record.get("_original", {}).items():
        if isinstance(value, (str, int, float)):
            values.append(str(value))

    return " ".join(values).casefold()


def search_records(records, query, mode):
    query = (query or "").strip()

    if not query:
        return []

    if mode == "Section Number":
        rank_results = []

        for record in records:
            rank = section_match_rank(record["Section"], query)
            if rank:
                rank_results.append((rank, record))

        # Exact matches first; base-section fallback follows.
        rank_results.sort(
            key=lambda pair: (
                -pair[0],
                normalize_section(pair[1]["Section"]),
            )
        )
        return [record for _, record in rank_results]

    terms = [term.casefold() for term in query.split() if term.strip()]
    results = []

    for record in records:
        haystack = searchable_text(record)

        # All words must be present; they may appear in different fields.
        if all(term in haystack for term in terms):
            results.append(record)

    return results


# =========================================================
# TIMER HELPERS
# =========================================================

def add_months(start_date, months):
    """Calendar-month addition; does not treat a month as 30 days."""
    month_index = start_date.month - 1 + months
    year = start_date.year + month_index // 12
    month = month_index % 12 + 1

    day = min(
        start_date.day,
        calendar.monthrange(year, month)[1],
    )

    return date(year, month, day)


def get_operational_timer(section, sr_sections, sr_days, non_sr_days):
    base = get_base_section(section)

    if base in sr_sections:
        return "SR Case", sr_days

    return "Non-SR Case", non_sr_days


def get_statutory_note(section, language):
    base = get_base_section(section)

    if base in BNSS_TWO_MONTH_SECTIONS:
        if language == "Hindi":
            return (
                "BNSS धारा 193(2): इस BNS धारा के लिए "
                "जांच पूरी करने की दो महीने की अवधि का प्रावधान है। "
                "वास्तविक मामले में लागू कानून और तथ्यों की पुष्टि करें।"
            )

        return (
            "BNSS Section 193(2): a two-month investigation "
            "completion period is provided for this BNS section. "
            "Confirm the applicable law and case facts."
        )

    if language == "Hindi":
        return (
            "इस डेटाबेस से कोई विशेष वैधानिक जांच अवधि निर्धारित "
            "नहीं की गई है। लागू कानून/विशेष अधिनियम की पुष्टि करें।"
        )

    return (
        "No specific statutory investigation period is inferred "
        "from this database. Check the applicable law or special Act."
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Search Settings")

language = st.sidebar.radio(
    "Display Language / भाषा",
    ["English", "Hindi"],
    horizontal=True,
)

st.sidebar.divider()

search_mode = st.sidebar.radio(
    "Search Type",
    ["Keyword / Crime Details", "Section Number"],
)

if search_mode == "Keyword / Crime Details":
    search_mode_internal = "Keyword"
    query_label = (
        "Enter crime, keyword or description"
        if language == "English"
        else "अपराध, शब्द या विवरण लिखें"
    )
    query_placeholder = (
        "Example: theft, murder, चोरी, हत्या"
    )
else:
    search_mode_internal = "Section Number"
    query_label = (
        "Enter BNS Section Number"
        if language == "English"
        else "BNS धारा संख्या लिखें"
    )
    query_placeholder = "Example: 103, 80(2), 64"

query = st.sidebar.text_input(
    query_label,
    placeholder=query_placeholder,
    help=(
        "Section search supports numbers and subsection formats "
        "such as 80(2) or 80 (2)."
    ),
)

st.sidebar.divider()
st.sidebar.subheader("⏱️ Operational Timer Settings")

sr_sections_text = st.sidebar.text_input(
    "SR Sections (comma-separated)",
    value=DEFAULT_SR_SECTIONS,
    help=(
        "Editable defaults retained from the original application. "
        "This list is not a legal classification."
    ),
)

sr_days = st.sidebar.number_input(
    "SR tracking days",
    min_value=1,
    max_value=365,
    value=DEFAULT_SR_DAYS,
    step=1,
)

non_sr_days = st.sidebar.number_input(
    "Non-SR tracking days",
    min_value=1,
    max_value=365,
    value=DEFAULT_NON_SR_DAYS,
    step=1,
)

calculate_timer = st.sidebar.checkbox(
    "Calculate tracking date from FIR date",
    value=False,
)

fir_date = None
if calculate_timer:
    fir_date = st.sidebar.date_input(
        "FIR Registration Date",
        value=date.today(),
        max_value=date.today(),
    )

st.sidebar.caption(
    "Timer values are configurable tracking references, "
    "not a substitute for statutory deadlines or case-specific orders."
)


# =========================================================
# HEADER
# =========================================================

if language == "Hindi":
    header_title = "⚖️ दुमका पुलिस — BNS/BNSS धारा लाइब्रेरी"
    header_subtitle = (
        "अपराध एवं धारा खोज • जांच अवधि संदर्भ • "
        "हिंदी/English डेटाबेस"
    )
else:
    header_title = "⚖️ DUMKA POLICE BNS/BNSS SECTIONS LIBRARY"
    header_subtitle = (
        "Crime & Section Search • Investigation Timeline Reference • "
        "Bilingual Database"
    )

st.markdown(
    f"""
    <div class="main-header">
        <h1>{html.escape(header_title)}</h1>
        <p>{html.escape(header_subtitle)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

try:
    with st.spinner("Loading sections database..."):
        records, data_source = load_database(language)

except Exception as exc:
    st.error(
        "Database could not be loaded. Please check the JSON filename "
        "and its format."
        if language == "English"
        else "डेटाबेस लोड नहीं हो पाया। JSON फाइल का नाम और फॉर्मेट जांचें।"
    )

    with st.expander("Technical details"):
        st.code(str(exc))

    st.info(
        "Keep the matching JSON file in the same folder as app.py. "
        "If running on Streamlit Community Cloud, commit both JSON files "
        "to the GitHub repository."
    )
    st.stop()


# =========================================================
# TOP METRICS
# =========================================================

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "Database Sections" if language == "English" else "कुल डेटाबेस प्रविष्टियां",
        f"{len(records):,}",
    )

with metric2:
    st.metric(
        "Search Mode" if language == "English" else "खोज प्रकार",
        (
            "Keyword"
            if search_mode_internal == "Keyword"
            else "Section"
        ),
    )

with metric3:
    st.metric(
        "Language" if language == "English" else "भाषा",
        language,
    )

st.caption(
    f"Database source: {data_source}"
    if language == "English"
    else f"डेटाबेस स्रोत: {data_source}"
)

if language == "Hindi":
    st.info(
        "हिंदी डेटाबेस में उपलब्ध शीर्षक और विवरण ही दिखाए जाएंगे। "
        "यदि किसी प्रविष्टि का हिंदी विवरण खाली है, तो वह खाली ही रहेगा; "
        "अनुवाद का अनुमान नहीं लगाया जाएगा।"
    )


# =========================================================
# SEARCH AND RESULTS
# =========================================================

if not query.strip():
    if language == "English":
        st.info(
            "Enter a keyword or section number in the sidebar to begin. "
            "Examples: theft, murder, 103, 80(2)."
        )
    else:
        st.info(
            "खोज शुरू करने के लिए साइडबार में अपराध का शब्द या धारा संख्या "
            "लिखें। उदाहरण: चोरी, हत्या, 103, 80(2)।"
        )
    st.stop()


if search_mode_internal == "Keyword":
    results = search_records(records, query, "Keyword")
else:
    results = search_records(records, query, "Section Number")


if not results:
    st.warning(
        "No matching sections found. Try another keyword or section number."
        if language == "English"
        else "कोई मिलती-जुलती धारा नहीं मिली। दूसरा शब्द या धारा संख्या आजमाएं।"
    )
    st.stop()


# If a subsection was requested but only the base section exists,
# explain that the displayed entry is the available database entry.
if search_mode_internal == "Section Number":
    normalized_query = normalize_section(query)
    has_exact = any(
        normalize_section(item["Section"]) == normalized_query
        for item in results
    )

    if "(" in normalized_query and not has_exact:
        st.warning(
            "The database does not contain an exact subsection match. "
            "Showing entries for the base section, if available."
            if language == "English"
            else "डेटाबेस में इस उपधारा का सटीक मिलान नहीं मिला। "
                 "उपलब्ध होने पर मूल धारा की प्रविष्टि दिखाई जा रही है।"
        )


# Remove duplicate section entries while preserving first occurrence.
unique_results = []
seen_sections = set()

for record in results:
    key = normalize_section(record["Section"])
    if key not in seen_sections:
        unique_results.append(record)
        seen_sections.add(key)

results = unique_results

st.success(
    f"Found {len(results)} matching section(s)."
    if language == "English"
    else f"कुल {len(results)} मिलती-जुलती प्रविष्टियां मिलीं।"
)

max_results = st.selectbox(
    "Results per page" if language == "English" else "एक पेज पर परिणाम",
    options=[10, 20, 30, 50],
    index=1,
)

total_pages = max(1, (len(results) + max_results - 1) // max_results)

page_number = st.number_input(
    "Page" if language == "English" else "पेज",
    min_value=1,
    max_value=total_pages,
    value=1,
    step=1,
)

start_index = (page_number - 1) * max_results
page_results = results[start_index:start_index + max_results]

st.caption(
    f"Showing {start_index + 1}–{start_index + len(page_results)} "
    f"of {len(results)}"
)


# =========================================================
# DISPLAY SECTION CARDS
# =========================================================

sr_sections = {
    normalize_section(item)
    for item in sr_sections_text.split(",")
    if item.strip()
}

# Two-column cards on desktop; Streamlit stacks on narrow screens.
columns = st.columns(2, gap="medium")

for index, record in enumerate(page_results):
    column = columns[index % 2]

    section = str(record.get("Section") or "").strip()
    title = record.get("Title") or (
        "Title not available"
        if language == "English"
        else "शीर्षक उपलब्ध नहीं"
    )
    definition = record.get("Legal Definition") or (
        "Definition not available in the selected database."
        if language == "English"
        else "चयनित डेटाबेस में विवरण उपलब्ध नहीं है।"
    )
    hindi_name = record.get("crime_name_hi") or ""

    # Escape database-provided content before HTML rendering.
    safe_section = html.escape(section)
    safe_title = html.escape(str(title))
    safe_definition = html.escape(str(definition))
    safe_hindi_name = html.escape(str(hindi_name))

    case_type, tracking_days = get_operational_timer(
        section,
        sr_sections,
        int(sr_days),
        int(non_sr_days),
    )

    # Safely handle timer values.
    case_type = str(case_type or "Not specified")
    tracking_days = int(tracking_days)

    statutory_note = (
        get_statutory_note(section, language) or ""
    )
    safe_statutory_note = html.escape(str(statutory_note))

    # Calculate tracking date.
    if fir_date:
        due_date = (
            fir_date + timedelta(days=tracking_days)
        ).strftime("%d-%m-%Y")

        tracking_date_text = (
            f"Due date: {due_date}"
            if language == "English"
            else f"ट्रैकिंग तिथि: {due_date}"
        )
    else:
        tracking_date_text = (
            "Select an FIR date in the sidebar to calculate a tracking date."
            if language == "English"
            else "ट्रैकिंग तिथि निकालने के लिए साइडबार में FIR की तारीख चुनें।"
        )

    with column:
        st.markdown(
            f"""
            <div class="section-card">

                <div class="small-label">
                    {"BNS SECTION" if language == "English" else "BNS धारा"}
                </div>

                <div class="section-number">
                    {safe_section}
                </div>

                <div class="section-title">
                    {safe_title}
                </div>

                <div class="small-label">
                    {"Legal Definition" if language == "English" else "कानूनी विवरण"}
                </div>

                <div class="definition">
                    {safe_definition}
                </div>

                {
                    f'''
                    <div style="margin-top:12px;">
                        <div class="small-label">हिंदी अपराध नाम</div>
                        <div class="definition">{safe_hindi_name}</div>
                    </div>
                    '''
                    if language == "English" and safe_hindi_name
                    else ""
                }

                <div class="timer-box">
                    <strong>
                        {
                            "Operational Tracking Reference"
                            if language == "English"
                            else "ऑपरेशनल ट्रैकिंग संदर्भ"
                        }
                    </strong>
                    <br>

                    {html.escape(case_type)} — {tracking_days}
                    {"days" if language == "English" else "दिन"}

                    <br>
                    {html.escape(tracking_date_text)}
                </div>

                <div class="legal-box">
                    <strong>
                        {
                            "Statutory timeline note"
                            if language == "English"
                            else "वैधानिक अवधि संबंधी सूचना"
                        }
                    </strong>
                    <br>
                    {safe_statutory_note or (
                        "No statutory note available."
                        if language == "English"
                        else "वैधानिक अवधि संबंधी सूचना उपलब्ध नहीं है।"
                    )}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        with st.expander(
            "View full details / पूरा विवरण",
            expanded=False,
        ):
            st.write(
                "**Section / धारा:**",
                section,
            )
            st.write(
                "**Title / शीर्षक:**",
                title or "Not available",
            )
            st.write(
                "**Definition / विवरण:**",
                definition or "Not available",
            )

            if hindi_name:
                st.write("**Hindi crime name / हिंदी अपराध नाम:**", hindi_name)

            st.download_button(
                label=(
                    "Download this section as JSON"
                    if language == "English"
                    else "इस धारा की JSON फाइल डाउनलोड करें"
                ),
                data=json.dumps(
                    record["_original"],
                    ensure_ascii=False,
                    indent=2,
                ),
                file_name=f"bns_section_{section}.json",
                mime="application/json",
                key=f"download_{language}_{section}_{index}",
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        <strong>DUMKA POLICE</strong><br>
        CCTNS IT Cell, Dumka<br>
        BNS / BNSS Sections Library • Built with Python & Streamlit<br>
        By Er. Bidhan Chandra Singh &amp; Team
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Disclaimer: This application is a search and tracking aid. "
    "Verify statutory provisions, amendments, special Acts, court orders "
    "and case-specific deadlines from authoritative sources before relying "
    "on a deadline."
)
