## 1. Project Objective

The objective of this project is to **build several types of indexes** from an e-commerce product dataset in order to **prepare the construction of a search engine**.

This project focuses **only on indexing**.
Web crawling is **out of scope** and handled in a separate project.



## 2. Input Data

The input is a **JSON Lines (`.jsonl`) file** containing **150 product documents**, one document per line.

Each document contains:

* `url`
* `title`
* `description`
* `product_features`
* `product_reviews`
* `links`

Example:

```json
{
  "url": "https://web-scraping.dev/product/10?variant=red-5",
  "title": "Cat-Ear Beanie",
  "description": "Add a touch of whimsy to your winter wardrobe...",
  "product_features": {
    "brand": "CatCozies",
    "made in": "USA",
    "material": "Acrylic"
  },
  "product_reviews": [
    {"rating": 4},
    {"rating": 5}
  ]
}
```



## 3. Implemented Functionalities and Index Structures

### 3.1 URL Processing

**What is done**

* The JSONL file is parsed line by line.
* From each URL:

  * the **product ID** is extracted (number after `/product/`)
  * the **variant** is extracted if present in query parameters.

**Output (enriched document)**

```json
{
  "url": "https://web-scraping.dev/product/10?variant=red-5",
  "product_id": "10",
  "variant": "red-5",
  "title": "...",
  "description": "..."
}
```

This step ensures that product identification is **explicit and structured**.



### 3.2 Inverted Index — Title

**What is done**

* Tokenization by whitespace
* Removal of stopwords
* Removal of punctuation
* Lowercasing

**Index structure (Python dictionary)**

```json
{
  "cat": [
    "https://web-scraping.dev/product/10",
    "https://web-scraping.dev/product/14"
  ],
  "beanie": [
    "https://web-scraping.dev/product/10"
  ]
}
```

Each token is associated with the **list of document URLs** in which it appears.



### 3.3 Inverted Index — Description

The same indexing strategy is applied to the `description` field.

**Example output**

```json
{
  "winter": [
    "https://web-scraping.dev/product/10",
    "https://web-scraping.dev/product/17"
  ],
  "warm": [
    "https://web-scraping.dev/product/12"
  ]
}
```

This index captures **richer textual information** than titles alone.



### 3.4 Positional Index — Title and Description

**What is done**

* For both `title` and `description`, an index is created that stores:

  * the document URL
  * the positions of each token in the text

**Index structure**

```json
{
  "sweet": {
    "https://web-scraping.dev/product/1": [1, 21],
    "https://web-scraping.dev/product/13": [1, 21]
  }
}
```

Token positions correspond to **token order after preprocessing**.

This index enables:

* phrase search
* proximity search



### 3.5 Reviews Index (Non-Inverted)

**What is done**
For each product:

* count total reviews
* compute average rating
* extract last rating

**Index structure**

```json
{
  "https://web-scraping.dev/product/12": {
    "total_reviews": 10,
    "mean_mark": 4.5,
    "last_rating": 5
  }
}
```

This index is **not inverted**, as required by the instructions, and is intended for **ranking purposes**.



### 3.6 Feature Indexes (Brand, Origin, Material)

Features are treated as **textual fields**.

A **separate inverted index is built for each feature**.

#### Brand index

```json
{
  "catcozies": [
    "https://web-scraping.dev/product/10",
    "https://web-scraping.dev/product/14"
  ]
}
```

#### Origin index (`made in`)

```json
{
  "usa": [
    "https://web-scraping.dev/product/10",
    "https://web-scraping.dev/product/17"
  ]
}
```

#### Material index (bonus feature)

```json
{
  "acrylic": [
    "https://web-scraping.dev/product/10",
    "https://web-scraping.dev/product/21"
  ]
}
```

**Bonus feature implemented**: `material`
(as allowed by the assignment instructions).



## 4. Index Persistence

Each index is saved into a **separate JSON file**, as required.

```text
indexes/
├── title_index.json
├── description_index.json
├── review_index.json
├── brand_index.json
├── made_in.json
```



## 5. How to Run the Project

### Requirements

* Python 3.8+
* spaCy English model

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Execution

```bash
python main.py
```

### Example usage inside `main.py`

```python
from indexer import Indexer
from utils import load_corpus

corpus = load_corpus("../input/products_enriched.jsonl")

indexer = Indexer(corpus)
indexer.build_text_indexes()
indexer.build_feature_index("brand")
indexer.build_feature_index("made in")
indexer.build_review_index()
indexer.save_indexes()
```


## 6. Design Choices

* **Python dictionaries** are used for all indexes to ensure:

  * simplicity
  * direct JSON serialization
* Each function performs **one single action**, in accordance with the programming guidelines.
* Indexing logic is encapsulated in a dedicated `Indexer` class for clarity and maintainability.



## 7. Conclusion

This project implements all the indexing mechanisms required by the assignment:

* inverted indexes (title, description),
* positional indexes,
* feature-based indexes,
* review index.

The produced indexes are **explicit, verifiable, and ready to be used** in a search engine ranking and querying stage.

