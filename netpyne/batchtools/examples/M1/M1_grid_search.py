from netpyne.batchtools.search import search
import pandas as pd
import os

# TODO: Compare the completed Grid-search with a similar Baysean Search...
sections  = ['soma', 'dendrite', 'axon_0', 'axon_1']
M1_file = os.path.abspath(__file__)

# Create parameter grid for search
search_params = {
    'sec'   : sections,
    'weight': [0.001, 0.002, 0.003],
}

# use batch_shell_config if running directly on the machine
shell_config = {'command': f'python {os.path.join(os.path.dirname(M1_file), "init.py")}'}

# Use batch_sge_config if running on a cluster
sge_config = {
    'queue'   : 'cpu.q',
    'cores'   : 5,
    'vmem'    : '4G',
    'realtime': '00:30:00',
    'command' : 'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python init.py'}


run_config = shell_config

result_grid = search(job_type = 'sh', # or Shell config
       comm_type       = 'socket',
       params          = search_params,
       run_config      = run_config,
       label           = 'grid_search',
       output_path     = os.path.join(os.path.dirname(M1_file), "grid_batch"),  
       checkpoint_path = './ray',
       num_samples     = 1,
       metric          = 'epsp',
       mode            = 'min',
       algorithm       = "variant_generator",
       max_concurrent  = 9)


# Save results to show data and adjust the code accordingly,
results = []
print("Starting result extraction...")

for trial in result_grid:
    trial_results = trial.metrics_dataframe # Turns the data from the search into a dataframe
    trial_config = trial.config             # Extract the configuration used for current trial
    if 'loss' in trial_results:
        
        results.extend([
            {
                'Section': section,                                  # Section being tested (e.g., soma, axon_0...etc)
                'iClamp' : trial_config[f'iclamp.{section}.{i+1}'],  # The iClamp value used in the trial
                'PT5B'   : trial_results.get('PT5B')[0],             # The PT5B metric result, defaulting to None if not found
                'Loss'   : trial_results.get('loss')[0]              # The loss metric result, defaulting to None if not found
            }
            for section in sections                                  # Loop through each section (DEND1, DEND2)
            for i in range(2)                                        # Loop through two indices (0, 1) for iClamp values
            if f'iclamp.{section}.{i+1}' in trial_config             # Check if the iClamp key is in the trial config
        ])
    
    print('Processed trial...')

# Convert the results list to a DataFrame
data_frame = pd.DataFrame(results)

# Full path for the CSV file to save,
csv_file_path = os.path.join(os.path.dirname(M1_file), 'M1_grid_results.csv')

# Save the DataFrame to a CSV file
data_frame.to_csv(csv_file_path, index=False)

print('Results saved')

# TODO: Bug fix - UNIX path too long, check dispatcher