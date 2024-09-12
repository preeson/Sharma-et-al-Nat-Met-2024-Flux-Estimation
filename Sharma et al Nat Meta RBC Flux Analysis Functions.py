# Sharma et al Nat Meta RBC Flux Analysis Functions
# Analysis code related to RBC Flux estimates in
# "A pathogenic role for IL-10 signalling in capillary stalling and cognitive impairment in type 1 diabetes"

# Written by Dr. Patrick Reeson, MSFHR Scholar, 2023
# Brown Lab, Division of Medical Sciences, University of Victoria

def open_data(file_name, ops):
    """ Opens, inverts and filters 1D time series

    This function opens a .csv file which should contain an 'X' and 'Y' column
    for a 1D timeseries, it then inverts the data based on 12 bit maximum of 4095
    and then filters the inverted data using Savitzky-Golay filtering
    https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter

    Args:
      file_name (str): path to .csv file to open
      ops (dict): analysis parameters

    Returns:
      data (pandas DataFrame): data with columns "X", "Y", "invert" and "Smoothed"

    Raises:
      AssertionError "does not exist" if file_name does not exist

    """
    import pandas as pd  # import pandas (data science tools)
    from pathlib import Path
    from scipy.signal import savgol_filter

    assert Path(file_name).exists(), f'{file_name} does not exist'
    data = pd.read_csv(file_name,encoding='unicode_escape')
    # NOTE The exact wording of the data coloumn can be "Y" or "Gray_Value"
    # Need to add a Try code to deal with both options
    data["invert"] = 4095 - data["Gray_Value"]  # create inverse data
    data['smoothed'] = savgol_filter(data['invert'],
                                     window_length=ops['window_length'],
                                     polyorder=ops['polyorder'])
    return data


def find_peaks(data, ops):
    """ Find peaks in 1D timeseries of RBC flux

  This function uses the scipy find_peaks function to identify significant
  peaks in the 1D timeseries data that satisfys specific criteria
  https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
  and then calculates estimated RBC flux from slow full feild raster scanning

  Args:
    data (pandas DataFrame): data with columns "X", "Y", "invert" and "Smoothed"
    ops (dict): analysis parameters

  Returns:
    data (pandas DataFrame): data with columns "X", "Y", "invert", "Smoothed" and "norm"
    RBCs (tuple): output from scipy.signal.find_peaks
    rbc_flux (float): esitmated rbc flux for pesudo linscan
  """
    import numpy as np
    from scipy.signal import find_peaks
    norm_factor = ops['norm_factor']  # percentile to normalize data
    min_height = ops['height']  # minimum height a peak must be
    width = ops['width']  # minimum width of peak
    dist = ops['dist']  # minimum distance between peaks
    prom = ops['prom']  # difference between adjacent peaks

    # Now find peaks on data
    bl = np.percentile(data["smoothed"], norm_factor)
    bl_sub = data["invert"] - bl
    norm = bl_sub / bl
    data["norm"] = norm
    RBCs = find_peaks(norm, height=min_height, threshold=None, distance=dist, prominence=prom,
                      width=width)
    # Now calculate the RBC flux from the raster scan intensity profile
    n_lines = data.shape[0]
    t_line = ops['t_line']
    total_time = n_lines * t_line
    peaks = RBCs[0]
    n_RBCs = len(peaks)
    rbc_flux = (n_RBCs / total_time) * 1000
    print(f" Therefore RBC flux was {rbc_flux:.2f}  / sec")
    return data, RBCs, rbc_flux
