#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: november 2020 -*-
# -*- copyright: GH/IPHC 2020 -*-
# -*- file: fisbar.py -*-
# -*- purpose: -*-


'''
Defines the fisbar funciton


subroutine fisrot(A,Z,il,bfis,segs,elmax)

c    This subroutine returns the barrier height bfis, the ground-state
c    energy segs, in MeV, and the angular momentum at which the fission
c    barrier disappears,  Lmax,  in units of h-bar,
c    when called with integer arguments iz, the atomic number,
c    ia, the atomic mass number, and il, the angular momentum in units
c    of h-bar, (Planck's constant divided by 2*pi).
'''

from typing import Dict, Union

from numpy.polynomial.legendre import legvander as legendrepoly

import fisbar.tables as tables


def fisbar(Z: int, A: int, il: int) -> dict:
    '''Returns a dictionarry woth the calculated bfis, egs and elmax'''
    out_dict: Dict[str, Union[str, float, int, bool]] = {
        'success': True,
        'Z': Z, 'A': A, 'L': il,
        'bfis': 0., 'elmax': 0., 'egs': 0.
    }
    try:
        assert 19 < Z < 111
        assert not (Z > 102 and il == 0)
    except AssertionError:
        out_dict['success'] = False
        out_dict['cause'] = "Parameters out of bound"
        return out_dict
    el: float = float(il)
    amin: float = 1.2 * Z + 0.01 * Z * Z
    amax: float = 5.8 * Z - 0.024 * Z * Z
    try:
        assert amin < A < amax
    except AssertionError:
        out_dict['success'] = False
        out_dict['cause'] = "Parameters out of bound"
        return out_dict
    aa: float = 2.5e-3 * A
    zz: float = 1.0e-2 * Z
    bfis0: float = 0.0
    pz = legendrepoly(zz, 7)[0]
    pa = legendrepoly(aa, 7)[0]
    for i in range(7):
        for j in range(7):
            bfis0 += tables.elzcof[j + i * 7] * pz[j] * pa[i]
    egs: float = 0.0
    segs: float = egs
    bfis: float = bfis0
    out_dict['bfis'] = bfis
    amin2: float = 1.4 * Z + 0.009 * Z * Z
    amax2: float = 20.0 + 3.0 * Z
    if ((A < amin2 - 5 or A > amax2 + 10) and il > 0):
        out_dict['success'] = False
        out_dict['cause'] = "Parameters out of bound"
        return out_dict
    el80: float = 0.0
    el20: float = 0.0
    elmax: float = 0.0
    for i in range(4):
        for j in range(5):
            el80 += tables.elmcof[j + i * 5] * pz[j] * pa[i]
            el20 += tables.emncof[j + i * 5] * pz[j] * pa[i]
    sel80 = float(el80)
    sel20 = float(el20)
    out_dict['sel80'] = sel80
    out_dict['sel20'] = sel20
    for i in range(5):
        for j in range(7):
            elmax += tables.emxcof[j + i * 7] * pz[j] * pa[i]
    selmax = elmax
    out_dict['elmax'] = selmax
    if il < 1:
        out_dict['exit'] = 'condition(il < 1)'
        return out_dict
    x = sel20 / selmax
    y = sel80 / selmax
    if el > sel20:
        aj = (-20.0 * x ** 5 + 25.0 * x ** 4 - 4.0) * (y - 1.0) ** 2 * y * y
        ak = (-20.0 * y ** 5 + 25.0 * y ** 4 - 1.0) * (x - 1.0) ** 2 * x * x
        q = 0.20 / ((y - x) * ((1.0 - x) * (1.0 - y) * x * y) ** 2)
        qa = q * (aj * y - ak * x)
        qb = -q * (aj * (2.0 * y + 1.0) - ak * (2.0 * x + 1.0))
        z = el / selmax
        a1 = 4.0 * z ** 5 - 5.0 * z ** 4 + 1.0
        a2 = qa * (2.0 * z + 1.0)
        bfis *= (a1 + (z - 1.0) * (a2 + qb * z) * z * z * (z - 1.0))
    else:
        q = 0.20 / (sel20 ** 2 * sel80 ** 2 * (sel20 - sel80))
        qa = q * (4.0 * sel80 ** 3 - sel20 ** 3)
        qb = -q * (4.0 * sel80 ** 2 - sel20 ** 2)
        bfis *= (1.0 + qa * el ** 2 + qb * el ** 3)
    if bfis <= 0.0:
        bfis = 0.0
        out_dict['found_bf_lower_than_0'] = True
    out_dict['bfis'] = bfis
    if el > selmax:
        bfis = 0.0
        out_dict['given_el_larger_than_elmax'] = True
    # c    Now calculate rotating ground-state energy
    ell = el / elmax
    if il == 1000:
        ell = 1.
    pl = legendrepoly(ell, 9)[0]
    for k in range(5):
        for l in range(7):
            for m in range(5):
                egs += tables.egs[m + (l + k * 7) * 5] * pz[l] * pa[k] * pl[2 * m - 1]
    segs = egs if egs >= 0. else 0.0
    out_dict['egs'] = segs
    return out_dict

# EOF
