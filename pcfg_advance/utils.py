import pickle 

def load_data(file_path):
    with open(file_path, 'rb') as f:
        train_data, test_data = pickle.load(f)
    return train_data, test_data