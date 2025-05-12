<p align="center">
  <a href="https://nikshay-setu.in" target="_blank">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=200&color=gradient&text=Ni-kshay%20SETU&fontSize=50&fontAlign=50&fontAlignY=34" alt="Ni-kshay Setu banner"/>
  </a>
</p>

<p align="center">
  <a href="https://nikshay-setu.in/" target="_blank">
    <img src="https://nikshay-setu.in/newLogo.b72ac552416e2a050fc6c22c0491143e.svg" width="200" alt="Ni-kshay SETU" />
  </a>
</p>

<div align="center">

![Subscribers](https://img.shields.io/badge/Subscribers-44k%2B-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-GPL%203.0-blue?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Web%20%7C%20Android%20%7C%20iOS-yellow?style=for-the-badge)
![Languages](https://img.shields.io/badge/Languages-8-orange?style=for-the-badge)

</div>

# Ni-Kshay SETU | Support to End TUberculosis

The Ni-kshay Setu app ([https://nikshay-setu.in/](https://nikshay-setu.in/)), already with **44K+ subscribers**, empowers healthcare providers to make informed decisions and contributes to India's mission to combat tuberculosis. Available on [web](https://nikshay-setu.in/), [Android](https://play.google.com/store/apps/details?id=com.iiphg.tbapp&pli=1), and [iOS](https://apps.apple.com/in/app/ni-kshay-setu/id1631331386) platforms in 8 languages, it offers real-time updates, interactive modules, and personalized insights, revolutionizing TB knowledge management and accessibility across India.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Features](#2-features)
3. [Technologies Used](#3-technologies-used)
4. [System Requirements](#4-system-requirements)
5. [Installation](#5-installation)
6. [Configuration](#6-configuration)
7. [Usage](#7-usage)
8. [Contribution Guidelines](#8-contribution-guidelines)
9. [License](#9-license)

## 1. Introduction

Ni-Kshay SETU is a groundbreaking digital solution available as a web application, Android application, and iOS application. With a mission to support healthcare providers in decision-making and transform knowledge into empowerment, this innovative and interactive learning tool is a catalyst in India's journey towards a TB-free nation. As a comprehensive digital platform, Ni-Kshay SETU revolutionizes the way healthcare providers approach TB management. By leveraging cutting-edge technology, it empowers medical professionals with real-time support and evidence-based recommendations, ensuring they have the most up-to-date information at their fingertips. With an intuitive interface and user-friendly design, Ni-Kshay SETU offers a seamless experience across devices, making it accessible to a wide range of users. The web application allows healthcare providers to access the platform from any computer, while the Android and iOS applications provide mobility and convenience for on-the-go professionals. Through a range of interactive modules, virtual simulations, and case studies, Ni-Kshay SETU transforms learning into a dynamic and engaging experience. Healthcare providers can enhance their knowledge and skills by practicing TB case management in a risk-free environment. They can diagnose, prescribe treatment plans, and monitor patient progress, gaining invaluable experience and building their confidence in TB management.

> The Ni-Kshay SETU app is part of the 'Closing the Gaps in TB care Cascade (CGC)' project, developed by the Indian Institute of Public Health, Gandhinagar (https://iiphg.edu.in/). This project aims to strengthen health systems' ability to comprehensively monitor and respond to the TB care cascade with quality improvement (QI) interventions. This digital solution is one of the key interventions of the project with the objectives to strengthen the knowledge support system of the health staff in TB patient-centric care and program management of the National TB Elimination Program.

> IIPHG, The Union, and NTEP are proud partners in the development and implementation of Ni-Kshay SETU.

> Technological support for this project is provided by Digiflux Technologies Pvt. Ltd. (https://www.digiflux.io), contributing to the development and implementation of the digital solution.


## Ni-Kshay SETU Chatbot

The Ni-Kshay SETU Chatbot is designed to facilitate inquiries related to tuberculosis (TB) management, NTEP functions, and other health-related terms. It dynamically selects the appropriate tool based on user queries, ensuring accurate and relevant responses.

### How It Works

The chatbot processes each query through a series of tools tailored for specific types of inquiries:

- **Prescription Generator:** Activates for health-related queries, especially those mentioning TB management terms like medications or treatments.
- **NTEP Tool:** Handles queries directly related to tuberculosis, utilizing a vast database to provide specific details on treatments, diagnostics, and NTEP functions. Also serves as the fallback tool.
- **Assessment Tool:** Engages when the query suggests the user is seeking a test or quiz related to health knowledge.
- **Query Response Tool:** Engases when the query suggests the user is seeking to know about their open queries.
Each query is initially checked against an in-memory system tool for quick responses. If a response is available, it is provided directly; otherwise, the query is processed further to determine the best-suited tool based on the keywords and context.

## 2. Features

- **Dynamic Tool Selection:** Automatically selects the best tool based on predefined criteria.
- **In-Memory System Tool:** Checks an in-memory system for quick responses; routes to other tools if no immediate answer is found.
- **Support for Abbreviations and Short Forms:** Understands and responds to abbreviations or short forms related to the health domain, especially TB.
- **Health Prescription Generator:** Generates personalized medical prescriptions based on user-provided health data.
- **Assessment Tool:** Offers links to quizzes and assessments when relevant keywords are detected.
- **NTEP Focused Responses:** Provides detailed information specifically related to the National Tuberculosis Elimination Program (NTEP).
- **Fallback to NTEP Tool:** Ensures responses are provided even when other tools do not yield results by using the NTEP tool as a fallback option.

## 3. Technologies Used 

- **Language**: Python 3.10 
- **Framework**: Fast Api
- **Database**: Mongo DB
- **Vector Database**: Pinecone DB
- **LLM**: gpt 4o-mini, Gemini 1.5 flash

## 4. System Requirements

-   Operating System: Windows, Linux, macOS
-   Python 3.10
-   Mongo DB
-   Internet connectivity for 3rd party api calls

## 5. Installation

1. **Ensure Python and all dependencies are installed.**
   - Install **Python 3.10**.
   - Install all dependencies using:
     ```bash
     pip install -r requirements.txt
     ```
2. Clone the project repository from GitHub: `git clone git@git.digiflux.io:hannahr/chatbot-opensource.git`

3. **Set up environment variables:**
   - Copy the example environment file and configure your environment variables:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file with appropriate values.

4. **Start the server using:**
   ```bash
   PYTHONPATH=. uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload
   ```

## 6. Configuration

The application requires certain configuration settings to work correctly. The main configuration file is `.env`. Update the following settings based on your environment:

| Variable Name             | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `OPENAI_API_KEY`         | API key for accessing OpenAI services.                                     |
| `AWS_ACCESS_KEY_ID`      | AWS access key ID for authenticating AWS services.                         |
| `AWS_SECRET_ACCESS_KEY`  | AWS secret access key for secure access.                                   |
| `AWS_REGION`             | AWS region where your services or resources are hosted.                    |
| `AWS_BUCKET`             | Name of the AWS S3 bucket used for storage.                                |
| `BASE_URL`               | Base URL for the application's backend API.                                |
| `PINECONE_API_KEY`       | API key for accessing Pinecone vector database services.                   |
| `PINECONE_ENV`           | Pinecone environment region (e.g., `us-east-1`).                           |
| `GOOGLE_API_KEY`         | Google API key for services like Maps or NLP.                              |
| `MONGO_CLIENT`           | MongoDB connection string used to connect to the database.                 |
| `MONGO_DB`               | Name of the MongoDB database to be used.                                   |
| `MONGO_COLLECTION`       | Collection name used within the MongoDB database.                          |
| `SYSTEM_TOOL_URL`        | URL of the system-level utility/tool integration endpoint.                 |
| `CHATBOT_INDEX_NAME`     | Name of the index used for chatbot-specific vector search.                 |
| `SYSTEM_QA_INDEX_NAME`   | Name of the index used for system-level Q&A or document search.            |
| `APP_ENV`                | Application environment (`development`, `staging`, or `production`).       |
| `MODEL_CONFIG_temp`      | Temperature setting for text generation randomness.                        |
| `MODEL_CONFIG_TOP_P`     | Top-p (nucleus) sampling threshold for generation control.                 |
| `MODEL_CONFIG_TOP_K`     | Top-k sampling threshold for generation diversity.                         |
| `MAX_OUTPUT_TOKENS`      | Maximum number of tokens allowed in the model output.                      |
| `RESPONSE_MIME_TYPE`     | Desired MIME type for the generated response (e.g., `text/plain`).         |
| `VECTOR_MODEL`           | Full identifier for the embedding model used in vector processing.         |
| `SENTENCE_TRANSFORMER_MODEL` | Name of the sentence transformer model used for encoding text.         |



## 7. Usage

The chatbot is accessible through a FastAPI interface, allowing easy integration with other applications or services.

### Endpoint

- **POST /process_query/**: Receives the user's query and processes it through the chatbot system.

### Payload

```json
{
  "text": "User's query here",
  "usreid": "123xyz",
  "sessionid":"123abc",
  "langcode": "en",
  "selected_mode": "desired mode of operation",
  "selected_option": "any additional options"
}
```

## Response
The response will contain the category of the tool used and the result of the query processed by that tool.

## 8. Contribution Guidelines

We welcome contributions from everyone! 🎉  
Please read our [CONTRIBUTING.md](CONTRIBUTING.md) guide to get started.  
If you find any issues or want to propose improvements, feel free to open an issue or a merge request.

## 9. License

Ni-kshay Setu project is licensed under the [GNU General Public License, Version 3.0](https://www.gnu.org/licenses/gpl-3.0).

![Static Badge](https://img.shields.io/badge/Licence-GPL%203.0-blue)


