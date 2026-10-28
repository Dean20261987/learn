def count_words(text):
    return len(text.split())

def is_palindrome(s):
    lower_s = s.lower()
    return lower_s == lower_s[::-1]

if __name__ == "__main__":
    print("自测：", count_words("a b c"), is_palindrome("Level")) 