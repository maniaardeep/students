import os
from pathlib import Path
import logging
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    # If colorama is not installed, fallback to normal logging
    class DummyColor:
        RESET_ALL = ""
    class Fore:
        GREEN = ""
        CYAN = ""
        YELLOW = ""
        RED = ""
    class Style(DummyColor):
        BRIGHT = ""

# ----------------------------
# Configuration
# ----------------------------
project_name = "mlproject"

list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/model_trainer.py",
    f"src/{project_name}/components/model_monitoring.py",
    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/pipelines/training_pipeline.py",
    f"src/{project_name}/pipelines/prediction_pipeline.py",
    f"src/{project_name}/exception.py",
    f"src/{project_name}/logger.py",
    f"src/{project_name}/utils.py",
    "main.py",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py"
]

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ----------------------------
# Startup banner
# ----------------------------
print(f"{Fore.CYAN}{Style.BRIGHT}🚀 Initializing Project Setup for: {project_name.upper()} {Style.RESET_ALL}")
print("-" * 80)
created_files = []
skipped_files = []

# ----------------------------
# Create directories and files
# ----------------------------
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    try:
        # Create directories if not exist
        if filedir:
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"{Fore.GREEN}Created directory: {filedir}{Style.RESET_ALL}")

        # Create file if not exist or empty
        if (not filepath.exists()) or (filepath.stat().st_size == 0):
            with open(filepath, 'w') as f:
                f.write("")  # create an empty file
            logging.info(f"{Fore.YELLOW}Created empty file: {filepath}{Style.RESET_ALL}")
            created_files.append(str(filepath))
        else:
            logging.info(f"{Fore.CYAN}File already exists: {filepath}{Style.RESET_ALL}")
            skipped_files.append(str(filepath))

    except Exception as e:
        logging.error(f"{Fore.RED}Error processing {filepath}: {e}{Style.RESET_ALL}")

# ----------------------------
# Summary
# ----------------------------
print("\n" + "=" * 80)
print(f"{Fore.CYAN}{Style.BRIGHT}📦 PROJECT SETUP SUMMARY{Style.RESET_ALL}")
print(f"Project Name: {project_name}")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 80)

print(f"{Fore.GREEN}✅ Files Created ({len(created_files)}):")
for f in created_files:
    print(f"  - {f}")

print(f"\n{Fore.CYAN}⚙️ Files Already Exist ({len(skipped_files)}):")
for f in skipped_files:
    print(f"  - {f}")

print("\n" + "=" * 80)
print(f"{Fore.GREEN}{Style.BRIGHT}🎯 Setup Completed Successfully!{Style.RESET_ALL}")
