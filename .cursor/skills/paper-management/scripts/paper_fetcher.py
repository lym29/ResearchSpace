#!/usr/bin/env python3
"""
Paper metadata fetcher - supports arXiv, HuggingFace, BibTeX, and paper name search
"""

import re
import json
from typing import Dict, Optional, List
from datetime import datetime
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


def extract_arxiv_id(url_or_id: str) -> Optional[str]:
    """Extract arXiv ID from URL or raw ID"""
    patterns = [
        r'arxiv\.org/abs/(\d+\.\d+)',
        r'arxiv\.org/pdf/(\d+\.\d+)',
        r'^(\d+\.\d+)(?:v\d+)?$',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None


def fetch_arxiv_metadata(arxiv_id: str) -> Optional[Dict]:
    """Fetch paper metadata from arXiv API"""
    try:
        import urllib.request
        
        url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_data = response.read().decode('utf-8')
        
        root = ET.fromstring(xml_data)
        
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entry = root.find('atom:entry', ns)
        
        if entry is None:
            return None
        
        title = entry.find('atom:title', ns)
        title_text = title.text.strip().replace('\n', ' ') if title is not None else ''
        
        authors = entry.findall('atom:author', ns)
        author_names = []
        for author in authors:
            name = author.find('atom:name', ns)
            if name is not None:
                author_names.append(name.text.strip())
        
        summary = entry.find('atom:summary', ns)
        summary_text = summary.text.strip().replace('\n', ' ') if summary is not None else ''
        
        published = entry.find('atom:published', ns)
        published_date = published.text[:10] if published is not None else ''
        
        categories = entry.findall('atom:category', ns)
        tags = []
        for cat in categories[:5]:
            term = cat.get('term')
            if term:
                tags.append(term)
        
        return {
            'title': title_text,
            'authors': ', '.join(author_names),
            'url': f'https://arxiv.org/abs/{arxiv_id}',
            'summary': summary_text[:500] + ('...' if len(summary_text) > 500 else ''),
            'published_date': published_date,
            'tags': tags,
            'source': 'arxiv'
        }
    except Exception as e:
        print(f"Error fetching arXiv metadata: {e}")
        return None


def extract_huggingface_paper_id(url: str) -> Optional[str]:
    """Extract paper ID from HuggingFace URL"""
    patterns = [
        r'huggingface\.co/papers/(\d+\.\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_huggingface_metadata(paper_id: str) -> Optional[Dict]:
    """Fetch paper metadata from HuggingFace (which uses arXiv IDs)"""
    return fetch_arxiv_metadata(paper_id)


def parse_bibtex(bibtex_str: str) -> Optional[Dict]:
    """Parse BibTeX entry and extract metadata"""
    try:
        title_match = re.search(r'title\s*=\s*[{"]([^}"]+)[}"]', bibtex_str, re.IGNORECASE)
        author_match = re.search(r'author\s*=\s*[{"]([^}"]+)[}"]', bibtex_str, re.IGNORECASE)
        url_match = re.search(r'(?:url|eprint)\s*=\s*[{"]([^}"]+)[}"]', bibtex_str, re.IGNORECASE)
        year_match = re.search(r'year\s*=\s*[{"]?(\d{4})[}"]?', bibtex_str, re.IGNORECASE)
        
        if not title_match:
            return None
        
        title = title_match.group(1).strip()
        authors = author_match.group(1).strip() if author_match else ''
        url = url_match.group(1).strip() if url_match else ''
        year = year_match.group(1) if year_match else ''
        
        if 'arxiv' in url.lower():
            arxiv_id = extract_arxiv_id(url)
            if arxiv_id:
                arxiv_data = fetch_arxiv_metadata(arxiv_id)
                if arxiv_data:
                    return arxiv_data
        
        return {
            'title': title,
            'authors': authors,
            'url': url,
            'summary': '',
            'published_date': f'{year}-01-01' if year else '',
            'tags': [],
            'source': 'bibtex'
        }
    except Exception as e:
        print(f"Error parsing BibTeX: {e}")
        return None


def search_paper_by_name(paper_name: str) -> Optional[Dict]:
    """Search for paper by name using arXiv API"""
    try:
        import urllib.request
        import urllib.parse
        
        query = urllib.parse.quote(paper_name)
        url = f"http://export.arxiv.org/api/query?search_query=ti:{query}&start=0&max_results=1"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_data = response.read().decode('utf-8')
        
        root = ET.fromstring(xml_data)
        
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entry = root.find('atom:entry', ns)
        
        if entry is None:
            return None
        
        id_elem = entry.find('atom:id', ns)
        if id_elem is not None:
            arxiv_url = id_elem.text
            arxiv_id = extract_arxiv_id(arxiv_url)
            if arxiv_id:
                return fetch_arxiv_metadata(arxiv_id)
        
        return None
    except Exception as e:
        print(f"Error searching for paper: {e}")
        return None


def detect_input_type(input_str: str) -> str:
    """Detect the type of input provided"""
    input_lower = input_str.lower().strip()
    
    if '@article' in input_lower or '@inproceedings' in input_lower or '@misc' in input_lower:
        return 'bibtex'
    
    if 'arxiv.org' in input_lower or re.match(r'^\d+\.\d+', input_str):
        return 'arxiv'
    
    if 'huggingface.co/papers' in input_lower:
        return 'huggingface'
    
    return 'paper_name'


def fetch_paper_metadata(input_str: str) -> Optional[Dict]:
    """
    Universal paper metadata fetcher
    
    Accepts:
    - arXiv URLs or IDs
    - HuggingFace paper URLs
    - BibTeX entries
    - Paper names (will search arXiv)
    
    Returns standardized metadata dict or None if not found
    """
    input_type = detect_input_type(input_str)
    
    if input_type == 'bibtex':
        return parse_bibtex(input_str)
    
    elif input_type == 'arxiv':
        arxiv_id = extract_arxiv_id(input_str)
        if arxiv_id:
            return fetch_arxiv_metadata(arxiv_id)
    
    elif input_type == 'huggingface':
        paper_id = extract_huggingface_paper_id(input_str)
        if paper_id:
            return fetch_huggingface_metadata(paper_id)
    
    elif input_type == 'paper_name':
        return search_paper_by_name(input_str)
    
    return None


def suggest_tags_from_metadata(metadata: Dict) -> List[str]:
    """Suggest relevant tags based on paper metadata"""
    suggested_tags = list(metadata.get('tags', []))
    
    title_lower = metadata.get('title', '').lower()
    summary_lower = metadata.get('summary', '').lower()
    
    keywords = {
        'transformer': ['transformers', 'attention'],
        'bert': ['bert', 'nlp', 'pretraining'],
        'gpt': ['gpt', 'nlp', 'language-models'],
        'vision': ['computer-vision'],
        'image': ['computer-vision'],
        'reinforcement': ['reinforcement-learning'],
        'neural network': ['deep-learning'],
        'deep learning': ['deep-learning'],
        'machine learning': ['machine-learning'],
        'diffusion': ['diffusion-models', 'generative'],
        'gan': ['gan', 'generative'],
        'llm': ['llm', 'language-models'],
        'multimodal': ['multimodal'],
        'survey': ['survey'],
    }
    
    for keyword, tags in keywords.items():
        if keyword in title_lower or keyword in summary_lower:
            for tag in tags:
                if tag not in suggested_tags:
                    suggested_tags.append(tag)
    
    return suggested_tags[:10]
