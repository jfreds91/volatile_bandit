# Volatile bandit — candidate instructions

<<<<<<< HEAD
You have a **multi-armed bandit** simulator. Your goal is to implement a **policy** that chooses which arm to pull each round so that **cumulative reward** is as high as possible.
=======
*Wayfair - Jesse Fredrickson - 2026*

![volatile bandit illustration](./image.png)

This repo presents you with a **simulator** which holds an array of **arms** to choose from. When chosen, each **arm** returns some reward. Your goal is to implement a **policy** that chooses which arm to pull each round so that **cumulative reward** is as high as possible.
>>>>>>> maintainer

## What’s in the repo

- **`main.py`** — Harness that runs 10,000 trials with a fixed seed, then prints cumulative reward and cumulative regret.
<<<<<<< HEAD
=======
-- **`reward.wasm`** - black box reward simulator. `main.py` handles this for you.
>>>>>>> maintainer
- **`policy.py`** — Contains an abstract `Policy` class to help you, and a concrete `RandomPolicy` implementation as a demo

Each round, the environment first samples a reward for every arm (you don’t see these until after you’ve chosen). You choose one arm; the harness then gives you that arm’s reward via `observe(arm, reward)`. Regret for the round is (best arm’s reward minus your arm’s reward).

## How to run

```bash
uv run python main.py
```

Use the **`--validate`** flag to run with a different seed. This helps check that your policy generalises instead of overfitting to the default seed:

```bash
uv run python main.py --validate
```

Your score may differ between the default run and the validation run; a policy that does well on both is more robust.

or, if you prefer pip
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
python main.py
```

## DO:

<<<<<<< HEAD
- You may use any development environment and resources you want. Google is fine. AI is fine.
=======
>>>>>>> maintainer
- You may use any logic inside your policy. You may add dependencies in `pyproject.toml` if needed.
- change `main.py` to select your policy, once you've implemented one

## DO NOT:

- Do not change `main.py` (outside of selecting a different policy)
- Do not modify `reward.wasm`

Good luck!