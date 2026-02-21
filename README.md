# Volatile bandit — candidate instructions

*Wayfair - Jesse Fredrickson - 2026*

The goal of this scenario is to assess your ability to solve an ambiguous problem with code, in a realistic setting. Googling is fine, AI is fine. You're here because you're smart - now show us how you like to work!

This repo presents you with a **simulator** which holds an array of 7 **arms** to choose from. When chosen, each **arm** returns some reward. Your goal is to implement a **policy** that chooses which arm to pull each round, and maximizes your total reward over 10,000 trials.

This class of problems is called a **multi-armed bandit**; NO EXPERIENCE with bandits is expected or necessary. Think about how you would solve this as a human. A simple solution can get you surprisingly far.

![volatile bandit illustration](./image.png)

If a real-world example is helpful: consider that you want to advertise a specific red sofa on Google, and you need to choose a lead image. You have 7 product photos to choose from. How would you pick what image to show every day/week? Is it possible that your choice could change over time?

## What’s in the repo

- **`main.py`** — Harness that runs 10,000 trials. Each trial, it asks a `policy` to choose an arm, and it informs the `policy` what the reward for choosing that arm was. At the end of the trials, it prints out a summary of Cumulative Reward and Cumulative Regret.
- **`policy.py`** — YOU IMPLEMENT THIS. Contains an abstract `Policy` class to help you, and a concrete `RandomPolicy` implementation as a demo.
- **`reward.wasm`** - black box reward simulator. `main.py` handles this for you.

## How to run

```bash
uv run python main.py [--validate]
```

Use the `--validate` flag to confirm your approach generalizes by setting a different random seed.

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

Good luck!
