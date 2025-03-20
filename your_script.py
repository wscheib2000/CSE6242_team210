import json
import sys

def main():
    # Example data
    user_input = sys.argv[1] if len(sys.argv) > 1 else "No input provided"
    data = {"input": user_input, "message": "Hello from Python!", "value": 42}
    
    # Output JSON formatted string
    print(json.dumps(data))

if __name__ == "__main__":
    main()