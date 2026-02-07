# Maintainer setup 

download wasi-sdk from https://github.com/WebAssembly/wasi-sdk/releases
unzip, locate folder for it

WASI_COMPILER=~/Documents/wasi-sdk/bin/clang++
WASI_SYSROOT=~/Documents/wasi-sdk/share/wasi-sysroot

mark it as trusted
sudo xattr -rd com.apple.quarantine ~/Documents/wasi-sdk

$WASI_COMPILER -O3 \
    --target=wasm32-wasi \
    --sysroot=$WASI_SYSROOT \
    -nostartfiles \
    -Wl,--no-entry \
    -Wl,--export=init_reward_engine \
    -Wl,--export=step \
    -Wl,--export=get_arm_reward \
    -Wl,--export=get_num_arms \
    -o reward.wasm reward.cpp
