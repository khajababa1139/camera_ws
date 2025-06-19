import sys
import subprocess
import os

def run_process(script_with_args, process_name):
    script_str = ' '.join(script_with_args)
    cmd = f"exec -a {process_name} python3 {script_str}"
    subprocess.Popen(["bash", "-c", cmd])

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 runner.py <script.py> <arg1> ... <proc_name> [more sets...]")
        print("Each set must end with a process name.")
        sys.exit(1)

    args = sys.argv[1:]
    all_sets = []
    current_set = []

    for arg in args:
        if os.path.isfile(arg) and current_set:
            all_sets.append(current_set)
            current_set = [arg]
        else:
            current_set.append(arg)
    all_sets.append(current_set)

    for arg_set in all_sets:
        *script_with_args, proc_name = arg_set
        if not script_with_args:
            print(f"Missing script for process {proc_name}")
            continue
        print(f"Running: {' '.join(script_with_args)} as '{proc_name}'")
        run_process(script_with_args, proc_name)

if __name__ == "__main__":
    main()
