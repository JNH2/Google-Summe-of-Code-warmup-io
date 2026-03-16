"""
Phase 1: Data Prepration.
Generates synthetiv binary datasets for I/O oerformance benhmarking.
"""

import os
import numpy as np
import logging

logging.basicConfig(level = logging.INFO, format = '%(levelname)s: %(message)s')

def generate_synthetic_data(data_dir="../data", num_files = 10, file_size_mb = 500):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logging.info(f"Created directorty: {data_dir}")

    np.random.seed(42)
    logging.info(f"Starting data generation in {data_dir}...")

    for i in range(num_files):
        file_path = os.path.join(data_dir, f"data_chunk_{i}.bin")

        chunks_per_file = 5
        chunk_size = 100 * 1024 * 1024

        try:
            with open(file_path, "wb") as f:
                for _ in range(chunks_per_file):
                    random_data = np.random.bytes(chunk_size)
                    f.write(random_data)
            logging.info(f"Generated: {file_path}(500 MB)")
        except IOError as e:
            logging.error(f"Failed to write{file_path}:{e}")
    
    logging.info(f"Successfully generated {num_files * file_size_mb / 1024:.2f} GB of data.")

if __name__ == "__main__":
    generate_synthetic_data()