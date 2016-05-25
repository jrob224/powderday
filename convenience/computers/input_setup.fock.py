#script intended to set up the qsub files and model*.py files assuming
#sphgr physical properties have been written out to an npz file, and
#that the system we're running on is Haverford's Fock cluster.

import numpy as np
from subprocess import call
import pdb,ipdb
from sphgr_progen import progen
#===============================================
#MODIFIABLE HEADER
#===============================================

#shell scripting
nnodes=6
startsnap=160
endsnap=161 #set the same as startsnap if you just want to do one snapshot
#model_dir='/Volumes/pegasus/pd_runs/m13m14_lr_Dec9_2013/geach_LAB1/'
#hydro_dir='/Volumes/pegasus2/gadgetruns/m13m14_lr_Dec9_2013/'

model_dir = '/Volumes/pegasus/pd_runs/MassiveFIRE/HR/B100_N512_M3e13_TL00004_baryon_toz2_HR_9915/geach_LAB1'
hydro_dir = '/Volumes/pegasus2/gadgetruns/MassiveFire/HR/B100_N512_M3e13_TL00004_baryon_toz2_HR_9915/'

#if we want to write the files locally, but have the paths in the
#parameters files lead to differnet paths (for a different computer),
#put those paths here.  otherweise, set these equal to whatever is in
#model_dir and hydro_dir
model_dir_remote = '/astro/desika/pd_runs/MassiveFIRE/HR/B100_N512_M3e13_TL00004_baryon_toz2_HR_9915/geach_LAB1/'
hydro_dir_remote = '/astro/desika/gadgetruns/MassiveFire/HR/B100_N512_M3e13_TL00004_baryon_toz2_HR_9915/'

model_run_name='MassiveFIRE'
COSMOFLAG=0 #flag for setting if the gadget snapshots are broken up into multiples or not



SPHGR_COORDINATE_REWRITE = True

#GAL = 14 #this is the galaxy from SPH_PROGEN we need to find the
         #progenitors for.  to do this you need to have run sphgr on
         #all the snaps. NOTE - sphgr has to be set up for the corret
         #galaxy for this to work!



#===============================================


#first call the initial setup_all_cluster shell


cmd = "./setup_all_cluster.sh "+str(nnodes)+' '+str(startsnap)+' '+str(endsnap)+' '+model_dir+' '+hydro_dir+' '+model_run_name+' '+str(COSMOFLAG)+' '+model_dir_remote+' '+hydro_dir_remote
print cmd
call(cmd,shell=True)


if SPHGR_COORDINATE_REWRITE == True: 
    data = np.load(hydro_dir+'/Groups/sphgr_physical_properties.npz')


    sph_snap = data['snaps'][::-1]
    sph_cmx = data['xpos'][::-1]
    sph_cmy = data['ypos'][::-1]
    sph_cmz = data['zpos'][::-1]
    snaps = np.arange(startsnap,endsnap)
   
    for i in snaps:
    

        wsph = (np.where(sph_snap == i))[0][0]
        x_cent = sph_cmx[wsph]
        y_cent = sph_cmy[wsph]
        z_cent = sph_cmz[wsph]


        #append positions
        modelfile = model_dir+'/model_'+str(i)+'.py'
        print 'appending coordinates to: ', modelfile
        with open(modelfile,"a") as myfile:
            myfile.write("\n\n")
            myfile.write("#===============================================\n")
            myfile.write("#GRID POSITIONS\n")
            myfile.write("#===============================================\n")
            myfile.write("x_cent = %s\n" % x_cent)
            myfile.write("y_cent = %s\n" % y_cent)
            myfile.write("z_cent = %s\n" % z_cent)

            
            myfile.write("\n")

   

