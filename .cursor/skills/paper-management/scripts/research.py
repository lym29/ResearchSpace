#!/usr/bin/env python3
"""
ResearchSpace - A personal research organization system
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    import click
    from colorama import Fore, Style, init
    from tabulate import tabulate
except ImportError:
    print("Error: Required dependencies not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

init(autoreset=True)

BASE_DIR = Path(__file__).parent
from paths import (
    PAPERS_DIR,
    TO_READ_FILE,
    READ_FILE,
    NOTES_DIR,
    SCRIPTS_DIR,
    WORKSPACE_ROOT,
    DASHBOARD_FILE,
)


class PaperManager:
    """Manages paper reading lists and metadata"""
    
    def __init__(self):
        self.to_read = self._load_papers(TO_READ_FILE)
        self.read = self._load_papers(READ_FILE)
    
    def _load_papers(self, filepath: Path) -> List[Dict]:
        """Load papers from JSON file"""
        if not filepath.exists():
            return []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    
    def _save_papers(self, papers: List[Dict], filepath: Path):
        """Save papers to JSON file"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
    
    def _regenerate_dashboard(self):
        """Regenerate the HTML dashboard after changes"""
        try:
            import subprocess
            dashboard_script = SCRIPTS_DIR / "generate_dashboard.py"
            if dashboard_script.exists():
                subprocess.run(
                    [sys.executable, str(dashboard_script)],
                    cwd=str(WORKSPACE_ROOT),
                    capture_output=True,
                    timeout=10,
                )
        except Exception:
            pass
    
    def save(self):
        """Save both lists"""
        self._save_papers(self.to_read, TO_READ_FILE)
        self._save_papers(self.read, READ_FILE)
        self._regenerate_dashboard()
    
    def find_paper(self, title: str, list_name: str = None) -> tuple:
        """Find paper by title in specified list or both
        Returns: (paper, list_name, index)
        """
        title_lower = title.lower()
        
        if list_name is None or list_name == 'to-read':
            for idx, paper in enumerate(self.to_read):
                if paper['title'].lower() == title_lower:
                    return (paper, 'to-read', idx)
        
        if list_name is None or list_name == 'read':
            for idx, paper in enumerate(self.read):
                if paper['title'].lower() == title_lower:
                    return (paper, 'read', idx)
        
        return (None, None, None)
    
    def add_to_read(self, title: str, authors: str = None, url: str = None,
                    priority: str = "medium", tags: List[str] = None,
                    notes: str = None) -> bool:
        """Add paper to reading list"""
        existing, _, _ = self.find_paper(title)
        if existing:
            return False
        
        paper = {
            "title": title,
            "authors": authors or "",
            "url": url or "",
            "added_date": datetime.now().strftime("%Y-%m-%d"),
            "priority": priority,
            "tags": tags or [],
            "notes": notes or ""
        }
        self.to_read.append(paper)
        self.save()
        return True
    
    def add_read(self, title: str, authors: str = None, url: str = None,
                 rating: int = None, tags: List[str] = None,
                 summary: str = None, notes: str = None,
                 read_date: str = None) -> bool:
        """Add paper directly to read list"""
        existing, _, _ = self.find_paper(title)
        if existing:
            return False
        
        paper = {
            "title": title,
            "authors": authors or "",
            "url": url or "",
            "added_date": datetime.now().strftime("%Y-%m-%d"),
            "read_date": read_date or datetime.now().strftime("%Y-%m-%d"),
            "rating": rating,
            "tags": tags or [],
            "summary": summary or "",
            "notes": notes or ""
        }
        self.read.append(paper)
        self.save()
        return True
    
    def mark_as_read(self, title: str, notes: str = None, rating: int = None,
                     summary: str = None) -> bool:
        """Move paper from to-read to read list"""
        paper, list_name, idx = self.find_paper(title, 'to-read')
        
        if not paper:
            return False
        
        self.to_read.pop(idx)
        
        paper['read_date'] = datetime.now().strftime("%Y-%m-%d")
        if notes:
            paper['notes'] = notes
        if rating is not None:
            paper['rating'] = rating
        if summary:
            paper['summary'] = summary
        else:
            paper['summary'] = ""
        
        self.read.append(paper)
        self.save()
        return True
    
    def remove_paper(self, title: str, from_list: str = None) -> bool:
        """Remove paper from list"""
        paper, list_name, idx = self.find_paper(title, from_list)
        
        if not paper:
            return False
        
        if list_name == 'to-read':
            self.to_read.pop(idx)
        else:
            self.read.pop(idx)
        
        self.save()
        return True
    
    def update_paper(self, title: str, **kwargs) -> bool:
        """Update paper metadata"""
        paper, list_name, idx = self.find_paper(title)
        
        if not paper:
            return False
        
        for key, value in kwargs.items():
            if value is not None:
                if key == 'tags' and isinstance(value, str):
                    value = [t.strip() for t in value.split(',')]
                paper[key] = value
        
        if list_name == 'to-read':
            self.to_read[idx] = paper
        else:
            self.read[idx] = paper
        
        self.save()
        return True
    
    def search_papers(self, query: str) -> List[tuple]:
        """Search papers by title, authors, tags, or notes
        Returns: [(paper, list_name), ...]
        """
        query_lower = query.lower()
        results = []
        
        for paper in self.to_read:
            if (query_lower in paper['title'].lower() or
                query_lower in paper.get('authors', '').lower() or
                query_lower in paper.get('notes', '').lower() or
                any(query_lower in tag.lower() for tag in paper.get('tags', []))):
                results.append((paper, 'to-read'))
        
        for paper in self.read:
            if (query_lower in paper['title'].lower() or
                query_lower in paper.get('authors', '').lower() or
                query_lower in paper.get('notes', '').lower() or
                query_lower in paper.get('summary', '').lower() or
                any(query_lower in tag.lower() for tag in paper.get('tags', []))):
                results.append((paper, 'read'))
        
        return results


def format_paper_table(papers: List[Dict], list_type: str) -> str:
    """Format papers as a table"""
    if not papers:
        return f"{Fore.YELLOW}No papers found.{Style.RESET_ALL}"
    
    if list_type == 'to-read':
        headers = ["#", "Title", "Authors", "Priority", "Tags", "Added"]
        rows = []
        for idx, paper in enumerate(papers, 1):
            priority_color = {
                'high': Fore.RED,
                'medium': Fore.YELLOW,
                'low': Fore.GREEN
            }.get(paper.get('priority', 'medium'), Fore.WHITE)
            
            rows.append([
                idx,
                paper['title'][:50] + ('...' if len(paper['title']) > 50 else ''),
                paper.get('authors', '')[:30] + ('...' if len(paper.get('authors', '')) > 30 else ''),
                f"{priority_color}{paper.get('priority', 'medium')}{Style.RESET_ALL}",
                ', '.join(paper.get('tags', []))[:30],
                paper.get('added_date', '')
            ])
    else:
        headers = ["#", "Title", "Authors", "Rating", "Tags", "Read Date"]
        rows = []
        for idx, paper in enumerate(papers, 1):
            rating = paper.get('rating')
            rating_str = f"{Fore.YELLOW}{'⭐' * rating}{Style.RESET_ALL}" if rating else 'N/A'
            
            rows.append([
                idx,
                paper['title'][:50] + ('...' if len(paper['title']) > 50 else ''),
                paper.get('authors', '')[:30] + ('...' if len(paper.get('authors', '')) > 30 else ''),
                rating_str,
                ', '.join(paper.get('tags', []))[:30],
                paper.get('read_date', '')
            ])
    
    return tabulate(rows, headers=headers, tablefmt='simple')


def print_paper_details(paper: Dict, list_type: str):
    """Print detailed paper information"""
    click.echo(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    click.echo(f"{Fore.GREEN}Title:{Style.RESET_ALL} {paper['title']}")
    
    if paper.get('authors'):
        click.echo(f"{Fore.GREEN}Authors:{Style.RESET_ALL} {paper['authors']}")
    
    if paper.get('url'):
        click.echo(f"{Fore.GREEN}URL:{Style.RESET_ALL} {paper['url']}")
    
    if list_type == 'to-read':
        priority = paper.get('priority', 'medium')
        priority_color = {
            'high': Fore.RED,
            'medium': Fore.YELLOW,
            'low': Fore.GREEN
        }.get(priority, Fore.WHITE)
        click.echo(f"{Fore.GREEN}Priority:{Style.RESET_ALL} {priority_color}{priority}{Style.RESET_ALL}")
    
    if list_type == 'read':
        if paper.get('rating'):
            click.echo(f"{Fore.GREEN}Rating:{Style.RESET_ALL} {Fore.YELLOW}{'⭐' * paper['rating']}{Style.RESET_ALL}")
        if paper.get('read_date'):
            click.echo(f"{Fore.GREEN}Read Date:{Style.RESET_ALL} {paper['read_date']}")
        if paper.get('summary'):
            click.echo(f"{Fore.GREEN}Summary:{Style.RESET_ALL} {paper['summary']}")
    
    if paper.get('tags'):
        click.echo(f"{Fore.GREEN}Tags:{Style.RESET_ALL} {', '.join(paper['tags'])}")
    
    if paper.get('added_date'):
        click.echo(f"{Fore.GREEN}Added:{Style.RESET_ALL} {paper['added_date']}")
    
    if paper.get('notes'):
        click.echo(f"{Fore.GREEN}Notes:{Style.RESET_ALL} {paper['notes']}")
    
    click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


@click.group()
def cli():
    """ResearchSpace - Personal research organization system"""
    pass


@cli.group()
def papers():
    """Manage research papers"""
    pass


@papers.command('add')
@click.argument('input_str', required=False)
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high']), 
              default='medium', help='Reading priority')
@click.option('--tags', '-t', help='Additional comma-separated tags')
@click.option('--notes', '-n', help='Additional notes')
@click.option('--read', '-r', is_flag=True, help='Add to read list instead of to-read')
@click.option('--rating', type=click.IntRange(1, 5), help='Rating (1-5) if marking as read')
@click.option('--preview', is_flag=True, help='Preview paper info without adding')
def add_paper(input_str, priority, tags, notes, read, rating, preview):
    """
    Add a paper automatically by fetching metadata from various sources
    
    Supports:
    - arXiv URLs or IDs (https://arxiv.org/abs/1706.03762 or 1706.03762)
    - HuggingFace paper URLs (https://huggingface.co/papers/...)
    - BibTeX entries (paste the entire @article{...} block)
    - Paper names (will search arXiv)
    
    Examples:
      python research.py papers add "https://arxiv.org/abs/1706.03762"
      python research.py papers add "1706.03762" --priority high
      python research.py papers add "Attention Is All You Need" --tags "must-read"
    """
    if not input_str:
        click.echo(f"{Fore.YELLOW}Please provide a paper URL, ID, BibTeX, or name{Style.RESET_ALL}")
        click.echo("\nExamples:")
        click.echo('  papers add "https://arxiv.org/abs/1706.03762"')
        click.echo('  papers add "1706.03762" --priority high')
        click.echo('  papers add "Attention Is All You Need"')
        sys.exit(1)
    
    try:
        from paper_skill import add_paper_auto, search_and_preview, format_paper_info
        
        if preview:
            result = search_and_preview(input_str)
            if result['success']:
                metadata = result['metadata']
                click.echo(f"\n{Fore.CYAN}Paper Preview{Style.RESET_ALL}")
                click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                click.echo(f"{Fore.GREEN}Title:{Style.RESET_ALL} {metadata['title']}")
                click.echo(f"{Fore.GREEN}Authors:{Style.RESET_ALL} {metadata['authors']}")
                click.echo(f"{Fore.GREEN}URL:{Style.RESET_ALL} {metadata['url']}")
                click.echo(f"{Fore.GREEN}Suggested Tags:{Style.RESET_ALL} {', '.join(result['suggested_tags'])}")
                if metadata.get('summary'):
                    summary = metadata['summary'][:300] + ('...' if len(metadata['summary']) > 300 else '')
                    click.echo(f"{Fore.GREEN}Summary:{Style.RESET_ALL} {summary}")
            else:
                click.echo(f"{Fore.RED}✗{Style.RESET_ALL} {result['message']}")
        else:
            tag_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []
            
            result = add_paper_auto(
                input_str,
                priority=priority,
                additional_tags=tag_list,
                additional_notes=notes,
                mark_as_read=read,
                rating=rating
            )
            
            if result['success']:
                click.echo(f"\n{Fore.GREEN}✓{Style.RESET_ALL} {result['message']}")
                click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                paper = result['paper']
                click.echo(f"{Fore.GREEN}Title:{Style.RESET_ALL} {paper['title']}")
                click.echo(f"{Fore.GREEN}Authors:{Style.RESET_ALL} {paper['authors']}")
                click.echo(f"{Fore.GREEN}URL:{Style.RESET_ALL} {paper['url']}")
                click.echo(f"{Fore.GREEN}Tags:{Style.RESET_ALL} {', '.join(result.get('tags', []))}")
                if not read:
                    click.echo(f"{Fore.GREEN}Priority:{Style.RESET_ALL} {result.get('priority', 'medium')}")
                click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
            else:
                click.echo(f"\n{Fore.RED}✗{Style.RESET_ALL} {result['message']}\n")
                sys.exit(1)
    
    except ImportError as e:
        click.echo(f"{Fore.RED}Error:{Style.RESET_ALL} Paper skill module not available")
        click.echo(f"Please ensure paper_skill.py and paper_fetcher.py are in the same directory")
        sys.exit(1)


@papers.command('add-to-read')
@click.argument('title')
@click.option('--authors', '-a', help='Paper authors')
@click.option('--url', '-u', help='Paper URL (e.g., arXiv, DOI)')
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high']), 
              default='medium', help='Reading priority')
@click.option('--tags', '-t', help='Comma-separated tags')
@click.option('--notes', '-n', help='Initial notes')
def add_to_read(title, authors, url, priority, tags, notes):
    """Add a paper to your reading list (manual entry)"""
    manager = PaperManager()
    
    tag_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []
    
    if manager.add_to_read(title, authors, url, priority, tag_list, notes):
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Added '{title}' to reading list")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Paper already exists")
        sys.exit(1)


@papers.command('add-read')
@click.argument('title')
@click.option('--authors', '-a', help='Paper authors')
@click.option('--url', '-u', help='Paper URL')
@click.option('--rating', '-r', type=click.IntRange(1, 5), help='Rating (1-5)')
@click.option('--tags', '-t', help='Comma-separated tags')
@click.option('--summary', '-s', help='Paper summary')
@click.option('--notes', '-n', help='Notes and insights')
@click.option('--read-date', '-d', help='Read date (YYYY-MM-DD)')
def add_read(title, authors, url, rating, tags, summary, notes, read_date):
    """Add a paper directly to read list"""
    manager = PaperManager()
    
    tag_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []
    
    if manager.add_read(title, authors, url, rating, tag_list, summary, notes, read_date):
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Added '{title}' to read list")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Paper already exists")
        sys.exit(1)


@papers.command('mark-read')
@click.argument('title')
@click.option('--notes', '-n', help='Reading notes and insights')
@click.option('--rating', '-r', type=click.IntRange(1, 5), help='Rating (1-5)')
@click.option('--summary', '-s', help='Paper summary')
def mark_read(title, notes, rating, summary):
    """Mark a paper as read"""
    manager = PaperManager()
    
    if manager.mark_as_read(title, notes, rating, summary):
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Marked '{title}' as read")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Paper not found in reading list")
        sys.exit(1)


@papers.command('remove')
@click.argument('title')
@click.option('--from', 'from_list', type=click.Choice(['to-read', 'read']),
              help='Specify which list to remove from')
def remove(title, from_list):
    """Remove a paper from your lists"""
    manager = PaperManager()
    
    if manager.remove_paper(title, from_list):
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Removed '{title}'")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Paper not found")
        sys.exit(1)


@papers.command('update')
@click.argument('title')
@click.option('--authors', '-a', help='Update authors')
@click.option('--url', '-u', help='Update URL')
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high']),
              help='Update priority')
@click.option('--tags', '-t', help='Update tags (comma-separated)')
@click.option('--notes', '-n', help='Update notes')
@click.option('--rating', '-r', type=click.IntRange(1, 5), help='Update rating (1-5)')
def update(title, authors, url, priority, tags, notes, rating):
    """Update paper metadata"""
    manager = PaperManager()
    
    updates = {}
    if authors is not None:
        updates['authors'] = authors
    if url is not None:
        updates['url'] = url
    if priority is not None:
        updates['priority'] = priority
    if tags is not None:
        updates['tags'] = tags
    if notes is not None:
        updates['notes'] = notes
    if rating is not None:
        updates['rating'] = rating
    
    if not updates:
        click.echo(f"{Fore.YELLOW}No updates specified{Style.RESET_ALL}")
        return
    
    if manager.update_paper(title, **updates):
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Updated '{title}'")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Paper not found")
        sys.exit(1)


@papers.command('list')
@click.argument('list_name', type=click.Choice(['to-read', 'read']))
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high']),
              help='Filter by priority (to-read only)')
@click.option('--rating', '-r', type=click.IntRange(1, 5),
              help='Filter by rating (read only)')
@click.option('--tag', '-t', help='Filter by tag')
def list_papers(list_name, priority, rating, tag):
    """List papers from to-read or read list"""
    manager = PaperManager()
    
    papers_list = manager.to_read if list_name == 'to-read' else manager.read
    
    if priority:
        papers_list = [p for p in papers_list if p.get('priority') == priority]
    
    if rating:
        papers_list = [p for p in papers_list if p.get('rating') == rating]
    
    if tag:
        papers_list = [p for p in papers_list if tag in p.get('tags', [])]
    
    title = f"{list_name.replace('-', ' ').title()} Papers"
    if priority or rating or tag:
        filters = []
        if priority:
            filters.append(f"priority={priority}")
        if rating:
            filters.append(f"rating={rating}")
        if tag:
            filters.append(f"tag={tag}")
        title += f" (filtered: {', '.join(filters)})"
    
    click.echo(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    click.echo(format_paper_table(papers_list, list_name))
    click.echo(f"\n{Fore.CYAN}Total: {len(papers_list)} paper(s){Style.RESET_ALL}\n")


@papers.command('search')
@click.argument('query')
def search(query):
    """Search papers by title, authors, tags, or notes"""
    manager = PaperManager()
    results = manager.search_papers(query)
    
    if not results:
        click.echo(f"\n{Fore.YELLOW}No papers found matching '{query}'{Style.RESET_ALL}\n")
        return
    
    click.echo(f"\n{Fore.CYAN}Search Results for '{query}'{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    to_read_results = [p for p, lst in results if lst == 'to-read']
    read_results = [p for p, lst in results if lst == 'read']
    
    if to_read_results:
        click.echo(f"{Fore.GREEN}To Read ({len(to_read_results)}):{Style.RESET_ALL}")
        click.echo(format_paper_table(to_read_results, 'to-read'))
        click.echo()
    
    if read_results:
        click.echo(f"{Fore.GREEN}Read ({len(read_results)}):{Style.RESET_ALL}")
        click.echo(format_paper_table(read_results, 'read'))
        click.echo()
    
    click.echo(f"{Fore.CYAN}Total: {len(results)} paper(s){Style.RESET_ALL}\n")


@papers.command('show')
@click.argument('title')
def show(title):
    """Show detailed information about a paper"""
    manager = PaperManager()
    paper, list_name, _ = manager.find_paper(title)
    
    if not paper:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Paper not found")
        sys.exit(1)
    
    print_paper_details(paper, list_name)


@papers.command('stats')
def stats():
    """Show paper reading statistics"""
    manager = PaperManager()
    
    click.echo(f"\n{Fore.CYAN}Paper Reading Statistics{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    click.echo(f"{Fore.GREEN}To Read:{Style.RESET_ALL} {len(manager.to_read)} papers")
    
    high_priority = len([p for p in manager.to_read if p.get('priority') == 'high'])
    medium_priority = len([p for p in manager.to_read if p.get('priority') == 'medium'])
    low_priority = len([p for p in manager.to_read if p.get('priority') == 'low'])
    
    if manager.to_read:
        click.echo(f"  {Fore.RED}High:{Style.RESET_ALL} {high_priority}")
        click.echo(f"  {Fore.YELLOW}Medium:{Style.RESET_ALL} {medium_priority}")
        click.echo(f"  {Fore.GREEN}Low:{Style.RESET_ALL} {low_priority}")
    
    click.echo(f"\n{Fore.GREEN}Read:{Style.RESET_ALL} {len(manager.read)} papers")
    
    if manager.read:
        rated_papers = [p for p in manager.read if p.get('rating')]
        if rated_papers:
            avg_rating = sum(p['rating'] for p in rated_papers) / len(rated_papers)
            click.echo(f"  {Fore.YELLOW}Average Rating:{Style.RESET_ALL} {avg_rating:.1f} ⭐")
        
        for rating in range(5, 0, -1):
            count = len([p for p in manager.read if p.get('rating') == rating])
            if count > 0:
                click.echo(f"  {Fore.YELLOW}{'⭐' * rating}:{Style.RESET_ALL} {count} papers")
    
    all_tags = {}
    for paper in manager.to_read + manager.read:
        for tag in paper.get('tags', []):
            all_tags[tag] = all_tags.get(tag, 0) + 1
    
    if all_tags:
        click.echo(f"\n{Fore.GREEN}Top Tags:{Style.RESET_ALL}")
        sorted_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:10]
        for tag, count in sorted_tags:
            click.echo(f"  {tag}: {count}")
    
    click.echo()


@cli.group()
def todos():
    """Manage TODO lists for papers"""
    pass


@todos.command('create')
@click.argument('title')
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high']),
              default='medium', help='Priority level')
@click.option('--notes', '-n', help='Notes about reading plan')
def create_todos(title, priority, notes):
    """Create a TODO list for a paper"""
    from paper_todo_skill import create_paper_todo
    
    result = create_paper_todo(title, priority=priority, notes=notes)
    
    if result['success']:
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} {result['message']}")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} {result['message']}")
        sys.exit(1)


@todos.command('add')
@click.argument('title')
@click.argument('todo_text', nargs=-1, required=True)
def add_todo(title, todo_text):
    """Add a TODO item to a paper's list"""
    from paper_todo_skill import add_todo_item
    
    todo_text_str = ' '.join(todo_text)
    result = add_todo_item(title, todo_text_str)
    
    if result['success']:
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} {result['message']}")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} {result['message']}")
        sys.exit(1)


@todos.command('complete')
@click.argument('title')
@click.argument('todo_ref', nargs=-1, required=True)
def complete_todo(title, todo_ref):
    """Mark a TODO item as complete (by text or index)"""
    from paper_todo_skill import mark_todo_complete
    
    todo_ref_str = ' '.join(todo_ref)
    
    if todo_ref_str.isdigit():
        result = mark_todo_complete(title, todo_index=int(todo_ref_str))
    else:
        result = mark_todo_complete(title, todo_text=todo_ref_str)
    
    if result['success']:
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} {result['message']}")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} {result['message']}")
        sys.exit(1)


@todos.command('incomplete')
@click.argument('title')
@click.argument('todo_ref', nargs=-1, required=True)
def incomplete_todo(title, todo_ref):
    """Mark a TODO item as incomplete"""
    from paper_todo_skill import mark_todo_incomplete
    
    todo_ref_str = ' '.join(todo_ref)
    
    if todo_ref_str.isdigit():
        result = mark_todo_incomplete(title, todo_index=int(todo_ref_str))
    else:
        result = mark_todo_incomplete(title, todo_text=todo_ref_str)
    
    if result['success']:
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} {result['message']}")
    else:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} {result['message']}")
        sys.exit(1)


@todos.command('list')
@click.argument('title', required=False)
@click.option('--show-completed/--hide-completed', default=True,
              help='Show or hide completed items')
def list_todos(title, show_completed):
    """List TODO items for a paper (or all papers)"""
    from paper_todo_skill import format_todo_list
    
    output = format_todo_list(title, show_completed)
    click.echo(output)


@todos.command('delete')
@click.argument('title')
@click.argument('todo_ref', nargs=-1, required=False)
@click.option('--all', 'delete_all', is_flag=True,
              help='Delete entire TODO list for the paper')
def delete_todo(title, todo_ref, delete_all):
    """Delete a TODO item or entire list"""
    if delete_all:
        from paper_todo_skill import delete_paper_todos
        result = delete_paper_todos(title)
        
        if result['success']:
            click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} {result['message']}")
        else:
            click.echo(f"{Fore.RED}✗{Style.RESET_ALL} {result['message']}")
            sys.exit(1)
    else:
        if not todo_ref:
            click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Must specify TODO item or use --all flag")
            sys.exit(1)
        
        from paper_todo_skill import delete_todo_item
        
        todo_ref_str = ' '.join(todo_ref)
        
        if todo_ref_str.isdigit():
            result = delete_todo_item(title, todo_index=int(todo_ref_str))
        else:
            result = delete_todo_item(title, todo_text=todo_ref_str)
        
        if result['success']:
            click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} {result['message']}")
        else:
            click.echo(f"{Fore.RED}✗{Style.RESET_ALL} {result['message']}")
            sys.exit(1)


@todos.command('stats')
@click.argument('title', required=False)
def todo_stats(title):
    """Show TODO statistics"""
    from paper_todo_skill import get_todo_stats
    
    result = get_todo_stats(title)
    
    if not result['success']:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} {result['message']}")
        sys.exit(1)
    
    stats = result['stats']
    
    if isinstance(stats, list):
        click.echo(f"\n{Fore.CYAN}TODO Statistics (All Papers){Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        for stat in sorted(stats, key=lambda x: x['progress'], reverse=True):
            progress_bar = '█' * int(stat['progress'] / 10) + '░' * (10 - int(stat['progress'] / 10))
            priority_color = {
                'high': Fore.RED,
                'medium': Fore.YELLOW,
                'low': Fore.GREEN
            }.get(stat['priority'], '')
            
            click.echo(f"{stat['paper'][:50]}")
            click.echo(f"  {progress_bar} {stat['progress']:.0f}% "
                      f"({stat['completed']}/{stat['total']}) "
                      f"- {priority_color}Priority: {stat['priority']}{Style.RESET_ALL}")
            click.echo()
    else:
        click.echo(f"\n{Fore.CYAN}TODO Statistics{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        click.echo(f"Paper: {stats['paper']}")
        click.echo(f"Progress: {stats['completed']}/{stats['total']} ({stats['progress']:.0f}%)")
        click.echo(f"Remaining: {stats['remaining']}")
        click.echo()


@cli.command('dashboard')
def generate_dashboard():
    """Generate/update the reading progress HTML dashboard"""
    import subprocess
    
    dashboard_script = SCRIPTS_DIR / "generate_dashboard.py"
    
    if not dashboard_script.exists():
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Dashboard script not found")
        sys.exit(1)
    
    try:
        result = subprocess.run(
            [sys.executable, str(dashboard_script)],
            cwd=str(WORKSPACE_ROOT),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Dashboard generated successfully")
            click.echo(f"\nOpen {Fore.CYAN}{DASHBOARD_FILE}{Style.RESET_ALL} in your browser to view your progress!")
        else:
            click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Failed to generate dashboard")
            if result.stderr:
                click.echo(result.stderr)
            sys.exit(1)
    except subprocess.TimeoutExpired:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Dashboard generation timed out")
        sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}✗{Style.RESET_ALL} Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
