import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from PIL import Image

raw_filename = ""
totals_collection = []
image_count = 50

for i in range(image_count):
    raw_filename = rf"C:\Users\ryans\Desktop\Spectrum1_tritium_ice_blue\{i}.jpg"
    im = np.asarray(Image.open(raw_filename))
    sliced_im = im[1100:1200, 970:1570] # use this to slice out the spectrum
    im = Image.fromarray(np.uint8(sliced_im)).convert('RGB')
    newsize = (300, im.size[1])
    im = im.resize(newsize)
    im = np.asarray(im)
    totals = [0] * im.shape[1]

    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            totals[x] += sum(im[y][x])

    totals = (np.array(totals) / 255).tolist()
    totals_collection.append(np.array(totals))

totals = (sum(totals_collection) / image_count).tolist()

totals.reverse()


def wavelength_to_rgb(wavelength, gamma=0.8):
    ''' taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    Additionally alpha value set to 0.5 outside range
    '''
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.
    else:
        A = 0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength > 750:
        wavelength = 750.
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R, G, B, A)


clim = (400, 700)
norm = plt.Normalize(*clim)
wl = np.arange(clim[0], clim[1] + 1, 2)
colorlist = list(zip(norm(wl), [wavelength_to_rgb(w) for w in wl]))
spectralmap = colors.LinearSegmentedColormap.from_list("spectrum", colorlist)

fig, axs = plt.subplots(1, 1, figsize=(8, 4), tight_layout=True)

mySpectra = {}
mySpectra['wavelengths'] = np.arange(400, 700, 1)
mySpectra['intensities'] = totals

wavelengths = mySpectra['wavelengths']
spectrum = mySpectra['intensities']
plt.plot(wavelengths, spectrum, color='black', linewidth=1)
plt.title("Emission Spectrum of a Ice Blue Tritium Vial")

y = mySpectra['intensities']
X, Y = np.meshgrid(wavelengths, y)

extent = (np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))

plt.imshow(X, clim=clim, extent=extent, cmap=spectralmap, aspect='auto')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')

plt.fill_between(wavelengths, spectrum, max(spectrum), color='w')
plt.savefig('WavelengthColors.png', dpi=200)

plt.show()
