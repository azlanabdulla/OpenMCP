# OpenMCP

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-black?style=flat&logo=next.js)](https://nextjs.org/)

**The Open Marketplace for AI Tools.**

OpenMCP is the world's largest open-source registry and package manager for MCP (Model Context Protocol) servers, AI tools, and AI plugins. It provides a mature, production-grade ecosystem—similar to npm, Docker Hub, or PyPI—but exclusively for the AI era.

---

## 🌟 Features

### For Developers
- **Publish & Manage:** Easily publish, update, and delete your AI tools and MCP servers.
- **Analytics:** Track daily/weekly/monthly installs, active users, and version usage via a comprehensive dashboard.
- **Organization Support:** Create organizations, invite members, and manage permissions.
- **Security:** Package signatures, checksum verification, and malware scanning hooks.

### For Users
- **Search & Discover:** Find tools by category, popularity, tags, and verified publishers.
- **Install & Use:** Seamlessly install tools via the `openmcp` CLI.
- **Review & Rate:** Leave reviews, rate tools, and bookmark your favorites.

---

## 🏗 Architecture

OpenMCP consists of four tightly-integrated components:

1. **CLI (`cli/`)**: A powerful Python Typer-based command-line interface for publishing and installing packages.
2. **Registry API (`backend/`)**: A fast, robust FastAPI backend utilizing SQLAlchemy, PostgreSQL, and Redis (via Celery) for background jobs.
3. **Web Marketplace (`frontend/`)**: A modern Next.js and TailwindCSS web application for discovering and managing tools.
4. **Developer SDK (`sdk/`)**: Native Python and JavaScript SDKs for interacting with the registry programmatically.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker and Docker Compose
- `pnpm` (for frontend)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/OpenMCP/OpenMCP.git
   cd OpenMCP
   ```

2. **Start Infrastructure Services**
   ```bash
   make up
   ```
   This will start PostgreSQL and Redis via Docker Compose.

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

---

## 💻 CLI Usage Examples

```bash
# Login to OpenMCP
openmcp login

# Install a tool
openmcp install github
openmcp install weather

# Publish your own tool
openmcp publish

# Search for tools
openmcp search "weather API"

# View tool info
openmcp info github
```

---

## 🔌 Plugin Format

Each plugin must include a `manifest.json` file. Here is an example:

```json
{
  "name": "github",
  "description": "GitHub MCP Server",
  "version": "1.0.0",
  "author": "OpenMCP",
  "license": "MIT",
  "repository": "https://github.com/OpenMCP/example-github",
  "homepage": "https://openmcp.org",
  "keywords": ["github", "mcp", "git"],
  "entry": "server.py",
  "dependencies": []
}
```

---

## 🛣 Roadmap

- [x] Core architecture & repository structure
- [ ] FastAPI backend & Database Models
- [ ] Authentication (GitHub OAuth, JWT)
- [ ] Web Marketplace (Next.js)
- [ ] CLI (Typer, Rich)
- [ ] Plugin verification & Malware scanning
- [ ] AI recommendations
- [ ] Enterprise edition (Private registries)
- [ ] VS Code extension

---

## 🤝 Contribution Guide

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to set up your development environment, run tests, and submit Pull Requests.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
