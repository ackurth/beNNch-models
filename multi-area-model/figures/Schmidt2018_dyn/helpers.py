import numpy as np

# Define path to original data (see README file for more information
# how to download the original data)
original_data_path = None

# Define path to the experimental spiking data of Chu et al. (2014) (see README)
chu2014_path = None

population_labels = ['2/3E', '2/3I', '4E', '4I', '5E', '5I', '6E', '6I']


# This path determines the location of the infomap
# installation and needs to be provided to execute the script for Fig. 7
infomap_path = None

tex_names = {'23': 'twothree', '4': 'four', '5': 'five', '6': 'six'}


def structural_gradient(target_area, source_area, arch_types):
    """
    Returns the structural gradient between two areas
    See Schmidt, M., Bakker, R., Hilgetag, C.C. et al.
    Brain Structure and Function (2018), 223:1409,
    for a definition.

    Parameters
    ----------
    target_area : str
        Name of target area.
    source_area : str
        Name of source area.
    arch_types : dict
       Dictionary containing the architectural type for each area.
    """
    if target_area != source_area:
        if arch_types[target_area] < arch_types[source_area]:
            return 'HL'
        elif arch_types[target_area] > arch_types[source_area]:
            return 'LH'
        else:
            return 'HZ'
    else:
        return 'same-area'


def write_out_lw(fn, C, std=False):
    """
    Stores line widths for arrows in path figures
    generated by pstricks to a txt file.

    Parameters
    ----------
    fn : str
        Filename of output file.
    C : dict
        Dictionary with line width values.
    std : bool
        Whether to write out mean or std values.
    """
    if not std:
        max_lw = 0.3  # This is an empirically determined value
        scale_factor = max_lw / np.max(list(C.values()))
        with open(fn, 'w') as f:
            for pair, count in list(C.items()):
                s = '\setboolean{{DRAW{}{}{}{}}}{{true}}'.format(tex_names[pair[0][:-1]],
                                                                 pair[0][-1],
                                                                 tex_names[pair[1][:-1]],
                                                                 pair[1][-1])
                f.write(s)
                f.write('\n')
                s = '\def\{}{}{}{}{{{}}}'.format(tex_names[pair[0][:-1]],
                                                 pair[0][-1],
                                                 tex_names[pair[1][:-1]],
                                                 pair[1][-1],
                                                 float(count) * scale_factor)
                f.write(s)
                f.write('\n')
    else:
        max_lw = 0.3
        scale_factor = max_lw / np.max(list(C['mean'].values()))
        with open(fn, 'w') as f:
            for pair, count in list(C['mean'].items()):
                s = '\setboolean{{DRAW\{}{}{}{}}}{{true}}'.format(tex_names[pair[0][:-1]],
                                                                  pair[0][-1],
                                                                  tex_names[pair[1][:-1]],
                                                                  pair[1][-1])
                f.write('\n')
                s = '\def\{}{}{}{}{{{}}}'.format(tex_names[pair[0][:-1]],
                                                 pair[0][-1],
                                                 tex_names[pair[1][:-1]],
                                                 pair[1][-1],
                                                 float(count) * scale_factor)
                f.write('\n')

            for pair, count in list(C['1sigma'].items()):
                f.write('\n')
                s = '\def\{}{}{}{}sigma{{{}}}'.format(tex_names[pair[0][:-1]],
                                                      pair[0][-1],
                                                      tex_names[pair[1][:-1]],
                                                      pair[1][-1],
                                                      float(count) * scale_factor)
                f.write('\n')


def area_population_list(structure, area):
    """
    Construct list of all populations in an area.

    Parameters
    ----------
    structure : dict
        Dictionary defining the structure of each area.
    area : str
        Area to construct list for.
    """
    complete = []
    for pop in structure[area]:
        complete.append(area + '-' + pop)
    return complete
