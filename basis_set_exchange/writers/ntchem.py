"""
Conversion of basis sets to NTChem format
"""

from .. import lut, manip, printing, sort


def write_ntchem(basis):
    """Converts a basis set to NTChem format
    """

    basis = manip.uncontract_general(basis, True)
    basis = manip.uncontract_spdf(basis, 0, True)  # 'SP' is not supported
    basis = sort.sort_basis(basis, True)

    electron_elements = set(k for k, v in basis['elements'].items() if 'electron_shells' in v)
    ecp_elements = set(k for k, v in basis['elements'].items() if 'ecp_potentials' in v)

    gto_type = 'cartesian' if 'gto_cartesian' in basis['function_types'] else 'spherical'
    s = '!&basinp gtotype={!r}/\n\n'.format(gto_type)

    if electron_elements:
        s += 'BASIS\n'

        for z in electron_elements:
            data = basis['elements'][z]
            symbol = lut.element_sym_from_Z(z, True)
            s += '{}\n'.format(symbol)

            for shell in data['electron_shells']:
                exponents = shell['exponents']
                coefficients = shell['coefficients']
                ncol = len(coefficients) + 1

                am = shell['angular_momentum']
                amchar = lut.amint_to_char(am, hij=False).upper()
                s += '{} {}\n'.format(amchar, len(exponents))

                point_places = [8 * i + 15 * (i - 1) for i in range(1, ncol + 1)]
                s += printing.write_matrix([exponents, *coefficients], point_places, convert_exp=True)

            s += '***\n'

        s += 'END\n'

    # Write out ECP
    if ecp_elements:
        s += '\n\nECP\n'

        for z in ecp_elements:
            data = basis['elements'][z]
            symbol = lut.element_sym_from_Z(z, True)
            max_ecp_am = max([x['angular_momentum'][0] for x in data['ecp_potentials']])
            max_ecp_amchar = lut.amint_to_char([max_ecp_am], hij=False)

            # Sort lowest->highest, then put the highest at the beginning
            ecp_list = sorted(data['ecp_potentials'], key=lambda x: x['angular_momentum'])
            ecp_list.insert(0, ecp_list.pop())

            s += '{}\n'.format(symbol)
            s += '{} {}\n'.format(max_ecp_am, data['ecp_electrons'])

            for pot in ecp_list:
                rexponents = pot['r_exponents']
                gexponents = pot['gaussian_exponents']
                coefficients = pot['coefficients']
                nprim = len(rexponents)

                am = pot['angular_momentum']
                amchar = lut.amint_to_char(am)

                if am[0] == max_ecp_am:
                    s += '{} potential\n'.format(amchar)
                else:
                    s += '{}-{} potential\n'.format(amchar, max_ecp_amchar)
                s += '{}\n'.format(nprim)

                point_places = [0, 10, 33]
                s += printing.write_matrix([rexponents, gexponents, *coefficients], point_places)

            s += '***\n'

        s += 'END\n'

    return s
