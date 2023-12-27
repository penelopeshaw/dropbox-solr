import os

directory_path = "data"

# Function to remove all text from a file
def remove_text_from_file(file_path):
    with open(file_path, 'w') as file:
        file.truncate(0)

# Check if the directory existss
if os.path.exists(directory_path) and os.path.isdir(directory_path):
    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            # Remove text from the file
            remove_text_from_file(file_path)
            print(f"Removed text from {filename}")
else:
    print(f"The directory '{directory_path}' does not exist.")

def main():
    remove_text_from_file("path")


if __name__ == '__main__':
    # handler = MyHandler()
    main()