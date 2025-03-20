import os
import subprocess
import datetime
import re

CYAN = "\033[96m"
ORANGE = "\033[38;5;214m"
RED = "\033[91m"
GREEN = "\033[92m"
GREY = "\033[90m"
RESET = "\033[0m"

def manage_crab_tasks(keyword=None):
    # Define the CRAB projects directory and log file
    crab_jobs_dir = "crab_projects"
    log_filename = f"CrabTask_manager_jobStatus_{keyword if keyword else 'ALL'}.log"
    log_OUTPUT_filename = f"CrabTask_manager_OUTPUT_DIRs_{keyword if keyword else 'ALL'}.txt"
    output_datasets = []

    # Open log file
    with open(log_filename, "w") as log_file:
        log_file.write("="*60 + "\n")
        log_file.write(f"CRAB Status Log - {datetime.datetime.now()}\n")
        log_file.write(f"Processing jobs matching: {keyword if keyword else 'ALL JOBS'}\n")
        log_file.write("="*60 + "\n")

        # Get all CRAB jobs (filter if keyword is specified)
        crab_jobs = [os.path.join(crab_jobs_dir, d) for d in os.listdir(crab_jobs_dir) 
                     if os.path.isdir(os.path.join(crab_jobs_dir, d)) and (keyword in d if keyword else True)]
        if not crab_jobs:
            print(f"[!] No CRAB jobs found in '{crab_jobs_dir}' matching '{keyword if keyword else 'ALL JOBS'}'.")
            return

        for job_dir in crab_jobs:
            print(f"\n'crab status -d {job_dir}'")
            log_file.write(f"\nChecking status of {job_dir}...\n")

            # Run crab status command
            status_cmd = f"crab status -d {job_dir}"
            result = subprocess.run(status_cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[X] Error retrieving status. ")
                continue

            # If job is finished, skip resubmission
            if "finished     		100.0%" in result.stdout:
                if "done         		100.0%" in result.stdout:
                    print(f"[✓] TASK DONE!")
                    log_file.write(f"[✓] TASK DONE! Dataset PATH SAVED \n")

                    for line in result.stdout.split("\n"):
                        if "Output dataset:" in line:
                            output_dir = line.split("Output dataset:")[-1].strip()
                            output_datasets.append(output_dir)
                            break
                    continue

                else:
                    print(f"[..] Saving outputs.")
                    log_file.write(f"[..] Saving outputs.")
                    continue

            log_file.write(result.stdout + "\n")
            log_file.write("#"*40 + "\n")
            log_file.write("#"*40 + "\n\n")

            for line in result.stdout.split("\n"):

                if "Publication status of" in line:
                    break

                if "finished     	" in line:  
                    FINISHED_jobs = re.search(r'\((.*?)\)', line).group(1)
                    print(f"{CYAN} {FINISHED_jobs} jobs FINISHED.{RESET}")

                if "running      	" in line:
                    RUNNING_jobs = re.search(r'\((.*?)\)', line).group(1)
                    print(f"{GREEN} {RUNNING_jobs} jobs RUNNIG.    {RESET}")

                if "idle         	" in line:  
                    IDLE_jobs = re.search(r'\((.*?)\)', line).group(1)
                    print(f"{GREY} {IDLE_jobs} jobs IDLE.          {RESET}")

                if "unsubmitted  	" in line:
                    UNSUBMITTED_jobs = re.search(r'\((.*?)\)', line).group(1)
                    print(f"{GREY} {UNSUBMITTED_jobs} jobs UNSUBMITTED. {RESET}")

                if "   failed   " in line:
                    FAILED_jobs = re.search(r'\((.*?)\)', line).group(1)
                    print(f"{RED} {FAILED_jobs} jobs FAILED.{RESET}")

                    if False:
                        print(f"{ORANGE}    [→] Resubmitting failed jobs.{RESET}")
                        log_file.write(f"[→] Resubmitting failed jobs. \n")

                        resubmit_cmd = f"crab resubmit --maxmemory 6000 -d {job_dir}"
                        resubmit_result = subprocess.run(resubmit_cmd, shell=True, capture_output=True, text=True)

                        if resubmit_result.returncode != 0:
                            print(f"{RED}    [X] Error resubmitting failed jobs. {RESET}")
                            log_file.write(f"[X] Error resubmitting failed jobs.\n\n")
                        else:
                            log_file.write("\n")
                    else:
                        print(f"{ORANGE}[→] Automatic REsubmission is FALSE.{RESET}")

                if "	toRetry" in line:
                    RETRY_jobs = re.search(r'\((.*?)\)', line).group(1)
                    print(f"{ORANGE} {RETRY_jobs} jobs to RETRY.{RESET}")

        print("\nAll tasks checked. See the log file for details:", log_filename)
    
    # Sort dataset paths alphabetically
    if len(output_datasets) > 0:
        output_datasets.sort()

        # Save sorted dataset paths to the log file
        with open(log_OUTPUT_filename, "w") as log_file2:
            for dataset in output_datasets:
                log_file2.write(dataset + "\n")

        print(f"Output directories saved to: {log_OUTPUT_filename}")
    else:
        print(f"Output directories not yet available.")

# Example usage:
if __name__ == "__main__":
    import sys

    # If an argument is given, use it as a keyword; otherwise, process all jobs
    keyword = sys.argv[1] if len(sys.argv) > 1 else None
    manage_crab_tasks(keyword)