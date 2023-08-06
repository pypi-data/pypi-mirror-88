'''Decorator for the compiled Fortran library tipsv.

'''

from dsmpy.flib import tipsv


def _pinput(parameter_file):
    inputs = tipsv.pinput_tipsv(parameter_file)
    return inputs


def _tipsv(
        re, ratc, ratl, tlen, nspc, omegai,
        imin, imax, nzone, vrmin, vrmax, rho,
        vpv, vph, vsv, vsh, eta, qmu, qkappa, r0, eqlat, eqlon, mt, nr,
        theta, phi, lat, lon, output, write_to_file):
    spcs = tipsv.tipsv(
        re, ratc, ratl, tlen, nspc, omegai,
        imin, imax, nzone, vrmin, vrmax, rho,
        vpv, vph, vsv, vsh, eta, qmu, qkappa, r0, eqlat, eqlon, mt, nr,
        theta, phi, lat, lon, output, write_to_file)
    return spcs
