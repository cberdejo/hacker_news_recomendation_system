from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from collections import Counter

from recommender import (
    spacy_preprocessor,
    ensure_spacy_model,
    is_collection_empty,
    create_qdrant_colletion_if_needed,
    store_news_in_qdrant,
    get_recomendations,
)
from scraper import scrap_from_algolia


def main():
    qdrant = QdrantClient(path="./data")

    nlp = ensure_spacy_model("en_core_web_sm")

    collection_name = "recom"
    model = SentenceTransformer(
        "sentence-transformers/average_word_embeddings_komninos"
    )

    if is_collection_empty(qdrant, collection_name):
        titles = scrap_from_algolia()
        keywords = [
            spacy_preprocessor(doc) for doc in nlp.pipe(titles, disable=["ner"])
        ]

        size_encoding = len(model.encode(["test"])[0])
        print("embedding size: ", size_encoding)  # 300

        create_qdrant_colletion_if_needed(qdrant, collection_name, size_encoding)

        vectors = model.encode(titles).tolist()

        store_news_in_qdrant(qdrant, collection_name, vectors, keywords, titles)

    # Lets imagine and simulate a user's keywords that should be inferred through history search
    user_history_search = [
        "Show HN: You can't trust ChatGPT's math skills (here's proof)",
        "Ask HN: How do you manage bookmarks and saved links?",
        "Nokia announces return of iconic 3210 phone",
        "Show HN: I built a text-based RPG game engine in Python",
        "Ask HN: What's your tech stack in 2024?",
        "Show HN: A browser extension to block cookie popups",
        "Why Git is hard and what we can do about it",
        "Faster Python through lazy imports",
        "Ask HN: What are you currently learning?",
        "The story behind SQLite",
        "Show HN: Build your own search engine with Rust",
        "Ask HN: What are the best books on software architecture?",
        "The evolution of the UNIX terminal",
        "A new approach to JavaScript frameworks",
        "Show HN: I made a Markdown editor for minimalists",
        "Why I switched from VS Code to Neovim",
        "Ask HN: How do you keep up with tech news?",
        "The cost of running a side project in the cloud",
        "What happens when you delete a GitHub repo",
        "Show HN: Visualizing code complexity in real time",
    ]

    user_keywords = [
        kw
        for doc in nlp.pipe(user_history_search, disable=["ner"])
        for kw in spacy_preprocessor(doc)
    ]

    keyword_counts = Counter(user_keywords)
    top_keywords = [kw for kw, _ in keyword_counts.most_common(4)]

    print("Top words to describe user: ", top_keywords)

    user_embedding = model.encode(user_history_search).mean(axis=0).tolist()  # mean

    recomendations = get_recomendations(
        qdrant, collection_name, user_embedding, top_keywords
    )

    # Here recomendations could be saved
    print(recomendations)


if __name__ == "__main__":
    main()
