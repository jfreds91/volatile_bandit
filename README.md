# Volatile bandit — candidate instructions

*Wayfair - Jesse Fredrickson - 2026*

This repo presents you with a **simulator** which holds an array of 7 **arms** to choose from. When chosen, each **arm** returns some reward. Your goal is to implement a **policy** that chooses which arm to pull each round so that **cumulative reward** is as high as possible.

![volatile bandit illustration](./image.png)

This class of problem is called a **multi-armed bandit**. Experience with these problems is not expected or necessary - in fact, getting a high score isn't even necessary! We want to see that you can develop a solution that you can explain comfortably and code well.

## What’s in the repo

- **`main.py`** — Harness that runs 10,000 trials. Each trial, it asks a `policy` to choose an arm, and it informs the `policy` what the reward for choosing that arm was. At the end of the trials, it prints out a summary of Cumulative Reward and Cumulative Regret.
- **`policy.py`** — YOU IMPLEMENT THIS. Contains an abstract `Policy` class to help you, and a concrete `RandomPolicy` implementation as a demo.
- **`reward.wasm`** - black box reward simulator. `main.py` handles this for you.

## How to run

```bash
// fixed seed A
uv run python main.py

// fixed seed B
uv run python main.py --validate
```

Use the `--validate` flag to confirm you approach generalizes.

or, if you prefer pip
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python3 -m pip install -e .
python3 main.py
```

## DELIVERABLES:

- A `Policy` implementation which scores a higher cumulative reward than the random policy
- Treat this as a real work task. How would you solve it at Wayfair?
    - Can you explain your solution in detail? Why does it work? What tradeoffs does it make?
    - Is your code production-ready?


## DO:

- You may use any development environment and resources you want. Google is fine. AI is fine.
- You may use any logic inside your policy. You may add dependencies in `pyproject.toml` if needed.


## DO NOT:

- Do not change `main.py` (outside of selecting a different policy)
- Do not modify `reward.wasm`

Good luck!
