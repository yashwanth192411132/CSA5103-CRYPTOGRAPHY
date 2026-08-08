import math

# Part A: Total possible keys
total_keys = math.factorial(25)

# Approximate power of 2
power = math.log2(total_keys)

# Part B: Effective unique keys
unique_keys = total_keys // 25
unique_power = math.log2(unique_keys)

print("Total possible keys =", total_keys)
print("Approximate power of 2 = 2^", round(power))

print("\nEffectively unique keys =", unique_keys)
print("Approximate power of 2 = 2^", round(unique_power))