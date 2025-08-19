# XML Prompt Templates

This repository contains XML prompt templates with XSD schema validation for structured AI prompt management.

## Files

- `prompt-template.xsd` - XML Schema Definition (XSD) file that defines the structure and validation rules for prompt templates
- `example-prompt-template.xml` - Comprehensive example of a code review assistant prompt template
- `simple-prompt-template.xml` - Simple example of a conversational AI assistant template

## Schema Features

The XSD schema supports:

### Core Structure
- **Metadata**: Title, description, author, timestamps, tags, and categories
- **Variables**: Typed variables with validation rules and default values
- **System Prompt**: AI system instructions with structured sections
- **User Prompt**: User-facing prompt content
- **Examples**: Input/output examples for demonstration
- **Constraints**: Rules and limitations for the prompt behavior

### Variable Types
- `string` - Text values
- `number` - Numeric values
- `boolean` - True/false values
- `date` - Date values
- `email` - Email addresses
- `url` - Web URLs
- `text` - Long-form text content

### Content Formats
- `plain` - Plain text
- `markdown` - Markdown formatted text
- `html` - HTML formatted text
- `json` - JSON structured content

### Categories
- `creative` - Creative writing and generation
- `analytical` - Data analysis and reasoning
- `conversational` - Chat and dialogue
- `technical` - Technical and programming tasks
- `educational` - Learning and teaching
- `business` - Business and professional tasks
- `other` - Other categories

## Validation

To validate XML templates against the schema:

```bash
xmllint --schema prompt-template.xsd your-template.xml --noout
```

## Template Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<pt:promptTemplate xmlns:pt="http://example.com/prompt-template"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://example.com/prompt-template prompt-template.xsd"
                   version="1.0"
                   id="unique-template-id">

    <pt:metadata>
        <!-- Template metadata -->
    </pt:metadata>

    <pt:variables>
        <!-- Variable definitions -->
    </pt:variables>

    <pt:systemPrompt>
        <!-- AI system instructions -->
    </pt:systemPrompt>

    <pt:userPrompt>
        <!-- User-facing prompt -->
    </pt:userPrompt>

    <pt:examples>
        <!-- Usage examples -->
    </pt:examples>

    <pt:constraints>
        <!-- Behavioral constraints -->
    </pt:constraints>

</pt:promptTemplate>
```

## Variable Placeholders

Use placeholders in prompts to substitute variables:

```xml
<pt:placeholder variable="variableName" fallback="default value"/>
```

## Usage Examples

See the included example files:
- `example-prompt-template.xml` - Complex template with sections and structured content
- `simple-prompt-template.xml` - Basic template with inline placeholders

Both templates validate against the XSD schema and demonstrate different approaches to prompt structuring.