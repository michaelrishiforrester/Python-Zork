# Contributing to KodeKloud Computer Quest

Thank you for considering contributing to KodeKloud Computer Quest! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We value inclusivity and welcome contributions from people of all backgrounds and experience levels.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a branch for your changes

```bash
# Clone your fork
git clone https://github.com/yourusername/computer-quest.git
cd computer-quest

# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
make dev-install  # Or: pip install -e ".[dev]" && pip install -r requirements.txt

# Create a branch
git checkout -b feature/your-feature-name
```

## Development Workflow

We follow a test-driven development (TDD) approach:

1. Write tests that define the expected behavior
2. Implement the feature or fix
3. Verify that the tests pass
4. Refactor as needed

### Testing

Always write tests for your changes. The project uses pytest for testing:

```bash
# Run all tests
python tests/run_tests.py

# Run specific tests
python tests/run_tests.py component

# Generate coverage report
python tests/run_tests.py --coverage
```

### Code Quality

Before submitting a pull request, make sure your code meets our quality standards:

```bash
# Format code
make format  # Or: black computerquest tests && isort computerquest tests

# Run linting
make lint  # Or: pylint computerquest tests && flake8 computerquest tests

# Type checking
make typecheck  # Or: mypy computerquest tests
```

## Pull Request Process

1. Update the README.md and documentation with details of your changes, if applicable
2. Update the CHANGELOG.md with a description of your changes
3. Ensure all tests pass and code quality checks succeed
4. Submit a pull request to the main repository

### Pull Request Guidelines

- Use a clear and descriptive title
- Include a detailed description of the changes
- Reference any related issues
- Update documentation as needed

## Adding New Features

When adding new features, follow these guidelines:

1. **Modular Design**: Keep components separate and focused
2. **Clean APIs**: Design clear and consistent interfaces
3. **Educational Value**: Remember that the game is educational - new features should help teach computer architecture concepts
4. **Documentation**: Document new features thoroughly

## Educational Content Guidelines

Since this is an educational game about computer architecture:

1. Accuracy is important - ensure technical information is correct
2. Make complex concepts accessible without oversimplification
3. Use appropriate terminology consistent with computer architecture education
4. Balance fun gameplay with educational value

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.

## Questions

If you have any questions or need help, please open an issue on GitHub.