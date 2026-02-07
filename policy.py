import random
from abc import ABC, abstractmethod


class Policy(ABC):
    """Abstract base class for bandit policies. Subclasses choose an arm each round and receive feedback via observe()."""

    def __init__(self, num_arms: int, seed: int) -> None:
        """Initialize the policy. Called once at the start of a run."""
        self._num_arms = num_arms

    @abstractmethod
    def choose_arm(self) -> int:
        """Return the arm to pull this round. Must be in [0, num_arms)."""
        ...

    @abstractmethod
    def observe(self, arm: int, reward: float) -> None:
        """Record that the given arm was pulled and produced the given reward. Called after each round."""
        ...

    @abstractmethod
    def debug_printout(self) -> str:
        """Return a string summarizing the policy's internal state. The harness prints it at the end of the run."""
        ...


class RandomPolicy(Policy):
    def __init__(self, num_arms: int, seed: int) -> None:
        super().__init__(num_arms, seed)
        self._rng = random.Random(seed)
        self._arms_chosen: list[int] = []
        self._rewards: list[float] = []

    def choose_arm(self) -> int:
        return self._rng.randrange(self._num_arms)

    def observe(self, arm: int, reward: float) -> None:
        self._arms_chosen.append(arm)
        self._rewards.append(reward)

    def debug_printout(self) -> str:
        lines = ["Policy state (arm chosen per round, reward per round)", ""]
        for arm in range(self._num_arms):
            indices = [i for i, a in enumerate(self._arms_chosen) if a == arm]
            pulls = len(indices)
            total = sum(self._rewards[i] for i in indices) if pulls else 0.0
            mean = total / pulls if pulls else 0.0
            lines.append(f"  Arm {arm}: pulls={pulls:,}, total_reward={total:,.4f}, mean_reward={mean:,.4f}")
        n = len(self._arms_chosen)
        total_reward = sum(self._rewards)
        lines.append(f"  Total: pulls={n:,}, total_reward={total_reward:,.4f}, mean_reward={total_reward / n:,.4f}" if n else "  Total: (no pulls)")
        return "\n".join(lines)
