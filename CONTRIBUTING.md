# Contributing to The Drone Integration Handbook

This handbook is built by operators, for operators. Contributions are welcome.

## What We're Looking For

- **Corrections:** Found an error in a frequency, protocol detail, or procedure? File an issue or submit a PR.
- **Clarifications:** If something is confusing, it's worth fixing. "I didn't understand this" is valid feedback.
- **New content:** Chapters, sections, diagrams, tables, or examples that fill gaps.
- **Field experience:** Real-world war stories that illustrate a concept better than theory.
- **Platform-specific details:** UART maps for specific FCs, antenna placement photos, mesh radio configs.

## How to Contribute

### Small fixes (typos, corrections)
1. Fork the repo
2. Edit the relevant chapter file
3. Submit a PR with a clear description of what changed and why

### New sections or chapters
1. Open an issue first describing what you want to add
2. Discuss scope and placement
3. Fork, write, submit PR

## Style Guide

- **Write for the bench.** The reader has a soldering iron in one hand and this doc on their phone in the other.
- **Be specific.** "Use the right baud rate" is useless. "CRSF requires 420000 baud" is useful.
- **No marketing.** This isn't a product pitch. If a product is good, say why. If it's bad, say why. Name names.
- **Tables over paragraphs** for reference data. Prose for explanations.
- **Show the failure mode.** Don't just say what to do — say what happens when you don't.
- **Cite your experience.** "In my testing with RFD900x at 5 km..." is more credible than "range is approximately..."

## Directory Structure

```
fundamentals/    — Part 1: RF Fundamentals (Chapters 1-4)
firmware/        — Part 2: Flight Controller Firmware (Chapters 5-8)
field/           — Part 3: Field Operations (Chapters 9-12)
integration/     — Part 4: Integration (Chapters 13-15)
platforms/       — Part 5: Platform-specific references
appendices/      — Quick reference cards and lookup tables
templates/       — Printable field cards and worksheets
assets/          — Diagrams, images, and media
```

## Formatting

- Standard Markdown
- Tables for reference data
- Code blocks for commands, packet formats, and configuration
- Bold for emphasis on key terms on first use
- No emojis, no fluff

## What We Don't Want

- Product placement or affiliate content
- Unverified claims without field data
- Content that encourages illegal operation (but we acknowledge regulatory reality — see Chapter 2)
- AI-generated filler

## License

By contributing, you agree that your contributions are licensed under CC BY-SA 4.0, consistent with the rest of the handbook.
