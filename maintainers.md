# Maintainer setup

## Prerequisites

Download wasi-sdk from https://github.com/WebAssembly/wasi-sdk/releases

```bash
# Unzip and place it somewhere, e.g. ~/Documents/wasi-sdk
WASI_COMPILER=~/Documents/wasi-sdk/bin/clang++
WASI_SYSROOT=~/Documents/wasi-sdk/share/wasi-sysroot

# macOS: mark as trusted
sudo xattr -rd com.apple.quarantine ~/Documents/wasi-sdk
```

## Compile train sim

```bash
$WASI_COMPILER -O3 \
    --target=wasm32-wasi \
    --sysroot=$WASI_SYSROOT \
    -nostartfiles \
    -Wl,--no-entry \
    -Wl,--export=init_reward_engine \
    -Wl,--export=step \
    -Wl,--export=get_arm_reward \
    -Wl,--export=get_num_arms \
    -o sims/train_sim.wasm reward.cpp
```

## Compile holdout (test) sim

The test sim uses `reward_test.cpp` which has arms shifted +1 (circular).
Do NOT commit `test_sim.wasm` or `reward_test.cpp` to main.

```bash
$WASI_COMPILER -O3 \
    --target=wasm32-wasi \
    --sysroot=$WASI_SYSROOT \
    -nostartfiles \
    -Wl,--no-entry \
    -Wl,--export=init_reward_engine \
    -Wl,--export=step \
    -Wl,--export=get_arm_reward \
    -Wl,--export=get_num_arms \
    -o test_sim.wasm reward_test.cpp
```

Upload `test_sim.wasm` to S3/GCS and set the URL as `TEST_WASM_URL` secret.

## GitHub setup

1. **Secrets** (Settings → Secrets → Actions):
   - `TEST_WASM_URL` — URL to the holdout WASM file
   - `LEADERBOARD_PAT` — fine-grained PAT with `contents:write` scope

2. **GitHub Pages**: Settings → Pages → Source: Deploy from branch → `main` / `/docs`

3. **Branch protection on `main`**: Require PR for all contributors except admins
