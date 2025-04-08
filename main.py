def read_visual_crossing_key():
    with open('visual_crossing_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

def main():
    print(read_visual_crossing_key())

if __name__ == "__main__":
    main()