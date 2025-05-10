from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from langchain.schema import HumanMessage
from tqdm import tqdm
from config import LLM_MODEL_NAME, LLM_TEMPERATURE, GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
import time 
import pandas as pd
class ContentAnalyzer:
    def __init__(self, crawler):
        self.crawler = crawler
        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL_NAME,
            temperature=LLM_TEMPERATURE,
            google_api_key=GOOGLE_API_KEY
        )
        self.tfidf = TfidfVectorizer(stop_words='english').fit(crawler.full_corpus)
        self.bm25 = BM25Okapi([doc.split() for doc in crawler.full_corpus])

    def analyze_cluster(self, keywords):
        tfidf_scores = []
        bm25_scores = []
        
        for kw in keywords:
            try:
                tfidf_scores.append(self.tfidf.transform([kw]).mean())
            except ValueError:
                tfidf_scores.append(0)
                
            bm25_scores.append(self.bm25.get_scores(kw.split()).mean())
        
        prompt = f"""Analyze keyword relevance to website content:
        Keywords: {", ".join(keywords)}
        Content Sample: {" ".join(self.crawler.full_corpus)[:50000]}"""
        
        analysis = self.llm.invoke([HumanMessage(content=prompt)]).content
        
        return {
            'avg_tfidf': np.mean(tfidf_scores),
            'avg_bm25': np.mean(bm25_scores),
            'llm_analysis': analysis
        }

def generate_report(cluster_df, crawler, output_path):
    analyzer = ContentAnalyzer(crawler)
    results = []
    
    for _, row in tqdm(cluster_df.iterrows(), total=len(cluster_df), desc="Analyzing clusters"):
        keywords = row['keyword'].split('; ')
        analysis = analyzer.analyze_cluster(keywords)
        results.append({
            'cluster_id': row['cluster_id'],
            'keyword': ', '.join(keywords),
            **analysis
        })
        time.sleep(1)  # Rate limiting
        
    report_df = pd.DataFrame(results)
    report_df.to_csv(output_path, index=False)
    return report_df