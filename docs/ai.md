# 🤖 AI-Powered Features

Redoc leverages AI to enhance document processing capabilities. This guide covers the AI features and how to use them effectively.

## AI Capabilities

### 1. Smart Document Processing
- **Content Analysis**: Extract key information from documents
- **Document Classification**: Automatically categorize documents
- **Entity Recognition**: Identify and extract entities (names, dates, amounts, etc.)
- **Sentiment Analysis**: Analyze the sentiment of text content

### 2. Content Generation
- **Text Summarization**: Generate concise summaries of documents
- **Content Expansion**: Expand bullet points into full paragraphs
- **Document Outlining**: Create structured outlines from unstructured text
- **Language Translation**: Translate content between languages

### 3. Data Extraction
- **Form Recognition**: Extract data from forms and invoices
- **Table Extraction**: Convert tables in documents to structured data
- **Key-Value Pair Extraction**: Extract structured data from unstructured text

## Getting Started with AI Features

### Prerequisites
1. Install Redoc with AI support:
   ```bash
   pip install "redoc[ai]"
   ```
2. Set up your AI provider (OpenAI, Ollama, etc.)

### Basic Usage

#### Text Summarization
```python
from redoc import Redoc

redoc = Redoc()
summary = redoc.ai.summarize("long_document.txt", length="brief")
print(summary)
```

#### Entity Recognition
```python
entities = redoc.ai.extract_entities("document.pdf")
for entity in entities:
    print(f"{entity['text']} - {entity['type']}")
```

## AI Providers

Redoc supports multiple AI providers:

### 1. Ollama (Local)
```python
from redoc.ai.providers import OllamaProvider

provider = OllamaProvider(model="mistral:7b")
redoc = Redoc(ai_provider=provider)
```

### 2. OpenAI
```python
from redoc.ai.providers import OpenAIProvider

provider = OpenAIProvider(api_key="your-api-key", model="gpt-4")
redoc = Redoc(ai_provider=provider)
```

### 3. Custom Provider
Implement your own provider by extending the `AIProvider` class:

```python
from redoc.ai.base import AIProvider

class MyAIProvider(AIProvider):
    def summarize(self, text: str, **kwargs) -> str:
        # Your implementation here
        return summary
```

## Advanced Usage

### Document Q&A
```python
answer = redoc.ai.ask("document.pdf", "What is the main topic?")
print(answer)
```

### Document Comparison
```diff
diff = redoc.ai.compare_documents("doc1.pdf", "doc2.pdf")
print(diff)
```

## Best Practices

1. **Data Privacy**: Be mindful of sensitive information when using cloud-based AI services
2. **Cost Management**: Monitor API usage to avoid unexpected costs
3. **Quality Control**: Always review AI-generated content
4. **Performance**: Cache results when processing multiple documents
5. **Fallbacks**: Implement fallback behavior for when AI services are unavailable

## Configuration

Configure AI settings in `~/.config/redoc/config.yaml`:

```yaml
ai:
  provider: ollama  # or 'openai', 'custom'
  model: mistral:7b
  temperature: 0.7
  max_tokens: 1000
  
  # Ollama specific
  ollama:
    base_url: http://localhost:11434
    
  # OpenAI specific
  openai:
    api_key: ${OPENAI_API_KEY}
    organization: ${OPENAI_ORG}
```

## Troubleshooting

### Common Issues

1. **Missing API Key**
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

2. **Model Not Found**
   ```bash
   # For Ollama
   ollama pull mistral:7b
   ```

3. **Rate Limiting**
   - Implement retry logic
   - Reduce request frequency
   - Check your API quota

## Next Steps
- Explore [templates](templates.md) for AI-powered document generation
- Check the [API Reference](api.md) for advanced usage
- Join our [Community](https://github.com/text2doc/redoc/discussions) for support
