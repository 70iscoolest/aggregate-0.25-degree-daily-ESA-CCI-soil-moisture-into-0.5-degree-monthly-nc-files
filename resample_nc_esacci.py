def interpolation(year, m, lats, lons):
    ym = str(year) + m
    filename = os.path.join(nc_dir, 'ESACCI_SM_' + ym + '_agg.nc')
    nc = xr.open_dataset(filename)
    new_nc = nc.interp(longitude=lons, latitude=lats, method="linear")

    new_nc.to_netcdf(os.path.join('../temp', 'ESACCI_SM_' + ym + '_agg_res05.nc'))
    return new_nc




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
    # if not os.path.exists(log_dir):
    #     os.mkdir(log_dir)

    # make_print_to_file(log_dir, 'average_monthly_nc_esacci_0616.py')

    nc_dir = '../DATA_monthly'
    op_dir = '../DATA_interp'
    if not os.path.exists(op_dir):
        os.mkdir(op_dir)

    years = range(1980, 2020)
    mon = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    lats = np.arange(-90, 90, 0.5)
    lons = np.arange(-180, 180, 0.5)

    nc_merge = []
    for year in years:
        for m in mon:
            new_nc = interpolation(year, m, lats, lons)
            file = new_nc['sm']
            nc_merge.append(file)

    da = xr.concat(nc_merge, dim='time')
    da.to_netcdf(os.path.join('../temp', 'ESACCI_SM_1980_2019_mon_res05.nc'))

    print('----------------------------------finish!----------------------------------------')





























































