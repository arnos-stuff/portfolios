import rich
import numpy as np
import pandas as pd
from pathlib import Path

__all__ = [
    "flatten", "toMatrix", "pkgdir", "rootdir",
    "store_markowitz", "load_markowitz"
]       

pkgdir = Path(__file__).parent

rootdir = pkgdir.parent

def store_markowitz(metadata: dict, outdir: Path = pkgdir / "data"):
    """Store the results of an experiment in a CSV file.

    Args:
        metadata (dict): A dictionary containing the metadata of the experiment.

    """
    metadata["results"].to_csv(
        outdir / f"results-{metadata['name']}@{metadata['date']}.csv", index=False
    )
    np.savetxt(f"mu-{metadata['name']}@{metadata['date']}.csv", metadata["mu"], delimiter=",")
    np.savetxt(f"sigma-{metadata['name']}@{metadata['date']}.csv", metadata["sigma"], delimiter=",")
    
    
def get_markowitz_files(files: list):
    for f in files:
            if "mu" in f.name:
                mu = np.genfromtxt(f, delimiter=",")
            elif "sigma" in f.name:
                sigma = np.genfromtxt(f, delimiter=",")
            else:
                results = pd.read_csv(f)
                
    return {"results": results, "mu": mu, "sigma": sigma}
    

def load_markowitz(name: str, outdir: Path = pkgdir / "data"):
    """Load the results of an experiment from a CSV file.

    Args:
        name (str): The name of the experiment.
        date (str): The date of the experiment.

    Returns:
        dict: A dictionary containing the metadata of the experiment.

    """
    outdir = Path(outdir)

    files = list(outdir.glob(f"results-{name}@*.csv"))
    if not files:
        raise FileNotFoundError(f"No results found for experiment {name}")
    elif len(files) == 3:
        return get_markowitz_files(files)
    elif not len(files) % 3:
        results = []
        for idx in range(len(files) // 3):
            date = files[idx].stem.split("@")[1]
            results += [get_markowitz_files(list(filter(lambda x: date in x.stem, files)))]
        return results
    else:
        raise FileNotFoundError(f"Missing files for experiment {name}")  
    

def flatten(dictionary, sep=".") -> dict:
    """Flatten a dictionary of dictionaries into a single dictionary.

    Args:
        dictionary (dict): A dictionary of dictionaries.

    Returns:
        dict: A flattened dictionary.

    """
    flattened = {}

    for key, value in dictionary.items():
        if isinstance(value, dict):
            lowered = flatten(value, sep=sep)
            for k, v in lowered.items():
                flattened[f"{key}{sep}{k}"] = v
        elif isinstance(value, list):
            for i, v in enumerate(value):
                if isinstance(v, dict):
                    lowered = flatten(v, sep=sep)
                    for k, v in lowered.items():
                        flattened[f"{key}{sep}nb{i}{sep}{k}"] = v
                else:
                    flattened[f"{key}{sep}nb{i}"] = v
        else:
            flattened[key] = value
    return flattened


def toMatrix(dictionary, sep=".") -> dict:
    """Convert a dictionary of dictionaries into a matrix.

    Args:
        dictionary (dict): A dictionary of dictionaries.

    Returns:
        dict: A matrix.

    """
    flattened = flatten(dictionary, sep=sep)
    keys = list(flattened.keys())
    values = list(flattened.values())
    max_len = max(len(key.split(sep)) for key in keys)
    matrix = np.empty((len(keys), max_len)).astype(object)
    matrix[:] = ''
    values = np.array(values)
    for i, key in enumerate(keys):
        for j, k in enumerate(key.split(sep)):
            matrix[i, j] = k
            
    matrix[:, -1] = values
    return matrix.tolist()