import sys
import pandas as pd

def main():
    # Example data
    center_node = sys.argv[1] if len(sys.argv) > 1 else "No input provided"

    data = pd.read_csv('./data/test.csv')
    
    # Output CSV formatted string
    print(data.to_csv(lineterminator='\n'), end="")

if __name__ == "__main__":
    main()