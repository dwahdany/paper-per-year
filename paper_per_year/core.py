"""Core functionality for paper-per-year."""

import sys
import os
from typing import List, Tuple, Optional
from pathlib import Path

import numpy as np
from scholarly import scholarly
import matplotlib.pyplot as plt
import seaborn as sns
import click

def get_year(pub: dict) -> int:
    """Extract year from a publication entry.
    
    Args:
        pub: Publication dictionary from scholarly
        
    Returns:
        int: Publication year or 0 if not found
    """
    if 'pub_year' in pub:
        return int(pub['pub_year'])
    if 'bib' in pub and 'pub_year' in pub['bib']:
        return int(pub['bib']['pub_year'])
    return 0

def search_author(name: str) -> List[dict]:
    """Search for an author on Google Scholar.
    
    Args:
        name: Author name to search for
        
    Returns:
        List[dict]: List of author results
        
    Raises:
        click.ClickException: If no authors found
    """
    results = [*scholarly.search_author(name)]
    if not results:
        raise click.ClickException(f"No authors found with name: {name}")
    return results

def display_authors(authors: List[dict]) -> None:
    """Display list of found authors.
    
    Args:
        authors: List of author dictionaries
    """
    click.secho("\nFound authors:", fg='green', err=True)
    for i, author in enumerate(authors):
        affiliation = author.get('affiliation', 'No affiliation')
        click.echo(f"{i+1}. {author['name']} - {affiliation}", err=True)

def get_author_choice(authors: List[dict]) -> Optional[dict]:
    """Get user selection of author.
    
    Args:
        authors: List of author dictionaries
        
    Returns:
        Optional[dict]: Selected author or None if cancelled
        
    Raises:
        click.Abort: If user cancels
    """
    while True:
        try:
            choice = click.prompt("\nSelect author number", type=int, default=1, 
                                show_default=True, err=True)
            if choice == 0:
                return None
            if 1 <= choice <= len(authors):
                return authors[choice-1]
            click.secho("Invalid selection. Please try again.", fg='yellow', err=True)
        except click.exceptions.Abort:
            raise

def get_publication_years(author: dict) -> Tuple[np.ndarray, np.ndarray]:
    """Get publication years and counts for an author.
    
    Args:
        author: Author dictionary from scholarly
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Unique years and their counts
        
    Raises:
        click.ClickException: If no valid publications found
    """
    author = scholarly.fill(author)
    years = np.array([get_year(x) for x in author['publications']])
    mask = years != 0
    years = years[mask]
    
    if len(years) == 0:
        raise click.ClickException("No publications with valid years found.")
        
    return np.unique(years, return_counts=True)

def create_plot(years: np.ndarray, counts: np.ndarray, author_name: str,
               style: str = 'darkgrid', context: str = 'talk') -> None:
    """Create publication count plot.
    
    Args:
        years: Array of years
        counts: Array of publication counts
        author_name: Name of the author
        style: Seaborn style
        context: Seaborn context
    """
    # Reset any existing style
    plt.style.use('default')
    sns.reset_defaults()
    
    # Set the style and context
    sns.set_theme(style=style, context=context)
    
    # Create figure with dark background if using dark style
    fig = plt.figure(figsize=(12, 6), dpi=300)
    if style in ['dark', 'darkgrid']:
        fig.patch.set_facecolor('#2e3440')
        plt.gca().set_facecolor('#2e3440')
    
    # Create the plot
    ax = sns.barplot(x=years, y=counts)
    
    # Adjust text color for dark themes
    text_color = 'white' if style in ['dark', 'darkgrid'] else 'black'
    
    # Add count labels on top of each bar
    for i, v in enumerate(counts):
        ax.text(i, v, str(v), ha='center', va='bottom', color=text_color)
    
    plt.title(f"Publications per Year - {author_name}", color=text_color)
    plt.xlabel("Year", color=text_color)
    plt.ylabel("Number of Publications", color=text_color)
    plt.xticks(rotation=45, color=text_color)
    plt.yticks(color=text_color)
    
    plt.tight_layout()

def save_plot(output_dir: str, author_name: str) -> str:
    """Save plot to file.
    
    Args:
        output_dir: Directory to save plot
        author_name: Name of the author
        
    Returns:
        str: Path to saved file
    """
    output_file = Path(output_dir) / f"{author_name.replace(' ', '_')}.pdf"
    plt.savefig(output_file)
    plt.close()  # Clean up
    return output_file

def print_year_counts(years: np.ndarray, counts: np.ndarray) -> None:
    """Print year counts to stdout.
    
    Args:
        years: Array of years
        counts: Array of publication counts
    """
    for year, count in zip(years, counts):
        click.echo(f"{year}\t{count}")

def process_author(author_name: str, output_dir: str = '.', 
                  style: str = 'darkgrid', context: str = 'talk') -> None:
    """Process author publications and generate plots."""
    search_query = scholarly.search_author(author_name)
    print("\nFound authors:")
    authors = []
    for i, author in enumerate(search_query, 1):
        authors.append(author)
        affiliation = author.get('affiliation', 'No affiliation')
        print(f"{i}. {author['name']} - {affiliation}")
    
    # Get user selection
    while True:
        try:
            selection = int(input("\nSelect author number [1]: ") or "1")
            if 1 <= selection <= len(authors):
                break
            print(f"Please enter a number between 1 and {len(authors)}")
        except ValueError:
            print("Please enter a valid number")
    
    # Fill in author data without progress bar
    author = scholarly.fill(authors[selection - 1], sections=['publications'])

    # Get publication data
    with click.progressbar(length=2, label='Fetching data') as bar:
        years, counts = get_publication_years(author)
        bar.update(2)

    # Create and save plot
    create_plot(years, counts, author['name'], style, context)
    output_file = save_plot(output_dir, author['name'])
    click.secho(f"\nPlot saved as: {output_file}", fg='green')
    
    # Output data
    print_year_counts(years, counts) 