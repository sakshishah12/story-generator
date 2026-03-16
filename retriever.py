import json
import os
from collections import defaultdict
import numpy as np

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever

# ------------------------------------------------
# EMBEDDING MODEL
# ------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

with open("ramayana_verses_with_scene.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total verses:", len(data))

# ------------------------------------------------
# BUILD CHUNK DOCUMENTS
# ------------------------------------------------

docs = []

for item in data:

    docs.append(
        Document(
            page_content=f"""
Book: {item['kanda_name']}
Theme: {item['theme']}
Characters: {item['characters']}

Text:
{item['verse']}
""",
            metadata={
                "chunk_id": item["id"],
                "scene_id": item["scene_id"],
                "kanda": item["kanda_name"],
                "canto": item["canto"],
                "theme": item["theme"],
                "characters": item["characters"]
            }
        )
    )

# ------------------------------------------------
# BUILD / LOAD CHUNK FAISS INDEX
# ------------------------------------------------

if not os.path.exists("ramayana_index"):

    print("Creating chunk FAISS index...")

    chunk_store = FAISS.from_documents(docs, embeddings)
    chunk_store.save_local("ramayana_index")

else:

    print("Loading chunk FAISS index...")

    chunk_store = FAISS.load_local(
        "ramayana_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

# ------------------------------------------------
# BUILD SCENE DATA
# ------------------------------------------------

scenes_by_canto = defaultdict(list)

for item in data:

    key = f"{item['kanda_name']}_{item['canto']}"
    scenes_by_canto[key].append(item)

scene_list = []

for i, (canto, items) in enumerate(scenes_by_canto.items()):

    scene_text = " ".join([x["verse"] for x in items])

    scene_list.append({
        "scene_id": i,
        "canto": canto,
        "text": scene_text
    })

print("Total scenes:", len(scene_list))

# ------------------------------------------------
# FAST SCENE LOOKUP
# ------------------------------------------------

scene_lookup = {}

for item in data:
    sid = item["scene_id"]
    if sid not in scene_lookup:
        scene_lookup[sid] = item

# ------------------------------------------------
# BUILD SCENE DOCUMENTS
# ------------------------------------------------

scene_docs = []

for scene in scene_list:

    first_chunk = scene_lookup.get(scene["scene_id"], {})

    kanda = first_chunk.get("kanda_name", "Unknown")
    theme = first_chunk.get("theme", "Unknown")

    characters_list = first_chunk.get("characters") or []
    characters = ", ".join(characters_list)

    scene_description = f"""
Book: {kanda}
Canto: {scene['canto']}
Theme: {theme}
Characters: {characters}

Scene:
{scene['text']}
"""

    scene_docs.append(
        Document(
            page_content=scene_description,
            metadata={
                "scene_id": scene["scene_id"],
                "canto": scene["canto"],
                "kanda": kanda,
                "theme": theme,
                "characters": characters_list
            }
        )
    )

# ------------------------------------------------
# BUILD / LOAD SCENE FAISS INDEX
# ------------------------------------------------

if not os.path.exists("ramayana_scene_index"):

    print("Creating scene FAISS index...")

    scene_store = FAISS.from_documents(scene_docs, embeddings)
    scene_store.save_local("ramayana_scene_index")

else:

    print("Loading scene FAISS index...")

    scene_store = FAISS.load_local(
        "ramayana_scene_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

# ------------------------------------------------
# BM25 RETRIEVER (SCENES)
# ------------------------------------------------

bm25 = BM25Retriever.from_documents(docs)
bm25.k = 20

# ------------------------------------------------
# VECTOR RETRIEVER (MMR)
# ------------------------------------------------

vector_retriever = scene_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 10,
        "fetch_k": 30
    }
)

# ------------------------------------------------
# QUERY EXPANSION
# ------------------------------------------------

def expand_query(query):

    return [
        query,
        f"Ramayana event where {query}",
        f"scene in Ramayana where {query}",
        f"story describing {query}",
        f"episode involving {query}"
    ]

# ------------------------------------------------
# REMOVE DUPLICATE SCENES
# ------------------------------------------------

def unique_scene_results(docs):

    seen = set()
    results = []

    for doc in docs:

        sid = doc.metadata["scene_id"]

        if sid not in seen:
            results.append(doc)
            seen.add(sid)

    return results

# RERANK

def rerank(query, docs):

    qvec = embeddings.embed_query("query: " + query)

    scored = []

    for doc in docs:

        dvec = embeddings.embed_query(doc.page_content)

        score = np.dot(qvec,dvec)/(np.linalg.norm(qvec)*np.linalg.norm(dvec))

        scored.append((score,doc))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [doc for score,doc in scored]

# deduplicate 
def deduplicate_docs(docs):

    seen=set()
    clean=[]

    for doc in docs:

        cid = doc.metadata.get("chunk_id")

        if cid not in seen:
            clean.append(doc)
            seen.add(cid)

    return clean
# ------------------------------------------------
# HYBRID RETRIEVAL
# ------------------------------------------------

def hybrid_retrieval(query):

    queries = expand_query(query)

    bm25_docs = []
    vector_docs = []

    for q in queries:
        bm25_docs += bm25.invoke(q)
        vector_docs += chunk_store.similarity_search(q, k=10)

    combined = bm25_docs + vector_docs

    combined = rerank(query, combined)

    combined = deduplicate_docs(combined)
    combined = unique_scene_results(combined)

    return combined[:8]

# ------------------------------------------------
# TEST QUERY
# ------------------------------------------------

# query = "when Rama breaks Shiva bow"

# results = hybrid_retrieval(query)

# print("\nTop Scenes:\n")
