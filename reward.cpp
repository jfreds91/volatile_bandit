#include <stdlib.h>
#include <math.h>

static const int NUM_ARMS = 7;
static float g_arm_rewards[NUM_ARMS];
static int g_iteration = 0;

// Arm 6: replenishing — decays when pulled, recovers when not
static float g_capacity   = 1.0f;
static const float DECAY  = 0.0005f;
static const float RECOV  = 0.0015f;
static const float CAP_MAX = 2.0f;

static float randf() {
    return (float)rand() / (float)RAND_MAX;
}

static float rand_normal(float mean, float sd) {
    float u1 = randf(), u2 = randf();
    if (u1 < 1e-10f) u1 = 1e-10f;
    return mean + sd * sqrtf(-2.0f * logf(u1)) * cosf(6.2831853f * u2);
}

extern "C" {

void init_reward_engine(int seed) {
    (void)seed;
    g_iteration = 0;
    g_capacity  = 1.0f;
}

void step(int last_chosen_arm, int rand_seed) {
    srand((unsigned)rand_seed);

    if (last_chosen_arm >= 0 && last_chosen_arm < NUM_ARMS) {
        if (last_chosen_arm == 6) {
            g_capacity -= DECAY;
            if (g_capacity < 0.0f) g_capacity = 0.0f;
        } else {
            g_capacity += RECOV;
            if (g_capacity > CAP_MAX) g_capacity = CAP_MAX;
        }
    }

    // 0: Normal(50, 10)
    g_arm_rewards[0] = rand_normal(50.0f, 10.0f);
    // 1: Exponential(rate=0.1), mean ≈ 10
    g_arm_rewards[1] = -logf(randf() + 1e-10f) / 0.1f;
    // 2: Uniform(0, 100)
    g_arm_rewards[2] = randf() * 100.0f;
    // 3: Bimodal — 50% N(25,8) / 50% N(75,8)
    g_arm_rewards[3] = randf() < 0.5f ? rand_normal(25.0f, 8.0f) : rand_normal(75.0f, 8.0f);
    // 4: Sinusoidal mean — N(50 + 30·sin(2π·t/1000), 10)
    float m4 = 50.0f + 30.0f * sinf(6.2831853f * (float)g_iteration / 1000.0f);
    g_arm_rewards[4] = rand_normal(m4, 10.0f);
    // 5: Normal(50,10) with 5% outlier N(400,50)
    g_arm_rewards[5] = randf() < 0.05f ? rand_normal(400.0f, 50.0f) : rand_normal(50.0f, 10.0f);
    // 6: Replenishing — N(50,10) × capacity
    g_arm_rewards[6] = rand_normal(50.0f, 10.0f) * g_capacity;

    g_iteration++;
}

float get_arm_reward(int arm_id) {
    if (arm_id >= 0 && arm_id < NUM_ARMS) return g_arm_rewards[arm_id];
    return 0.0f;
}

int get_num_arms() { return NUM_ARMS; }

} // extern "C"
