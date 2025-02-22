# Biomedical Knowledge Base - SPARQL Query Interface

This project provides a **web-based interface** for querying a **biomedical knowledge base** using **SPARQL**. The system dynamically builds SPARQL queries based on user-provided keywords and fetches relevant biomedical articles.

## **1. Prerequisites**
Ensure you have the following installed:
- Python 3.8+
- Apache Jena Fuseki (SPARQL server)
- Required Python packages

## **2. Setting Up the SPARQL Server (Apache Jena Fuseki)**

### **Step 1: Download and Install Fuseki**
1. Download **Apache Jena Fuseki** from [Apache Jena](https://jena.apache.org/download/index.cgi).
2. Extract the downloaded **`apache-jena-fuseki-*.zip`** file.
3. Open a terminal/command prompt and navigate to the extracted folder.

### **Step 2: Start the Fuseki Server**
Run the following command inside the Fuseki folder:
```bash
./fuseki-server --update --mem /dataset
```
- `--update`: Enables updates via SPARQL.
- `--mem`: Runs Fuseki in-memory (for testing).
- `/dataset`: The dataset endpoint (SPARQL queries will use `http://localhost:3030/dataset/sparql`).

### **Step 2: Download Data from PubMed**
Run `python ontologizePubMedData.py` to parse pubmed for data, and create a turtle file from this.
- Ensure that you replace your `NCBI email`, as well as configure the `search terms of interest` and `max responses` count.

### **Step 3: Load the Biomedical Ontology Data**
1. Open your browser and go to **`http://localhost:3030/`**.
2. Click **"Manage datasets"** → **"Add new dataset"**.
3. Name it `dataset` and select **Persistent** (optional).
4. Upload the **biomedical ontology TTL file** (`biomedical_ontology.ttl`).
5. Click **"Upload"** to store it in Fuseki.

### **Step 4: Verify the Data**
Run this query in the **Fuseki Query Panel**:
```sparql
PREFIX biomed: <http://example.org/biomedical#>
SELECT ?s ?p ?o WHERE {
    ?s ?p ?o .
} LIMIT 10
```
If data appears, the server is correctly configured!

## **3. Setting Up the Web Interface**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/kevin-411/biomedical-sparql-ui.git
cd biomedical-sparql-ui
```

### **Step 2: Install Python Dependencies**
```bash
pip install flask SPARQLWrapper
```

### **Step 3: Run the Flask Server**
```bash
python app.py
```
If successful, you should see:
```
Running on http://127.0.0.1:5000/
```

### **Step 4: Access the Web Interface**
1. Open your browser and go to: **`http://127.0.0.1:5000/`**.
2. Enter a **keyword** (e.g., `diabetes`) and click **"Search"**.
3. The system dynamically builds a SPARQL query and retrieves results.

## **4. Troubleshooting**

### **Issue: No Results Found?**
1. Ensure **biomedical_ontology.ttl** contains data:
   ```bash
   cat biomedical_ontology.ttl
   ```
2. Run a basic query in Fuseki to check if data exists:
   ```sparql
   SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10
   ```

### **Issue: Fuseki Server Not Starting?**
- Ensure **Java 8+** is installed (`java -version`).
- Run with `--debug` for more details:
  ```bash
  ./fuseki-server --debug --mem /dataset
  ```

## **5. Summary**
✅ **Apache Jena Fuseki** as the SPARQL server.  
✅ **Flask** serves the web interface.  
✅ **User-friendly keyword-based search**.  
✅ **Dynamic SPARQL queries to fetch biomedical articles**.  


