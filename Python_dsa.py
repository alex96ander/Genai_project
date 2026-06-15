
sender_1 = (101, "alex_99")
sender_2 = (102, "sam_dev")

inbox_messages = [
    "Hey! Are you learning Python today? #coding",
    "Let me know when you finish the project. #coding",
    "Call me later, urgent! #life"
]

unread_counts = {
    "alex_99": 2,
    "sam_dev": 1
}

unique_hashtags = {"#coding", "#life", "#coding"}

def linear_search_messages(keyword: str) -> bool:

    print(f"\n Searching for keyword: '{keyword}'...")
    for message in inbox_messages:
        if keyword.lower() in message.lower():
            print(f"Found Match: \"{message}\"")
            return True
    print("No matching messages found.")
    return False


def sort_tags_by_popularity():

    print("\nSorting Hashtags Alphabetically...")
    sorted_tags = sorted(list(unique_hashtags))
    print(f"Sorted Result: {sorted_tags}")

if __name__ == "__main__":
    print("=== SOCIAL MEDIA INBOX RUNNING ===")
    print(f"Loaded Sender Profile: ID {sender_1[0]} is User '{sender_1[1]}'")
    print(f"User '{sender_2[1]}' has {unread_counts.get(sender_2[1])} unread alert(s).")
    print(f"Unique tags discovered in inbox: {unique_hashtags}")
    linear_search_messages("project")
    sort_tags_by_popularity()
