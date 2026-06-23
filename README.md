Utilized Darshan on the Perlmutter supercomputer to profile multi-node data ingestion, optimizing file access patterns to maximize throughput for large-scale data pipelines(Technical report in progress)


This repository contains the results and scripts for the Google Summer of Code warmup task, focused on evaluating I/O performance bottlenecks in a PyTorch DataLoader environment and analyzing Darshan characterization logs.

1. Experimental Setup
- Platform: GitHub Codespace
- Dataset: 10 synthetic binary files (~500MB each, total 4.88GB).
- Storage: Local SSD (managed through a cloud-based environment).

2. Key Scripts
- `scripts/generate_data.py`: Generates the 5GB synthetic dataset used for benchmarking.
- `scripts/benchmark.py`: Evaluates PyTorch DataLoader throughput across varying `num_workers`.

3. Benchmarking Results

The following table summarizes the I/O throughput measured on the cloud environment:

| Workers | Throughput (S/s) | Parallel Efficiency (%) |
| :--- | :--- | :--- |
| 1 | 188.45 | 100.00 |
| 2 | 191.82 | 50.89 |
| 4 | 228.50 | 30.31 |
| 8 | 221.51 | 14.69 |

Analysis:
The throughput scaling is severely sub-linear. Increasing the number of workers from 1 to 8 only resulted in a marginal throughput gain (~17.5%), while parallel efficiency plummeted to 14.69%. This indicates a massive **I/O bottleneck** where the storage bandwidth is saturated, and process contention overhead outweighs the benefits of parallelism.

4. Troubleshooting & Engineering Challenges
During the benchmarking process, the environment hit a **critical disk space limit (< 1% available) due to the large synthetic dataset. 
-Solution**: Manually purged the `.bin` data files to restore filesystem operations and ensure successful synchronization of source code via Git.
- **Takeaway**: This incident highlights the importance of **Storage Quota Management in High-Performance Computing (HPC) environments, a core challenge when scaling data-intensive workloads.

5. Future Work
- Analysis of Darshan HTML reports to identify specific metadata vs. read/write overheads.
- Exploring data container formats (e.g., HDF5 or WebDataset) to mitigate small-file I/O overhead.
