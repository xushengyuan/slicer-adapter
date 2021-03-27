import os
import shutil
from PIL import Image

process_dir="E:\\_xyzCalibration_cube_"

gcode_in = open(os.path.join(process_dir,'run.gcode'),'r')
gcode=gcode_in.readlines()

burnin_range_str=gcode[22][18:-1]
print(burnin_range_str)
burnin_range=int(burnin_range_str)
total_range_str=gcode[24][12:-1]
print(total_range_str)
total_range=int(total_range_str)
stardard_range=total_range-burnin_range


jobinfo_tmpl='VoxelDepth 0.001969'
data_proc_info_tmpl='''-------------- Data processing information sheet ------------

-------------------------------------------------------------

Machine settings:
 o Machine type       : Ultra
 o Resolution (pixel) : 1920 x 1200
 o Platform size (mm) : 266.65 x 165.83

-------------------------------------------------------------

Material settings:
 o Material type      : LS600

-------------------------------------------------------------

Scene informations:
 o Scene dimensions:
    - x-Axis (mm): 169.97 [+50.72, +220.70]
    - y-Axis (mm): 36.25 [+62.39, +98.64]
    - z-Axis (mm): 46.13 [+0.00, +46.13]
 o Processed data:
    - Model   No.1: Mesh1_sup.stl
    - Perfactory Support No.1: Mesh1_sup_s.stl

-------------------------------------------------------------

Raster settings:
 o Voxel depth:
     -  50 um in range [0.00 - 2147483.65) mm
 o Number of voxel data sets: %d

-------------------------------------------------------------

Voxel conversion settings       :
 o Converter type               : 'DBS V2.9'
 o Buildfilter version          : '2.9 Standard'
 o Plugin DLL version           : '2.9.1753.1110'
 o Buildfilter type          : 'Xede/Xtreme'
 o Number solid base plates     : 0
 o Height of burn-in range      : %d
 o Height of stardard range     : %d
 o Perfactory Support widening (um)       : 285
 o Perfactory Support base widening (um)  : 1500
 o Perfactory Support base height (um)     : 500
 o ERM module                    : Not activated
 o Number of active voxel      : 0
 o Number of billed voxel      : 5844841

-------------------------------------------------------------


-------------------------------------------------------------

'''%(burnin_range+stardard_range,burnin_range,stardard_range)

gcode_filtered=[]
for line in gcode:
    if line[:5]=='M6054' or (line[:2]=='G4' and line[:6]!='G4 P0;'):
        gcode_filtered.append(line)

buildlist=''
assert len(gcode_filtered)%2==0
for i in range(0,len(gcode_filtered),2):
    image_filename=gcode_filtered[i][7:-17]
    expose_time=int(gcode_filtered[i+1][4:-2])

    im=Image.open(os.path.join(process_dir,image_filename+'.png'))
    im=im.convert('L')

    im.save(os.path.join(process_dir,'vds_'+image_filename+'#0.bmp'))#,dpi=(119,119),bits=8)
    buildlist_str='<file = "vds_%s#0.bmp" expose_time = %d add = 0>'%(image_filename,expose_time/2)
    print(buildlist_str)
    buildlist+=buildlist_str+'\n'

    im.save(os.path.join(process_dir,'vds_'+image_filename+'#1.bmp'))#,dpi=(119,119),bits=8)
    buildlist_str='<file = "vds_%s#1.bmp" expose_time = %d add = 1>'%(image_filename,expose_time/2)
    print(buildlist_str)
    buildlist+=buildlist_str+'\n'

jobinfo_out=open(os.path.join(process_dir,'Jobinfo.txt'),'w')
jobinfo_out.write(jobinfo_tmpl)
jobinfo_out.close()

data_proc_info_out=open(os.path.join(process_dir,'Data_Processing_Info.txt'),'w')
data_proc_info_out.write(data_proc_info_tmpl)
data_proc_info_out.close()

buildlist_out=open(os.path.join(process_dir,'BuildList.txt'),'w')
buildlist_out.write(buildlist)
buildlist_out.close()

