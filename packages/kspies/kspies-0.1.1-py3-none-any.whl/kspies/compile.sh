f2py -c --fcompiler=gnu95 --f90flags='-fopenmp' -lgomp -llapack kspies_fort.f90 -m kspies_fort
