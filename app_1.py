sponse.text or not response.text.strip():
            st.error("Received empty response from Gemini AI")
            return None

        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating mindmap: {str(e)}")
        return None

def create_markmap_html(markdown_content):
    """Create HTML with enhanced Markmap visualization."""
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
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.14.3/dist/browser/index.min.js"></script>
    </head>
    <body>
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
    st.set_page_config(layout="wide")
    
    st.title("📚 AI-Powered Mindmap Converter App ") 
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

    st.subheader("📓Generate Mindmap from PDF file")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    # Add buttons for PDF conversion and text prompt conversion
    if st.button("Convert PDF to Mindmap"):
        if uploaded_file is not None:
            with st.spinner("🔄 Processing PDF and generating mindmap..."):
                text = extract_text_from_pdf(uploaded_file)
                
                if text:
                    st.info(f"Successfully extracted {len(text)} characters from PDF")
                    
                    markdown_content = create_mindmap_markdown(text)
                    
                    if markdown_content:
                        tab1, tab2 = st.tabs(["📊 Mindmap", "📝 Markdown"])
                        
                        with tab1:
                            st.subheader("Interactive Mindmap")
                            html_content = create_markmap_html(markdown_content)
                            components.html(html_content, height=700, scrolling=True)
                        
                        with tab2:
                            st.subheader("Generated Markdown")
                            st.text_area("Markdown Content", markdown_content, height=400)
                            
                            st.download_button(
                                label="⬇️ Download Markdown",
                                data=markdown_content,
                                file_name="mindmap.md",
                                mime="text/markdown"
                            )

    # Add a text area for user-provided prompt
    st.subheader("📓Generate Mindmap from Text")
    prompt_text = st.text_area("Enter your text prompt here:", height=200)

    if st.button("Convert Text to Mindmap"):
        if prompt_text.strip():
            with st.spinner("🔄 Generating mindmap from text prompt..."):
                markdown_content = generate_mindmap_from_prompt(prompt_text)

                if markdown_content:
                    tab1, tab2 = st.tabs(["📊 Mindmap", "📝 Markdown"])

                    with tab1:
                        st.subheader("Interactive Mindmap")
                        html_content = create_markmap_html(markdown_content)
                        components.html(html_content, height=700, scrolling=True)

                    with tab2:
                        st.subheader("Generated Markdown")
                        st.text_area("Markdown Content", markdown_content, height=400)

                        st.download_button(
                            label="⬇️ Download Markdown",
                            data=markdown_content,
                            file_name="mindmap_from_prompt.md",
                            mime="text/markdown"
                        )

if __name__ == "__main__":
    main()
