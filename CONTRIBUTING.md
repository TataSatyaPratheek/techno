# Contributing to Techno Music Generator

Thank you for your interest in contributing to the Techno Music Generator! This document provides guidelines and information for contributors.

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## How to Contribute

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/yourusername/techno.git
   cd techno
   ```

3. **Set up the development environment** (project uses a `src/` layout):

   ```bash
   # Create the environment and install dev deps
   uv sync --dev

   # Editable install so your local edits are active
   pip install -e .
   ```

4. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Workflow

1. **Make your changes** following the coding standards
2. **Add tests** for new functionality
3. **Run the test suite**:
   ```bash
   uv run pytest
   ```
4. **Check code quality**:
   ```bash
   uv run black .
   uv run isort .
   uv run mypy src/techno
   ```

Note: CI runs a strict check pipeline; prefer using the `uv run` invocations above (they are configured to run tools against the `src/` package layout).

For a concise developer quickstart and instructions for building local wheels (private distribution), see the `Developer quickstart` and `Local release / private wheel (HOWTO)` sections in `README.md`.

### Repository publishing policy

This repository is not published to PyPI and there is no automated publishing configured for public release. The project is intended for local development, research, and private use. If maintainers later decide to publish, they should:

- Add clear release notes and a changelog entry.
- Ensure reviewers and maintainers agree to the release.
- Add publishing automation and repository secrets deliberately and separately from development changes.

## Development Workflow (continuation)

1. **Commit your changes**:

   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

1. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

1. **Create a Pull Request** on GitHub

```text
src/techno/
├── cli/                 # Command-line interface
├── core/                # Core audio primitives
├── composition/         # Musical composition algorithms
├── generators/          # Audio generators and synthesizers
├── mixers/              # Mixing and mastering tools
├── processing/          # Audio effects and processing
├── presets/             # Style presets and configurations
└── tests/               # Test suite
```

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:

```text
1. `feat`: New feature
1. `fix`: Bug fix
1. `docs`: Documentation changes
1. `style`: Code style changes
1. `refactor`: Code refactoring
1. `test`: Test additions/changes
1. `chore`: Maintenance tasks
```

Examples:

```text
feat(generator): add industrial techno style support
fix(mixer): resolve audio clipping in high-gain scenarios
docs(readme): update installation instructions
```

### Testing

- Maintain test coverage above 90%
- Write unit tests for all new functions
- Write integration tests for complex workflows
- Use descriptive test names and docstrings

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions
- Update CHANGELOG.md for significant changes
- Keep code comments clear and helpful

## Project Structure

```text
src/techno/
├── cli/                 # Command-line interface
├── core/                # Core audio primitives
├── composition/         # Musical composition algorithms
├── generators/          # Audio generators and synthesizers
├── mixers/              # Mixing and mastering tools
├── processing/          # Audio effects and processing
├── presets/             # Style presets and configurations
└── tests/               # Test suite
```

## Audio Development Guidelines

When working with audio generation:

- **Sample rates**: Use 44100 Hz as default
- **Bit depth**: Use 16-bit PCM for WAV files
- **Normalization**: Keep audio levels between -1.0 and 1.0
- **Performance**: Optimize for real-time generation where possible
- **Testing**: Use short durations for automated tests

## Pull Request Process

1. **Ensure CI passes** - All tests and linting must pass
2. **Update documentation** - README, CHANGELOG, etc.
3. **Squash commits** - Combine related commits into logical units
4. **Write clear PR description** - Explain what and why
5. **Request review** - Tag maintainers for review

## Issue Reporting

When reporting bugs:

- Use the issue template
- Include Python version, OS, and dependency versions
- Provide minimal reproduction case
- Include error messages and stack traces
- Describe expected vs. actual behavior

## Feature Requests

For new features:

- Check existing issues first
- Describe the use case clearly
- Explain why it's needed
- Consider implementation complexity
- Be open to alternative solutions

## Recognition

Contributors will be recognized in:

- CHANGELOG.md for significant contributions
- GitHub repository contributors list
- Project documentation

Thank you for contributing to the Techno Music Generator! 🎵
