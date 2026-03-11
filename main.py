import argparse
import json
import random

import wasmtime
from rich.console import Console
from rich.table import Table

import policy

# ── Change this to whatever policy you want to compete with ──
CHOSEN_POLICY = policy.EpsilonGreedyPolicy

DEFAULT_SEED = 42
VALIDATE_SEED = 123
NUM_TRIALS = 10_000


class RewardEngine:
    """Wrapper for reward module. No need to read or understand this code."""

    def __init__(self, wasm_path: str, seed: int) -> None:
        engine = wasmtime.Engine()
        self._store = wasmtime.Store(engine)
        module = wasmtime.Module.from_file(engine, wasm_path)
        instance = wasmtime.Instance(self._store, module, [])
        exports = instance.exports(self._store)

        self._step = exports["step"]
        self._get_arm_reward = exports["get_arm_reward"]
        self._get_num_arms = exports["get_num_arms"]

        exports["init_reward_engine"](self._store, seed)

    @property
    def num_arms(self) -> int:
        return self._get_num_arms(self._store)

    def step(self, last_chosen_arm: int, entropy: int) -> None:
        self._step(self._store, last_chosen_arm, entropy)

    def get_arm_reward(self, arm: int) -> float:
        return self._get_arm_reward(self._store, arm)

    def best_reward(self) -> float:
        return max(self.get_arm_reward(i) for i in range(self.num_arms))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the bandit harness.")
    parser.add_argument(
        "--sim",
        default="sims/train_sim.wasm",
        help="Path to the WASM simulator (default: sims/train_sim.wasm).",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Use a different seed to validate (prevents overfitting to the default seed).",
    )
    parser.add_argument(
        "--score-only",
        action="store_true",
        help="Print only a JSON line with score and policy name, then exit.",
    )
    args = parser.parse_args()

    seed = VALIDATE_SEED if args.validate else DEFAULT_SEED
    engine = RewardEngine(args.sim, seed)
    pol = CHOSEN_POLICY(engine.num_arms, seed)
    rng = random.Random(seed)

    cumulative_reward, cumulative_regret = 0.0, 0.0
    last_chosen_arm = -1

    for _ in range(NUM_TRIALS):
        engine.step(last_chosen_arm, rng.getrandbits(32))

        chosen_arm = pol.choose_arm()
        chosen_reward = engine.get_arm_reward(chosen_arm)
        pol.observe(chosen_arm, chosen_reward)

        cumulative_reward += chosen_reward
        cumulative_regret += engine.best_reward() - chosen_reward
        last_chosen_arm = chosen_arm

    if args.score_only:
        print(json.dumps({
            "score": round(cumulative_reward, 4),
            "regret": round(cumulative_regret, 4),
            "policy": CHOSEN_POLICY.__name__,
        }))
        return

    table = Table(title="Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="green")
    table.add_row("Policy", pol.__class__.__name__)
    table.add_row("Seed", str(seed) + (" (validate)" if args.validate else ""))
    table.add_row("Trials", f"{NUM_TRIALS:,}")
    table.add_row("Cumulative reward", f"{cumulative_reward:,.4f}")
    table.add_row("Cumulative regret", f"{cumulative_regret:,.4f}")
    Console().print(table)

    print("\n--- User debugging (policy.debug_printout()) ---\n")
    print(pol.debug_printout())


if __name__ == "__main__":
    main()
