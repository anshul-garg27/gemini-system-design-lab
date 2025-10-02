# Simple API Key Checker 🚀

## What It Does
Checks all 75+ API keys in your `config.py` to see which ones work, are rate-limited, or have issues.

## Usage
```bash
python3 simple_api_key_checker.py
```

## Features ⭐
- ✅ **No Prompts** - Doesn't send topic generation requests
- ⚡ **Super Fast** - Tests 10 keys simultaneously  
- 🔍 **Detailed Status** - Shows exact error for each key
- 📊 **Clear Summary** - Counts working vs problematic keys
- 💾 **Auto-Save** - Creates JSON file with full results
- ⏱️ **Minimal Delay** - Only sends simple "test" message

## Status Types
- ✅ **WORKING** - API key is active and healthy
- ⏱️ **RATE_LIMITED** - Key hit rate limits (usually temporary)
- 📊 **QUOTA_EXCEEDED** - Monthly quota reached
- ❌ **INVALID_KEY** - API key doesn't work
- 🌐 **CONNECTION_ERROR** - Network/internet issues
- ⏰ **TIMEOUT** - Request took too long
- 💥 **ERROR** - Other unexpected errors

## Sample Output
```
Total Keys: 75
✅ Working: 47        (62% success rate)
⏱️ Rate Limited: 28    (37% temporarily limited)
📊 Quota Exceeded: 0   (0% quota issues)
❌ Invalid Keys: 0     (0% broken keys)

✅ Working Keys:
  #7 - AIzaSyAQBi...
  #8 - AIzaSyA4Sq...
  #13 - AIzaSyBMpz...
  ... and 44 more
```

## The Magic 🪄
Instead of wasting quota with topic generation, it sends:
```json
{"contents": [{"parts": [{"text": "test"}]}]}
```

This tiny message tells us everything we need to know!

## Files Created
- `api_key_results_[timestamp].json` - Full detailed results with full API keys

## Perfect For:
- 👀 Checking which keys still work
- ⏱️ Finding rate-limited keys  
- 📊 Identifying quota issues
- 🔄 Before/after cleanup comparisons
- 📈 Monitoring API key health trends


