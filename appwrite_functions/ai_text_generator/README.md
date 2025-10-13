# AI Text Generator Function

This Appwrite Function generates AI-powered project descriptions and summaries for BuildLog.

## Features

- Generate project descriptions
- Create milestone summaries
- Write feature announcements
- Auto-summarize build logs

## Setup

### 1. Create Function in Appwrite

1. Go to Appwrite Console > Functions
2. Create new function:
   - Function ID: `ai_text_generator`
   - Name: AI Text Generator
   - Runtime: Python 3.9+
   - Entry point: `main.py`

### 2. Add Environment Variables

Add the following environment variables to your function:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Deploy

Deploy the function using Appwrite CLI:

```bash
appwrite functions createDeployment \
    --functionId=ai_text_generator \
    --activate=true \
    --entrypoint=main.py \
    --code=.
```

## Usage

### API Request

```bash
POST /v1/functions/ai_text_generator/executions
```

### Request Payload

```json
{
    "prompt": "Write a description for my hackathon project",
    "context": "Built with Python, FastAPI, and Appwrite. Features include project tracking and markdown export.",
    "max_length": 500
}
```

### Response

```json
{
    "success": true,
    "generated_text": "This innovative hackathon project...",
    "prompt": "Write a description for my hackathon project",
    "timestamp": "2025-10-13T12:00:00.000Z"
}
```

## Integration with BuildLog

The AI text generator can be integrated into BuildLog in several ways:

1. **Auto-generate project descriptions** when creating a new project
2. **Suggest log entry content** based on project context
3. **Generate submission documents** for hackathons
4. **Create social media posts** from project updates

## Local Testing

Run locally for testing:

```bash
python main.py
```

## AI Provider Options

### OpenAI (Recommended)
- Best quality
- Requires API key
- Pay per use

### Hugging Face
- Free tier available
- Good quality
- More setup required

### Local Models
- Completely free
- Requires more resources
- Privacy-focused

## Future Enhancements

- Support multiple AI providers
- Custom prompt templates
- Style customization
- Multi-language support
- Code snippet generation
- Image generation for project thumbnails

## License

MIT License - See main project LICENSE file
