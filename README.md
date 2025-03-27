# KodeKloud Computer Quest

An educational text-based adventure game that teaches computer architecture concepts.

![KodeKloud Computer Quest](https://img.shields.io/badge/KodeKloud-Computer%20Quest-blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

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

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/kodekloud-computer-quest.git
cd kodekloud-computer-quest

# Optional: Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the game
pip install -e .

# Run the game
python main.py
```

## Detailed Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Options

#### Basic Installation

For end-users who just want to play the game:

```bash
# Install from the cloned repository
pip install -e .

# Run the game
python main.py
```

#### Development Installation

For developers who want to contribute or modify the game:

```bash
# Install development dependencies
pip install -e ".[dev]"
pip install -r requirements.txt

# Or use the Makefile
make dev-install
```

## Usage

### Game Commands

The game supports a wide range of commands, including:

- Movement: `north` (n), `south` (s), `east` (e), `west` (w), etc.
- Exploration: `look` (l), `map` (m), `motherboard` (mb)
- Inventory: `inventory` (i), `take` (t), `drop` (d)
- Security: `scan` (s), `analyze` (a), `quarantine` (q)
- Information: `help` (h), `about`, `knowledge` (k)
- Educational: `visualize` (v), `simulate` (sim)

Type `help` in-game for a complete list of commands.

### Game Mechanics

- **Exploration**: Navigate through the computer system using directional commands
- **Knowledge**: Learn about computer components by visiting and interacting with them
- **Security**: Find and neutralize viruses using scan, analyze, and quarantine commands
- **Progression**: Track your progress with the knowledge and progress systems

## For Developers

### Project Structure

The codebase follows a modular design with clear separation of concerns:

```
.
├── computerquest/       # Main package
│   ├── models/          # Data models (Component, Player)
│   ├── world/           # World generation (Architecture)
│   ├── mechanics/       # Game mechanics (Progress, Minigames)
│   └── utils/           # Utility functions
├── data/                # Game data files
├── tests/               # Unit tests for all modules
└── docs/                # Documentation
```

### Development Tools

The project uses several tools to maintain code quality:

- **pytest**: For unit testing
- **pytest-cov**: For test coverage reporting
- **black**: For code formatting
- **isort**: For import sorting
- **pylint**: For code linting
- **flake8**: For style checking
- **mypy**: For static type checking

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test modules
python tests/run_tests.py component  # Tests the Component class
python tests/run_tests.py player     # Tests the Player class

# Generate coverage report
python tests/run_tests.py --coverage

# Or use the Makefile
make test       # Run all tests
make coverage   # Generate coverage report
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type check
make typecheck
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`make dev-install`)
4. Write tests for your changes
5. Format your code (`make format`)
6. Ensure all tests pass (`make test`)
7. Run linting checks (`make lint`)
8. Ensure type checking passes (`make typecheck`)
9. Commit your changes
10. Push to the branch
11. Open a Pull Request

## Testing Strategy

The project follows these testing principles:
- **Test-Driven Development**: Write tests before implementing features
- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test interactions between components
- **Comprehensive Coverage**: Aim for high test coverage across all modules

## License

This project is licensed under the MIT License - see the LICENSE file for details.