import pandas as pd
import time
from keyword_analyzer.clustering import cluster_keywords
from keyword_analyzer.crawler import WebsiteCrawler
from keyword_analyzer.analysis import generate_report
from config import CRAWL_URL
import dotenv

def main(input_csv, clusters_output, report_output):
    # Step 1: Cluster keywords
    cluster_df = cluster_keywords(input_csv, clusters_output)
    
    # Step 2: Crawl website
    crawler = WebsiteCrawler()
    crawler.crawl(CRAWL_URL)
    
    # Step 3: Generate report
    report_df = generate_report(cluster_df, crawler, report_output)
    
    print(f"Analysis complete. Results saved to {clusters_output} and {report_output}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Keyword Cluster Analyzer')
    parser.add_argument('--input', required=True, help='Input CSV file with keywords')
    parser.add_argument('--clusters', default='clusters.csv', help='Output clusters CSV')
    parser.add_argument('--report', default='report.csv', help='Output report CSV')
    
    args = parser.parse_args()
    main(args.input, args.clusters, args.report)