# 📝 Templates

Redoc's template system allows you to create dynamic documents using HTML and JSON templates. This guide covers how to create and use templates effectively.

## Template Basics

### Template Structure
A Redoc template consists of:
- An HTML file for layout and styling
- Optional JSON schema for data validation
- Support for variables, loops, and conditionals

### Example Template
```html
<!-- invoice.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Invoice {{ invoice.number }}</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .total { font-weight: bold; }
    </style>
</head>
<body>
    <h1>Invoice {{ invoice.number }}</h1>
    <p>Date: {{ invoice.date }}</p>
    
    <table>
        <tr>
            <th>Description</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Total</th>
        </tr>
        {% for item in invoice.items %}
        <tr>
            <td>{{ item.description }}</td>
            <td>{{ item.quantity }}</td>
            <td>${{ "%.2f"|format(item.price) }}</td>
            <td>${{ "%.2f"|format(item.quantity * item.price) }}</td>
        </tr>
        {% endfor %}
        <tr class="total">
            <td colspan="3">Total:</td>
            <td>${{ "%.2f"|format(invoice.total) }}</td>
        </tr>
    </table>
</body>
</html>
```

## Template Variables

### Basic Variables
```html
<p>Hello, {{ user.name }}!</p>
```

### Loops
```html
<ul>
{% for item in items %}
    <li>{{ item.name }} - ${{ item.price }}</li>
{% endfor %}
</ul>
```

### Conditionals
```html
{% if user.is_premium %}
    <p>Welcome back, premium user!</p>
{% else %}
    <p>Upgrade to premium for more features!</p>
{% endif %}
```

## Template Inheritance

### Base Template
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

### Child Template
```html
{% extends "base.html" %}

{% block title %}My Page{% endblock %}

{% block content %}
    <h1>Welcome to my page!</h1>
{% endblock %}
```

## Best Practices

1. **Keep templates simple** - Move complex logic to Python code
2. **Use includes** - Break down large templates into smaller components
3. **Validate data** - Always validate template data with JSON Schema
4. **Security** - Escape user input to prevent XSS attacks
5. **Performance** - Cache rendered templates when possible

## Advanced Features

### Custom Filters
```python
from redoc import Redoc

def format_currency(value):
    return f"${value:.2f}"

redoc = Redoc()
redoc.jinja_env.filters['currency'] = format_currency
```

### Global Variables
```python
redoc = Redoc()
redoc.jinja_env.globals.update({
    'now': datetime.datetime.now,
    'version': '1.0.0'
})
```

## Template Debugging

Enable debug mode to get better error messages:
```python
redoc = Redoc(debug=True)
```

Check template syntax:
```bash
redoc check-template template.html
```

## Next Steps

- Learn about [AI-powered templates](ai.md)
- Explore the [API Reference](api.md) for advanced usage
- Check out [example templates](https://github.com/text2doc/redoc/tree/main/examples/templates)
