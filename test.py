import re

# Function to check if any number greater than 10 with the "th" suffix is in a string
def contains_numberth(string):
    # Regular expression to match numbers greater than 10 with the "th" suffix
    # This pattern matches numbers 11 and greater followed by "th" (e.g., "11th", "59th", "100th", etc.)
    pattern = r'\d{1,2}(?:st|nd|rd|th)'
    match = re.search(pattern, string)
    return bool(match)

# Example usage
text = "This is the 59th example, and here is the 100th case."
print(contains_numberth(text))  # Output: True

text2 = "This is the 5th example."
print(contains_numberth(text2))  # Output: False