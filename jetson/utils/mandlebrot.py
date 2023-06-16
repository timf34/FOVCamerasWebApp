import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import numpy as np
import matplotlib.pyplot as plt
import time
import signal
import sys

# Create CUDA kernel
mod = SourceModule("""
__global__ void mandelbrot(float *dest, float *Xs, float *Ys, int max_iter) {
    const int i = threadIdx.x + blockDim.x * blockIdx.x;
    const int j = threadIdx.y + blockDim.y * blockIdx.y;
    const int width = gridDim.x * blockDim.x;
    const int idx = j * width + i;
    float c_re = Xs[i];
    float c_im = Ys[j];
    float x = 0, y = 0;
    int iteration = 0;
    while (x*x + y*y <= 4 && iteration < max_iter) {
        float x_new = x*x - y*y + c_re;
        y = 2*x*y + c_im;
        x = x_new;
        iteration++;
    }
    dest[idx] = iteration;
}
""")

mandelbrot = mod.get_function("mandelbrot")

# Grid size (adjust for your GPU)
grid = (64, 64, 1)
block = (32, 32, 1)
width = grid[0] * block[0]
height = grid[1] * block[1]

# Create coordinate arrays
X = np.linspace(-2.0, 1.0, width).astype(np.float32)
Y = np.linspace(-1.0, 1.0, height).astype(np.float32)

output = np.empty((width, height), dtype=np.float32)

# GPU benchmark
start_time = time.time()

# Allow to stop the program using Ctrl+C
def signal_handler(sig, frame):
    print("Stopping after {:.2f} seconds".format(time.time() - start_time))
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

while True:
    mandelbrot(drv.Out(output), drv.In(X), drv.In(Y), np.int32(1000), block=block, grid=grid)
    if time.time() - start_time > 120:  # 2 minutes
        break

plt.imshow(output, extent=(-2, 1, -1, 1))
plt.show()
