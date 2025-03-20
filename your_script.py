import json

def main():
    # Example data
    data = {"message": "Hello from Python!", "value": 42}
    
    # Output JSON formatted string
    print(json.dumps(data))

if __name__ == "__main__":
    main()