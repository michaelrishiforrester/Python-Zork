"""
Helper utilities for KodeKloud Computer Quest
"""

def prefix_match(prefix, candidates):
    """
    Match a prefix with candidates, return the full string if unique match is found
    
    Args:
        prefix (str): The prefix to match
        candidates (list): List of possible matches
        
    Returns:
        str: The full match if unique, otherwise the original prefix
    """
    if len(prefix) < 2:
        return prefix  # Don't try to match single-letter prefixes
        
    # Check for exact match first
    if prefix in candidates:
        return prefix
        
    # Check for prefix match
    matches = [item for item in candidates if item.startswith(prefix)]
    
    # Return the matched item if only one match, otherwise return original
    if len(matches) == 1:
        return matches[0]
    else:
        return prefix

def format_box(title, content, width=70):
    """
    Create a nicely formatted text box
    
    Args:
        title (str): Title for the box
        content (str): Content to display in the box
        width (int): Width of the box
        
    Returns:
        str: Formatted text box
    """
    result = "+" + "-" * width + "+\n"
    result += "|" + title.center(width) + "|\n"
    result += "+" + "-" * width + "+\n"
    
    for line in content.split('\n'):
        result += "| " + line.ljust(width-1) + "|\n"
    
    result += "+" + "-" * width + "+"
    return result

def truncate_desc(desc, max_length=50):
    """
    Truncate description to a reasonable length
    
    Args:
        desc (str): Description to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated description
    """
    if not desc:
        return ""
        
    # Get first sentence or use whole string
    short_desc = desc.split('.')[0] if '.' in desc else desc
    
    # Truncate if too long
    if len(short_desc) > max_length:
        short_desc = short_desc[:max_length-3] + "..."
        
    return short_desc

def format_list(items, prefix="- "):
    """
    Format a list of items with prefixes
    
    Args:
        items (list): List of items to format
        prefix (str): Prefix for each line
        
    Returns:
        str: Formatted list as string
    """
    if not items:
        return ""
        
    return "\n".join(f"{prefix}{item}" for item in items)