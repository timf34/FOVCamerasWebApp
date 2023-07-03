import torch
from torchvision import models
import time
import numpy as np

# Load the pre-trained model
model = models.resnet50(pretrained=True)

# Ensure the model is set to evaluation mode
model.eval()

# Move the model to the GPU
device = torch.device("cuda")
model = model.to(device)

# Create the noise tensor
noise = torch.rand(1, 3, 240, 240, device=device)

# Test the model for 5 minutes
start_time = time.time()
print("Starting test...")
while time.time() - start_time < 1 * 60:
    # Make sure no gradients are calculated
    with torch.no_grad():
        # Move the noise tensor to the GPU and add batch dimension
        noise = noise.to(device)

        # Run the model
        output = model(noise)
        print("Output: ", output)

print("Done!")
