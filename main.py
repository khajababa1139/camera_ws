import sys
import subprocess
import os
import signal
import time

processes = []

def run_process(script_with_args, process_name):
    script_str = ' '.join(script_with_args)
    # Use exec to replace bash, and set process name for ps output
    cmd = f"exec -a {process_name} python3 {script_str}"
    # Start subprocess with preexec_fn=os.setsid to create a new process group
    p = subprocess.Popen(
        ["bash", "-c", cmd],
        preexec_fn=os.setsid  # Important to send signals to the whole group later
    )
    processes.append(p)

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

    try:
        for arg_set in all_sets:
            *script_with_args, proc_name = arg_set
            if not script_with_args:
                print(f"Missing script for process {proc_name}")
                continue
            print(f"Running: {' '.join(script_with_args)} as '{proc_name}'")
            run_process(script_with_args, proc_name)

        # Wait forever (or you could implement some wait logic)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[runner.py] KeyboardInterrupt detected. Terminating child processes...")
        for p in processes:
            try:
                # Send SIGINT to the process group of the child
                os.killpg(os.getpgid(p.pid), signal.SIGINT)
            except Exception as e:
                print(f"Error terminating process {p.pid}: {e}")

        # Optionally wait for processes to finish
        for p in processes:
            p.wait()

        print("[runner.py] All child processes terminated. Exiting.")

if __name__ == "__main__":
    main()
