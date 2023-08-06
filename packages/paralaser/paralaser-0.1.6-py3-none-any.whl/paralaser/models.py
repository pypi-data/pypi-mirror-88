import wget
from .tools import laser_dir

models_dir = laser_dir / "models"

encoder = str(models_dir / "bilstm.93langs.2018-12-26.pt")
bpe_codes = str(models_dir / "93langs.fcodes")

base_url = "https://dl.fbaipublicfiles.com/laser/models"
networks = [
    "bilstm.eparl21.2018-11-19.pt",
    "eparl21.fcodes", "eparl21.fvocab",
    "bilstm.93langs.2018-12-26.pt",
    "93langs.fcodes", "93langs.fvocab"
]

def download_models():
    print("Checking for paralaser models...")
    models_dir.mkdir(parents=True, exist_ok=True)
    for name in networks:
        path = models_dir / name
        if not path.exists():
            print("Downloading", name)
            wget.download(f"{base_url}/{name}", str(path))
            print("")
    print("All models downloaded")

if __name__ == "__main__":
    download_models()
