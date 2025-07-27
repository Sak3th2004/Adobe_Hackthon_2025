# Adobe Challenge 1B – Semantic Search over PDF Collections

This project performs semantic search over multiple PDF collections to extract answers based on persona and job context using OpenAI embeddings and LlamaIndex. It's containerized using Docker and runs on CPU.

---

## 📁 Folder Structure

ADOBE_1B/
├── input/
│ └── pdfs/
│ ├── collection 1/
│ ├── collection 2/
│ └── collection 3/
├── Collection1/ # Output files for Collection 1
├── Collection2/ # Output files for Collection 2
├── Collection3/ # Output files for Collection 3
├── main.py # Main semantic search pipeline
├── Dockerfile # Docker configuration
├── requirements.txt # Python dependencies
├── execution_instruction.txt
└── README.md # This file


---

## ⚙️ How It Works

- The PDFs from each collection directory are analyzed semantically using OpenAI embeddings and LlamaIndex.
- The application takes a defined `persona`, `job`, and `query` for each collection and generates answers based on the document content.
- Answers are saved in JSON format under the respective output folders.

---

## 🧠 Example Persona Input

Each collection has a query input structured like:

```json
{
  "persona": "A 25-year-old fitness enthusiast...",
  "job": "Personal trainer",
  "query": "Dinner ideas"
}

Docker Setup
Step 1: Build Docker Image
docker build --platform linux/amd64 -t adobe:challenge1b .
 Step 2: Run the Container
 docker run --platform linux/amd64 -it --rm adobe:challenge1b
