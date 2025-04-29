import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# Define the API key directly in the code
API_KEY = "AIzaSyAD5-tRTbhtr17baOAVq307Fguv5oa49hY"

def configure_genai():
    """Configure the Gemini AI with the API key."""
    if not API_KEY:
        st.error("API Key không hợp lệ. Xin hãy cung cấp Google API key hợp lệ.")
        return False
    try:
        genai.configure(api_key=API_KEY)
        return True
    except Exception as e:
        st.error(f"Error configuring Google API: {str(e)}")
        return False


def create_mindmap_markdown(text):
    """Generate mindmap markdown using Gemini AI."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        max_chars = 90000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
            st.warning(f"Trích xuất tổng cộng {max_chars} ký tự dựa trên độ dài văn bản.")
        
        prompt = """
        Create a hierarchical markdown mindmap from the following text. 
        Use proper markdown heading syntax (# for main topics, ## for subtopics, ### for details).
        Focus on the main concepts and their relationships.
        Include relevant details and connections between ideas.
        Keep the structure clean and organized.
        
        Format the output exactly like this example:
        # Main Topic
        ## Subtopic 1
        ### Detail 1
        - Key point 1
        - Key point 2
        ### Detail 2
        ## Subtopic 2
        ### Detail 3
        ### Detail 4
        
        Text to analyze: {text}
        
        Respond only with the markdown mindmap, no additional text.
        """
        
        response = model.generate_content(prompt.format(text=text))
        
        if not response.text or not response.text.strip():
            st.error("Received empty response from Gemini AI")
            return None
            
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating mindmap: {str(e)}")
        return None

def generate_mindmap_from_prompt(prompt_text):
    """Generate a mindmap markdown from a user-provided prompt text."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""
        Create a hierarchical markdown mindmap from the following text. 
        Use proper markdown heading syntax (# for main topics, ## for subtopics, ### for details).
        Focus on the main concepts and their relationships.
        Include relevant details and connections between ideas.
        Keep the structure clean and organized.

        Format the output exactly like this example:
        # Main Topic
        ## Subtopic 1
        ### Detail 1
        - Key point 1
        - Key point 2
        ### Detail 2
        ## Subtopic 2
        ### Detail 3
        ### Detail 4

        Text to analyze: {prompt_text}

        Respond only with the markdown mindmap, no additional text.
        """

        response = model.generate_content(prompt)

        if not response.text or not response.text.strip():
            st.error("Received empty response from Gemini AI")
            return None

        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating mindmap: {str(e)}")
        return None

def create_markmap_html(markdown_content):
    """Create HTML with enhanced Markmap visualization and a download button."""
    markdown_content = markdown_content.replace('`', '\\`').replace('${', '\\${')
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            #mindmap {{
                width: 100%;
                height: 600px;
                margin: 0;
                padding: 0;
                background: white;
            }}
            #downloadButton {{
                margin: 10px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }}
            #downloadButton:hover {{
                background-color: #45a049;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.14.3/dist/browser/index.min.js"></script>
    </head>
    <body>
        <button id="downloadButton">⬇️ Tải xuống file SVG</button>
        <svg id="mindmap"></svg>
        <script>
            window.onload = async () => {{
                try {{
                    const markdown = `{markdown_content}`;
                    const transformer = new markmap.Transformer();
                    const {{root}} = transformer.transform(markdown);
                    const mm = new markmap.Markmap(document.querySelector('#mindmap'), {{
                        maxWidth: 300,
                        color: (node) => {{
                            const level = node.depth;
                            return ['#2196f3', '#4caf50', '#ff9800', '#f44336'][level % 4];
                        }},
                        paddingX: 16,
                        autoFit: true,
                        initialExpandLevel: 2,
                        duration: 500,
                    }});
                    mm.setData(root);
                    mm.fit();

                    // Download button logic
                    document.getElementById('downloadButton').addEventListener('click', () => {{
                        const svgElement = document.getElementById('mindmap');
                        const serializer = new XMLSerializer();
                        let source = serializer.serializeToString(svgElement);

                        // Add namespaces
                        if(!source.match(/^<svg[^>]+xmlns="http\\:\\/\\/www\\.w3\\.org\\/2000\\/svg"/)) {{
                            source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
                        }}
                        if(!source.match(/^<svg[^>]+"http\\:\\/\\/www\\.w3\\.org\\/1999\\/xlink"/)) {{
                            source = source.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
                        }}

                        const svgBlob = new Blob([source], {{type:"image/svg+xml;charset=utf-8"}});
                        const url = URL.createObjectURL(svgBlob);
                        const link = document.createElement('a');
                        link.href = url;
                        link.download = "mindmap.svg";
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        URL.revokeObjectURL(url);
                    }});
                }} catch (error) {{
                    console.error('Error rendering mindmap:', error);
                    document.body.innerHTML = '<p style="color: red;">Error rendering mindmap. Please check the console for details.</p>';
                }}
            }};
        </script>
    </body>
    </html>
    """
    return html_content



def main():
    st.set_page_config(page_title="Text to Mindmap",page_icon="🧠",layout="wide")
    
    st.title("📚 AI chuyển gợi ý thành Sơ đồ MindMap ") 
    st.markdown(
        """
        <style>
        h1 {
            text-align: center;
            color: darkblue;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Add custom CSS for dark blue buttons
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
    
    if not configure_genai():
        return

    # Add a text area for user-provided prompt
    st.subheader("📓Tạo Mindmap từ gợi ý")
    prompt_text = st.text_area("Nhập đoạn gợi ý, yêu cầu của bạn tại đây:", placeholder="Nhập vào gợi ý, yêu cầu.....", height=200)

    if st.button("Tạo Mindmap"):
        if prompt_text.strip():
            with st.spinner("🔄 Xuất ra Mindmap từ gợi ý văn bản..."):
                markdown_content = generate_mindmap_from_prompt(prompt_text)

                if markdown_content:
                    tab1, tab2 = st.tabs(["📊 Mindmap", "📝 Ghi chú"])

                    with tab1:
                        st.subheader("Mindmap trực quan")
                        html_content = create_markmap_html(markdown_content)
                        components.html(html_content, height=700, scrolling=True)

                    with tab2:
                        st.subheader("Ghi chú")
                        st.text_area("Markdown Content", markdown_content, height=400)

                        st.download_button(
                            label="⬇️ Tải xuống ghi chú",
                            data=markdown_content,
                            file_name="mindmap_from_prompt.md",
                            mime="text/markdown"
                        )

if __name__ == "__main__":
    main()
