# Contributing to Techno Generator

Thank you for your interest in contributing! This guide will help you set up your development environment and understand our workflow.

## 🚀 Quick Setup

### Prerequisites

- Python 3.10, 3.11, or 3.12
- Git
- FFmpeg
- UV package manager

### Initial Setup

```
# 1. Fork the repository on GitHub
# Click "Fork" at https://github.com/TataSatyaPratheek/techno

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/techno.git
cd techno

# 3. Add upstream remote
git remote add upstream https://github.com/TataSatyaPratheek/techno.git

# 4. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# 5. Install dependencies
uv sync

# 6. Verify setup
uv run pytest
```

## 🧪 Development Workflow

### 1. Create a Branch

```
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

```
# Edit code
# Write tests
# Update documentation
```

### 3. Test Your Changes

```
# Run all tests
uv run pytest

# Run specific tests
uv run pytest tests/test_timing.py -v

# Check coverage
uv run pytest --cov=techno --cov-report=html
```

### 4. Format and Lint

```
# Format code
uv run black src/techno tests

# Sort imports
uv run isort src/techno tests

# Type check
uv run mypy src/techno

# Lint
uv run flake8 src/techno tests --max-line-length=127
```

### 5. Commit Changes

```
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new subgenre support for hard techno"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Open Pull Request
```
1. Go to https://github.com/TataSatyaPratheek/techno
2. Click "Pull Requests" → "New Pull Request"
3. Select your fork and branch
4. Fill in description
5. Submit PR
```

## 📝 Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

### Examples

```
feat(mixers): add hard techno mixer
fix(timing): correct BPM calculation for 140+ tempos
docs(readme): update installation instructions
test(composition): add integration tests for structure
```

## 🧪 Testing Guidelines

### Writing Tests

```
# tests/test_new_feature.py
import pytest
from techno.your_module import YourClass


class TestYourClass:
    """Test YourClass functionality"""
    
    def test_basic_functionality(self):
        """Test basic usage"""
        obj = YourClass(param=123)
        result = obj.method()
        assert result == expected_value
    
    def test_edge_case(self):
        """Test edge case"""
        obj = YourClass(param=0)
        with pytest.raises(ValueError):
            obj.method()
```

### Test Coverage

```
- Aim for >90% coverage
- Test edge cases and error conditions
- Write docstrings for test classes and methods
```

### Running Tests

```
# All tests
uv run pytest

# Specific file
uv run pytest tests/test_timing.py

# Specific test
uv run pytest tests/test_timing.py::TestTimingCalculator::test_bars_to_ms

# With coverage
uv run pytest --cov=techno --cov-report=term-missing

# Verbose output
uv run pytest -vv
```

## 📚 Documentation

### Docstring Format

Use Google-style docstrings:

```
def generate_track(bpm: int, subgenre: str) -> AudioSegment:
    """Generate techno track.
    
    Args:
        bpm: Beats per minute (100-180)
        subgenre: Subgenre name ('minimal', 'industrial', etc.)
    
    Returns:
        AudioSegment containing generated track
    
    Raises:
        ValueError: If BPM is out of range
    
    Example:
        >>> track = generate_track(130, 'minimal')
        >>> track.export("output.wav", format="wav")
    """
```

### Update README

```
If you add features, update:
- Usage examples
- API documentation
- Roadmap
```

## 🎯 Pull Request Checklist

Before submitting:
```
- [ ] Tests pass locally (`uv run pytest`)
- [ ] Code is formatted (`uv run black .`)
- [ ] Imports are sorted (`uv run isort .`)
- [ ] Type checks pass (`uv run mypy src/techno`)
- [ ] Linting passes (`uv run flake8 src/techno tests`)
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (if significant change)
- [ ] Commit messages follow convention
```

## 🐛 Bug Reports

### Before Reporting
```
1. Search existing issues
2. Verify bug exists in latest version
3. Try minimal reproduction
```

### Bug Report Template

```
## Bug Description: Brief description

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Ubuntu 24.04
- Python: 3.12.1
- Package version: 0.1.0

## Minimal Example

## Additional Context
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Feature Request Template

```
## Feature Description
What feature do you want?

## Use Case
Why is this useful?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches?

## Additional Context
Mockups, examples, etc.
```

## 🤔 Questions?

- Open a [GitHub Discussion](https://github.com/TataSatyaPratheek/techno/discussions)
- Check existing issues
- Read documentation

## 📜 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow GitHub's Community Guidelines

## 🎉 Recognition

Contributors are recognized in:
- GitHub contributors list
- CHANGELOG.md for significant contributions
- Special thanks in releases

---
Thank you for contributing! 🎵
