import streamlit as st

from src.helper import (load_url_data, 
                        create_chunks, 
                        create_vectorstore, 
                        save_vectorstore,
                        get_retrieval_chain, 
                        get_answer_and_source,)

# Initialize the list to store URLs
if "url_list" not in st.session_state:
    st.session_state["url_list"] = []

# Initialize the list of processed URLs
if "processed_urls" not in st.session_state:
    st.session_state["processed_urls"] = []

def add_url():
    # Append the URL from input to the list
    url = st.session_state.url_input
    if url:
        if url not in st.session_state.url_list:
            st.session_state.url_list.append(url)
        st.session_state.url_input = ""  # Clear the input box after adding


main_placeholder_text = st.empty()
main_placeholder_text_input = st.empty()
vectorstore_filepath = "vectorstore.pkl"

def create_sidebar():

    st.sidebar.header("URL Input")
    st.sidebar.title("URL Input")

    # Text input for URL
    st.sidebar.text_input("Enter URL:", key="url_input")

    # Add URL button
    if st.sidebar.button("Add URL", on_click=add_url):
        
        st.sidebar.success("URL added successfully.")

    # Process button
    if st.sidebar.button("Process URLs"):
        # Placeholder: Perform some operation with the list of URLs
        st.sidebar.write("Processing URLs:")
        # Process the URLs that are not in st.session_state.processed_urls

        url_list_to_process = []
        urls = st.session_state.url_list
        for url in urls:
            if url not in st.session_state.processed_urls:
                url_list_to_process.append(url)
        if url_list_to_process:
            main_placeholder_text.text("Loading URL data...✅✅✅")
            url_data = load_url_data(urls=url_list_to_process)

            # Check if any document's page_content is empty
            empty_documents = [doc for doc in url_data if not doc.page_content.strip()]
            if not empty_documents:
                main_placeholder_text.text("Creating document chunks...✅✅✅")
                chunks = create_chunks(documents=url_data)
                main_placeholder_text.text("Creating Vectorstore...✅✅✅")
                vectorstore = create_vectorstore(chunks=chunks)
                main_placeholder_text.text("Saving vectorstore...✅✅✅")
                save_vectorstore(vectorstore=vectorstore, 
                                filepath=vectorstore_filepath)
                st.session_state.processed_urls.extend(url_list_to_process)
                main_placeholder_text.text("")
                st.sidebar.success("URLs processed successfully.")
        else:
            main_placeholder_text.text("")
            st.sidebar.success("No URLs to process.")

    # Show list of URLs added so far
    st.sidebar.write("URLs List:")
    for url in st.session_state.url_list:
        st.sidebar.write(url)

def create_main_content():
    st.title("WebWhiz: Your Gateway to Knowledge: Converse with Content!")
    st.header("AI Assistant")

    user_input = main_placeholder_text_input.text_input("Question:")
    if user_input:
        chain = get_retrieval_chain(vectorstore_filepath=vectorstore_filepath)
        result = get_answer_and_source(question=user_input, chain=chain)
        st.header("Answer")
        st.write(result["answer"])

        sources = result.get("source", "")
        if sources:
            st.subheader("Sources:")
            sources_list = sources.split("\n")  # Split the sources by newline
            for source in sources_list:
                st.write(source)


def main():
    create_sidebar()
    create_main_content()

if __name__ == "__main__":
    main()
