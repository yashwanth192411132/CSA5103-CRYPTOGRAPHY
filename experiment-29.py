# SHA-3 Sponge State Demonstration
# Block/Rate size = 1024 bits
# Lane size = 64 bits
# Permutation is intentionally ignored.

STATE_SIZE = 1600
LANE_SIZE = 64
RATE_SIZE = 1024

# Number of lanes
TOTAL_LANES = STATE_SIZE // LANE_SIZE
RATE_LANES = RATE_SIZE // LANE_SIZE
CAPACITY_LANES = TOTAL_LANES - RATE_LANES


# ---------------------------------------
# Initial State
# ---------------------------------------

# 25 lanes, each represented by a Boolean:
# True  = lane contains at least one nonzero bit
# False = lane is completely zero

state = [False] * TOTAL_LANES


# First 16 lanes belong to the rate portion.
# Assume every lane in P0 has at least one
# nonzero bit.

for i in range(RATE_LANES):
    state[i] = True


# ---------------------------------------
# Display Initial State
# ---------------------------------------

print("========== SHA-3 STATE ==========")

print("State size       :", STATE_SIZE, "bits")
print("Rate             :", RATE_SIZE, "bits")
print("Capacity         :", STATE_SIZE - RATE_SIZE, "bits")
print("Lane size        :", LANE_SIZE, "bits")
print("Total lanes      :", TOTAL_LANES)
print("Rate lanes       :", RATE_LANES)
print("Capacity lanes   :", CAPACITY_LANES)

print("\nInitial state:")
print("Rate lanes       :", state[:RATE_LANES])
print("Capacity lanes   :", state[RATE_LANES:])


# ---------------------------------------
# Absorption without permutation
# ---------------------------------------

print("\n========== ABSORPTION ==========")

for block in range(1, 11):

    # Message is XORed only with rate portion.
    # Capacity lanes are not modified because
    # the permutation is being ignored.

    for i in range(RATE_LANES):
        state[i] = True

    capacity_nonzero = sum(
        state[i]
        for i in range(RATE_LANES, TOTAL_LANES)
    )

    print(
        "After block", block,
        ": nonzero capacity lanes =",
        capacity_nonzero,
        "/", CAPACITY_LANES
    )


# ---------------------------------------
# Final Result
# ---------------------------------------

if all(state[i] for i in range(RATE_LANES, TOTAL_LANES)):

    print("\nAll capacity lanes became nonzero.")

else:

    print("\nResult:")
    print("The capacity lanes remain zero.")
    print("They will NEVER become nonzero")
    print("when the permutation is ignored.")