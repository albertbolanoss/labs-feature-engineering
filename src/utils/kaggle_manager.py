import kagglehub
import zipfile
import json
import pandas as pd
from pathlib import Path
from typing import Optional

class KaggleManager:
    """
    Utility class to download datasets from Kaggle and load JSON files 
    into Pandas DataFrames.
    """

    @staticmethod
    def get_file(handle: str, filename: str, version: Optional[int] = None) -> str:
        """
        Downloads a file from a Kaggle dataset. 
        If the downloaded file is a ZIP, it decompresses it, extracts the content, 
        and deletes the ZIP to save space.
        
        Args:
            handle (str): The dataset identifier (e.g., "yelp-dataset/yelp-dataset").
            filename (str): The specific file name to download.
            version (int, optional): The specific dataset version. If None, downloads the latest.
        
        Returns:
            str: The absolute path of the file ready for use.
        """
        
        # 1. Build the handle with version if necessary
        full_handle = f"{handle}/versions/{version}" if version else handle
        version_label = f"v{version}" if version else "latest"
        print(f"Starting download of: {filename} ({version_label})...")

        # 2. Download file
        try:
            downloaded_path = Path(kagglehub.dataset_download(full_handle, path=filename))
        except Exception as e:
            raise RuntimeError(f"Error downloading from Kaggle: {e}")

        # 3. Check if it is a ZIP and decompress
        if zipfile.is_zipfile(downloaded_path):
            print("Compressed file detected. Processing...")
            
            # Rename to .zip so zipfile understands it correctly
            zip_path = downloaded_path.with_suffix(".zip")
            downloaded_path.rename(zip_path)
            
            # Extract in the same folder
            try:
                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(zip_path.parent)
                
                # Update the path to the extracted file
                downloaded_path = zip_path.parent / filename
                print("File extracted successfully.")
            
            finally:
                # Cleanup: delete the zip regardless of success or failure
                if zip_path.exists():
                    zip_path.unlink()
                    print("Temporary zip file deleted.")
        else:
            print("Normal file detected (no decompression required).")

        print(f"Ready to use at: {downloaded_path}")
        return str(downloaded_path)

    @staticmethod
    def load_json_df(filename: str, num_bytes: int = -1) -> pd.DataFrame:
        """
        Loads the first `num_bytes` of a JSON file and converts each line 
        into a row in a Pandas DataFrame.
        
        Args:
            filename (str): Path to the JSON file.
            num_bytes (int): Number of bytes to read. -1 reads the entire file.
        """
        print(f"Loading DataFrame from: {Path(filename).name}...")
        
        # Use 'with' to ensure the file is always closed
        with open(filename, encoding='utf-8') as fs:
            if num_bytes == -1:
                lines = fs.readlines()
            else:
                lines = fs.readlines(num_bytes)
                
            data = [json.loads(x) for x in lines]
            
        return pd.DataFrame(data)