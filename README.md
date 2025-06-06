# SDM Lab 2 - Knowledge Graphs

This repository contains the solutions and resources developed for **Lab Assignment 2**. 
The lab focuses on hands-on work with **knowledge graphs**, involving RDF schema modeling, data transformation using RDFLib, 
and semantic querying using SPARQL in **GraphDB**.

---

## 🧠 Project Overview

The main objectives of this lab were:

- Design and implement an ontology (TBOX) for the research publication domain.
- Create an instance dataset (ABOX) using RDFLib based on structured data.
- Use reasoning and inference in GraphDB to enhance semantic querying.

## ⚙️ Setup Instructions

1. **Install GraphDB**  
   Download and install GraphDB Free:  
   👉 [https://www.ontotext.com/products/graphdb/graphdb-free/](https://www.ontotext.com/products/graphdb/graphdb-free/)

2. **Start GraphDB**  
   Launch the application and access [http://localhost:7200/](http://localhost:7200/)

3. **Create a Repository**  
   - Go to `Setup > Repositories > Create new repository`
   - Use ruleset: `RDFS (Optimized)`
   - Enable autocomplete in `Setup > Autocomplete`

4. **Import RDF Data**  
   Load the TBOX and ABOX files into the GraphDB repository via the `Import > RDF` tab:

5. **Run Queries**  
   Go to the `SPARQL` tab and run the provided queries in the `assets/` directory.
