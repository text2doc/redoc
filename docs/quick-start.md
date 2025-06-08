# 🚀 Quick Start Guide

This guide will help you get started with redoc in just a few minutes.

## Prerequisites

- Ollama with Mistral:7b model installed (see [Installation Guide](installation.md))
- Python 3.8 or higher
- Basic familiarity with command line

## Your First Architecture

1. **Start with a simple command**:
   ```bash
   redoc "I need a REST API for a todo app with user authentication"
   ```

2. **Interactive Mode**:
   ```bash
   redoc shell
   ```
   Then type your requirements in the interactive prompt.

## Basic Commands

### Generate Architecture
```bash
# Basic usage
redoc "Your architecture requirements here"

# Specify output format (default: markdown)
redoc --format json "Your requirements"

# Save output to a file
redoc "Your requirements" > architecture.md
```

### Interactive Shell
```bash
# Start interactive shell
redoc shell

# In the shell:
> help                 # Show available commands
> clear               # Clear screen
> exit                # Exit the shell
```

## Example Workflow

1. **Define your requirements**:
   ```bash
   redoc "I need a REST API for a blog with user authentication and comments"
   ```

2. **Review the generated architecture** in the terminal output

3. **Generate implementation code**:
   ```bash
   redoc "Generate implementation code for the blog API"
   ```

4. **Save the output** to a file for future reference:
   ```bash
   redoc "Generate implementation code for the blog API" > blog_implementation.md
   ```

## Advanced Example

1. **Generate a microservices architecture**:
   ```bash
   redoc "I need a microservices architecture for an e-commerce platform with:
   - Product catalog
   - User authentication
   - Shopping cart
   - Payment processing
   - Order management"
   ```

2. **Review the generated architecture**

3. **Refine and iterate**:
   ```bash
   redoc "Add Redis caching to the previous architecture"
   ```

## Next Steps

- Explore more [features](features.md) of redoc
- Check out the [API Reference](api.md) for advanced usage
- Review the [installation guide](installation.md) for configuration options

## Getting Help

- Run `redoc --help` for command-line options
- [Open an issue](https://github.com/text2doc/redoc/issues) for bugs or feature requests
