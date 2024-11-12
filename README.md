# AI Agent Dashboard

## Project Description

AI Agent Dashboard is a web application that helps you extract and analyze information from web search results. The app allows you to:
- Upload data through CSV files or Google Sheets
- Perform automated web searches about companies, products, or any entities
- Extract relevant information using AI-powered analysis
- Download results in CSV format for further use

Built with Streamlit, SerpAPI, Groq, and Google Sheets integration, this tool makes web research and data analysis simple and efficient.

---

## Setup Instructions

### 1. Install Dependencies
Clone the repository and install the required packages:
```bash
# Clone the repository
https://github.com/blsailaja/AI-AGENTS-BREAKOUT-TECH.git
```
# Install required packages
```bash
pip install -r requirements.txt
```
### 2. Set Up Environment
Create a .env file in the project root directory with the following content:
```bash
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```


### 3. Set up Google Sheets API integration using a service account, follow these exact steps:
#### Step 1:  Enable the Google Sheets API in Google Cloud Console
###### 1. Go to Google Cloud Console: Visit Google Cloud Console(https://shorturl.at/pnwYn)
###### 2.Create a New Project
- Click on the Project dropdown in the top-left corner.
- Click New Project.
- Enter a project name, then click Create.
###### 3. Enable the Google Sheets API:
- Select your project, then go to APIs & Services > Library.
- Search for Google Sheets API and select it.
- Click Enable to activate it for your project.

####  Step 2: Create a Service Account for API Access
###### 1. Go to the Service Accounts Section:
- Navigate to IAM & Admin > Service Accounts.

###### 2.Create a New Service Account:

- Click + CREATE SERVICE ACCOUNT at the top.
- Enter a name and description for the service account (e.g., "Google Sheets API Access").
- Click Create and Continue.
###### 3. Grant the Service Account Role:

- Choose the Editor role (or Viewer if only read access is needed).
- Click Continue and then Done.
###### 4.Generate a JSON Key for the Service Account:

- In the Service Accounts list, click on the service account you just created.
- Go to the Keys tab.
- Click ADD KEY, then Create new key.
- Select JSON as the key type, then click Create. A JSON file containing your service account credentials will be downloaded.

#### Step 3: Configure the Service Account in Your Project
##### Move the JSON Key File:

- Rename the downloaded JSON file to google_sheets_credentials.json.
- Place this file in the root directory of your project.
### 4. Run the Application
Run the Streamlit app to start the application:
```bash
streamlit run app.py
```
The app will be available at http://localhost:8501.

---
## Usage Guide
### Using CSV Files
- Select CSV Upload from the sidebar.
- Upload your CSV file containing entities to analyze.
- Choose the column with your target entities.
- Enter your custom search prompt.
- Click Process Data to start the analysis.
- Download the results using the Download Results button.

### Using Google Sheets
- Set up Google Sheets credentials (refer to the "Google Sheets Setup" above).
- Select Google Sheets in the sidebar.
- Enter the URL of your Google Sheet.
- Choose the target column with your entities.
- Enter your search prompt and click Process Data to begin the analysis.
- After processing, download the results using the Download Results button.

---

### Search Query Configuration
- Enter a custom search prompt using the {entity} placeholder (e.g., "What are the main products of {entity}?").
- The system will replace {entity} with the actual values from your data (CSV or Google Sheets).
- Once the data is processed, you'll be able to view and export the results.

---

### API Keys and Environment Variables
#### Required API Keys
1.Groq API Key
- Sign up at Groq and get your API key.
- Add it to your .env file as GROQ_API_KEY.

2.SerpAPI Key
- Register at SerpAPI to get your API key.
- Add it to your .env file as SERPAPI_API_KEY.

3.Google Sheets Credentials
- Create a project in Google Cloud Console and enable the Google Sheets API.
- Download your service account credentials as a JSON file.
- Rename the file to google_sheets_credentials.json and place it in the project root directory.
- Make sure all API keys are correctly added to the .env file for the application to work properly.

---
### Optional Features
#### Enhanced Search Options
- Adjust Search Results: Customize the number of search results to process from each search query.
- AI Response Parameters: Configure AI response parameters such as temperature and maximum token length for better control over the responses.
- Custom Search Templates: Modify search query templates to meet specific needs.

#### Data Validation
- Automatic Missing Value Detection: The app will automatically detect and flag missing values in the data.
- Input Validation: Ensure correct Google Sheets URL format and prevent issues with incorrect URLs.
- Error Notifications: The application will notify users of any issues with the data or setup.

#### Export Options
- CSV Export: Download results in CSV format for further processing.
- Real-time Processing Progress: View real-time updates on the processing status.
- Data Preview: Preview the data before starting the processing.

---

## Troubleshooting

#### Common Issues and Solutions
- API Key Errors: Ensure the API keys are correctly entered in the .env file.
- Google Sheets Access: Double-check that the Google Sheet is shared with the service account email.
- Missing Dependencies: If any dependencies are missing, re-run the following command:
```bash
pip install -r requirements.txt
```
- Runtime Errors: Check the console output for detailed error messages, which may help identify configuration issues.

---

### Contributing
- Feel free to fork this repository and submit pull requests for any improvements or bug fixes. You can also report issues using the GitHub issues tab.


