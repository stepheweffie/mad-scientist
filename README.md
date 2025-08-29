# 🧪 Mad Scientist AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.108.0-009688.svg)](https://fastapi.tiangolo.com/)

[![CI](https://github.com/stepheweffie/mad-scientist/actions/workflows/ci.yml/badge.svg)](https://github.com/stepheweffie/mad-scientist/actions/workflows/ci.yml)
[![CD](https://github.com/stepheweffie/mad-scientist/actions/workflows/cd.yml/badge.svg)](https://github.com/stepheweffie/mad-scientist/actions/workflows/cd.yml)
[![Security](https://github.com/stepheweffie/mad-scientist/actions/workflows/security.yml/badge.svg)](https://github.com/stepheweffie/mad-scientist/actions/workflows/security.yml)
[![Docker](https://ghcr.io/stepheweffie/mad-scientist/badges/latest/size)](https://github.com/stepheweffie/mad-scientist/pkgs/container/mad-scientist)
[![Release](https://img.shields.io/github/v/release/stepheweffie/mad-scientist)](https://github.com/stepheweffie/mad-scientist/releases)

An open-source AI chat interface with avatar generation, built as a guard railing project to promote responsible AI development and community collaboration.

## ✨ Features

- 🤖 **Multi-Model AI Chat**: Support for multiple language models (Mistral-7B, Hermes 2 Pro)
- 🎨 **AI Avatar Generation**: Create custom avatars with Dreamshaper-8 LCM
- 🔒 **Responsible AI**: Built-in guard rails for scientific accuracy and disambiguation
- 📊 **Comprehensive Logging**: Detailed logging system with rotating files
- 🔧 **Easy Deployment**: Ready for Digital Ocean App Platform
- ⚡ **FastAPI Backend**: High-performance async Python web framework
- 🎯 **Session Management**: Persistent chat sessions with state tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Cloudflare AI API access (for model inference)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/stepheweffie/mad-scientist.git
   cd mad-scientist
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration values
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Open your browser**
   Navigate to `http://localhost:8000`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Cloudflare API Configuration
API_BASE_URL=https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/
ACCOUNT_ID=your_cloudflare_account_id
AUTH_TOKEN=your_cloudflare_api_token

# Application Configuration
SECRET_KEY=your_secret_key_for_sessions
GTAG=your_google_analytics_tag

# Logging Configuration
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Cloudflare Setup

1. Create a [Cloudflare account](https://cloudflare.com)
2. Get your Account ID from the Cloudflare dashboard
3. Generate an API token with AI permissions
4. Update your `.env` file with these credentials

## 🏗️ Architecture

### Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML/CSS with Jinja2 templates
- **AI Models**: Cloudflare Workers AI
- **Session Management**: Starlette sessions
- **Logging**: Python logging with rotating file handlers

### Project Structure

```
mad-scientist/
├── main.py              # FastAPI application and routes
├── mad_scientist.py     # Core AI interaction logic
├── logging_config.py    # Logging configuration
├── static.py           # CSS styles
├── templates/          # HTML templates
│   └── chat.html       # Chat interface template
├── requirements.txt    # Python dependencies
├── .env.example       # Environment configuration template
├── Dockerfile         # Container configuration
└── logs/              # Application logs (created at runtime)
```

## 🤖 Available AI Models

### Text Models
- **Mad Sci Mistral-7B Instruct**: Fine-tuned for scientific accuracy
- **Mistral-7b Instruct**: General-purpose instruction following
- **Hermes 2 Pro on Mistral 7B**: Enhanced reasoning and function calling

### Image Models
- **Dreamshaper-8 LCM**: Photorealistic image generation

## 📝 Logging

The application includes comprehensive logging:

- **Console Output**: Real-time application status
- **File Logging**: Rotating log files in `logs/` directory
  - `mad_scientist.log`: General application logs
  - `mad_scientist_errors.log`: Error-specific logs
- **Log Levels**: Configurable via `LOG_LEVEL` environment variable

## 🚀 Deployment

### Digital Ocean App Platform

1. Fork this repository to your GitHub account
2. Visit the [Digital Ocean App Platform setup](https://cloud.digitalocean.com/apps/new?source_provider=github&i=8b9068)
3. Connect your forked repository
4. Add your environment variables in the Digital Ocean dashboard
5. Deploy!

### Docker

```bash
# Build the image
docker build -t mad-scientist .

# Run the container
docker run -p 8000:8000 --env-file .env mad-scientist
```

### Manual Deployment

1. Set up your server with Python 3.8+
2. Clone and configure the application
3. Use a process manager like `systemd` or `supervisor`
4. Set up a reverse proxy (nginx/Apache) for production

## 🛡️ Guard Rails & Responsible AI

This project emphasizes responsible AI development:

- **Scientific Accuracy**: The Mad Scientist persona focuses on disambiguating scientific terms
- **Error Correction**: Built-in logic to identify and correct common misconceptions
- **Transparency**: Open-source code for community review and improvement
- **Logging**: Comprehensive monitoring for debugging and accountability

## 🔄 CI/CD Pipeline

Mad Scientist AI features a comprehensive CI/CD pipeline with GitHub Actions:

### 🧪 Continuous Integration (CI)

- **Code Quality**: Linting with flake8, Black, and isort
- **Testing**: Multi-version Python testing (3.9, 3.10, 3.11)
- **Security**: Bandit, Safety, and vulnerability scanning
- **Docker**: Container build validation
- **Health Checks**: Application startup and endpoint testing

### 🚀 Continuous Deployment (CD)

- **Multi-Platform Builds**: AMD64 and ARM64 Docker images
- **Registry**: Automatic publishing to GitHub Container Registry
- **Security Scanning**: Trivy container vulnerability scanning
- **Environments**: Automated staging and production deployments
- **Rollback**: Automatic rollback on deployment failures

### 🔒 Security Workflows

- **Dependency Scanning**: Weekly security vulnerability checks
- **Code Analysis**: Static analysis with multiple tools
- **License Compliance**: Automated license checking
- **Automated Updates**: Dependency update PRs

### 📋 Workflow Triggers

| Workflow | Trigger | Purpose |
|----------|---------|----------|
| CI | Push/PR to main | Code quality and testing |
| CD | Push to main, releases | Build and deploy |
| Security | Weekly, PR | Security scanning |
| Release | Conventional commits | Automated releases |
| PR Checks | Pull requests | Fast validation |

### 🏷️ Release Management

- **Semantic Versioning**: Automated version bumping
- **Conventional Commits**: Automatic changelog generation
- **GitHub Releases**: Automated release creation
- **Docker Tags**: Multiple tag strategies (latest, semver, SHA)

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md):

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with debug logging
export LOG_LEVEL=DEBUG
uvicorn main:app --reload
```

### Commit Convention

We use [Conventional Commits](https://conventionalcommits.org/) for automated releases:

```
feat: add new AI model support
fix: resolve session timeout issue
docs: update installation guide
chore: update dependencies
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/stepheweffie/mad-scientist/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/stepheweffie/mad-scientist/discussions)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [Cloudflare](https://cloudflare.com) for AI model hosting
- The open-source community for inspiration and tools

---

**Built with ❤️ for responsible AI development**
