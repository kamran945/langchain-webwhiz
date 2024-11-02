# langchain-webwhiz
* langchain-webwhiz (a project that lets users chat with an LLM to get information from a list of website URLs) could be highly useful across different fields, helping people efficiently gather, synthesize, and explore web-based information. Here are some potential use cases for WebWhiz in various sectors:
    * Education: Students and educators can use WebWhiz for research assistance, homework help, and generating discussion prompts from educational resources.
    * Healthcare: Medical professionals can input links to studies and receive summaries of key findings, drug interactions, and usage guidelines.
     * Legal: Legal practitioners can streamline case research and simplify complex legal documents for client understanding.
     * Finance: Financial analysts and investors can extract insights from market reports and educational articles on financial literacy.
     * Business and Marketing: Marketers can conduct competitor analysis, generate content ideas, and analyze consumer sentiment based on provided links.
     * Real Estate: Real estate professionals can analyze property listings and market trends while simplifying regulations for clients.
     * Journalism and Media: Journalists can aggregate news stories, verify facts, and gather background information efficiently.
     * E-commerce: Businesses can summarize product research, enhance customer service responses, and analyze supplier offerings.
     * Technology and Development: Developers can clarify technical documentation, learn from tutorials, and receive assistance with code reviews.
     * Travel and Tourism: Travelers and agents can plan trips by summarizing destination guides and creating suggested itineraries.
* FAISS is utilized in this project for efficient vector similarity searches, enabling quick retrieval of relevant information from large datasets. Its speed and scalability enhance the overall performance of content retrieval and analysis.

## Prerequisites
* Python
* Poetry 
* langchain
* streamlit

## Installation and Usage
1. Clone the repository: `git clone https://github.com/[username]/[repo-name].git`
2. Install dependencies using Poetry: `poetry install`
3. Set up your environment variables: create a `.env` file in the root directory and add the following environment variables:
    ```
    HUGGINGFACEHUB_API_TOKEN=[your-huggingface-api-token]
    GROQ_API_KEY=[your-groq-api-key]
    ```
4. Activate the Poetry shell to run the app: `poetry shell`
5. Run the app: `streamlit run app.py`
