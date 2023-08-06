import numpy as np

def binary_indices(path):
    indices = []
    with open(path, "rb") as f:
        i = 0
        for line in f:
            indices.append(i)
            i += len(line)
    return np.array(indices, dtype=np.int64)

def save_binary_indices(txt_fname):
    fname = txt_fname.replace('.txt', '.ref.bin64')
    with open(fname, "wb") as f:
        binary_indices(txt_fname).tofile(f)
