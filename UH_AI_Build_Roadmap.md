# UH AI Build Roadmap: From Scratch LLM (Inspired by Karpathy's nanoGPT)

Goal: Build UH AI—a multilingual, philosophy/literature-focused LLM for "navigation through feeling and human expression" (per "UH AI - Personal Desires and Dreams.txt"). Use latest advances (e.g., Grok-4 MoE for sparsity, CAI for alignment).

## Phase 1: Setup and Data Foundation (Weeks 1-3, July 28-ongoing 2025)
- **Status**: Complete setup; in progress on data.
- Environment: WSL, PyTorch/CUDA verified on RTX 5090 (24GB VRAM). nanoGPT cloned/tested: Baseline on TinyShakespeare successful (perplexity ~6.0).
- Data: Plans for Gutenberg (philosophers: Plato/Aristotle; poets: Dante/Shakespeare) and OSCAR (multilingual corpora for synonyms/interconnections via PanLex).
- Logs: See phase1_log.md. Tracker script/alias implemented for auto-updates.
- Milestones: CUDA tests passed; repo tracking fixed (commits pushed July 30).

## Phase 2: Model Architecture (Weeks 3-5)
- **Status**: Pending Phase 1 data.
- Add MoE (4 experts, top-1 routing) to nanoGPT for efficiency (ties to Grok-4; ~150M params active ~40M).
- Test: Forward passes on subsets; interpretability hooks for "philosophy circuits" (Anthropic 2025 style).

## Phase 3: Training Pipeline (Weeks 5-8)
- Scaling laws: ~2B tokens on 350M MoE (~20 tokens/param).
- FP16/mixed precision for RTX 5090 (~2-4 hours/epoch).

## Phase 4: Fine-Tuning and Alignment (Weeks 8-10)
- CAI integration: Rules for truthful literary analysis.
- RLAIF self-critique on desires (e.g., multilingual synonyms).

## Phase 5: Deployment and UI (Weeks 10-12)
- Gradio chat UI with profiles (e.g., respond as Plato).
- Multimodal tease: CLIP for image-poetry ties.

## Phase 6: Evaluation and Iteration (Weeks 12+)
- Benchmarks: MMLU philosophy subset; perplexity <5.0.
- Cloud scaling if needed (xAI API for Grok-4 inspiration).

Timeline: 10-14 weeks flexible. Current Focus: Finalize Phase 1 data (Gutenberg/OSCAR scripts ready).