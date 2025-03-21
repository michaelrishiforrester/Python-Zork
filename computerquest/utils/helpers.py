"""
Helper utilities for KodeKloud Computer Quest
"""
import textwrap
from computerquest.config import DIRECTION_NAMES

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

def format_fancy_box(title, content, width=70, border_char="━"):
    """
    Create a fancy formatted text box with unicode characters
    
    Args:
        title (str): Title for the box
        content (str): Content to display in the box
        width (int): Width of the box
        border_char (str): Character to use for borders
        
    Returns:
        str: Formatted fancy text box
    """
    result = "┏" + border_char * (width-2) + "┓\n"
    result += "┃ " + title.ljust(width-4) + " ┃\n"
    result += "┗" + border_char * (width-2) + "┛\n"
    
    # Process content lines
    for line in content.split('\n'):
        result += "  " + line + "\n"
    
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

def format_look_output(location, connections, items, technical_details=None):
    """
    Format the look command output for better readability.
    
    Args:
        location: Component object with name and description
        connections: Dictionary of directions and connected components
        items: Dictionary of items in the location
        technical_details: Optional list of technical details to display
        
    Returns:
        str: Formatted look output
    """
    output = []
    
    # Location header
    output.append("┏" + "━" * 20 + " LOCATION " + "━" * 20 + "┓")
    output.append(f"  {location.name}")
    output.append("┗" + "━" * 51 + "┛\n")
    
    # Description
    output.append("Description:")
    description_lines = textwrap.wrap(location.desc, width=70)
    output.extend([f"  {line}" for line in description_lines])
    output.append("")
    
    # Connections
    output.append("┏" + "━" * 18 + " AVAILABLE CONNECTIONS " + "━" * 18 + "┓")
    
    # Format regular connections
    reg_connections = []
    for direction, connected_room in connections.items():
        dir_name = DIRECTION_NAMES.get(direction, direction).upper()
        if len(dir_name) == 1:
            reg_connections.append(f"[{dir_name}]orth: {connected_room.name}")
        elif len(dir_name) == 2:
            reg_connections.append(f"[{dir_name}]: {connected_room.name}")
        else:
            reg_connections.append(f"[{dir_name[0]}]{dir_name[1:]}: {connected_room.name}")
    
    # Split into lines of 2-3 connections each
    conn_lines = []
    for i in range(0, len(reg_connections), 3):
        conn_lines.append("  " + "  ".join(reg_connections[i:i+3]))
    
    output.extend(conn_lines)
    output.append("┗" + "━" * 60 + "┛\n")
    
    # Create ASCII directional compass
    compass = [
        "      N      ",
        "    NW NE    ",
        "   W  +  E   ",
        "    SW SE    ",
        "      S      "
    ]
    
    # Add directional compass only if has enough directions
    if len(connections) > 1:
        output.append("  Directional Compass:")
        available_directions = connections.keys()
        for line in compass:
            output.append(f"  {line}")
    
    # Components
    if items:
        output.append("\n┏" + "━" * 20 + " COMPONENTS " + "━" * 20 + "┓")
        for item in items:
            output.append(f"  • {item}")
        output.append("┗" + "━" * 51 + "┛")
        output.append("\nType 'examine [component]' or 'take [component]' to interact.\n")
    
    # Technical details if visited
    if technical_details:
        output.append("┏" + "━" * 19 + " TECHNICAL DETAILS " + "━" * 19 + "┓")
        for line in technical_details:
            output.append(f"  {line}")
        output.append("┗" + "━" * 51 + "┛")
    
    # Status line
    total_viruses = 5  # Total number of viruses from config
    output.append("\n" + "━" * 70)
    output.append(f"  Status: Items: {len(items)}/8 | Viruses: {len(location.items.get('found_viruses', []))}/{total_viruses} Found, {len(location.items.get('quarantined_viruses', []))}/{total_viruses} Quarantined")
    output.append("  Commands: [L]ook [I]nventory [T]ake [H]elp [M]ap [Q]uit")
    output.append("━" * 70)
    
    return "\n".join(output)