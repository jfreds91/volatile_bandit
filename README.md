# Volatile Bandit

*A multi-armed bandit competition.*

This repo presents you with a **simulator** holding 7 **arms**. Each arm returns some reward when pulled. Your goal is to implement a **policy** that chooses which arm to pull each round and maximizes **cumulative reward** over 10,000 trials.

![volatile bandit illustration](./image.png)

## Quick start

```bash
# Clone
git clone <repo-url>
cd volatile_bandit

# Run with uv (recommended)
uv run python main.py

# Or with pip
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
python main.py
```

## How to compete

1. **Check out your own branch** — `git checkout -b your-name`
2. **Write your policy** in `policy.py`. Subclass `Policy` and see `RandomPolicy` for the interface.
3. **Set `CHOSEN_POLICY`** in `main.py` to point at your class.
4. **Test locally** — `python main.py` (train sim). Use `--validate` to test with a different seed.
5. **Push your branch** — a GitHub Action will evaluate your policy against a holdout simulator and post your score to the leaderboard.

## Leaderboard

Scores are posted automatically after each push.

**[View the leaderboard](https://jfreds91.github.io/volatile_bandit/)**

## What's in the repo

| File | Purpose |
|------|---------|
| `main.py` | Harness — runs 10,000 trials, reports results. Change `CHOSEN_POLICY` here. |
| `policy.py` | Your policies go here. Ships with `Policy` ABC and `RandomPolicy` baseline. |
| `sims/train_sim.wasm` | Training simulator (black box). |

## Rules

- Edit `policy.py` (your policies) and `CHOSEN_POLICY` in `main.py`.
- Do not modify `sims/`, `docs/`, or `.github/`.
- Each push to your branch is scored independently. Push as often as you like.
- The holdout simulator has the same arms as the training sim, but in a **different order**. Solutions that hardcode arm indices will not generalize.
