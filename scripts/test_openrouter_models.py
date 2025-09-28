#!/usr/bin/env python3
"""Utility script to send a sample prompt to multiple OpenRouter models.

Usage:
  python scripts/test_openrouter_models.py --prompt "Explain quicksort in 2 sentences."

By default the script reads the OpenRouter API key from the
`OPENROUTER_API_KEY` environment variable. You can also pass it explicitly
with `--api-key`, but avoid storing secrets in plain text files.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Iterable, Optional
from urllib.parse import urlparse

import requests

try:  # Optional dependency for users who want to rely on the official openai client.
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency at runtime
    OpenAI = None

OPENROUTER_CHAT_COMPLETIONS = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


@dataclass(frozen=True)
class ModelTarget:
    """Represents a model slug plus its documentation URL."""

    slug: str
    doc_url: str


RAW_MODEL_URLS = [
    "https://openrouter.ai/x-ai/grok-code-fast-1/api",
    "https://openrouter.ai/deepseek/deepseek-chat-v3.1:free",
    "https://openrouter.ai/qwen/qwen3-coder:free",
    "https://openrouter.ai/moonshotai/kimi-k2:free",
    "https://openrouter.ai/tngtech/deepseek-r1t2-chimera:free",
]


def _slug_from_model_url(url: str) -> str:
    """Convert a documentation URL into a model slug suitable for API calls."""
    path = urlparse(url).path.strip("/")
    # Trim optional trailing "/api" segment and any ":<variant>" suffix (e.g., ":free").
    if path.endswith("/api"):
        path = path[: -len("/api")]
    if ":" in path:
        path = path.split(":", maxsplit=1)[0]
    return path


MODEL_TARGETS: tuple[ModelTarget, ...] = tuple(
    ModelTarget(slug=_slug_from_model_url(url), doc_url=url) for url in RAW_MODEL_URLS
)


prompt = """
================================================================================
FINAL PROMPT SENT TO GEMINI API
Platform: instagram
Format: story
Topic ID: 1727
Generated: 2025-09-19T23:51:38.021246
================================================================================

SYSTEM:
You are "MultiPlatformContentGen—IGStory". Generate content for EXACTLY ONE Instagram Story.
Return STRICT JSON only (no prose, no markdown). No nulls—use "" or [].

INPUT VARIABLES (provided by caller):
- topic_id: "1727"
- topic_title: "How infrastructure as code deploys entire systems with one command"
- topic_description: Discover how Infrastructure as Code (IaC) transforms system deployment and management by treating infrastructure configurations like software code. This topic explores declarative and imperative approaches, version control, and automation tools that enable repeatable, consistent, and auditable infrastructure provisioning. Learn to manage complex cloud environments efficiently and reliably.
- audience: "intermediate"
- tone: "clear, confident, non-cringe"
- locale: "en"
- primary_url: "https://example.com/topic/1727"
- brand: { "site_url":"https://example.com/topic/1727",
           "handles":{"instagram":"@systemdesign","x":"@systemdesign","linkedin":"@systemdesign","youtube":"@systemdesign","github":"@systemdesign"},
           "utm_base":"utm_source=instagram&utm_medium=story" }
- seo:
  { "primary_keywords": ["system design", "architecture", "scalability"],
    "secondary_keywords": ["distributed systems", "microservices", "performance"],
    "lsi_terms": ["load balancing", "database sharding", "caching"] }
- options:
  { "include_images": true,
    "max_length_levels":"standard",
    "variance_seed":"default",
    "length_hint": 0 }

# DYNAMIC IMAGE GENERATION RULES:
- Analyze the topic complexity and content depth to determine optimal image count (1-3 images)
- Choose appropriate image roles based on what best serves the content:
  * Always include: "background" (required)
  * Choose from: "pattern_background", "broll_bg"
- All images: ratio "9:16", size "1080x1920"
- Return your chosen count and roles in the meta.image_plan object

# NEW (generic topic taxonomy; if your provided SEO lists are placeholders, you MAY auto-correct them)
- keyword_tiers_policy:
  "Derive topic-appropriate tags when necessary:
   broad(3–5), niche(4–6), micro_niche(3–5), intent(2–3), branded(0–1).
   Use locale when natural. Lowercase; no spaces (camelCase/underscores ok)."

AUTO-CORRECTION RULE (safe):
- If provided SEO keywords obviously do not match {topic_title}/Discover how Infrastructure as Code (IaC) transforms system deployment and management by treating infrastructure configurations like software code. This topic explores declarative and imperative approaches, version control, and automation tools that enable repeatable, consistent, and auditable infrastructure provisioning. Learn to manage complex cloud environments efficiently and reliably., infer replacements and set meta.keyword_overrides=true while returning the corrected sets in meta.primary_keywords/secondary_keywords/lsi_terms.

PLATFORM RULES (Instagram Story):
- 3–5 story frames, each ~15s.
- Frames: 1 Hook → 2 Micro-insight (use poll or quiz) → 3 CTA (add countdown or link).
- Keep copy tight (Hook ≤12 words; Insight ≤14; CTA ≤10). High-contrast, mobile-safe.
- Include interactive stickers suggestions per frame (poll/question/quiz/countdown/link).
- Link strategy: if https://example.com/topic/1727 present → provide swipe/link text + UTM "https://example.com/topic/1727?{brand.utm_base}", else omit link.
- Time-sensitive angle: propose urgency (e.g., "only this week," "drop at 6 PM").
- Visual style: text-first; optional soft background if images enabled.
- Image plan (if options.include_images=true):
  - Analyze topic complexity and determine optimal image count (1-3 images)
  - Always include "background" as first image
  - Choose additional roles based on content needs: pattern_background, broll_bg
  - Return exactly the number you determine is optimal for this specific topic

VISUAL & TYPOGRAPHY GUARDRAILS:
- Aesthetic: elegant, minimalist, off-white background; thin vector strokes; subtle grid; one restrained accent color; generous margins; high contrast labels; no drop shadows or faux 3D.
- Negative prompt baseline for images: "no busy texture, no clutter, no photoreal faces, no brand logos, no neon, no 3D bevels, no fake UI chrome, no stock icon noise".
- Safe margins: keep text ≥96 px from edges (1080x1920).

CONTENT SHAPE (must appear inside "content"):
{
  "frames":[
    {"copy":"Hook line (≤12 words)","sticker_ideas":["poll: ..."]},
    {"copy":"Insight (≤14 words)","sticker_ideas":["quiz: ..."]},
    {"copy":"CTA (≤10 words)","sticker_ideas":["countdown: ..."]}
  ],
  "image_prompts": options.include_images ? [
    {
      "title":"Story Background",
      "prompt":"Soft off-white canvas with faint grid; small corner glyph of {concept}; space for overlay text.",
      "negative_prompt":"no busy texture",
      "style_notes":"very subtle, unobtrusive",
      "ratio":"9:16","size_px":"1080x1920"
    }
  ] : []
}

TASK:
Generate Instagram Story sequence for topic: How infrastructure as code deploys entire systems with one command
Context: Discover how Infrastructure as Code (IaC) transforms system deployment and management by treating infrastructure configurations like software code. This topic explores declarative and imperative approaches, version control, and automation tools that enable repeatable, consistent, and auditable infrastructure provisioning. Learn to manage complex cloud environments efficiently and reliably.

Requirements:
- 3-5 story frames (15 seconds each)
- Interactive elements (polls, questions, quizzes)
- Swipe-up/link sticker strategy
- Time-sensitive content angle
- Behind-the-scenes or quick tip format

OUTPUT — RETURN THIS EXACT JSON SHAPE:
{
  "meta": {
    "topic_id": "1727",
    "topic_title": "How infrastructure as code deploys entire systems with one command",
    "platform": "instagram",
    "format": "story",
    "content_schema_version": "v1.0.0",
    "model_version": "gemini-2.5-flash",
    "prompt_version": "ig-story-1.1",
    "audience": "intermediate",
    "tone": "clear, confident, non-cringe",
    "locale": "en",
    "primary_keywords": ["system design", "architecture", "scalability"],
    "secondary_keywords": ["distributed systems", "microservices", "performance"],
    "lsi_terms": ["load balancing", "database sharding", "caching"],
    "canonical": "https://example.com/topic/1727",
    "brand": {
      "site_url": "https://example.com/topic/1727",
      "handles": {"instagram":"@systemdesign","x":"@systemdesign","linkedin":"@systemdesign","youtube":"@systemdesign","github":"@systemdesign"},
      "utm_base": "utm_source=instagram&utm_medium=story"
    },
    "options": { "include_images": true, "max_length_levels":"standard", "variance_seed":"default" },
    "keyword_overrides": false,                      // NEW: set true if you auto-correct mismatched SEO sets
    "keyword_tiers": {                               // NEW: optional, for transparent overlay hashtag building
      "broad": [], "niche": [], "micro_niche": [], "intent": [], "branded": []
    },
    "image_plan": {                                  // NEW: AI-determined plan based on content analysis
      "count": 0, "roles": [], "ratio": "9:16", "size_px": "1080x1920", "reasoning": "Brief explanation of why this count/roles chosen"
    }
  },

  "content": {
    "frames":[
      {
        "index": 1,
        "role": "hook",
        "copy": "Hook line (≤12 words)",
        "sticker_ideas": ["poll: …", "question: …"],
        "overlay_notes": "large headline; high contrast",
        "layout": "centered title; big margins",
        "alt_text": "Describe the hook text for accessibility",
        "duration_seconds": 15
      },
      {
        "index": 2,
        "role": "micro_insight",
        "copy": "Insight (≤14 words)",
        "sticker_ideas": ["quiz: …", "emoji slider: …"],
        "overlay_notes": "two short lines max",
        "layout": "top headline; bottom quiz",
        "alt_text": "Describe the insight text and quiz",
        "duration_seconds": 15
      },
      {
        "index": 3,
        "role": "cta",
        "copy": "CTA (≤10 words)",
        "sticker_ideas": ["countdown: …", "link: https://example.com/topic/1727?{brand.utm_base}"],
        "overlay_notes": "bold CTA; arrow to link",
        "layout": "CTA bottom; link sticker above",
        "alt_text": "Describe the CTA and link",
        "duration_seconds": 15
      }
      /* Optionally add frames 4–5 as bonus tips/BTS; keep total ≤5 */
    ],

    "stickers": {
      "global": ["keep polls simple (2 options)", "use quiz with 3 options max"],
      "link_strategy": {
        "enabled": true,
        "link_url": "https://example.com/topic/1727?{brand.utm_base}",
        "link_text": "Read more",
        "placement_hint": "bottom center above CTA"
      },
      "time_sensitive_angle": "Explain why acting today matters (drop, deadline, window)."
    },

    "image_prompts": [
      {
        "role":"background",
        "title":"Story Background",
        "prompt":"Soft off-white canvas with faint dotted grid; small semantic corner glyph representing {{topic_title}} (choose abstract metaphor like process arrows, layered cards, node-edge, book/page, gear, flask, leaf, waveform); ample negative space for overlay text; generous margins; flat vector aesthetic; high mobile legibility.",
        "negative_prompt":"no busy texture, no photos, no faces, no logos, no neon, no 3D bevels, no gradients >5%",
        "style_notes":"very subtle, unobtrusive; single accent color only",
        "ratio":"9:16","size_px":"1080x1920","alt_text":"Subtle background canvas with small metaphor glyph"
      }
      ,{
        "role":"pattern_background",                  // OPTIONAL — include only if image_plan.count >= 2
        "title":"Pattern Background",
        "prompt":"Light repeating geometric pattern that suggests How infrastructure as code deploys entire systems with one command (lines, dots, nodes); extremely low contrast; ample center whitespace for text; flat vector.",
        "negative_prompt":"no noise, no moiré, no logos",
        "style_notes":"keep pattern <5% contrast",
        "ratio":"9:16","size_px":"1080x1920","alt_text":"Light geometric pattern background"
      },
      {
        "role":"broll_bg",                             // OPTIONAL — include only if image_plan.count >= 3
        "title":"B-roll BG Still",
        "prompt":"Abstract motion-friendly backdrop hinting How infrastructure as code deploys entire systems with one command; diagonal flow shapes; off-white; single accent; space for captions.",
        "negative_prompt":"no baked-in text, no photos",
        "style_notes":"supports motion overlays",
        "ratio":"9:16","size_px":"1080x1920","alt_text":"Abstract flow backdrop"
      }

      // GENERATE ADDITIONAL IMAGES BASED ON YOUR ANALYSIS:
      // Add more image prompts here if your image_plan.count > 1
      // Choose from roles: pattern_background, broll_bg
      // Each should follow the same structure with role, title, prompt, negative_prompt, style_notes, ratio, size_px, alt_text
    ],

    "overlay_hashtags": [ 
      "OPTIONAL: 3–6 short tags derived from keyword_tiers; keep subtle or hide behind sticker" 
    ],

    "compliance": {
      "frames_total": 0,                // fill real count (3–5)
      "has_link": false,                // set true if primary_url present
      "checks": [
        "3–5 frames",
        "Hook ≤12 words; Insight ≤14; CTA ≤10",
        "each frame has at least one sticker idea",
        "link omitted if primary_url empty",
        "safe margins ≥96px",
        "image_prompts length == image_plan.count when include_images=true"
      ]
    }
  }
}

VALIDATION:
- Ensure EXACT structure above is returned.
- Total frames between 3 and 5.
- Each frame includes copy (within limits), at least one sticker idea, alt_text, and duration_seconds.
- If https://example.com/topic/1727 is empty → stickers.link_strategy.enabled=false and no link in copy.
- When options.include_images=true:
  - Analyze the topic and determine optimal image count (1-3 images)
  - Set meta.image_plan.count to your chosen number and populate roles array
  - Generate exactly that many image_prompts with appropriate roles
  - Provide reasoning in meta.image_plan.reasoning for your choice
- If you auto-correct SEO keywords, set `meta.keyword_overrides=true` and return corrected sets.
- Return STRICT JSON. NO EXTRA TEXT.


================================================================================
END OF PROMPT
================================================================================

"""
def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--api-key",
        dest="api_key",
        help="OpenRouter API key. Defaults to the OPENROUTER_API_KEY environment variable.",
    )
    parser.add_argument(
        "--prompt",
        default=prompt,
        help="Prompt to send to each model.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Temperature value for sampling (default: 0.2).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Maximum tokens to request from each model (default: 512).",
    )
    parser.add_argument(
        "--client",
        choices=("requests", "openai"),
        default="requests",
        help="HTTP client implementation to use (default: requests).",
    )
    parser.add_argument(
        "--referer",
        default=None,
        help="Optional HTTP-Referer header to supply to OpenRouter.",
    )
    parser.add_argument(
        "--title",
        default="OpenRouter Model Tester",
        help="Optional X-Title header to supply to OpenRouter.",
    )
    return parser.parse_args(argv)


def resolve_api_key(cli_key: Optional[str]) -> str:
    api_key = cli_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit(
            "OpenRouter API key not provided. Supply via --api-key or OPENROUTER_API_KEY env var."
        )
    return api_key


def build_request_payload(model_slug: str, prompt: str, temperature: float, max_tokens: int) -> dict:
    return {
        "model": model_slug,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "system",
                "content": "You are a concise assistant that only returns valid JSON when asked to.",
            },
            {"role": "user", "content": prompt},
        ],
    }


def call_model(
    session: requests.Session,
    api_key: str,
    target: ModelTarget,
    prompt: str,
    temperature: float,
    max_tokens: int,
    referer: Optional[str],
    title: Optional[str],
) -> dict:
    payload = build_request_payload(target.slug, prompt, temperature, max_tokens)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if referer:
        headers["HTTP-Referer"] = referer
    if title:
        headers["X-Title"] = title

    try:
        response = session.post(OPENROUTER_CHAT_COMPLETIONS, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
    except requests.HTTPError as exc:  # pragma: no cover - CLI script
        try:
            details = response.json()
        except Exception:  # noqa: BLE001
            details = response.text
        raise RuntimeError(f"{target.slug} responded with HTTP {response.status_code}: {details}") from exc
    except requests.RequestException as exc:  # pragma: no cover - CLI script
        raise RuntimeError(f"Request to {target.slug} failed: {exc}") from exc

    return response.json()


def call_model_openai(
    client: "OpenAI",
    target: ModelTarget,
    prompt: str,
    temperature: float,
    max_tokens: int,
    referer: Optional[str],
    title: Optional[str],
) -> dict:
    extra_headers = {}
    if referer:
        extra_headers["HTTP-Referer"] = referer
    if title:
        extra_headers["X-Title"] = title

    completion = client.chat.completions.create(
        model=target.slug,
        messages=[
            {
                "role": "system",
                "content": "You are a concise assistant that only returns valid JSON when asked to.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        extra_headers=extra_headers or None,
    )

    try:
        return completion.model_dump()
    except AttributeError:  # pragma: no cover - fallback if model_dump missing
        from dataclasses import asdict  # noqa: WPS433 - local import fallback

        return json.loads(json.dumps(asdict(completion)))  # type: ignore[arg-type]


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    api_key = resolve_api_key(args.api_key)

    session: Optional[requests.Session] = None
    openai_client: Optional[OpenAI] = None

    if args.client == "requests":
        session = requests.Session()
    else:
        if OpenAI is None:
            raise SystemExit(
                "openai package not installed. Install with `pip install openai` or use --client requests."
            )
        openai_client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)

    print("Testing OpenRouter models...", file=sys.stderr)
    print(
        json.dumps(
            {
                "prompt": args.prompt,
                "temperature": args.temperature,
                "max_tokens": args.max_tokens,
                "models": [target.slug for target in MODEL_TARGETS],
                "client": args.client,
            },
            indent=2,
        ),
        file=sys.stderr,
    )

    for target in MODEL_TARGETS:
        print(f"\n=== {target.slug} ===", file=sys.stderr)
        try:
            if args.client == "requests":
                assert session is not None  # For type-checkers
                result = call_model(
                    session,
                    api_key,
                    target,
                    args.prompt,
                    args.temperature,
                    args.max_tokens,
                    args.referer,
                    args.title,
                )
            else:
                assert openai_client is not None
                result = call_model_openai(
                    openai_client,
                    target,
                    args.prompt,
                    args.temperature,
                    args.max_tokens,
                    args.referer,
                    args.title,
                )
        except Exception as exc:  # pragma: no cover - CLI script
            print(f"Error: {exc}", file=sys.stderr)
            continue

        choice = result.get("choices", [{}])[0]
        message = choice.get("message", {})
        content = message.get("content")
        usage = result.get("usage")

        print("Response:", file=sys.stderr)
        if content:
            print(content.strip(), file=sys.stderr)
        else:
            print(json.dumps(result, indent=2), file=sys.stderr)

        if usage:
            print("Usage:", json.dumps(usage, indent=2), file=sys.stderr)

    print("\nDone.", file=sys.stderr)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI script
    raise SystemExit(main())
