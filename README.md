# Role Match AI
---

## Overview
Role Match AI is an intelligent job-matching application that utilizes **Azure OpenAI (AzureChatOpenAI)** and **CrewAI** to analyze resumes, search for job postings, and rate job opportunities. The application integrates job search, and rating APIs like **Jooble**, **Glassdoor**, and **Serper** to retrieve job listings and provides structured evaluations based on user-submitted resumes and job preferences.

---

## Features
- **Resume Analysis**: Extracts and processes key information from uploaded resumes.
- **Job Search API Integration**: Fetches job listings from **Jooble** and **Glassdoor**.
- **AI-Powered Job Matching**: Uses **CrewAI agents** to analyze job postings and match them to resumes.
- **Company Evaluation**: Retrieves and rates companies based on relevant factors.
- **Flask Web API**: Accepts job search parameters such as keywords, job location, and resume files.
- **Structured JSON Output**: Provides well-formatted results for easy integration.

---

## Tech Stack
- **Backend**: Python, Flask
- **AI Models**: Azure OpenAI (AzureChatOpenAI)
- **Orchestration**: CrewAI
- **Job Search and Ratings APIs**: Jooble, Serper
- **Data Processing**: Python, Pandas

### Setting Up Accounts & API Keys

To use the application, you need API keys for Jooble and Azure OpenAI. Follow the steps below to set up your accounts:

#### Jooble API
- Sign up for a Jooble API key at [Jooble API](https://jooble.org/api/about).
- Once registered, obtain your JOOBLE_HOST and JOOBLE_API_KEY.

#### Serper API
- Sign Up: Create a free account at [Serper](https://serper.dev).
- Obtain API Key: Once registered, acquire your SERPER_API_KEY.

#### Azure OpenAI API
- Sign up for an Azure account at [Azure Portal](https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize?redirect_uri=https%3A%2F%2Fportal.azure.com%2Fsignin%2Findex%2F&response_type=code%20id_token&scope=https%3A%2F%2Fmanagement.core.windows.net%2F%2Fuser_impersonation%20openid%20email%20profile&state=OpenIdConnect.AuthenticationProperties%3DmsvIcQ2tdnIXeJa96ozN49dXD2XPVBqIpx-9O3Hb4eopnHuAanQ5At02iWirBY2gwmmnOfi9gwH3I5rpJhepmjglzGqpYd9ckEcLI-881rfHyvVeXSyEwzK1hBVkAm4cyz8rQ2V7oIbHusCu9ufB6NOWGvgOX1pmniu_ePA2GBW72w-1PR27dZ8trNMXTMFkHpleVRs-dyxrbPIWZdejLc3yP22IsWIH3PgWButHfjYLoCr_IKYduSMduNU1sBq50WQjB-Eri2MFNuQo4J_q529Z07mBSVoyB8EyMrFwH8RaI4sBIEm5FRDiHRnU1ijxwzFEvkKd_b8mYPiMwQrDFT80jgGMNv5GMSmHbzhDyNDuANcqWa6FA88UuHQLGENgTPOEIL-sRTnt6bRTbIO5RAxGY9HxerB_RihAuEbDHZZsCMTWLJCR3b8w0gg6yhKNgAJwD7rKs2XiVMzQO2p6OBdVMHu7-ssaZse6lSeha18&response_mode=form_post&nonce=638762877063219873.MGMwNzdmNTMtZTE0Ny00NjAwLTliNmYtOGU2NTY4MDlhMDRjMWZiOTkyODktZTVhNC00OThmLWEyNWEtODY0MjJmN2EwNWIz&client_id=c44b4083-3bb0-49c1-b47d-974e53cbdf3c&site_id=501430&client-request-id=989489b1-e658-49c4-824e-be46fdd2446f&x-client-SKU=ID_NET472&x-client-ver=7.5.0.0).
- Navigate to Azure OpenAI Service and deploy a new model.
- Retrieve your AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and OPENAI_API_VERSION.
- For additional documentation, visit [Azure OpenAI Docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/).

---

## Project Structure
```
├── README.md
├── data
│   ├── resumes
│   │   └── Professional Resume - 2025.docx.txt
│   ├── sample_jobs.json
│   ├── sample_result.json
│   └── sample_resume.txt
├── environment.yml
├── requirements.txt
├── src
│   ├── agent.py          # CrewAI agents for job search & evaluation
│   ├── config
│   │   ├── agents.yml    # Configuration for AI agents
│   │   └── tasks.yml     # Task definitions for job search & rating
│   ├── main.py          # Main execution script
│   ├── models
│   │   └── models.py    # AI model configurations
│   ├── services
│   │   ├── jooble.py    # Jooble API integration
│   │   └── search_jobs.py # Job search functions
│   ├── tasks.py         # Job-related task execution
│   └── utils
│       ├── parser.py    # Resume parsing utilities
│       └── utils.py     # Helper functions
└── web
    ├── app.py          # Flask Web API
    ├── static
    │   └── css
    │       └── styles.css
    └── templates
        ├── index.html   # Search input page
        └── results.html # Job search results page
```

---

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/judesantos/job_search_assistant.git
   cd job_search_assistant
   ```
2. **Set up the Miniconda environment**:
   ```bash
   conda env create -f environment.yml
   conda activate mlagent
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   - Create a `.env` file in the root directory and use `.env.development` as a guide. Add the following entries:
     ```
     SERPER_API_KEY=<signup_for_a_free_serper_api_key>

     JOOBLE_HOST=<signup_for_a_free_jooble_api_key>
     JOOBLE_API_KEY=<the_jooble_api_key>

     AZURE_OPENAI_ENDPOINT=<the_azure_openai_endpoint_in_your_azure_account>
     AZURE_OPENAI_KEY=<the_azure_openai_key_in_your_azure_account>
     OPENAI_API_VERSION=<the_openai_api_version_in_your_azure_account>
     ```
---

## Documentation Links
- **Azure OpenAI:** Azure OpenAI Docs
- **Jooble API:** Jooble API Docs
- **CrewAI:** CrewAI Documentation

---

## Usage
### Running the Web API
```bash
python -m web.app
```
Access the web app at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Running Job Search & Rating via CLI
```bash
python src/main.py --resume data/resumes/sample_resume.txt --keywords "Software Engineer" --location "New York"
```
---

## API Endpoints
### 1. **Upload Resume & Search Jobs**
   - **Endpoint:** `/search`
   - **Method:** `POST`
   - **Parameters:**
     - `resume` (file)
     - `keywords` (string)
     - `location` (string)
   - **Response:** JSON object containing job listings and ratings.

### 2. **Fetch Job Search Results**
   - **Endpoint:** `/results`
   - **Method:** `GET`
   - **Response:** JSON object with job listings and evaluations.

---

## JSON Output Format
```json
{
  "jobs": [
    {
      "id": "12345",
      "location": "New York",
      "title": "Software Engineer",
      "company": "TechCorp",
      "description": "Exciting opportunity for a software engineer...",
      "provider": "Glassdoor",
      "url": "https://example.com/job12345",
      "rating": 9,
      "rating_notes": "Matches skills and experience closely.",
      "company_rating": 8,
      "company_notes": "Well-rated company with growth opportunities."
    }
  ]
}
```
---

## Future Enhancements
- **Add more job search sources (LinkedIn, Indeed, etc.)**
- **Improve AI matching using deep learning models**
- **Enhance Flask UI for better user experience**

---

## Contributors
- **Jude Santos** ([judesantos](https://github.com/judesantos))

---

## License
This project is licensed under the MIT License.

