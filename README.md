# KodeKloud Computer Quest

An educational text-based adventure game that teaches computer architecture concepts.

## Overview

KodeKloud Computer Quest is an interactive text adventure where players navigate through a computer system, learning about various hardware components while searching for and neutralizing viruses. The game simulates the internals of a modern computer, from the CPU cores to memory, storage, and peripherals.

## Features

- Detailed simulation of computer architecture components
- Exploration-based learning of computer hardware concepts
- Virus hunting gameplay that teaches security concepts
- Progressive knowledge system that tracks player learning
- Mini-games that demonstrate CPU pipelines and memory hierarchies
- Save/load system to preserve progress
- Enhanced UI with improved visuals and readability

## UI Improvements

The interface has been updated with several visual improvements:

1. **Enhanced Box Formatting**
   - Unicode box drawing characters for better-looking UI
   - Consistent styling for all game sections
   - Improved readability with clear section dividers

2. **Directional Information**
   - ASCII Directional Compass showing available paths
   - Improved formatting for direction names
   - Clearer connections between components

3. **Clearer Structure & Organization**
   - Better section separation with themed headers
   - Aligned component lists with bullet points
   - Improved status display

4. **Progress Visualization**
   - Progress bars for virus discovery and quarantine
   - Knowledge level indicators with visual meters
   - Overall progress tracking

5. **Command Shortcuts Reference**
   - Quick reference for command shortcuts
   - Movement shortcuts clearly displayed
   - One-letter shortcuts for common actions

6. **Status Line**
   - Current health and inventory capacity
   - Virus discovery and quarantine progress
   - Available command shortcuts

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kodekloud-computer-quest.git
cd kodekloud-computer-quest

# Optional: Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the game
python main.py
```

## Commands

The game supports a wide range of commands, including:

- Movement: `north`, `south`, `east`, `west`, etc.
- Exploration: `look`, `map`, `motherboard`
- Inventory: `inventory`, `take`, `drop`
- Security: `scan`, `analyze`, `quarantine`
- Information: `help`, `about`, `knowledge`
- Educational: `visualize`, `simulate`

Type `help` in-game for a complete list of commands.

## Project Structure

The codebase follows a modular design with clear separation of concerns:

- `computerquest/`: Main package
  - `models/`: Data models (Component, Player)
  - `world/`: World generation (Architecture)
  - `mechanics/`: Game mechanics (Progress, Minigames)
  - `utils/`: Utility functions
- `data/`: Game data files
- `tests/`: Unit tests for all modules

## Testing

The project includes a comprehensive test suite to ensure all components function correctly.

### Running the Tests

To run all tests:

```bash
# Run all tests
python tests/run_tests.py

# Run a specific test module
python tests/run_tests.py component  # Tests the Component class
python tests/run_tests.py player     # Tests the Player class
python tests/run_tests.py commands   # Tests the Command pattern implementation
```

### Test Coverage

The test suite covers:
- Component and Player models
- Command pattern implementation
- Game controller logic
- Progress tracking
- World generation
- Helper utilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`python tests/run_tests.py`)
5. Commit your changes
6. Push to the branch
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.