# 📘 TP3 – Web Indexation: Search Engine

**ENSAI – 2025**



## 1. Scope of the Project

This project focuses **exclusively on the search and ranking component** of a web indexing system.

The crawling and index construction phases were implemented in a previous assignment and are therefore **out of scope** for this project.
All indexes are **precomputed and provided as input** in JSON format.

The objective is to exploit these indexes in order to:

* process user queries,
* filter relevant documents,
* rank them using multiple relevance signals,
* and return structured search results.



## 2. Inputs

### 2.1 Precomputed Indexes

The following indexes are loaded from the `input/` directory:

* `title_index.json`
* `description_index.json`
* `brand_index.json`
* `origin_index.json`
* `reviews_index.json`

No index construction is performed in this project.



### 2.2 Document Corpus

The file `products_enriched.jsonl` contains the document corpus.
Each line represents one document with at least:

* `url`
* `title`
* `description`

Optional fields include:

* `product_features` (brand, origin, material)
* `product_reviews`

Each **product variant URL is treated as an independent document**, which simplifies indexing and ranking.



## 3. Query Processing

Query processing is implemented in `tokenization.py` and includes the following steps:

### 3.1 Tokenization

* spaCy-based tokenization
* Lemmatization applied
* Only alphabetic tokens are kept

### 3.2 Normalization

* Lowercasing
* Removal of punctuation and non-alphabetic tokens

### 3.3 Stopwords Removal

* Stopwords are removed using the **NLTK English stopword list**, as required by the assignment.

### 3.4 Query Expansion (Synonyms)

* Query expansion is applied only to **product origin**
* Synonyms are loaded from `origin_synonyms.json`

Example:

```
"made in Unites States of Africa" → "usa"
```

This improves recall for origin-related queries without introducing excessive noise.



## 4. Document Filtering

Document filtering is applied **before ranking** to reduce the search space.

Two strategies are implemented in `filtering.py`:

### 4.1 AND Filtering (Strict)

* A document must contain **all query tokens**, except stopwords.

### 4.2 OR Filtering (Fallback)

* Applied if AND filtering returns no documents.
* A document is kept if it contains **at least one query token**.

Filtering is performed on the **title index**, as titles are highly discriminative.



## 5. Analysis of Available Signals

Before designing the ranking function, the available data was analyzed to identify relevant relevance signals.

### Textual Content

Each document contains a title and a description.

* Titles are short and highly descriptive.
* Descriptions provide additional context.

**Decision:**
Both fields are used, with a higher weight assigned to title matches.



### Token Frequency

Inverted indexes provide term frequency and document frequency information.

**Decision:**
Token frequency is exploited through the BM25 ranking function.



### Positional Information

The positional index provides token positions within documents.

**Decision:**
Tokens appearing early in a document are considered more informative and receive a small ranking boost.



### Structured Features

Some documents contain structured attributes such as:

* brand
* origin
* material

**Decision:**
Brand and origin are indexed separately and used as ranking signals.


### User Reviews

Review data includes:

* average rating
* number of reviews

**Decision:**
Reviews are used as secondary ranking signals to promote higher-quality products.



### Signals Not Used

Other potential signals (e.g. price, availability) were not available in the dataset and were therefore not considered.



## 6. Ranking Strategy

Ranking is implemented in `scoring.py` using a **linear combination of multiple relevance signals**.

### Signals Used

* BM25 score on title
* BM25 score on description
* Exact phrase match using positional information
* Token position signal
* Brand and origin matching
* Review-based signals (average rating and number of reviews)

A linear scoring function was chosen for its interpretability and ease of tuning.



## 7. Search Pipeline

The complete search pipeline implemented in `search.py` consists of:

1. Query processing
2. Document filtering (AND / OR)
3. Scoring of candidate documents
4. Ranking by descending score

The `search()` function returns a list of `(url, score)` pairs.



## 8. Output Format (Deliverable)

Search results are formatted in JSON in `main.py`.

### Output Structure

```json
{
  "query": "warm winter beanie made in usa",
  "total_documents": 120,
  "filtered_documents": 18,
  "results": [
    {
      "title": "Cat-Ear Beanie",
      "url": "https://web-scraping.dev/product/24",
      "description": "...",
      "score": 20.19
    }
  ]
}
```

### Metadata

* `total_documents`: total number of indexed documents
* `filtered_documents`: number of documents retained after filtering



## 9. Testing & Optimization

The system was tested using a variety of queries, including:

* short queries (e.g. `"beanie"`)
* descriptive queries (e.g. `"warm winter beanie"`)
* attribute-based queries (e.g. `"beanie made in usa"`)
* color-based queries (e.g. `"pink beanie"`)

Observations from these tests guided the adjustment of feature weights in the ranking function.



## 10. Design Choices and Their Impact

### Query Expansion

Synonym-based expansion was restricted to product origin.

**Impact:**
Improved recall for origin-related queries without query drift.



### Filtering Strategy

AND filtering is applied first, followed by OR filtering as a fallback.

**Impact:**
Ensures high precision while avoiding empty result sets.



### Field Weighting

Title matches are weighted more heavily than description matches.

**Impact:**
Documents whose titles match the query are consistently ranked higher.



### Reviews as a Signal

User reviews are incorporated into ranking.

**Impact:**
Promotes products with higher user satisfaction.



### Treatment of Product Variants

Each product variant is treated as an independent document.

**Impact:**
Simplifies ranking but may result in multiple similar results.
Grouping variants was identified as a possible improvement.



## 11. Methodological Approach and Practical Considerations

### Iterative Development

The system was developed incrementally, starting from a simple textual ranking and progressively integrating additional signals.



### Long Queries

Long queries are handled implicitly through token-based processing and BM25 scoring.
Strict AND filtering may become too restrictive for long queries, which is mitigated by the OR-based fallback strategy.



### Rare Terms

Rare terms are handled naturally through BM25’s inverse document frequency component.



### Robustness

Fallback strategies ensure that the system always returns results, even for complex or noisy queries.


## 12. How to Run

### Requirements

* Python 3.8+
* `spacy`
* `nltk`

Make sure NLTK stopwords are downloaded:

```python
import nltk
nltk.download("stopwords")
```

### Run the search engine

```bash
python main.py
```

Results are saved to:

```
output/search_results_all_queries.json
```


## 13. Conclusion

This project implements a **complete, modular, and interpretable search engine pipeline** using precomputed indexes.
It demonstrates the practical application of Information Retrieval concepts such as query processing, filtering, ranking, and evaluation, while remaining aligned with the constraints and objectives of the assignment.

