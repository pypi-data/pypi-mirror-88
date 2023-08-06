# SpectroscPy 0.3.1
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Minde Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

# Checks to see if there are any type of resonances, which can be problematic for the mathematics, 
# because of singularities

from .parameters import fermi_threshold, martin_threshold, plancs_constant, speed_of_light

# Function: "Are we dealing with a Fermi resonance?"
# Uses the Martin parameters as thresholds: See e.g. J. Chem. Phys 136, 124108 (2012) 
# and J. Chem. Phys. 122, 014108 (2005) eq 52 and 53
# delta is (wi + wj - wk), or if i == j (2wi - wk)
def is_fermi_resonance(delta, cubic_force_ijk, i_is_j):
    fermi = False
    #return fermi
    if (abs(delta) <= fermi_threshold):
        if (i_is_j):
            martin_parameter = cubic_force_ijk**4/(256.0*delta**3)
            if (abs(martin_parameter) >= martin_threshold):
                fermi = True
            else:
                fermi = False
        else:
            martin_parameter = cubic_force_ijk**4/(64.0*delta**3)
            if (abs(martin_parameter) >= martin_threshold):
                fermi = True
            else:
                fermi = False

    return fermi


def add_fermi_resonance(total_list, new_element):

    i = new_element[0]
    j = new_element[1]
    k = new_element[2]
    l = new_element[3]

    j, k = sorted([j, k])
    new_element[0] = i
    new_element[1] = j
    new_element[2] = k
    new_element[3] = l

    if not new_element in total_list:
        total_list.append(new_element)

    return total_list


def is_11_resonance(delta, coupling_factor, coupling_type):

    delta = delta/(plancs_constant*speed_of_light*100)
    if (coupling_type == 'cubic'):
        coupling_factor = coupling_factor/(plancs_constant*speed_of_light*100)**2
    elif(coupling_type == 'quartic'):
        coupling_factor = coupling_factor/(plancs_constant*speed_of_light*100)
    else:
        print(contribution_type)
        print('Error in is_11_resonance.  No, or incorrect, coupling_type has been stated.')

    if (abs(delta) <= 100.0):
        if (abs(coupling_factor) >= 10.0):
            return True
        else:
            if (abs(coupling_factor/(delta**2)) >= 1.0):
                return True
            else:
                return False
    else:
        return False
