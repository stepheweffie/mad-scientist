# Contributing to Mad Scientist AI

Thank you for your interest in contributing to Mad Scientist AI! We welcome contributions from the community and are excited to see what you'll build.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A Cloudflare account with AI API access (for testing)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mad-scientist.git
   cd mad-scientist
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the development server**
   ```bash
   export LOG_LEVEL=DEBUG
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📋 Code of Conduct

### Our Standards

- **Be Respectful**: Treat all contributors with respect and kindness
- **Be Inclusive**: Welcome people of all backgrounds and experience levels
- **Focus on Responsible AI**: Keep the project's mission of responsible AI development in mind
- **Scientific Accuracy**: Maintain high standards for scientific information and guard rails

### Unacceptable Behavior

- Harassment, discrimination, or offensive language
- Spam or self-promotion unrelated to the project
- Publishing others' private information without permission
- Any behavior that would be inappropriate in a professional setting

## 🛠️ How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Fixes**: Fix issues or improve existing functionality
- **Features**: Add new capabilities or AI models
- **Documentation**: Improve README, code comments, or guides
- **Testing**: Add test coverage or improve existing tests
- **UI/UX**: Enhance the user interface and experience
- **Performance**: Optimize code or reduce resource usage

### Contribution Process

1. **Check existing issues** to see if your idea is already being worked on
2. **Create an issue** to discuss new features or major changes
3. **Fork the repository** and create a feature branch
4. **Make your changes** following our coding standards
5. **Test your changes** thoroughly
6. **Submit a pull request** with a clear description

### Branch Naming

Use descriptive branch names:
- `feature/add-new-model`
- `fix/session-timeout-bug`
- `docs/update-installation-guide`
- `refactor/improve-logging`

### Commit Messages

Write clear, descriptive commit messages:

```
Add comprehensive error handling for API calls

- Implement retry logic for network failures
- Add specific error messages for different failure types
- Update logging to capture error details
- Add tests for error scenarios

Fixes #123
```

## 🧪 Testing

### Manual Testing

1. Test all major functionality:
   - Avatar generation
   - Chat interactions
   - Session management
   - Error handling

2. Test with different configurations:
   - Different log levels
   - Various AI models
   - Edge cases and error conditions

### Automated Testing

While we're working on comprehensive test coverage, please ensure:
- Your code doesn't break existing functionality
- New features include basic validation
- Error handling is properly implemented

## 📝 Documentation

### Code Documentation

- Add docstrings to new functions and classes
- Include type hints where appropriate
- Comment complex logic or algorithms
- Update README.md if you change functionality

### Example Documentation

```python
async def generate_avatar(request: Request, model: str, prompt: str) -> str:
    \"\"\"
    Generate an AI avatar using the specified model and prompt.
    
    Args:
        request: FastAPI request object for session management
        model: Name of the AI model to use for generation
        prompt: Text prompt describing the desired avatar
        
    Returns:
        Data URL string containing the generated image
        
    Raises:
        HTTPException: If the API call fails or model is not found
    \"\"\"
```

## 🔍 Code Style

### Python Style Guide

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Keep functions focused and reasonably sized
- Use async/await for I/O operations
- Handle errors gracefully with appropriate logging

### Import Organization

```python
# Standard library imports
import os
import logging
from typing import Any, Dict

# Third-party imports
import requests
from fastapi import FastAPI, HTTPException

# Local imports
from logging_config import get_logger
from mad_scientist import MadScientist
```

## 🚨 Security Guidelines

### Environment Variables

- Never commit API keys or secrets to the repository
- Use the `.env` file for local development
- Document all required environment variables
- Use meaningful default values where possible

### Input Validation

- Validate all user inputs
- Sanitize data before processing
- Use appropriate error messages that don't leak sensitive information
- Implement rate limiting where appropriate

## 🤖 AI Model Guidelines

### Adding New Models

When adding new AI models:

1. **Update the models list** in `mad_scientist.py`
2. **Test thoroughly** with various inputs
3. **Document capabilities** and limitations
4. **Consider guard rails** for responsible AI use
5. **Update the README** with model information

### Responsible AI Practices

- Implement appropriate content filtering
- Add warnings for potentially sensitive outputs
- Maintain transparency about model capabilities
- Consider bias and fairness implications

## 📦 Release Process

### Versioning

We follow semantic versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Test deployment on staging
- [ ] Update documentation
- [ ] Create GitHub release with notes

## 💬 Communication

### Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Pull Request Comments**: For code review discussions

### Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the problem
2. **Steps to Reproduce**: Detailed steps to recreate the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: Python version, OS, browser (if applicable)
6. **Logs**: Relevant log entries (remove sensitive information)

### Feature Requests

For feature requests, please include:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: What alternatives have you considered?
4. **Additional Context**: Any other relevant information

## 🙏 Recognition

Contributors will be recognized in:
- The project README
- Release notes for their contributions
- GitHub's contributor graph

## 📞 Questions?

If you have questions about contributing, please:
1. Check this guide and the README
2. Search existing issues and discussions
3. Create a new discussion for general questions
4. Create an issue for specific problems

Thank you for contributing to Mad Scientist AI! Together, we can build amazing and responsible AI tools. 🧪✨
