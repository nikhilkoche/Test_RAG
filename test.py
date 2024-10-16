import platform
import subprocess
import GPUtil

def get_cpu_name():
    if platform.system() == "Windows":
        cpu_info = subprocess.check_output("wmic cpu get name").decode().strip().split("\n")
        return cpu_info[1].strip() if len(cpu_info) > 1 else "Unknown CPU"
    elif platform.system() == "Linux":
        cpu_info = subprocess.check_output("lscpu").decode().strip().split("\n")
        for line in cpu_info:
            if "Model name" in line:
                return line.split(":")[1].strip()
    elif platform.system() == "Darwin":
        cpu_info = subprocess.check_output("sysctl -n machdep.cpu.brand_string").decode().strip()
        return cpu_info
    return "Unknown CPU"

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    if gpus:
        for gpu in gpus:
            gpu_info.append((gpu.name, gpu.memoryTotal))  # (name, memory size in MB)
    return gpu_info if gpu_info else [("No GPU found", 0)]

# Get CPU and GPU information
cpu_name = get_cpu_name()
gpu_info = get_gpu_info()

# Print CPU name
print(f'CPU Name: {cpu_name}')

# Print GPU names and memory sizes
for name, memory in gpu_info:
    print(f'GPU Name: {name}, Memory Size: {memory} MB')
