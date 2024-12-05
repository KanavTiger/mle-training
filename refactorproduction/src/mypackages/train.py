import argparse
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model(dataset_path, output_path):
    # Load dataset, train model, and save model
    model = RandomForestClassifier()
    # Assume the data is loaded and split here
    model.fit(X_train, y_train)
    joblib.dump(model, os.path.join(output_path, 'model.pkl'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-path', type=str, required=True, help='Path to training dataset')
    parser.add_argument('--output-path', type=str, required=True, help='Path to save trained model')
    args = parser.parse_args()

    train_model(args.dataset_path, args.output_path)
