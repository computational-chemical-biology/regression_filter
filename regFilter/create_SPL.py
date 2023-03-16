import pandas as pd

#Exclusion list -> It's a .csv file generated by create_report.py
def create_SPL(exclusion_list, peaks_info):
    df = pd.read_csv(exclusion_list)
    lista = df.iloc[:, 0].tolist()
    
    dfx = peaks_info.reset_index()
    dfx.drop(['index'], axis=1, inplace=True)
    dfx.set_index('row ID', inplace = True)
    dfx.index = dfx.index.astype(int)
    dfx.drop(lista, 0, inplace = True)

    name = []
    time = []
    time_tol = []
    mass_begin = []
    mass_end = []

    for item in dfx.index:
        name.append('')
        time.append(dfx['row retention time'][item]*60)
        time_tol.append(30)
        mass_begin.append(dfx['row m/z'][item])
        mass_end.append('')
    
    col_names = ["Compound Name", "Time", "Time Tolerance", "Mass Begin", "Mass End"]
    SPL = pd.DataFrame(zip(name,time,time_tol,mass_begin,mass_end), columns = col_names)
    SPL.to_csv("SPL_list.csv")