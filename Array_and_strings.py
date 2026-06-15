
class ContentModerator:
    def __init__(self, blocklist_array: list):
        self.blocklist = blocklist_array

    def censor_text(self, raw_text: str) -> str:
        words_array = raw_text.split(" ")
        censored_words_array = []

        for word in words_array:
            clean_word = word.strip(".,!?\"'").lower()
            
            if clean_word in self.blocklist:
                masked_string = "*" * len(word)
                censored_words_array.append(masked_string)
            else:
                censored_words_array.append(word)
        return " ".join(censored_words_array)

    def analyze_metrics(self, raw_text: str) -> dict:
        char_count = len(raw_text) 

        words_array = raw_text.split(" ")
        word_count = len(words_array)
        
        return {
            "total_characters": char_count,
            "total_words": word_count
        }

if __name__ == "__main__":
    banned_terms = ["scam", "malware", "hate"]
    moderator = ContentModerator(blocklist_array=banned_terms)
    user_post = "Warning! This website contains a malicious scam and dangerous malware links."
    print(f"Original Text: \n\"{user_post}\"\n")

    metrics = moderator.analyze_metrics(user_post)
    print(f"Text Metrics: {metrics['total_words']} words, {metrics['total_characters']} characters.")

    clean_output = moderator.censor_text(user_post)
    print(f"Moderated Output: \n\"{clean_output}\"")
