"""
Functions for reading specifically formatted data
"""


# for ENVI spectral libraries
def spectralLibrary(path):
    """
    Reads an ENVI-format spectral library into memory.

    :param path: file path to the ENVI spectral library file. Looks for an accompanying .hdr file.
    :return s: an earthlib spectralObject with the spectral library data
    """
    import numpy as np
    import spectral

    from earthlib.utils import checkFile, spectralObject

    # check for header files
    if checkFile(path[:-4] + ".hdr"):
        hdr = path[:-4] + ".hdr"
    else:
        if checkFile(path + ".hdr"):
            hdr = path + ".hdr"
        else:
            return None

    # read the spectral data
    slib = spectral.envi.open(hdr, path)

    # create the spectral object
    s = spectralObject(
        slib.params.nrows,
        slib.params.ncols,
        band_centers=np.asarray(slib.bands.centers),
        band_unit=slib.bands.band_unit,
        band_quantity=slib.bands.band_quantity,
    )

    # set the spectra and names
    s.spectra = slib.spectra
    s.names = slib.names

    # return the final object
    return s


def endmembers():
    """
    Reads the earthlib spectral endmember library

    :return s: an earthlib spectralObject with the endmember library reflectance data
    """
    from .utils import _endmember_path

    s = spectralLibrary(_endmember_path)
    return s


# ascii spectra from the joint fire science program (https://www.frames.gov/assessing-burn-severity/spectral-library/overview)
def jfsp(path):
    """
    Reads the ASCII format spectral data from the joint-fire-science-program
    and returns an object with the mean and +/- standard deviation reflectance data

    :param path: file path to the JFSP spectra text file
    :return s: an earthlib spectralObject with the JFSP reflectance data
    """
    import numpy as np

    from earthlib.utils import spectralObject

    # create the spectral object
    s = spectralObject(1, type="asd")
    s.spectra_stdevm = np.zeros(s.spectra.shape)
    s.spectra_stdevp = np.zeros(s.spectra.shape)

    # open the file and read the data
    with open(path, "r") as f:
        f.readline()
        for i, line in enumerate(f):
            line = line.strip().split()
            s.spectra[0, i] = line[1]
            s.spectra_stdevp[0, i] = line[2]
            s.spectra_stdevm[0, i] = line[3]

        # return the spectral object
        return s


# ascii spetra from the USGS (https://www.sciencebase.gov/catalog/item/5807a2a2e4b0841e59e3a18d)
def usgs(path):
    """
    Reads the ascii format spectral data from USGS and returns an object with the mean and +/- standard deviation

    :param path: file path the the USGS spectra text file
    :return s: an earthlib spectralObject with the USGS reflectance data
    """
    import numpy as np

    from earthlib.utils import spectralObject

    # open the file and read header info
    with open(path, "r") as f:
        x_start = "gibberish"
        for line in f:
            if x_start in line:
                break
            if "Name:" in line:
                spectrum_name = line.strip().split("Name:")[-1].strip()
            if "X Units:" in line:
                band_unit = line.strip().split()
                band_unit = band_unit[-1].strip("()").capitalize()
            if "Y Units:" in line:
                refl_unit = line.strip().split()
                refl_unit = refl_unit[-1].strip("()").capitalize()
            if "First X Value:" in line:
                x_start = line.strip().split()[-1]
            if "Number of X Values:" in line:
                n_values = int(line.strip().split()[-1])

        # now that we got our header info, create the arrays
        #  necessary for output
        band_centers = np.empty(n_values)
        reflectance = np.empty(n_values)

        line = line.strip().split()
        band_centers[0] = float(line[0])
        reflectance[0] = float(line[1])

        # resume reading through file
        i = 1
        for line in f:
            line = line.strip().split()
            band_centers[i] = float(line[0])
            reflectance[i] = float(line[1])
            i += 1

        # some files read last -> first wavelength. resort as necessary
        if band_centers[0] > band_centers[-1]:
            band_centers = band_centers[::-1]
            reflectance = reflectance[::1]

        # convert units to nanometers and scale 0-1
        if band_unit.lower() == "micrometers":
            band_centers *= 1000.0
            band_unit = "Nanometers"
        if refl_unit.lower() == "percent":
            reflectance /= 100.0

        # create the spectral object
        s = spectralObject(
            1,
            n_values,
            band_centers=band_centers,
            band_unit=band_unit,
            band_quantity="Wavelength",
        )

        # assign relevant values
        s.spectra[0] = reflectance
        if spectrum_name:
            s.names[0] = spectrum_name

    # return the final object
    return s
