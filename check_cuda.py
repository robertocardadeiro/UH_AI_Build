import torch

try:
    is_available = torch.cuda.is_available()
    device_name = torch.cuda.get_device_name(0) if is_available else "No GPU"
    cuda_version = torch.version.cuda if is_available else "N/A"
    print(f"CUDA Available: {is_available}")
    print(f"Device: {device_name}")
    print(f"CUDA Version: {cuda_version}")
    with open("cuda_check_log.txt", "w") as f:
        f.write(f"CUDA Available: {is_available}\nDevice: {device_name}\nCUDA Version: {cuda_version}")
except Exception as e:
    print(f"Error: {e}")
    with open("cuda_check_log.txt", "w") as f:
        f.write(f"Error: {e}")