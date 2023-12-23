import subprocess
import os

def run_ipfs_command(command, file=False):
    print("Got response to act 4")
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Failed to run command: {command}, stderr: {stderr.decode()}")
            return None

        if file:
            return stdout.decode().strip()
        else:
            return True
    except Exception as e:
        print(e)
        return None


def get_only_cid(file_path: str) -> str:
    """
    Get the CID of a file without uploading it to IPFS.

    Args:
        file_path: A string representing the path to the file.

    Returns:
        A string representing the CID of the file.
    """

    command = f"ipfs add --only-hash {file_path}"
    cid =  run_ipfs_command(command)

    if cid is None:
        print("[-] An error occurred while uploading to IPFS.")
        return None
    else:
        return cid.split(" ")[1]
    
    
    
def upload_to_ipfs(file_path):
    """
    Upload File to the IPFS.

    Args:
        file_path: A string representing the path to the file.

    Returns:
        A string representing the CID of the file.
    """
        
    command = f"ipfs add -Q {file_path}"
    cid = run_ipfs_command(command)

    if cid is None:
        print("[-] An error occurred while uploading to IPFS.")
        return None
    else:
        return cid


def Check_dir(directory) -> bool:
    """
    Ensure that a directory exists.

    Args:
        directory: A string representing the path to the directory.
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
        else:
            return True
    except:
        return False


def download_from_ipfs(CID):
    """
    Download File from the IPFS.

    Args:
        CID: A string representing the CID of the file.

    Returns:
        A string representing the path to the file.
    """
    print("Got response to act 1")
    dir_status = Check_dir(f"Storage/{CID}")
    if not dir_status:
        print("[-] An error occurred while creating the directory.")
        return None
    else:
        # extension = filename.split(".")[-1]
        # filename = f"{CID}.{extension}"
        print("Got response to act 2")
        path = f"Storage/{CID}/"
        command = f"ipfs get {CID} -o {path}"
        print("Got response to act 3")
        try:
            File = run_ipfs_command(command, file=True)
            print("Got response to act 5")
        except Exception as e:
            print(e)
            return None

    if File is None:
        print("[-] An error occurred while downloading from IPFS.")
        return None
    else:
        return File
