# Phase 1 Log: Setup and Data Foundation (Weeks 1-3)

## July 28-30, 2025: Environment and Hardware Setup
- Verified hardware per "my_computer_specs.txt" and "dxdiag_specs.txt": Intel Core Ultra 9 275HX (24 cores), NVIDIA RTX 5090 Laptop GPU (24GB VRAM), 64GB RAM.
- Installed WSL (Ubuntu), Python venv, PyTorch with CUDA 12.9: `torch.cuda.is_available()` → True; device name: "NVIDIA GeForce RTX 5090 Laptop GPU".
- Cloned nanoGPT: `git clone https://github.com/karpathy/nanoGPT`.
- Baseline test: Ran `prepare.py` and `train.py` on TinyShakespeare (batch_size=32, n_layer=4, n_head=4, n_embd=128, max_iters=5000). Final loss ~1.8, perplexity ~6.0 after ~1 hour (VRAM usage ~5-8GB). Generation sample: Coherent Shakespeare-like text.
- Issues/Fixes: Minor pip conflicts resolved with `--index-url https://download.pytorch.org/whl/cu129`.

## July 30, 2025: Repo Tracking Fixes
- Initialized core files: README.md (project overview), UH_AI_Build_Roadmap.md (phase outlines), phase1_log.md (this log).
- Added uh_ai_project_tracker.py: Auto-updates logs, commits, pushes. Tested with user input for entries.
- Set bash alias: `alias track='python uh_ai_project_tracker.py'` in ~/.bashrc. Ran `track` to log: "Phase 1 progress: Setup complete, ready for data."
- Commit history: Initial commits pushed; no junk—cleaned placeholders.

## Next Steps (Ongoing)
- Data collection: Plans for Gutenberg (e.g., Plato's Republic ID:150) and OSCAR (English/Portuguese subsets via Hugging Face). Estimate: ~2B tokens for scaling laws compliance.
- Tie to Desires: Focused on philosophers (Plato/Aristotle) and poets (Shakespeare/Dante) for "navigation through feeling."