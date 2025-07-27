import os
import json
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util
import torch
from datetime import datetime

# === Constraints ===
device = "cpu"
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# === Configuration ===
PDF_FOLDER = "input\Collection 3\PDFs"
OUTPUT_FOLDER = "Collection3"
TOP_K = 3
# User context
persona = "Food Contractor"
job = "Prepare vegetarian buffet-style dinner menu for corporate gathering"
USER_CONTEXT = f"As a {persona}, my goal is to {job}.\n\n"

# === Query input ===
query_input = os.environ.get("QUERY", "Extract recipes that are quick to cook (under 30 minutes), use healthy ingredients, and are suitable for family dinners.")
query = USER_CONTEXT + query_input  # <-- includes persona and job context

query_embedding = model.encode(query, convert_to_tensor=True)

# === Ensure output folder exists ===
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Process each PDF ===
for filename in os.listdir(PDF_FOLDER):
    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, filename)
    reader = PdfReader(pdf_path)

    page_texts = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
            if text.strip():
                page_texts.append({
                    "document": filename,
                    "page_number": i + 1,
                    "content": text.strip()
                })
        except:
            continue


    if not page_texts:
        continue

    # === Embeddings & Semantic similarity ===
    corpus_embeddings = model.encode(
        [page["content"] for page in page_texts],
        convert_to_tensor=True
    )

    similarities = util.cos_sim(query_embedding, corpus_embeddings)[0]
    scored_pages = sorted([
        {**page_texts[i], "similarity": float(similarities[i])}
        for i in range(len(page_texts))
    ], key=lambda x: x["similarity"], reverse=True)[:TOP_K]

    # === Final JSON Output ===
    json_output = {
        "metadata": {
            "input_document": filename,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "extracted_section": [],
        "sub_section_analysis": []
    }

    for rank, item in enumerate(scored_pages, 1):
        json_output["extracted_section"].append({
            "document": item["document"],
            "page_number": item["page_number"],
            "section_title": item["content"].split('\n')[0].strip()[:80],
            "importance_rank": rank
        })
        json_output["sub_section_analysis"].append({
            "document": item["document"],
            "refined_text": item["content"][:500] + ("..." if len(item["content"]) > 500 else ""),
            "page_number": item["page_number"]
        })

    # === Save JSON File ===
    out_path = os.path.join(OUTPUT_FOLDER, filename.replace(".pdf", ".json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4, ensure_ascii=False)

    print(f"✅ Processed: {filename} -> {out_path}")
