# Using DeepSeek API (Free Alternative)

The TechCheck validator now supports DeepSeek's free API as an alternative to OpenAI.

## Quick Setup for DeepSeek

### 1. Get DeepSeek API Key
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Sign up for a free account
3. Go to API Keys section
4. Create a new API key

### 2. Configure Environment
Create/edit your `.env` file:
```bash
# DeepSeek Configuration (free!)
DEEPSEEK_API_KEY=your_deepseek_api_key_here
API_BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
```

### 3. Start the Server
```bash
python start.py
```

## Available Models

- `deepseek-chat` - General purpose model (recommended)
- `deepseek-coder` - Code-focused model
- Check [DeepSeek docs](https://platform.deepseek.com/api-docs/) for latest models

## Other Supported APIs

The system works with any OpenAI-compatible API:

### Ollama (Local)
```bash
API_BASE_URL=http://localhost:11434/v1
MODEL_NAME=llama3
DEEPSEEK_API_KEY=ollama  # Any value for local
```

### Together AI
```bash
API_BASE_URL=https://api.together.xyz/v1
MODEL_NAME=meta-llama/Llama-3-70b-chat-hf
DEEPSEEK_API_KEY=your_together_key
```

### OpenRouter
```bash
API_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=anthropic/claude-3-haiku
DEEPSEEK_API_KEY=your_openrouter_key
```

## Notes

- **DeepSeek** offers generous free tier
- **Tool calling** support varies by provider/model
- **Performance** may vary compared to GPT-4
- The system will automatically use the configured API

## Troubleshooting

If you get errors:
1. Check your API key is correct
2. Verify the base URL is right
3. Ensure the model name exists
4. Some models may not support tool calling

## Cost Comparison

- **OpenAI GPT-4**: ~$0.03 per 1K tokens
- **DeepSeek**: Free tier, then very low cost
- **Local (Ollama)**: Free but requires powerful hardware

The validator will work with any of these options!