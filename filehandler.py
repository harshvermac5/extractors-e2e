def load_keywords_from_file(file_path):
    # Initialize an empty list to store the keywords
    keywords = []

    # Open the file and read each line
    with open(file_path, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Strip any leading/trailing whitespace (like newline characters)
            keyword = line.strip()
            
            # Add the keyword to the list if it's not an empty line
            if keyword:
                keywords.append(keyword)

    return keywords

def save_array_to_file(array, filename):
    """Overwrites file with entire array — use at start or for final write."""
    with open(filename, 'w') as file:
        for element in array:
            file.write(str(element) + '\n')

def append_to_file(item, filename):
    """Appends a single item to the file — use during intermediate saves."""
    with open(filename, 'a') as file:
        file.write(str(item) + '\n')
