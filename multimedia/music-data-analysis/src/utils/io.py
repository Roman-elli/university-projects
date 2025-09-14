import numpy as np
import os

def save_csv(filename, data, fmt="%.6f", delimiter=","):
    os.makedirs('data', exist_ok=True)
    np.savetxt(f"data/{filename}", data, fmt=fmt, delimiter=delimiter)

def load_csv(filename, delimiter=",", dtype=float):
    return np.genfromtxt(filename, delimiter=delimiter, dtype=dtype)

def append_text(filename, header, content):
    with open(f"data/{filename}", "a") as f:
        f.write(f"\n{header}\n")
        f.write(content)

def write_text(filename, header, arrays):
    with open(f"data/{filename}", "w") as f:
        f.write(header + "\n")
        for arr in arrays:
            np.savetxt(f, [arr[0]], fmt="%s")
            np.savetxt(f, [arr[1]], fmt="%.6f")

def write_ranking(filename, header, files, dists):
    with open(f"data/{filename}", "a") as f:
        f.write(header + "\n")
        np.savetxt(f, [files], fmt="%s")
        np.savetxt(f, [dists], fmt="%.6f")
        f.write("\n")

def append_precision(filename, prec_euclidean, prec_manhattan, prec_cosine):
    with open(f"data/{filename}", "a") as f:
        f.write("\nPrecision: {:.1f}\n".format(prec_euclidean))
        f.write("Precision dm: {:.1f}\n".format(prec_manhattan))
        f.write("Precision dc: {:.1f}\n".format(prec_cosine))
        f.write("\n")