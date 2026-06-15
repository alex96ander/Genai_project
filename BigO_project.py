import time

def find_duplicates_slow(items: list) -> list:
    """
    Time Complexity: O(N²) - Nested loops look through the list repeatedly.
    """
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

def find_duplicates_fast(items: list) -> list:
    """
    Time Complexity: O(N) - Uses a hash set to look up items instantly.
    """
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

# --- TEST THE SPEED DIFFERENCE ---
if __name__ == "__main__":
    # Create a large list of 10,000 numbers
    large_dataset = list(range(10000)) + [5, 99, 500] 

    # Measure the O(N²) Slow Method
    start = time.perf_counter()
    find_duplicates_slow(large_dataset)
    print(f"Slow O(N²) Method took: {time.perf_counter() - start:.4f} seconds")

    # Measure the O(N) Fast Method
    start = time.perf_counter()
    find_duplicates_fast(large_dataset)
    print(f"Fast O(N) Method took: {time.perf_counter() - start:.4f} seconds")
