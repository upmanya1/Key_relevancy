Here's a comprehensive README.md file for your project:

```markdown
# Keyword Relevance Analyzer 🔍📊

A sophisticated tool for analyzing keyword clusters against website content using semantic clustering, statistical analysis, and large language models (LLMs).

## Features 🌟

- **Automated Website Crawling**  
  - Intelligent URL discovery with duplicate detection
  - Content cleaning and text normalization
  - Polite crawling with rate limiting
  - Image URL filtering and fragment skipping

- **Semantic Keyword Clustering**  
  - State-of-the-art sentence embeddings (Sentence-BERT)
  - Hierarchical clustering with adjustable thresholds
  - PCA visualization of keyword clusters
  - Automatic deduplication and normalization

- **Multi-Metric Analysis**  
  - TF-IDF scoring with custom vectorizer
  - BM25 ranking implementation
  - Google Gemini LLM integration
  - Combined statistical + semantic analysis

- **Enterprise-Ready Architecture**  
  - Modular component design
  - Configurable parameters
  - Progress tracking and logging
  - Rate limiting for API safety
  - Comprehensive error handling

## Workflow Diagram 📌

```
[Input CSV] → Keyword Clustering → Website Crawling → Multi-Metric Analysis → [Output Reports]
            (Semantic Grouping)    (Content Harvesting)  (TF-IDF/BM25/LLM)   (CSV Format)
```

## Installation 💻

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/keyword-analyzer.git
cd keyword-analyzer
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Setup**
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

## Usage 🚀

**Basic Command**
```bash
python main.py --input keywords.csv --clusters clusters_output.csv --report analysis_report.csv
```

**Arguments**
| Flag | Description | Default |
|------|-------------|---------|
| `--input` | Input CSV file with keywords | Required |
| `--clusters` | Output file for clusters | clusters.csv |
| `--report` | Output file for analysis | report.csv |
| `--url` | Website URL to analyze | Config value |

**Input CSV Format**
```csv
keyword
"real estate investment"
"property management services"
"commercial real estate"
...
```

## Configuration ⚙️ (`config.py`)

```python
# Crawling
CRAWL_URL = "https://www.example.com"  # Target website
MAX_CRAWL_PAGES = 100                  # Safety limit
USER_AGENT = "Research Bot/1.0"        # Crawler identity

# Clustering
CLUSTERING_DISTANCE_THRESHOLD = 0.4    # Lower = more clusters
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # Sentence-BERT model

# LLM Analysis
LLM_MODEL_NAME = "gemini-2.0-flash-thinking-exp-01-21"
LLM_TEMPERATURE = 1.0                  # 0-2 (creativity control)
```

## Outputs 📂

1. **Clusters CSV**
```csv
cluster_id,keywords
0,"property investment; real estate portfolio;..."
1,"tenant screening; lease agreements;..."
```

2. **Analysis Report**
```csv
cluster_id,keywords,avg_tfidf,avg_bm25,llm_analysis
0,"property investment...",0.452,12.34,"The cluster shows strong alignment with..."
1,"tenant screening...",0.289,8.91,"These operational keywords..."
```

## Example Report 📝

**Cluster Analysis**
```
Cluster 42 (12 keywords)
---------------------------------
TF-IDF Score: 0.672 | BM25 Score: 15.23

LLM Analysis:
"The 'commercial leasing' cluster demonstrates excellent relevance to the website's 
focus on corporate real estate solutions. The high BM25 scores indicate strong 
term frequency patterns in the crawled content. Recommended actions:
1. Prioritize these keywords in SEO metadata
2. Develop dedicated service page for commercial leasing
3. Create case studies highlighting industrial property success stories"
```

## Troubleshooting 🛠️

**Common Issues**
1. **Missing API Key**  
   Ensure `.env` file exists with valid `GOOGLE_API_KEY`

2. **CSV Format Errors**  
   Verify input CSV has exactly one "keyword" column

3. **Crawling Limitations**  
   - Check robots.txt restrictions
   - Increase timeout in config.py for slow websites
   - Verify network connectivity

4. **LLM Rate Limits**  
   - Implement exponential backoff
   - Reduce batch sizes
   - Monitor API usage dashboard

## Dependencies 📦

- Core: `pandas`, `numpy`, `requests`
- NLP: `sentence-transformers`, `rank_bm25`, `scikit-learn`
- LLM: `google-generativeai`, `langchain_google_genai`
- Utils: `tqdm`, `beautifulsoup4`, `python-dotenv`

## Contributing 🤝

1. Fork repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push branch (`git push origin feature/improvement`)
5. Open Pull Request

## License 📄

MIT License - See [LICENSE](LICENSE) for details

---

**Project Roadmap**  
✅ Core analysis pipeline  
✅ Website crawler  
✅ Cluster visualization  
🔜 Multi-LLM support  
🔜 Automatic report generation (PDF/HTML)  
🔜 REST API interface
```

This README provides:
1. Comprehensive feature overview
2. Clear installation/usage instructions
3. Configuration documentation
4. Example inputs/outputs
5. Troubleshooting guide
6. Contribution guidelines
7. Future development roadmap

The structure is optimized for both technical users and project stakeholders, balancing implementation details with high-level functionality overview.