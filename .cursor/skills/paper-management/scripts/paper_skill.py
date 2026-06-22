#!/usr/bin/env python3
"""
Paper Management Skill - Agent-friendly interface for paper organization

This module provides a unified interface for adding papers to your research library
by automatically fetching metadata from various sources.

Usage:
    from paper_skill import add_paper_auto
    
    # Add paper by arXiv URL
    result = add_paper_auto("https://arxiv.org/abs/1706.03762")
    
    # Add paper by arXiv ID
    result = add_paper_auto("1706.03762")
    
    # Add paper by HuggingFace link
    result = add_paper_auto("https://huggingface.co/papers/2303.08774")
    
    # Add paper by BibTeX
    result = add_paper_auto('''
        @article{vaswani2017attention,
          title={Attention is all you need},
          author={Vaswani, Ashish and others},
          year={2017}
        }
    ''')
    
    # Add paper by name (searches arXiv)
    result = add_paper_auto("Attention Is All You Need")
"""

import sys
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

# Ensure the script directory is in the path for local imports
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import from local directory (works for both direct execution and symlink)
from paper_fetcher import fetch_paper_metadata, suggest_tags_from_metadata, detect_input_type
from research import PaperManager
from dashboard_service import get_dashboard_url


def _with_dashboard_url(result: Dict) -> Dict:
    if result.get("success"):
        result["dashboard_url"] = get_dashboard_url()
    return result


def add_paper_auto(
    input_str: str,
    priority: str = "medium",
    additional_tags: List[str] = None,
    additional_notes: str = None,
    mark_as_read: bool = False,
    rating: Optional[int] = None,
    custom_summary: Optional[str] = None
) -> Dict:
    """
    Automatically add a paper to your research library
    
    Args:
        input_str: Any of the following:
            - arXiv URL (https://arxiv.org/abs/1706.03762)
            - arXiv ID (1706.03762)
            - HuggingFace paper URL (https://huggingface.co/papers/...)
            - BibTeX entry (complete @article{...} block)
            - Paper name (will search arXiv)
        
        priority: Priority level for to-read list ('low', 'medium', 'high')
        additional_tags: Extra tags to add beyond auto-suggested ones
        additional_notes: Extra notes to append to fetched summary
        mark_as_read: If True, add to read list instead of to-read
        rating: Rating (1-5) if marking as read
        custom_summary: Custom summary to use instead of auto-fetched one
    
    Returns:
        Dict with keys:
            - success (bool): Whether operation succeeded
            - message (str): Human-readable result message
            - paper (dict): Paper metadata if successful
            - input_type (str): Type of input detected
    """
    
    input_type = detect_input_type(input_str)
    
    print(f"🔍 Detected input type: {input_type}")
    print(f"📥 Fetching paper metadata...")
    
    metadata = fetch_paper_metadata(input_str)
    
    if not metadata:
        return {
            'success': False,
            'message': f'Could not fetch paper metadata from {input_type} input',
            'paper': None,
            'input_type': input_type
        }
    
    print(f"✓ Found paper: {metadata['title'][:80]}...")
    
    suggested_tags = suggest_tags_from_metadata(metadata)
    
    all_tags = suggested_tags.copy()
    if additional_tags:
        all_tags.extend([tag for tag in additional_tags if tag not in all_tags])
    
    notes = metadata.get('summary', '')
    if additional_notes:
        notes = f"{notes}\n\n{additional_notes}" if notes else additional_notes
    
    manager = PaperManager()
    
    if mark_as_read:
        summary = custom_summary if custom_summary else metadata.get('summary', '')
        
        success = manager.add_read(
            title=metadata['title'],
            authors=metadata['authors'],
            url=metadata['url'],
            rating=rating,
            tags=all_tags,
            summary=summary,
            notes=notes,
            read_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        if success:
            return _with_dashboard_url({
                'success': True,
                'message': f"✓ Added '{metadata['title']}' to read list",
                'paper': metadata,
                'input_type': input_type,
                'tags': all_tags
            })
        else:
            return {
                'success': False,
                'message': f"✗ Paper '{metadata['title']}' already exists in your library",
                'paper': metadata,
                'input_type': input_type
            }
    
    else:
        success = manager.add_to_read(
            title=metadata['title'],
            authors=metadata['authors'],
            url=metadata['url'],
            priority=priority,
            tags=all_tags,
            notes=notes
        )
        
        if success:
            return _with_dashboard_url({
                'success': True,
                'message': f"✓ Added '{metadata['title']}' to reading list",
                'paper': metadata,
                'input_type': input_type,
                'tags': all_tags,
                'priority': priority
            })
        else:
            return {
                'success': False,
                'message': f"✗ Paper '{metadata['title']}' already exists in your library",
                'paper': metadata,
                'input_type': input_type
            }


def search_and_preview(input_str: str) -> Dict:
    """
    Search for a paper and preview its metadata without adding it
    
    Args:
        input_str: Same as add_paper_auto
    
    Returns:
        Dict with metadata preview
    """
    input_type = detect_input_type(input_str)
    metadata = fetch_paper_metadata(input_str)
    
    if not metadata:
        return {
            'success': False,
            'message': f'Could not fetch paper metadata from {input_type} input',
            'input_type': input_type
        }
    
    suggested_tags = suggest_tags_from_metadata(metadata)
    
    return {
        'success': True,
        'input_type': input_type,
        'metadata': metadata,
        'suggested_tags': suggested_tags
    }


def format_paper_info(result: Dict) -> str:
    """Format paper info for display"""
    if not result.get('success'):
        return f"❌ {result.get('message', 'Unknown error')}"
    
    paper = result.get('paper', {})
    tags = result.get('tags', [])
    
    output = []
    output.append("="*70)
    output.append(f"📄 {paper.get('title', 'Unknown title')}")
    output.append("-"*70)
    
    if paper.get('authors'):
        output.append(f"👥 Authors: {paper['authors']}")
    
    if paper.get('url'):
        output.append(f"🔗 URL: {paper['url']}")
    
    if tags:
        output.append(f"🏷️  Tags: {', '.join(tags)}")
    
    if result.get('priority'):
        output.append(f"⚡ Priority: {result['priority']}")
    
    if paper.get('summary'):
        summary = paper['summary']
        if len(summary) > 200:
            summary = summary[:200] + "..."
        output.append(f"📝 Summary: {summary}")
    
    output.append("="*70)
    output.append(f"✅ {result.get('message', 'Success')}")
    
    return "\n".join(output)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python paper_skill.py <arxiv_url|arxiv_id|huggingface_url|bibtex|paper_name>")
        print("\nExamples:")
        print("  python paper_skill.py 'https://arxiv.org/abs/1706.03762'")
        print("  python paper_skill.py '1706.03762'")
        print("  python paper_skill.py 'Attention Is All You Need'")
        sys.exit(1)
    
    input_str = ' '.join(sys.argv[1:])
    
    result = add_paper_auto(input_str)
    print("\n" + format_paper_info(result))
    
    sys.exit(0 if result['success'] else 1)
