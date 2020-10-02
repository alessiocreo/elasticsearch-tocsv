from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from helpers.csv_handlers import *
from helpers.utility_functions import *
from helpers.interval_builders import *
from helpers.connection_tools import *
from helpers.arguments_checkers import *
from utils.TqdmLoggingHandler import TqdmLoggingHandler
from utils.CustomLogger import CustomLogger

def main():
  args = fetch_arguments()
  args = check_arguments_conflicts(args, log)
  test_es_connection(args)
  check_csv_already_written(args['export_path'])

  log.info("################ EXTRACTING DATA ################\n")

  if args['enable_multiprocessing']:
    log.info('Connection to ES host established -- Multiprocessing enabled\n')
    processes_to_use = min(multiprocessing.cpu_count(), safe_toint_cast(args['process_number'])) if args['process_number'] != None else multiprocessing.cpu_count()
    
    # Split total time range in equals time intervals so to let each process work on a partial set of data and store the resulting list as a sublist of the lists_to_join list
    if args['load_balance_interval'] == None:
      log.info("No --load_balance_interval has been set. Intervals will be created on a time basis\n")
      processes_intervals = make_time_intervals(args, processes_to_use, args['starting_date'], args['ending_date'])
    else:
      log.info("Having set the --load_balance_interval option, intervals will be created on a load basis as far as possible according to the -lbi set\n")
      processes_intervals = make_intervals_by_load(args, processes_to_use, args['starting_date'], args['ending_date'])

    # Build the list of arguments to pass to the function each process will run
    process_function_arguments = [[args for i in range(processes_to_use)], *processes_intervals, [i for i in range(processes_to_use)]]
    
    processes_done = [None for i in range(processes_to_use)]

    # Create and start processes_to_use number of processes
    with ProcessPoolExecutor(processes_to_use) as executor:
      processes_done = executor.map(fetch_es_data, *process_function_arguments)

    while list(set(processes_done)) != [True]:
      continue
  else:
    log.info('Connection to ES host established -- Single process run\n')
    fetch_es_data(args, args['starting_date'], args['ending_date'])

  # Joining partial csv files previously created into a single one
  log.info('Joining partial csv files\n')
  final_df = join_partial_csvs(args['export_path'][:-4])
  
  # Remove duplicates
  final_df = remove_duplicates(args, final_df)

  # Write the CSV from the dataframe
  log.info('Creating the csv at the following export path --> "{}".\n'.format(args['export_path']))
  write_csv(args['export_path'], args['fields_to_export'], "Something went wrong when trying to write the final csv after the merge of the partial csv files. The partial csv files won't be deleted.", df=final_df)

  # Delete partial csvs

  if not args['keep_partials']: 
    log.info('Deleting partial csv files\n')
    delete_partial_csvs(args['export_path'][:-4])

  log.info("################ EXITING SUCCESSFULLY ################\n")

if __name__ == "__main__":
  log = CustomLogger(__name__).logger
  main()
