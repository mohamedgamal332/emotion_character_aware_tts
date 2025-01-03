import os
import subprocess

def run_scripts(scripts_folder="scripts"):
    """
    Automatically runs all numbered Python scripts in the specified folder in order.

    Args:
        scripts_folder (str): The folder containing the numbered scripts. Default is "scripts".
    """
    # Ensure the scripts folder exists
    if not os.path.exists(scripts_folder):
        print(f"Error: The folder '{scripts_folder}' does not exist.")
        return

    # Get all files in the scripts folder
    files = os.listdir(scripts_folder)

    # Filter out only the numbered Python scripts
    script_files = [f for f in files if f.endswith(".py") and f.split("_")[0].isdigit()]

    # Sort the scripts by their numeric prefix
    script_files.sort(key=lambda x: int(x.split("_")[0]))

    # Run each script in order
    for script in script_files:
        script_path = os.path.join(scripts_folder, script)
        print(f"Running script: {script_path}")
        try:
            # Run the script using subprocess
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running {script_path}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error while running {script_path}: {e}")
            break
        print(f"Finished running: {script_path}\n")

    print("All scripts executed successfully.")

if __name__ == "__main__":
    # Run the scripts in the "scripts" folder
    run_scripts(".\\scripts")