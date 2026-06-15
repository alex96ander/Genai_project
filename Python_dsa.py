# =====================================================================
# 1. THE DATA STRUCTURES
# =====================================================================

# A. TUPLE (Immutable Identity)
# Used for data that should never change while the program runs.
sender_1 = (101, "alex_99")
sender_2 = (102, "sam_dev")

# B. LIST (Ordered Sequence)
# Used to hold messages in the exact order they arrive.
inbox_messages = [
    "Hey! Are you learning Python today? #coding",
    "Let me know when you finish the project. #coding",
    "Call me later, urgent! #life"
]

# C. DICTIONARY (Key-Value Lookups)
# Perfect for lightning-fast O(1) lookups of dynamic user metadata.
unread_counts = {
    "alex_99": 2,
    "sam_dev": 1
}

# D. SET (Unique Collection)
# Automatically filters out duplicates to keep a clean list of tags.
unique_hashtags = {"#coding", "#life", "#coding"}  # Duplicates disappear!


# =====================================================================
# 2. THE ALGORITHMS
# =====================================================================

def linear_search_messages(keyword: str) -> bool:
    """ALGORITHM 1: Linear Search - O(N) Time Complexity.
    Loops step-by-step through the list to find a keyword match.
    """
    print(f"\n🔍 Searching for keyword: '{keyword}'...")
    for message in inbox_messages:
        if keyword.lower() in message.lower():
            print(f"🎯 Found Match: \"{message}\"")
            return True
    print("❌ No matching messages found.")
    return False


def sort_tags_by_popularity():
    """ALGORITHM 2: Sorting - O(N log N) Time Complexity.
    Organizes messy raw data into a structured order.
    """
    print("\n📊 Sorting Hashtags Alphabetically...")
    # Convert set to a list so it can be sorted
    sorted_tags = sorted(list(unique_hashtags))
    print(f"Sorted Result: {sorted_tags}")


# =====================================================================
# 3. RUNNING THE SYSTEM
# =====================================================================
if __name__ == "__main__":
    print("=== SOCIAL MEDIA INBOX RUNNING ===")
    
    # Showcase Tuple usage
    print(f"Loaded Sender Profile: ID {sender_1[0]} is User '{sender_1[1]}'")
    
    # Showcase Dictionary usage
    print(f"User '{sender_2[1]}' has {unread_counts.get(sender_2[1])} unread alert(s).")
    
    # Showcase Set uniqueness
    print(f"Unique tags discovered in inbox: {unique_hashtags}")

    # Run Algorithm 1: Search
    linear_search_messages("project")

    # Run Algorithm 2: Sort
    sort_tags_by_popularity()
