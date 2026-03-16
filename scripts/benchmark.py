import os
import time
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader

class SyntheticBinDataset(Dataset):
    def __init__(self, data_dir="../data"):
        self.file_list = sorted([os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.bin')])
        self.samples_per_file = 500
        self.total_samples = len(self.file_list) * self.samples_per_file

    def __len__(self):
        return self.total_samples
    
    def __getitem__(self, idx):
        file_idx = idx // self.samples_per_file
        with open(self.file_list[file_idx], 'rb') as f:
            f.seek((idx % self.samples_per_file) * 1024 * 1024)
            data = f.read(1024 * 1024)
        return torch.from_numpy(np.frombuffer(data[:100], dtype=np.uint8))

def run_benchmark(num_workers, batch_size=64):
    dataset = SyntheticBinDataset()
    loader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False)

    start_time = time.time()
    num_samples = 0

    for batch in loader:
        num_samples += batch.size(0)
        
    end_time = time.time()
    total_time = end_time - start_time
    throughput = num_samples / total_time
    return total_time, throughput

if __name__ == "__main__":
    worker_counts = [1, 2, 4, 8]
    print(f"{'Workers':<10} | {'Time (s)':<10} | {'Throughput(S/s)':<15} | {'Efficiency(%)':<10}")
    print("-" * 60)

    t1 = 0
    for n in worker_counts:
        try:
            t_n, throughput = run_benchmark(n)
            if n == 1:
                t1 = t_n
                efficiency = 100.0
            else:
                efficiency = (t1 / (n * t_n)) * 100
            
            print(f"{n:<10} | {t_n:<10.2f} | {throughput:<15.2f} | {efficiency:<10.2f}")
        except Exception as e:
            print(f"Error at workers {n}: {e}")
