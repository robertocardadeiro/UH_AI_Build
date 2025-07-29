# UH AI Phase 1 Log

## Day 1: Hardware Verification and Base Setup

**Date**: July 29, 2025

**Status**: WSL installed and updated successfully.
- Ran `wsl --install -d Ubuntu` in PowerShell.
- Set up username/password in Ubuntu.
- Executed `sudo apt update && sudo apt upgrade -y` without errors.
- Verified WSL version: [paste output from `lsb_release -a`, e.g., Ubuntu 24.04 LTS]
- Fixed file error: Created `phase1_log.md` and committed to Git.
- Pushed to main branch at https://github.com/robertocardadeiro/UH_AI_Build.git
- nvidia-smi
Tue Jul 29 23:58:16 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 575.64.04              Driver Version: 577.00         CUDA Version: 12.9     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5090 ...    On  |   00000000:01:00.0 Off |                  N/A |
| N/A   40C    P0             27W /  175W |       0MiB /  24463MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
- pip list | grep torch
torch                    2.7.1+cu128
torchaudio               2.7.1+cu128
torchvision              0.22.1+cu128           
- python3 check_cuda.py
CUDA Available: True
Device: NVIDIA GeForce RTX 5090 Laptop GPU
CUDA Version: 12.8