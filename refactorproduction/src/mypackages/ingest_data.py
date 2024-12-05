import argparse
import os

def download_and_create_data(output_path):
    # Implementation for downloading and creating datasets
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-path', type=str, default='data', help='Path to save the data')
    args = parser.parse_args()

    download_and_create_data(args.output_path)
