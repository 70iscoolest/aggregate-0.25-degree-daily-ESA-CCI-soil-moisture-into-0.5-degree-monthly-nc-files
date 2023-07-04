def assign_nan(nc_file):
    nc_org = xr.open_dataset(nc_file)
    # replace missing values with NaN
    sm_values = nc_org.variables['sm'][:].data
    R = np.where(sm_values == -9999.0) # missing values were assigned with -9999.0
    sm_values[R] = np.nan
    sm_values.astype(np.float32)

    # nc_org.variables['sm'][:] = sm_values
    print('the minimum sm value: ', np.nanmin(sm_values))

    # temp = sm_values.reshape(1, -1)
    return sm_values

def month_aggregate(year, m):
    print('month number: ', m)
    aa = str(year) + m
    m_files = [x for x in daily_files if aa in x]
    print('file numbers in this month: ', len(m_files))

    sum_temp = np.empty(shape=(len(m_files), 720, 1440))

    for id, nc_file in enumerate(m_files):
        sm_values = assign_nan(nc_file)
        sum_temp[id, :, :] = sm_values

    mean_temp = np.nanmean(sum_temp, axis=0, dtype=np.float32)
    mean_sm_values = np.reshape(mean_temp, (1, 720, 1440))

    ref_nc = nc.Dataset(m_files[0])
    ref_lat = ref_nc.variables['lat'][:].data
    ref_lon = ref_nc.variables['lon'][:].data
    ref_time = ref_nc.variables['time'][:].data
    # ref_attrs = ref_nc.attrs

    filename = os.path.join(op_dir, 'ESACCI_SM_' + str(year) + m + '_agg.nc')

    mean_nc = nc.Dataset(op_ncfilename, "w", format="NETCDF4")
    mean_nc.createDimension("latitude", len(ref_lat))
    mean_nc.createDimension("longitude", len(ref_lon))
    mean_nc.createDimension("time", 1)

    mean_nc.createVariable("latitude", "f", ("latitude"))
    mean_nc.createVariable("longitude", "f", ("longitude"))
    settime = mean_nc.createVariable("time", ref_nc.variables['time'].datatype,
                                  ref_nc.variables['time'].dimensions)
    settime.units = ref_nc.variables['time'].units
    settime.longname = 'time'


    mean_nc.createVariable(varname="sm", datatype="f", dimensions = ("time", "latitude", "longitude"), fill_value=1.e20)

    mean_nc.variables["latitude"][:] = ref_lat
    mean_nc.variables["longitude"][:] = ref_lon

    mean_nc.variables["time"][:] = ref_time

    mon_nc.variables['sm'][:] = mean_sm_values
    

    ref_nc.close()
    mon_nc.close()

    # mon_nc.setncattr(ref_attrs)


if __name__ == '__main__':
    import os
    import glob
    import xarray as xr
    import netCDF4 as nc
    import numpy as np
    from print_logging import *
    import warnings
    # import scipy
    warnings.filterwarnings("ignore")

    log_dir = './log/'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    make_print_to_file(log_dir, 'average_monthly_nc_esacci_0616.py') #print to txt

    nc_dir = '../DATA_org/'#where original daily files are saved
    op_dir = '../DATA_monthly'#where monthly nc files will be saved
    if not os.path.exists(op_dir):
        os.mkdir(op_dir)

    years = range(1980, 2020)
    mon = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    for year in years:

        daily_dir = os.path.join(nc_dir, str(year))
        daily_files = glob.glob(daily_dir + '/*.nc')

        for m in mon:
            month_aggregate(year, m)

        print('finish aggregate daily netCDF files in year {} to monthly scale!'.format(year))

    print('----------------------------------finish!----------------------------------------')





























































