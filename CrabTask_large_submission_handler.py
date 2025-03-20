import os
import re
import subprocess

CYAN = "\033[96m"
ORANGE = "\033[38;5;214m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

crab_config_file = "crabConfig_X_PbPb.py"

# Paths to log files and CRAB configuration file
DIR_file = "CrabTask_manager_OUTPUT_DIRs_miniAOD.txt"

# Define name for output log file
log_name_suffix = {
    "GEN_SIM": "DIGI_RAW",
    "DIGI_RAW": "RECO",
    "RECO": "miniAOD",
    "miniAOD": "Bfinder" ## DOUBLE CHECK THIS
}

# Extract the suffix from DIR_file and create the submission log file name
suffix = re.search(r'_DIRs_(.*)\.txt', DIR_file).group(1)
submission_log_file = f"CrabTask_large_submission_{log_name_suffix[suffix]}.log"

#####################################################################################
## Toggle submission (set to False for testing, True for actual submission) ##
##                                                                          ## 
#######################                                                     ##
submit_jobs = True  ##                                                     ##
#######################                                                     ##
##                                                                          ##
## Toggle submission (set to False for testing, True for actual submission) ##
#####################################################################################

# Open and read DIRs from the log file
try:
    with open(DIR_file, "r") as log_file:
        datasets = log_file.readlines()
except FileNotFoundError:
    print(f"{RED}[X] Error: Log file {DIR_file} not found. {RESET}")
    exit(1)

# Open the submission log file
with open(submission_log_file, "w") as log_file:
    log_file.write("="*60 + "\n")
    log_file.write("CRAB Submission Log\n")
    log_file.write("="*60 + "\n\n")

    last_step_message = None

    for dataset in datasets:
        dataset = dataset.strip()  # Remove whitespace/newline
        if not dataset:
            continue  

        print(f"\n[..] Processing dataset: {dataset}")
        log_file.write(f"\n[..] Processing dataset: {dataset}\n")

        # Extract the dataset name
        match = re.search(r'-(.*)-', dataset)
        if not match:
            print(f"{RED}[X] Error: Could not extract dataset name. {RESET}")
            log_file.write(f"[X] Error: Could not extract dataset name.\n")
            continue

        dataset_name = match.group(1)

        # Determine the next processing step and corresponding PSet
        if "_DIGI_RAW" in dataset_name:
            new_dataset_name = dataset_name.replace("_DIGI_RAW", "_RECO")
            pset_file = "step3_RECO_pset.py"
            last_step_message = "Starting step: RECO"
        elif "_RECO" in dataset_name:
            new_dataset_name = dataset_name.replace("_RECO", "_miniAOD")
            pset_file = "step4_miniAOD_pset.py"
            last_step_message = "Starting step: miniAOD"
        elif "_miniAOD" in dataset_name:
            new_dataset_name = dataset_name.replace("_miniAOD", "_Bfinder")
            pset_file = "forest_miniAOD_run3_MC_wBfinder.py"
            last_step_message = "Running Bfinder"
        else:
            new_dataset_name = dataset_name.replace("_GEN_SIM", "_DIGI_RAW")
            pset_file = "step2_DIGI2RAW_pset.py"
            last_step_message = "Starting step: DIGI-RAW"

        # Update CRAB config with new dataset and PSet
        try:
            with open(crab_config_file, "r") as file:
                config_content = file.readlines()

            new_content = []
            for line in config_content:
                if "config.Data.inputDataset" in line:
                    new_content.append(f"config.Data.inputDataset = '{dataset}'\n")
                elif "config.General.requestName" in line:
                    new_content.append(f"config.General.requestName = 'MC_PbPb_{new_dataset_name}'\n")
                elif "config.Data.outputDatasetTag" in line:
                    new_content.append(f"config.Data.outputDatasetTag = '{new_dataset_name}'\n")
                elif "config.JobType.psetName" in line:
                    new_content.append(f"config.JobType.psetName = '{pset_file}'\n")  # Automatically set PSet
                else:
                    new_content.append(line)

            with open(crab_config_file, "w") as file:
                file.writelines(new_content)

            print(f"{GREEN}[✓] CRAB config updated.{RESET}")

            # Submit CRAB job only if submit_jobs is True
            if submit_jobs:
                submit_command = f"crab submit -c {crab_config_file}"
                result = subprocess.run(submit_command, shell=True, capture_output=True, text=True)

                # Log the output
                log_file.write("\n--- CRAB Submission Output ---\n")
                log_file.write(result.stdout)
                log_file.write("--- End of Submission Output ---\n\n")

                if result.returncode == 0:
                    print(f"{CYAN} [→] Successfully submitted CRAB job! {RESET}")
                else:
                    if "Please change the requestName in the config file" in result.stdout:
                        print(f"{ORANGE}[!] Task previously submitted -- skipping it.{RESET}")
                    else:
                        print(f"{RED}[X] Submission failed! Check the log file for details. {RESET}")
            else:
                print(f"{ORANGE}[!] SAFE MODE: CRAB job submission skipped.{RESET}")
                log_file.write(f"[!] SAFE MODE: CRAB job submission skipped.\n")

        except Exception as e:
            print(f"{RED} [X] Error modifying {crab_config_file}: {e} {RESET}")
            log_file.write(f"[X] Error modifying {crab_config_file}: {e}\n")

# Print and log the last step message once at the end
if last_step_message:
    step_summary = f"\n{'='*30}\n {last_step_message} \n{'='*30}\n"
    print(step_summary)
    with open(submission_log_file, "a") as log_file:
        log_file.write(step_summary)

print(f"\n Submission log saved to: {submission_log_file}")


