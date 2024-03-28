from pyopenms import *
import numpy as np

def getTIC(mzml):
    frags = MSExperiment()
    MzMLFile().load(mzml, frags)
    # 2) get TIC data using list comprehensions
    ms2dict = {}
    retention_times = []
    intensities = []
    for spec in frags:
        if spec.getMSLevel() == 1:
            retention_times.append(spec.getRT())
            intensities.append(sum(spec.get_peaks()[1]))
        elif spec.getMSLevel() == 2:
            ms2dict[retention_times[-1]] = {'parent':spec.getPrecursors()[0].getMZ(),
                                     'rt':spec.getRT(),
                                     'peaks':[spec.get_peaks()[0].tolist(), spec.get_peaks()[1].tolist()]}
        else:
            pass
    return {'rt': retention_times, 'int': intensities}, ms2dict


def getPoints(tic, lst):
    retention_times = tic['rt']
    intensities = tic['int']
    rt = []
    inty = []
    for i in lst.index:
      xtime = lst.loc[i, 'Time']
      ydiff = np.abs(retention_times-xtime)
      yloc = np.where((ydiff.min()==ydiff))[0][0]
      #rt.append(lst.loc[i, 'Time'])
      rt.append(retention_times[yloc])
      inty.append(intensities[yloc])
    return {'rt': rt, 'int': inty}

#https://github.com/CCMS-UCSD/GNPS_Workflows/blob/8c6772e244c6f3e5ea7cd5eae873b6faa48b7313/molecular-librarysearch-gc/tools/molecularsearch-gc/ming_spectrum_library.py#L461
def get_mgf_string(spectrum):
    output_string = "BEGIN IONS\n"
    output_string += "PEPMASS=" + str(spectrum['parent']) + "\n"
    #output_string += "CHARGE=" + str(self.spectrum.charge) + "\n"
    output_string += "MSLEVEL=" + "2" + "\n"
    #output_string += "SOURCE_INSTRUMENT=" + self.instrument + "\n"
    output_string += "FILENAME=" + spectrum['file'] + "\n"
    output_string += "SEQ=" + "*..*" + "\n"
    output_string += "NOTES=" + f"gnps2:{spectrum['gnps']}chw:{spectrum['chw']}" + "\n"
    #output_string += "IONMODE=" + self.ionmode + "\n"
    #output_string += "ORGANISM=" + self.libraryname + "\n"
    #output_string += "NAME=" + self.compound_name + "\n"
    #output_string += "SMILES=" + self.smiles + "\n"
    #output_string += "INCHI=" + self.inchi + "\n"
    #output_string += "LIBRARYQUALITY=" + self.libraryquality + "\n"
    #output_string += "SPECTRUMID=" + self.spectrumid + "\n"
    #output_string += "ACTIVATION=" + self.activation + "\n"
    #output_string += "INSTRUMENT=" + self.instrument + "\n"
    output_string += "SCANS=" + spectrum['scan'] + "\n"
    output_string += '\n'.join(['%s\t%s' % x for x in list(zip(*spectrum['peaks']))])
    output_string += "\nEND IONS\n"

    return output_string

