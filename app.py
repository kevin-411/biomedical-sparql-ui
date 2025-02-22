from flask import Flask, request, jsonify, render_template
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

# Set up SPARQL endpoint (Change if using another triple store)
SPARQL_ENDPOINT = "http://localhost:3030/dataset/sparql"
sparql = SPARQLWrapper(SPARQL_ENDPOINT)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query_ontology():
    keyword = request.json.get("keyword")  # Get user keyword

    # Build SPARQL query
    sparql_query = f"""
    PREFIX biomed: <http://example.org/biomedical#>
    SELECT ?article ?title ?journal WHERE {{
        ?article a biomed:Article .
        ?article biomed:hasTitle ?title .
        ?article biomed:publishedIn ?journal .
        FILTER (CONTAINS(LCASE(?title), LCASE("{keyword}")))
    }}
    """

    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        return jsonify(results["results"]["bindings"])
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
