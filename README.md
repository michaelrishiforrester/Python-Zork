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

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kodekloud-computer-quest.git
cd kodekloud-computer-quest

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.