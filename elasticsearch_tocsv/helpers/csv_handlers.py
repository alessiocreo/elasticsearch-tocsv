import os, sys, glob
import pandas as pd

def check_csv_already_written(filename):
  if os.path.exists(filename):
    overwrite_file = ''
    while overwrite_file not in ['y', 'n']:
      overwrite_file = input(f"\nThere is already a csv file at the given path ({filename}). Do you want to overwrite it? (y/n)").lower().strip()
    if overwrite_file == 'n':
      sys.exit("\nExiting script not to overwrite the file. No query has been run.")
    elif overwrite_file != 'y':
      print("Please answer with 'y' or 'n'")
  return filename

def write_csv(export_path, fields_to_export, exception_message='', df=None, list_to_convert=False):
  df = pd.DataFrame(list_to_convert, columns=fields_to_export) if list_to_convert else df
  try: 
    df.to_csv(export_path, index=False, columns=fields_to_export)
  except Exception as e:
    sys.exit(f"{exception_message} Here's the exception: \n\n{e}")

def join_partial_csvs(filename):
  try: 
    list_of_csvs = sorted([csv for csv in glob.glob(f"{filename}_process*.csv")])
    final_df = pd.concat([pd.read_csv(csv) for csv in list_of_csvs])
    return final_df
  except Exception as e:
    sys.exit(f"Something went wrong when trying to merge partial csv files previously created. The partial csv files won't be deleted. Here's the exception: \n\n{e}")

def delete_partial_csvs(basic_filename):
  try:
    list_of_csvs = sorted([csv for csv in glob.glob(f"{basic_filename}_process*.csv")])
    for csv in list_of_csvs:
      os.remove(csv)
    return True
  except Exception as e:
    sys.exit(f"Something went wrong when trying to delete partial csv files previously created. Here's the exception: \n\n{e}")