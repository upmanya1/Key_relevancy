#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

# Build LLMChain with identical notebook prompt
SYSTEM_PROMPT = ("Analyze these keywords for relevance given the website content:\n"  
                 "Keywords: {Keywords}\n"  
                 "Website Excerpt: {excerpt}\n"  
                 "For each keyword, return a line: keyword,score (0.0-1.0),one-sentence insight.")


def build_llm_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "")
    ])
    return LLMChain(llm=llm, prompt=prompt, memory=ConversationBufferMemory(memory_key="chat_history"))


def analyze_clusters(cluster_csv, crawled_csv, api_key, domain, out_file='keyword_analysis.csv'):
    df_clusters = pd.read_csv(cluster_csv)
    df_crawl = pd.read_csv(crawled_csv)

    # Prepare corpus excerpt
    excerpt = " ".join(df_crawl['Page Text'].tolist())[:5000]

    # Scoring models
    corpus = df_clusters['Keyword'].tolist()
    tfidf = TfidfVectorizer().fit(corpus)
    bm25 = BM25Okapi([doc.split() for doc in corpus])

    # LLM setup
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21", api_key=api_key)
    chain = build_llm_chain(llm)

    records = []
    for cid, group in df_clusters.groupby('cluster_id'):
        kws = group['Keyword'].tolist()
        tfidf_scores = []
        for kw in kws:
            try:
                tfidf_scores.append(tfidf.transform([kw]).mean())
            except ValueError as e:
                print(f"[!] Error processing keyword '{kw}': {e}")
                tfidf_scores.append(0.0)  # Assign a default score of 0.0 in case of error
        bm25_scores = [bm25.get_scores(kw.split()).mean() for kw in kws]
        llm_input = {'Keywords': ", ".join(kws), 'excerpt': excerpt}
        llm_resp = chain.invoke(llm_input)['text']

        for kw, t, b in zip(kws, tfidf_scores, bm25_scores):
            records.append({
                'cluster_id': cid,
                'Keyword': kw,
                'avg_tfidf': float(t),
                'avg_bm25': float(b),
                'llm_analysis': llm_resp
            })

    pd.DataFrame(records).to_csv(out_file, index=False)
    print(f"[✓] Analysis saved to {out_file}")
    return out_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--clusters', '-c', required=True)
    parser.add_argument('--crawled', '-r', required=True)
    parser.add_argument('--api_key', '-k', required=True)
    parser.add_argument('--domain', '-d', required=True)
    parser.add_argument('--output', '-o', default='keyword_analysis.csv')
    args = parser.parse_args()

    analyze_clusters(args.clusters, args.crawled, args.api_key, args.domain, args.output)