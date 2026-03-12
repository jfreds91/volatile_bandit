"""Upsert a score into docs/scores.json. Used by CI after evaluating a submission."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SCORES_PATH = Path(__file__).parent / "scores.json"


def load_scores() -> list[dict]:
    if SCORES_PATH.exists():
        return json.loads(SCORES_PATH.read_text())
    return []


def save_scores(scores: list[dict]) -> None:
    SCORES_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCORES_PATH.write_text(json.dumps(scores, indent=2) + "\n")


def upsert(
    scores: list[dict],
    commit: str,
    branch: str,
    policy: str,
    score: float,
    regret: float,
    author: str,
    timestamp: str,
) -> list[dict]:
    entry = {
        "commit": commit,
        "branch": branch,
        "policy": policy,
        "score": score,
        "regret": regret,
        "author": author,
        "timestamp": timestamp,
    }

    existing_idx = next(
        (i for i, s in enumerate(scores) if s["commit"] == commit), None
    )
    if existing_idx is not None:
        scores[existing_idx] = entry
    else:
        scores.append(entry)

    scores.sort(key=lambda s: s["score"], reverse=True)
    return scores


def main() -> None:
    parser = argparse.ArgumentParser(description="Update the leaderboard scores.")
    parser.add_argument("--commit", required=True, help="Commit SHA")
    parser.add_argument("--branch", required=True, help="Branch name")
    parser.add_argument("--policy", required=True, help="Policy class name")
    parser.add_argument("--score", required=True, type=float, help="Cumulative reward")
    parser.add_argument("--regret", required=True, type=float, help="Cumulative regret")
    parser.add_argument("--author", required=True, help="GitHub username or identity of submitter")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).isoformat(),
        help="ISO timestamp (default: now)",
    )
    args = parser.parse_args()

    scores = load_scores()
    scores = upsert(scores, args.commit, args.branch, args.policy, args.score, args.regret, args.author, args.timestamp)
    save_scores(scores)
    print(f"Updated scores.json — {len(scores)} entries, top score: {scores[0]['score']}")


if __name__ == "__main__":
    main()
