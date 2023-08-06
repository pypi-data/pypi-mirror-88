# NMJ_Analyser
The code was created using python 3.7 and the following version of packages
## Requirements
 - scipy 1.5.3
 - Pillow 7.2.0
 - numpy 1.19.1
 - pandas 1.1.0
 - nibabel 3.1.1
 
In addition, the following modules are imported
 - glob
 - os
 - argparse
 - sys

Performs analysis of NMJ data 

## Usage

The NMJ Analyser takes as input directories where jpg files have been stored 

For each subject, the input is presented as 
SUBJ/JPEG/*jpg
The ..... files must contain the keyword red or RED
The ..... files must contain the keyword green or GREEN
The slices should ordered numerically ex Mouse1_GREEN_0001.jpg.... Mouse1_GREEN_0010.jpg

The following parameters are given to the system:
 - -p regular expression of the subject path
 - -dx planar resolution
 - -dz slice thickness
 - -t threshold for voxels to be considered as positives
 
## Output
 For each subject the following parameters are calculated for each RED connected component and intersection of GREEN on RED component
 
### RegionProperties
 - 'centre of mass': (self.centre_of_mass, ['CoMx',
                                                     'CoMy',
                                                     'CoMz']),
 - 'centre_abs': (self.centre_abs, ['Truex, Truey, Truez']),
 - 'volume': (self.volume,
                       ['NVoxels', 'NVolume']),
 - 'fragmentation': (self.fragmentation, ['Fragmentation']),
 - 'mean_intensity': (self.mean_int, ['MeanIntensity']),
 - 'surface': (self.surface, ['NSurface', 'Nfaces_surf',
                                       'NSurf_ext', 'Nfaces_ext']),
 - 'surface_dil': (self.surface_dil, ['surf_dil', 'surf_ero']),
 - 'surface volume ratio': (self.sav, ['sav_dil', 'sav_ero']),
 - 'compactness': (self.compactness, ['CompactNumbDil'
                                               ]),
 - 'eigen': (self.eigen, ['eigenvalues']),
 - 'std': (self.std_values, ['std']),
 - 'quantiles': (self.quantile_values, ['quantiles']),
 - 'bounds': (self.bounds, ['bounds']),
 - 'cc': (self.connect_cc, ['N_CC']),
 - 'cc_dist': (self.dist_cc, ['MeanDistCC']),
 - 'cc_size': (self.cc_size, ['MinSize', 'MaxSize', 'MeanSize']),
 - 'max_extent': (self.max_extent, ['MaxExtent']),
 - 'shape_factor': (self.shape_factor, ['ShapeFactor',
                                                 'shapefactor_surfcount']),
 - 'skeleton_length': (self.skeleton_length, ['SkeletonLength'])
 
### Comparison Properties
 - 'green volume': (self.n_pos_ref, 'Volume_(Green)'),
 - 'red volume': (self.n_pos_seg, 'Volume_(Red)'),
 - 'n_intersection': (self.n_intersection, 'Intersection'),
 - 'n_union': (self.n_union, 'Union'),
 - 'IoU': Intersection of union
 - 'coverage': Overlap        
 - 'vol_diff': Volume difference
 - 'ave_dist': Average distance
 - 'haus_dist': Hausdorff distance
 - 'haus_dist95': 95% HD
 - 'com_dist': distance between centre of mass
 - 'com_ref': centre of mass RED
 - 'com_seg': centre of mass GREEN
