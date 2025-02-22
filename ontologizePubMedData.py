from Bio import Entrez
from rdflib import Graph, URIRef, Literal, Namespace, RDF

# Set up your email (NCBI requires this)
Entrez.email = "<NCBI email address here>"
search_term = 'Diabetes'
max_results_count = 10

def fetch_pubmed_articles(query, max_results=5):
    """
    Fetch articles from PubMed based on a search query.
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    article_ids = record["IdList"]

    articles = []
    for article_id in article_ids:
        summary_handle = Entrez.esummary(db="pubmed", id=article_id)
        summary = Entrez.read(summary_handle)
        # article = summary["DocumentSummarySet"]["DocumentSummary"][0]
        # article = summary[article_ids.index(article_id)]
        article = summary[0]
        articles.append({
            "id": article_id,
            "title": article["Title"],
            "journal": article.get("Source", "Unknown Journal"),
            "pub_date": article.get("PubDate", "Unknown Date"),
            "authors": [author for author in article.get("AuthorList", [])],
        })

    return articles


# Example: Fetch diabetes-related articles
articles = fetch_pubmed_articles(search_term, max_results=max_results_count)
print(articles)
# from rdflib import Graph, URIRef, Literal, Namespace, RDF

# Define the ontology namespace
BIOMED = Namespace("http://example.org/biomedical#")

# Create a new RDF graph
g = Graph()

# Bind the namespace
g.bind("biomed", BIOMED)


def add_article_to_graph(article):
    """
    Adds a PubMed article and its metadata to the RDF graph.
    """
    article_uri = URIRef(BIOMED + "Article_" + article["id"])

    # Add Article instance
    g.add((article_uri, RDF.type, BIOMED.Article))
    g.add((article_uri, BIOMED.hasTitle, Literal(article["title"])))
    g.add((article_uri, BIOMED.hasPublicationDate, Literal(article["pub_date"])))

    # Add Journal instance
    journal_uri = URIRef(BIOMED + "Journal_" + article["journal"].replace(" ", "_"))
    g.add((journal_uri, RDF.type, BIOMED.Journal))
    g.add((article_uri, BIOMED.publishedIn, journal_uri))

    # Add Authors
    for author in article["authors"]:
        author_uri = URIRef(BIOMED + "Author_" + author.replace(" ", "_"))
        g.add((author_uri, RDF.type, BIOMED.Author))
        g.add((article_uri, BIOMED.hasAuthor, author_uri))


# Add articles to the RDF graph
for article in articles:
    add_article_to_graph(article)

# Save the graph as a Turtle file
ttl_filename = "biomedical_ontology.ttl"
g.serialize(destination=ttl_filename, format="turtle")

print(f"Ontology saved as {ttl_filename}")
