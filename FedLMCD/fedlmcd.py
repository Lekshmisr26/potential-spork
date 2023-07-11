# Import required libraries
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

# Generate a sample dataset
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    n_classes=2,
    random_state=42
)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert the numpy arrays to tensors
train_features = torch.from_numpy(X_train).float()
train_labels = torch.from_numpy(y_train).long()
test_features = torch.from_numpy(X_test).float()
test_labels = torch.from_numpy(y_test).long()

# Define the client-side model architecture
class DDoSDetectionModel(nn.Module):
    def __init__(self):
        super(DDoSDetectionModel, self).__init__()
        self.fc1 = nn.Linear(20, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 2)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Define the training function for the client-side
def train(model, train_data, num_epochs, learning_rate):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)

    features, labels = train_data
    train_loader = torch.utils.data.DataLoader(list(zip(features, labels)), batch_size=32, shuffle=True)
    
    for epoch in range(num_epochs):
        running_loss = 0.0
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, running_loss))

# Define the server-side model aggregation function
def aggregate_models(models):
    # Aggregate the model updates from multiple clients
    # using averaging

    aggregated_model = DDoSDetectionModel()
    num_clients = len(models)
    
    for name, param in aggregated_model.named_parameters():
        updated_param = torch.zeros_like(param.data)
        for model in models:
            updated_param += model[name]
        
        updated_param /= num_clients
        param.data = updated_param
    
    return aggregated_model

# Main federated learning loop
def federated_learning(num_clients, num_epochs, learning_rate, train_data, test_data):
    # Initialize models on each client
    client_models = []
    for _ in range(num_clients):
        model = DDoSDetectionModel()
        client_models.append(model)

    # Training loop
    for epoch in range(num_epochs):
        client_updates = []
        for i in range(num_clients):
            # Train the client model using local data
            train(client_models[i], train_data, num_epochs, learning_rate)

            # Extract the model updates
            client_updates.append(client_models[i].state_dict())

        # Aggregate the model updates on the server
        aggregated_model = aggregate_models(client_updates)

        # Evaluate the aggregated model on the test data
        test_predictions = aggregated_model(test_features.clone().detach()).argmax(dim=1)
        confusion = confusion_matrix(test_labels, test_predictions)

        print('Epoch [{}/{}], Confusion Matrix:'.format(epoch+1, num_epochs))
        print(confusion)

# Start federated learning
num_clients = 10
num_epochs = 5
learning_rate = 0.001
train_data = (train_features, train_labels)  # Replace with your actual training data
test_data = (test_features, test_labels)  # Replace with your actual test data
federated_learning(num_clients, num_epochs, learning_rate, train_data, test_data)
