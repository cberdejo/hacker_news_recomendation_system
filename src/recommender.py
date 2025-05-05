import spacy
from spacy.cli import download
import importlib.util


from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)


def ensure_spacy_model(model_name: str):
    if importlib.util.find_spec(model_name) is None:
        print(f"Downloading the spaCy model '{model_name}'...")
        download(model_name)
    else:
        print(f"Model spaCy '{model_name}' available.")

    return spacy.load("en_core_web_sm")


def spacy_preprocessor(doc) -> list[str]:
    """
    Preprocesa un documento spaCy extrayendo solo los lemas de sustantivos,
    en minúsculas, sin dígitos, sin puntuación y sin stopwords.
    """
    return [
        token.lemma_.lower()
        for token in doc
        if token.pos_ == "NOUN"
        and not token.is_digit
        and not token.is_stop
        and not token.is_punct
    ]


def create_qdrant_colletion_if_needed(
    qdrant: QdrantClient, name: str, size: int, distante=Distance.COSINE
):
    """
    Ensures that a Qdrant collection with the specified name exists. If the collection
    does not exist, it creates a new one with the given configuration.
    Args:
        qdrant (QdrantClient): The Qdrant client instance used to interact with the Qdrant service.
        name (str): The name of the collection to check or create.
        size (int): The dimensionality of the vectors to be stored in the collection.
        distante (Distance, optional): The distance metric to be used for vector similarity.
            Defaults to Distance.COSINE.
    Returns:
        None
    """
    if not qdrant.collection_exists(name):
        qdrant.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )


def is_collection_empty(qdrant: QdrantClient, name: str) -> bool:
    """
    Checks if a specified collection in the Qdrant database is empty.
    Args:
        qdrant (QdrantClient): An instance of the Qdrant client used to interact with the database.
        name (str): The name of the collection to check.
    Returns:
        bool: True if the collection is empty or does not exist, False otherwise.

    """
    try:
        res = qdrant.scroll(collection_name=name, limit=1)
        return len(res[0]) == 0
    except:
        return True


def store_news_in_qdrant(
    qdrant: QdrantClient,
    name: str,
    vectors: list[list[float]],
    keywords: list[list[str]],
    titles: list[str],
):
    """
    Stores news data in a Qdrant collection by upserting points with associated vectors and keywords.
    Args:
        qdrant (QdrantClient): The Qdrant client instance used to interact with the Qdrant database.
        name (str): The name of the Qdrant collection where the data will be stored.
        vectors (list[list[float]]): A list of vectors representing the news data.
        keywords (list[list[str]]): A list of lists containing keywords associated with each vector.
    Returns:
        None

    """
    qdrant.upsert(
        collection_name=name,
        points=[
            PointStruct(
                id=i,
                vector=vectors[i],
                payload={"keywords": keywords[i], "titles": titles[i]},
            )
            for i in range(len(vectors))
        ],
    )


def get_recomendations(
    qdrant: QdrantClient,
    collection_name: str,
    user_embedding: list[float],
    top_keywords: list[str],
    limit: int = 5,
):
    """
    Retrieves recomendations from a Qdrant collection based on a user's embedding and top keywords.
    Args:
        qdrant (QdrantClient): The Qdrant client instance used to interact with the Qdrant database.
        collection_name (str): The name of the Qdrant collection to query.
        user_embedding (list[float]): The user's embedding vector for similarity comparison.
        top_keywords (list[str]): A list of keywords to filter the recomendations.
        limit (int, optional): The maximum number of recomendations to retrieve. Defaults to 5.
    Returns:
        list: A list of recommended articles with their scores and keywords.
    """
    filters = Filter(
        should=[
            FieldCondition(key="keywords", match=MatchValue(value=kw))
            for kw in top_keywords
        ]
    )

    results = qdrant.query_points(
        collection_name=collection_name,
        query=user_embedding,
        limit=limit,
        query_filter=filters,
    )

    return results
