# ChalkBotX - A Smart Chatbot for Student Queries

ChalkBotX is an intelligent chatbot designed to assist students with their academic queries. It allows students to ask questions by uploading PowerPoint presentations (PPT), PDF files, images, or scanned books, and the chatbot will provide relevant answers.

## Team Members

- Samyuktha M S - 20Z243
- S Charumathi - 20Z240
- Shifa Mohamed Ibrahim - 20Z249
- Glory C J - 21Z433
- Darsana R - 20Z212

## How it Works

1. **Upload Files:** Students can upload their academic materials, such as PPTs, PDFs, images, or scanned books.

2. **Ask Questions:** Using natural language, students can ask questions related to the uploaded materials.

3. **AI Processing:** ChalkBotX analyzes the content and generate appropriate responses.

4. **Instant Replies:** The chatbot provides instant replies with answers, explanations, or suggestions based on the uploaded materials.

## Steps to Replicate 

1. Fork this repository and create a codespace in GitHub as I showed you in the youtube video OR Clone it locally.
```
git clone https://github.com/samyuktha-12/ChalkBotX
cd ChalkBotX
```

2. In .env file add the OpenAI API key as follows. Get OpenAI API key from this [URL](https://platform.openai.com/account/api-keys). You need to create an account in OpenAI webiste if you haven't already.
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Create a virtualenv and activate it
  
   ```
   conda create -n .venv python=3.11 -y && source activate .venv
   ```

4. Run the following command in the terminal to install necessary python packages:
   ```
   pip install -r requirements.txt
   ```

5. Run the following command in your terminal to start the chat UI:
   ```
   chainlit run app.py
   ```
---

