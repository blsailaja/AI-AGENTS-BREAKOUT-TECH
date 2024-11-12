# app.py
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from io import StringIO
import os
from dotenv import load_dotenv
import requests
import groq
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

class APIClients:
    """Handles API client initialization and configuration."""
    
    def __init__(self):
        self.groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")

class WebSearcher:
    """Handles web search operations using SerpAPI."""
    
    def __init__(self, serpapi_key: str):
        self.serpapi_key = serpapi_key
    
    def search(self, entity: str, prompt: str) -> str:
        """
        Perform a web search using SerpAPI.
        
        Args:
            entity: The entity to search for
            prompt: The search prompt template
            
        Returns:
            str: Combined search result snippets
        """
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": prompt.format(entity=entity),
                "api_key": self.serpapi_key,
                "num": 5
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            results = response.json().get("organic_results", [])
            
            snippets = [result.get("snippet", "") for result in results]
            return "\n".join(snippets)
        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"Error during web search: {str(e)}")
            return ""

class LLMProcessor:
    """Handles LLM-based information extraction using Groq."""
    
    def __init__(self, groq_client):
        self.groq_client = groq_client
    
    def extract_information(self, entity: str, prompt: str, search_results: str) -> str:
        """
        Extract information from search results using Groq's LLM.
        
        Args:
            entity: The entity being processed
            prompt: The extraction prompt template
            search_results: Raw search results to process
            
        Returns:
            str: Extracted information
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts specific information from web search results."},
            {"role": "user", "content": f"Extract information from the following search results based on the prompt: '{prompt.format(entity=entity)}'\n\nSearch Results:\n{search_results}\n\nExtracted Information:"}
        ]
        try:
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                max_tokens=150,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.sidebar.error(f"Error during LLM extraction: {str(e)}")
            return ""

class DataProcessor:
    """Handles data processing operations."""
    
    def __init__(self, web_searcher: WebSearcher, llm_processor: LLMProcessor):
        self.web_searcher = web_searcher
        self.llm_processor = llm_processor
    
    def process_entities(self, entities: List[str], prompt: str) -> List[Dict[str, str]]:
        """
        Process a list of entities and return results.
        
        Args:
            entities: List of entities to process
            prompt: The prompt template to use
            
        Returns:
            List[Dict[str, str]]: Processing results
        """
        results = []
        for entity in entities:
            search_results = self.web_searcher.search(entity, prompt)
            if search_results:
                extracted_info = self.llm_processor.extract_information(entity, prompt, search_results)
                results.append({"Entity": entity, "Extracted Information": extracted_info})
            else:
                results.append({"Entity": entity, "Extracted Information": "No data found"})
        return results

class DataLoader:
    """Handles data loading from different sources."""
    
    @staticmethod
    def load_csv(uploaded_file) -> Optional[pd.DataFrame]:
        """Load data from uploaded CSV file."""
        try:
            csv_data = uploaded_file.read().decode("utf-8")
            return pd.read_csv(StringIO(csv_data))
        except Exception as e:
            st.sidebar.error(f"Error reading CSV file: {str(e)}")
            return None
    
    @staticmethod
    def load_google_sheet(sheet_url: str) -> Optional[pd.DataFrame]:
        """Load data from Google Sheet."""
        try:
            creds = Credentials.from_service_account_file(
                "google_sheets_credentials.json",
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            client = gspread.authorize(creds)
            sheet = client.open_by_url(sheet_url).sheet1
            data = sheet.get_all_values()
            headers = data.pop(0)
            return pd.DataFrame(data, columns=headers)
        except Exception as e:
            st.sidebar.error(f"Error connecting to Google Sheet: {str(e)}")
            return None

def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(page_title="AI Insight Miner", layout="wide")
    
    # Initialize API clients
    api_clients = APIClients()
    
    # Initialize components
    web_searcher = WebSearcher(api_clients.serpapi_key)
    llm_processor = LLMProcessor(api_clients.groq_client)
    data_processor = DataProcessor(web_searcher, llm_processor)
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    # Title
    st.title("AI Insight Miner Dashboard")
    
    # Sidebar for data input
    st.sidebar.header("Data Input")
    data_source = st.sidebar.radio("Choose data source:", ("CSV Upload", "Google Sheets"))
    
    # Handle data loading
    if data_source == "CSV Upload":
        uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")
        if uploaded_file is not None:
            st.session_state.data = DataLoader.load_csv(uploaded_file)
            if st.session_state.data is not None:
                st.sidebar.success("CSV file uploaded successfully!")
    else:
        sheet_url = st.sidebar.text_input("Enter Google Sheet URL")
        if sheet_url:
            st.session_state.data = DataLoader.load_google_sheet(sheet_url)
            if st.session_state.data is not None:
                st.sidebar.success("Google Sheet connected successfully!")
    
    # Main content
    if st.session_state.data is not None:
        st.header("Data Preview")
        st.dataframe(st.session_state.data.head())
        
        # Column selection
        st.header("Select Primary Column")
        primary_column = st.selectbox(
            "Choose the column containing the entities",
            st.session_state.data.columns
        )
        
        # Check for missing values
        if st.session_state.data[primary_column].isnull().any():
            st.warning(f"The selected column '{primary_column}' contains missing values. Please clean the data.")
        
        # Custom prompt input
        st.header("Custom Prompt")
        custom_prompt = st.text_area(
            "Enter your custom prompt for information extraction",
            "What is the main product or service of {entity}?"
        )
        
        # Process data
        if st.button("Process Data"):
            with st.spinner("Processing data..."):
                results = data_processor.process_entities(
                    st.session_state.data[primary_column].tolist(),
                    custom_prompt
                )
                st.session_state.results = results
            st.success("Data processing complete!")
        
        # Display results
        if st.session_state.results:
            st.header("Results")
            result_df = pd.DataFrame(st.session_state.results)
            st.dataframe(result_df)
            
            # Download results
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="ai_agent_results.csv",
                mime="text/csv"
            )
    else:
        st.info("Please upload a CSV file or connect to a Google Sheet to get started.")
    
    # Add custom styling
    st.markdown("""
    <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 4px;
        }

        .stButton > button:hover {
            background-color: #45a049;
        }

        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
