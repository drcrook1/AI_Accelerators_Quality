import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader
import os
import copy
import argparse
import json
import time
import pandas as pd

from model.autoencoder import AutoencoderModel

from azureml.core.run import Run
# get the Azure ML run object
run = Run.get_context()


def load_data(data_dir, batch_size):
    """Load the train/val data."""
    
    X_train = pd.read_pickle(data_dir + "/X_train.pkl.gz")
    X_test = pd.read_pickle(data_dir + "/X_test.pkl.gz")

    X_train_dl = DataLoader(X_train.values, batch_size=batch_size, shuffle=True)
    X_test_dl = DataLoader(X_test.values)

    dataloaders = {'train':X_train_dl, 'val':X_test_dl}
    dataset_sizes = {'train':len(X_train), 'val':len(X_test)}

    return dataloaders, dataset_sizes


def train_model(model, criterion, optimizer, scheduler, args):
    """Train the model."""

    # load training/validation data
    dataloaders, dataset_sizes = load_data(args.data_dir, args.batch_size)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_loss = None

    for epoch in range(args.num_epochs):
        print('Epoch {}/{}'.format(epoch, args.num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                scheduler.step()
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs in dataloaders[phase]:
                inputs = inputs.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, inputs)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)

            epoch_loss = running_loss / dataset_sizes[phase]

            print('{} Loss: {:.4f}'.format(
                phase, epoch_loss))

            # deep copy the model
            if phase == 'val' and (best_loss is None or epoch_loss < best_loss):
                best_loss = epoch_loss
                best_model_wts = copy.deepcopy(model.state_dict())

            # log the best val accuracy to AML run
            if best_loss is not None:
                run.log('best_loss', float(best_loss))

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val loss: {:4f}'.format(best_loss))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model


def run_training(args):
    """Create and train a model."""

    # log the hyperparameter metrics to the AML run
    run.log('lr', float(args.learning_rate))
    run.log('weight_decay', float(args.weight_decay))

    model_ft = AutoencoderModel()

    device = torch.cuda.current_device() if torch.cuda.is_available() else torch.device('cpu')
    model_ft = model_ft.double().to(device)

    criterion = nn.MSELoss()

    # Observe that all parameters are being optimized
    optimizer_ft = optim.Adam(
        model_ft.parameters(),
        lr=args.learning_rate,
        weight_decay = args.weight_decay
    )

    # Decay LR by a factor of 0.1 every num_epochs/3 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(
        optimizer_ft, step_size=args.num_epochs/3, gamma=0.1)

    model = train_model(model_ft, criterion, optimizer_ft,
                        exp_lr_scheduler, args)

    return model


def main():
    print("Torch version:", torch.__version__)

    # get command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_epochs', type=int, default=2,
                        help='number of epochs to train')
    parser.add_argument('--data_dir', type=str, default=".", help='data directory')
    parser.add_argument('--output_dir', type=str, default="./outputs", help='output directory')
    parser.add_argument('--learning_rate', type=float,
                        default=0.01, help='learning rate')
    parser.add_argument('--weight_decay', type=float, default=0.0001, help='weight decay')
    parser.add_argument('--batch_size', type=int, default=3000, help='batch size')
    args = parser.parse_args()

    print("data directory is: " + args.data_dir)
    model = run_training(args)
    os.makedirs(args.output_dir, exist_ok=True)
    torch.save(model, os.path.join(args.output_dir, 'model.pt'))
    print('Model saved to {}'.format(args.output_dir))


if __name__ == "__main__":
    main()
