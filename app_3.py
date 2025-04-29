import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import json

# Setup Gemini API
genai.configure(api_key="AIzaSyAD5-tRTbhtr17baOAVq307Fguv5oa49hY")

def get_events_from_gemini(description):
    prompt = f"""
    Given the description below, generate ONLY a list of events with dates. If requirement is in Vietnamese, show result in Vietnamese language.
    Output format must be strict JSON array like:
    
    [
      {{"date": "1957-10-15", "event": "FORTRAN introduced"}},
      {{"date": "1991-02-20", "event": "Python released"}}
    ]
    
    If no exact day available, just use year, e.g. "1957".

    Description: {description}
    """
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    # Find first JSON block
    text = response.text.strip()
    start = text.find('[')
    end = text.rfind(']')
    json_text = text[start:end+1]
    events = json.loads(json_text)
    return events

def build_mermaid_timeline(title, events):
    mermaid = "timeline\n"
    mermaid += f"    title {title}\n"
    for event in events:
        mermaid += f"    {event['date']} : {event['event']}\n"
    return mermaid

def render_mermaid(mermaid_code):
    # Embed the correct mermaid.js setup
    components.html(
        f"""
        <script type="module">
          import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
          mermaid.initialize({{ startOnLoad: true }});
        </script>
        <div class="mermaid">
        {mermaid_code}
        </div>
        """,
        height=700,
        scrolling=True,
    )


# Streamlit app UI
st.set_page_config(page_title="AI Timeline Builder",page_icon="🧠", layout="wide")
st.title("📚 AI tạo biểu đồ Timeline")

title = st.text_input("Tên biểu đồ Timeline", placeholder="Nhập vào tên biểu đồ.....")
description = st.text_area("Nhập vào đoạn mô tả cho biểu đồ Timeline", placeholder="Nhập vào đoạn mô tả tại đây.....", height=150)

if st.button("Tạo biểu đồ"):
    if description:
        with st.spinner('AI đang tạo biểu đồ cho bạn...'):
            try:
                events = get_events_from_gemini(description)
                mermaid_code = build_mermaid_timeline(title, events)
                st.subheader("Biểu đồ Timeline")
                render_mermaid(mermaid_code)
                st.code(mermaid_code, language='markdown')
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {e}")
    else:
        st.warning("Xin hãy nhập vào đoạn mô tả.")

st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: blue;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        div.stButton > button:hover {
            background-color: #002244;
        }
        </style>
        """,
        unsafe_allow_html=True
)
