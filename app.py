import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import io

def add_file_to_dataframe(uploaded_file):
    reader = PdfReader(uploaded_file)
    num_pages = len(reader.pages)
    return {
        "File Name": uploaded_file.name,
        "Pages": num_pages,
        "File": uploaded_file
    }

def update_file_list(order, index):
    if order == 'up' and index > 0:
        df = st.session_state.file_dataframe
        df.iloc[[index, index - 1]] = df.iloc[[index - 1, index]].values
    elif order == 'down' and index < len(st.session_state.file_dataframe) - 1:
        df = st.session_state.file_dataframe
        df.iloc[[index, index + 1]] = df.iloc[[index + 1, index]].values
    reset_order_column()

def reset_order_column():
    st.session_state.file_dataframe['Order'] = range(1, len(st.session_state.file_dataframe) + 1)

def remove_file(index):
    st.session_state.file_dataframe = st.session_state.file_dataframe.drop(index).reset_index(drop=True)
    reset_order_column()

def merge_pdfs(file_list):
    writer = PdfWriter()
    for file_info in file_list:
        reader = PdfReader(file_info["File"])
        for page in range(len(reader.pages)):
            writer.add_page(reader.getPage(page))
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output

st.title('Easy PDF Merger')
st.subheader('*Bind your PDF files easier*', divider='red')

if 'file_dataframe' not in st.session_state:
    st.session_state.file_dataframe = pd.DataFrame(columns=["File Name", "Pages", "File"])


st.sidebar.markdown("#  ")
st.sidebar.markdown("#  ")

# Sidebar Instruction
with st.sidebar.expander("Instructions"):
    st.write("""
        This application allows you to merge multiple PDF files into one. 
        
        How to use:
        
        1. Upload your PDF files using the 'Select PDF files' button or "Drag and Drop" files.
        2. The uploaded files will appear in the main. You can adjust the order by selecting a file and using the 'Up' and 'Down' buttons.
        3. Once you're satisfied with the order, click the 'Merge PDFs' button to merge the files.
        4. Download the merged PDF by clicking the 'Download Merged PDF' button.
        
        Note: You can clear the uploaded files list at any time using the 'Clear File List' button.
    """)
st.sidebar.divider()

uploaded_files = st.sidebar.file_uploader(
    "Select PDF files", accept_multiple_files=True, type=['pdf']
)
if uploaded_files:
    new_files = [
        add_file_to_dataframe(uploaded_file) for uploaded_file in uploaded_files
        if uploaded_file.name not in st.session_state.file_dataframe["File Name"].values
    ]
    if new_files:
        st.session_state.file_dataframe = pd.concat(
            [st.session_state.file_dataframe, pd.DataFrame(new_files)], ignore_index=True
        )
        reset_order_column()

if st.sidebar.button('Clear File List'):
    st.session_state.file_dataframe = pd.DataFrame(columns=["File Name", "Pages", "File"])

st.markdown("""
<style>
.custom-container {
    max-width: 90%;
    margin: auto;
}
.custom-table {
    width: 100%;
    border-collapse: collapse;
}
.custom-table th, .custom-table td {
    border: 1px solid #ddd;
    padding: 8px;
}
.custom-table th {
    text-align: center;
    color: #FFFFFF;
    background-color: #FF4B4B;
    background-opacity: 0.4;
}
.custom-table td:nth-child(1), .custom-table td:nth-child(3) {
    text-align: center;
    width: 10%;
}
.custom-table td:nth-child(2) {
    width: 60%;
}
</style>
""", unsafe_allow_html=True)

if not st.session_state.file_dataframe.empty:
    with st.container():
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        st.write("Uploaded Files:")
        df_html = st.session_state.file_dataframe[["Order", "File Name", "Pages"]].to_html(
            classes="custom-table", index=False
        )
        st.markdown(df_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.file_dataframe.empty:
    cols = st.columns([3, 1, 4, 1, 1])
    with cols[0]:
        st.markdown('#  ')
        if st.button('Merge PDFs', type="primary"):
            if len(st.session_state.file_dataframe) > 1:
                merged_pdf = merge_pdfs(st.session_state.file_dataframe.to_dict('records'))
                st.download_button(
                    label="Download Merged PDF",
                    data=merged_pdf,
                    file_name="merged.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Please upload two or more files.")

    selected_filename = st.session_state.selected_filename if 'selected_filename' in st.session_state else None
    file_names = st.session_state.file_dataframe["File Name"].tolist()
    with cols[2]:
        selected_filename = st.selectbox(
            "Select a file to reorder",
            options=file_names,
            index=file_names.index(selected_filename) if selected_filename in file_names else 0
        )
        st.session_state.selected_filename = selected_filename

    if selected_filename:
        selected_index = st.session_state.file_dataframe.index[
            st.session_state.file_dataframe["File Name"] == selected_filename
        ].tolist()[0]
        with cols[3]:
            st.markdown('#  ')
            if st.button('🔺'):
                update_file_list('up', selected_index)
        with cols[4]:
            st.markdown('#  ')
            if st.button('🔻'):
                update_file_list('down', selected_index)
