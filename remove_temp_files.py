import os 
import shutil


def remove_tool(folder_path):
    folder_path_temp = os.path.join(folder_path, 'temp')
    if os.path.exists(folder_path_temp):
        # Remove the contents of the directory
        for filename in os.listdir(folder_path_temp):
            file_path = os.path.join(folder_path_temp, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

        # Remove the empty directory
        os.rmdir(folder_path_temp)



    folder_path_temps = os.path.join(folder_path, 'temps')
    if os.path.exists(folder_path_temps):
        # Remove the contents of the directory
        for filenames in os.listdir(folder_path_temps):
            file_paths = os.path.join(folder_path_temps, filenames)
            try:
                if os.path.isfile(file_paths) or os.path.islink(file_paths):
                    os.unlink(file_paths)
                elif os.path.isdir(file_paths):
                    shutil.rmtree(file_paths)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

        # Remove the empty directory
        os.rmdir(folder_path_temps)