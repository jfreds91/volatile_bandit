import argparse
import random

import wasmtime
from rich.console import Console
from rich.table import Table

from policy import RandomPolicy

DEFAULT_SEED = 42
VALIDATE_SEED = 123


def load_reward_module() -> tuple[wasmtime.Store, wasmtime.Instance]:
    engine = wasmtime.Engine()
    store = wasmtime.Store(engine)
    module = wasmtime.Module.from_file(engine, "reward.wasm")
    return store, wasmtime.Instance(store, module, [])


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the bandit harness.")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Use a different seed to validate (prevents overfitting to the default seed).",
    )
    args = parser.parse_args()

    seed = VALIDATE_SEED if args.validate else DEFAULT_SEED

    store, instance = load_reward_module()
    exports = instance.exports(store)

    init_reward_engine = exports["init_reward_engine"]
    step = exports["step"]
    get_arm_reward = exports["get_arm_reward"]
    get_num_arms = exports["get_num_arms"]

    init_reward_engine(store, seed)
    num_arms = get_num_arms(store)
    policy = RandomPolicy(num_arms, seed)
    rng = random.Random(seed)

    cumulative_reward = 0.0
    cumulative_regret = 0.0
    num_trials = 10_000
    last_chosen_arm = -1

    for _ in range(num_trials):
        step(store, last_chosen_arm, rng.getrandbits(32))
        chosen_arm = policy.choose_arm()
        chosen_reward = get_arm_reward(store, chosen_arm)
        policy.observe(chosen_arm, chosen_reward)
        best_reward = max(get_arm_reward(store, i) for i in range(num_arms))
        cumulative_reward += chosen_reward
        cumulative_regret += best_reward - chosen_reward
        last_chosen_arm = chosen_arm

    table = Table(title="Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="green")
    table.add_row("Policy", policy.__class__.__name__)
    table.add_row("Seed", str(seed) + (" (validate)" if args.validate else ""))
    table.add_row("Trials", f"{num_trials:,}")
    table.add_row("Cumulative reward", f"{cumulative_reward:,.4f}")
    table.add_row("Cumulative regret", f"{cumulative_regret:,.4f}")
    Console().print(table)

    print("\n--- User debugging (policy.debug_printout()) ---\n")
    print(policy.debug_printout())


if __name__ == "__main__":
    main()
