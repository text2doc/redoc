# 🌀 redoc

**Multi-Level Solution Architecture Generator**

redoc is a powerful AI tool that uses Ollama Mistral:7b to generate multi-level solution architectures. Inspired by the movie "Inception", it creates nested tasks leading to complete implementations.

## ✨ Key Features

- 🧠 **AI-Powered**: Integration with Ollama Mistral:7b
- 🏗️ **Multi-Level**: 3-5 levels of architecture (LIMBO → DREAM → REALITY → DEEPER → DEEPEST)
- 🔍 **Context-Aware**: Automatic context analysis from a single sentence
- 💻 **Interactive CLI**: Rich shell interface
- 📊 **Structured Output**: JSON/YAML export
- 🚀 **Zero-Setup**: Works out of the box with local Ollama

## 🚀 Quick Start

```bash
# Installation
pip install redoc

# Basic usage
redoc "I need a login system with Flask + React"

# Interactive shell
redoc shell
```

[Get Started →](quick-start.md){ .md-button .md-button--primary }
```

## 📦 Installation

### System Requirements

- Python 3.8+
- Ollama with Mistral:7b model
- 4GB RAM (minimum)
- Internet connection (for model download)

### Installing Ollama

### macOS/Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral:7b
```

### Windows
[Pobierz installer](https://ollama.ai/download) i uruchom:
```cmd
ollama pull mistral:7b
```

## Instalacja redoc

### Przez pip (Recommended)
```bash
pip install redoc
```

### Z źródła
```bash
git clone https://github.com/yourusername/redoc.git
cd redoc
pip install -e .
```

### Development setup
```bash
git clone https://github.com/yourusername/redoc.git
cd redoc
pip install -e ".[dev]"
```

## Weryfikacja instalacji

```bash
# Sprawdź Ollama
ollama list

# Sprawdź redoc
redoc --version
redoc status
```
```

### docs/guide/basic-usage.md
```markdown
# 📖 Basic Usage

## Pierwsze kroki

### 1. Generowanie prostej architektury

```bash
redoc "system logowania dla aplikacji web"
```

### 2. Ustawienie liczby poziomów

```bash
redoc "CI/CD pipeline" --levels 4
```

### 3. Interaktywny shell

```bash
redoc shell
```

W shell można używać:

```bash
dream> dream "monitoring system dla microservices"
dream> show
dream> save my_monitoring_system
dream> export json
```

## Przykłady komend

### Analiza kontekstu
```bash
dream> context "urgent Python security audit dla GDPR compliance"
```

### Różne formaty output
```bash
# JSON output
redoc "problem" --output json

# YAML output  
redoc "problem" --output yaml

# Rich summary (default)
redoc "problem" --output summary
```

### Praca z workspace
```bash
dream> workspace        # Otwiera folder
dream> history          # Historia komend
dream> config           # Konfiguracja
```
```

## 🚀 Uruchomienie dokumentacji:

```bash
# Instalacja MkDocs
pip install mkdocs-material mkdocstrings[python] mkdocs-awesome-pages-plugin

# Development server
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## 🎨 Customizacja:

### Custom CSS (docs/assets/css/custom.css):
```css
:root {
  --md-primary-fg-color: #1976d2;
  --md-accent-fg-color: #00bcd4;
}

.md-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.inception-logo {
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

### Custom JavaScript (docs/assets/js/custom.js):
```javascript
// Terminal animation for code examples
document.addEventListener('DOMContentLoaded', function() {
  // Initialize terminal animations
  const terminals = document.querySelectorAll('.termynal');
  terminals.forEach(terminal => {
    new Termynal(terminal);
  });
});
```


**Następne kroki:**
1. Stwórz folder `docs/` i dodaj podstawowe pliki
2. Uruchom `mkdocs serve` 
3. Dostosuj treść do swojego projektu
4. Deploy na GitHub Pages z `mkdocs gh-deploy`