import os
import pandas as pd
from pyopenms import *
import matplotlib.pyplot as plt
import warnings

def matchFeats(query, ref, ppm=15, rtabs=20):
    mzdiff = ref['row m/z'].apply(lambda a: ((a-query['row m/z'])/query['row m/z'])*10**6).abs()
    rtdiff = (ref['row retention time']-query['row retention time']).abs()

    diff = (mzdiff < ppm) & (rtdiff < rtabs)

    ans = ref.loc[diff, ['row ID', 'row m/z', 'row retention time']]

    if len(ans):
        ans['q-id'] = query['row ID']
        ans['q-m/z'] = query['row m/z']
        ans['q-rt'] = query['row retention time']
        ans['ppm'] = mzdiff[diff]
        ans['rtabs'] = rtdiff[diff]
        return ans
    else:
        return pd.DataFrame()

def getMatchingMS2(lst, exp, mzabs=0.1):
  """
  Searches for MS2 events inside a reference table with time and mass windows.
  Parameters:
  -------------------
  lst: pandas.DataFrame
    Reference table with peak time windows
  exp: pyopenms.MSExperiment
    Spectra object from pyopenms
  -------------------
  Returns:
    Nested list with reference table index, scan number,
    precursor mass and retention time
  """
  ms2 = []
  for spec in exp:
    if spec.getMSLevel() == 2:
      rt = spec.getRT()
      pr = spec.getPrecursors()[0].getMZ()
      idx = (lst['Sec Begin'] <= rt) & (lst['Sec End'] >= rt) & (abs(lst['Mass Begin']-pr)<mzabs)
      if idx.sum()==1:
        ind = lst[idx].index.values[0]
      elif idx.sum()>1:
        warnings.warn("Overlaping time windows, selecting first match.")
        ind = lst[idx].index.values[0]
      else:
        continue
      scan = int(spec.getNativeID().replace('scan=', '')) - 1
      ms2.append([ind, scan, pr, rt])
  return ms2

def getSpecStat(peaks):
    n = len(peaks[0])
    if n==0:
        return None
    mn = peaks[1].min()
    mx = peaks[1].max()
    me = peaks[1].mean()
    sd = peaks[1].std()
    return [n, mn, mx, me, sd]

def eventSummary(frag_list, chrom_obj):
    frmatch = getMatchingMS2(frag_list, chrom_obj)

    spec_stat = []

    for x in frmatch:
        statlst = getSpecStat(chrom_obj.getSpectrum(x[1]).get_peaks())
        if statlst is not None:
            spec_stat.append(x[:2]+statlst)

    spec_stat_df = pd.DataFrame(spec_stat)
    spec_stat_df.columns = ['lst_id', 'scan_id', 'num peaks', 'min', 'max', 'mean', 'std']

    ct = spec_stat_df['lst_id'].value_counts()

    mean_chrom = spec_stat_df.groupby('lst_id', group_keys=True).mean().drop(['scan_id'], axis=1)
    mean_chrom['ms2_events'] = 0
    mean_chrom.loc[ct.index, 'ms2_events'] = ct
    return mean_chrom

def plotMirror(spec1, spec2):
    for i in range(len(spec1[0])):
      plt.vlines(x = spec1[0][i], ymin = -spec1[1][i], ymax = 0,
                colors = 'green',
                label = 'List')

    for j in range(len(spec2[0])):
      plt.vlines(x = spec2[0][j], ymin = 0, ymax = spec2[1][j],
                colors = 'red',
                label = 'DDA')

    plt.title('Non normalized mirror plot')
    plt.ylabel('Intensity')
    leg = plt.legend(labels=['Query', 'Reference'], loc = 'upper left')
    leg.legendHandles[0].set_color('red')
    leg.legendHandles[1].set_color('green')

def plotMS2cube(chrom_obj):
    ax = plt.figure(figsize=(12,10)).add_subplot(projection='3d')
    for spec in chrom_obj:
        if spec.getMSLevel() == 2:
            y = spec.getRT()
            p = spec.getPrecursors()[0]
            x = p.getMZ()
            z = p.getIntensity()
            ax.plot([x, x], [y, y], [0, z], 'k--', linewidth=0.5)

    ax.set_xlabel('m/z')
    ax.set_ylabel('Retention time')
    ax.set_zlabel('Intensity')

def getEventsWithRep(dr, lst):
    fls = [x for x in os.listdir(dr) if 'mzML' in x]
    event_list = []
    if len(fls):
        print('Found %s mzML files in the directory.' % len(fls))
    else:
        raise Exception("No mzML files detected")
    for i in range(len(fls)):
        fl = fls[i]
        frags = MSExperiment()
        MzMLFile().load(f"{dr}/{fl}", frags)
        mean_frags = eventSummary(lst, frags)
        print('Found %s ions for replicate %s' % (len(mean_frags), i+1))
        mean_frags['replicate'] = i+1
        event_list.append(mean_frags)

    return pd.concat(event_list)

def generateUID(comparison_table, reference_table, regFilterFiltered):
    comparison_table['uid'] = comparison_table.apply(lambda a: f"{str(a['q-m/z']).split('.')[0]}_{str(a['q-rt']).split('.')[0]}",
                                                     axis=1)
    print(f"Reference table has {reference_table.shape[0]} entries.")
    reference_table_uid = pd.merge(reference_table[['row ID', 'row m/z', 'row retention time']],
                              comparison_table[['row ID', 'uid']], on='row ID', how='left')
    reference_table_uid.loc[reference_table_uid.uid.isna(), 'uid'] = reference_table_uid.apply(lambda a: f"{str(a['row m/z']).split('.')[0]}_{str(a['row retention time']).split('.')[0]}",
                                                                                               axis=1)[reference_table_uid.uid.isna()]
    print(f"Reference table with unique IDs has {reference_table_uid.shape[0]} entries, including duplications.")
    print(f"Reference table had {len(reference_table_uid.uid.unique())} unique IDs.")
    print(f"regFilterFiltered table has {regFilterFiltered.feat_tab[regFilterFiltered.sel==1].shape[0]} entries.")
    regFilterFiltered_uid = pd.merge(regFilterFiltered.feat_tab.loc[regFilterFiltered.sel==1,
                                                            ['row ID', 'row m/z', 'row retention time']],
                        comparison_table[['q-id', 'uid']], left_on='row ID', right_on='q-id',
                        how='left')

    regFilterFiltered_uid.loc[regFilterFiltered_uid.uid.isna(), 'uid'] = regFilterFiltered_uid.apply(lambda a: f"{str(a['row m/z']).split('.')[0]}_{str(a['row retention time']).split('.')[0]}",
                                                                                                     axis=1)[regFilterFiltered_uid.uid.isna()]
    print(f"regFilterFiltered table with unique IDs has {regFilterFiltered_uid.shape[0]} entries, including duplications.")
    print(f"regFilterFiltered table had {len(regFilterFiltered_uid.uid.unique())} unique IDs.")

    return reference_table_uid, regFilterFiltered_uid
