# Prompt Design

Notes on how we structure agent prompts. Read this before writing a new agent.

## Anatomy of an agent prompt

Every agent prompt has the same five sections:

```
1. ROLE         — who you are
2. CONTEXT      — what's loaded into your view of the tree
3. PROTOCOL     — Ask → Options → Decide → Draft → Approve
4. OUTPUT SPEC  — exact shape of your output (JSON schema or markdown structure)
5. EXAMPLES     — one shot of input + output (k-shot for difficult agents)
```

## Section 1: ROLE

State the seat at the table, the experience the agent represents, the temperament. Two paragraphs maximum.

> You are the **Chapter Writer**. You have written dozens of novels under
> contract — literary, commercial, genre. You are not precious about your
> prose; you are an executor with taste. You receive a beat plan and you
> render it into chapter-shaped prose.

## Section 2: CONTEXT

Tell the agent which subset of the novel tree is loaded. Always minimal — agents do better when they don't see irrelevant nodes.

> You are given:
> - `world_bible` (read-only)
> - `characters` (read-only, only those appearing in this chapter)
> - `chapter.metadata` (POV, location, time, opening_image, midpoint, climax_beat)
> - `chapter.beats` (the plan you are rendering)
> - `prior_chapters_summary` (one-paragraph recap of every chapter before this)
> - `voice_cards` for characters who speak
> You are NOT given the full outline. Trust the beat plan.

## Section 3: PROTOCOL

The five-step protocol. Most agents inherit it verbatim from `CLAUDE.md`. Override only when necessary.

For full-auto mode, collapse to:

> Ask only if the input is missing a required field. Otherwise produce the
> output and present it.

For manual mode, collapse to:

> Do not produce text. Critique the user's text. Suggest specific fixes.

## Section 4: OUTPUT SPEC

This is the most important section. Be precise. Agents should know exactly what they're producing.

For structured output:

```yaml
output_format: json
schema:
  type: object
  required: [logline]
  properties:
    logline:
      type: string
      maxLength: 200
    candidates:
      type: array
      items: { type: string, maxLength: 200 }
      minItems: 3
      maxItems: 5
```

For prose output:

> Write in markdown. Use `##` for scene breaks. No headers above scene level.
> Em-dashes are `—` (U+2014), not `--`. Use straight quotes; the formatter
> will smarten them at compile time.
> Length target: <beat.length_target> words ±15%.

## Section 5: EXAMPLES

One shot for most agents. K-shot (3-4) for hard agents (logline-specialist, ai-voice-detector, voice-coach).

## Voice constraints (every agent)

When agents produce prose, they observe these constraints. These are also what `ai-voice-detector` flags:

**Banned by default** (overridable per project):

- "delve", "tapestry", "navigate" (figuratively), "leverage", "robust"
- "It's not just X — it's Y" construction
- Em-dash addiction (>3 per page)
- The "of course," / "indeed," opener
- "In conclusion," / "Ultimately,"
- Three-word adjective stacks ("a long, slow, painful breath")
- "She felt that…" — convert to direct sensation
- "She knew that…" — convert to dramatized knowing

**Encouraged**:

- Concrete nouns over abstract
- Verbs over adjectives
- Direct over filtered ("the room was cold" → "the cold pressed in")
- Specific over general (a brand name, a street name, a year)
- One unusual word per paragraph (not five)
- Period over comma when uncertain

## Length discipline

Every prose-producing agent enforces a length target. If the beat says 500 words
and the agent produces 1200, it has failed — even if the prose is good. The
revision plan will trim it.

## Voice anchoring per character

Each named character has a `voice_card`:

```yaml
character: Lin Wei
sentence_length: short_to_medium
register: legal_clinical_with_synesthete_lapses
verbal_tics:
  - never says "I think" — says "I am persuaded that"
  - converts emotions into colours: "I felt a flat blue"
banned_for_her: [contractions, sentimental adjectives]
example_lines:
  - "The defendant's testimony tastes of tin."
  - "Strike the metaphor. Strike it."
```

When the agent writes dialogue for this character, it pulls the voice card.

## Failure modes & fallbacks

Each agent declares its failure modes in frontmatter:

```yaml
failure_modes:
  - llm_timeout: retry once, then emit a length-zero stub with TODO marker
  - schema_violation: log + return original input unchanged
  - over_length: trim to target × 1.15, log warning
  - banned_phrase_detected: surface to style-critic, do not block output
```

The orchestrator handles these without halting the pipeline. The user sees a
report of which agents fell back at the end.
