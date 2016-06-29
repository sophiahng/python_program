# -*- coding: cp936 -*-
import arcgisscripting,sys,os,os.path
import math
import string
gp=arcgisscripting.create()
gp.Workspace= "E:/LUCCexpiriment/"
gp.overwriteoutput=1
os.makedirs(r'E:/arcgis/tmp')
#os.makedirs(r'E:/arcgis/output')
in_path = "E:/shenzhen/"
tmp_path= "E:/arcgis/tmp/"
out_path = "E:/shenzhen/national/"

city="sz_"
year=[1975,1990,1995,2000,2005,2010]
Nyr=len(year)
i=0
while i<Nyr:
    print("Transforming LUC map "+str(year[i]))
    inPreUfile= in_path+city+str(year[i])
    gp.RasterToOtherFormat_conversion(inPreUfile,tmp_path,"GRID")
    InRaster= tmp_path+city+str(year[i])
    OutRaster=tmp_path+city+str(year[i])+"u_nu"
    try:
      gp.CheckOutExtension("Spatial")
      #需要根据自己建设用地的code修改
      gp.Con_sa(InRaster, "1", OutRaster, "0", "VALUE = 4")
    except:
    # If an error occurred while running a tool, then print the messages.
      print gp.GetMessages()
    i=i+1
print("adjust 2000")
i=Nyr

inpre2=tmp_path+city+str(year[i-5])+"u_nu"
inpre1=tmp_path+city+str(year[i-4])+"u_nu"
incur=tmp_path+city+str(year[i-3])+"u_nu"
inpos1=tmp_path+city+str(year[i-2])+"u_nu"
inpos2=tmp_path+city+str(year[i-1])+"u_nu"
inraster="\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos1+"\'"+";"+"\'"+inpos2+"\'"
outraster=tmp_path+city+str(year[i-3])+"c"
gp.Combine_sa(inraster, outraster)
outadj=tmp_path+city+"2000adj1"
field1=city+str(year[i-5])+"U_NU"
field2=city+str(year[i-4])+"U_NU"
field3=city+str(year[i-2])+"U_NU"
field4=city+str(year[i-1])+"U_NU"
expression=field1+" = "+field2+" and "+field1+" = "+field3+" and "+field3+" = "+field4
gp.Con_sa(outraster, inpre1, outadj, incur, expression)

print("adjust 2005") 
inpre2=tmp_path+city+str(year[i-4])+"u_nu"
inpre1=tmp_path+city+str(year[i-3])+"u_nu"
incur=tmp_path+city+str(year[i-2])+"u_nu"
inpos=tmp_path+city+str(year[i-1])+"u_nu"
inraster="\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos+"\'"    
outraster=tmp_path+city+str(year[i-2])+"c"
gp.Combine_sa(inraster, outraster)
outadj=tmp_path+city+"2005adj1"
field1=city+str(year[i-4])+"U_NU"
field2=city+str(year[i-3])+"U_NU"
field3=city+str(year[i-1])+"U_NU"
expression=field1+" = "+field2+" and "+field1+" = "+field3
gp.Con_sa(outraster, inpre1, outadj, incur, expression)

print("adjust 2010")
inpre4=tmp_path+city+str(year[i-6])+"u_nu"
inpre3=tmp_path+city+str(year[i-5])+"u_nu"
inpre2=tmp_path+city+str(year[i-4])+"u_nu"
inpre1=tmp_path+city+str(year[i-3])+"u_nu"
incur=tmp_path+city+str(year[i-2])+"u_nu"
inpos=tmp_path+city+str(year[i-1])+"u_nu"
inraster="\'"+inpre4+"\'"+";"+"\'"+inpre3+"\'"+";"+"\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos+"\'"    
outraster=tmp_path+city+str(year[i-1])+"c"
gp.Combine_sa(inraster, outraster)
outadj=tmp_path+city+"2010adj1"
field1=city+str(year[i-6])+"U_NU"
field2=city+str(year[i-5])+"U_NU"
field3=city+str(year[i-4])+"U_NU"
field4=city+str(year[i-3])+"U_NU"
field5=city+str(year[i-2])+"U_NU"
expression=field1+"=1"+" and "+field2+"=1"+" and "+field3+"=1"+" and "+field4+"=1"+" and "+field5+"=1"
gp.Con_sa(outraster, 1, outadj, inpos, expression)

print("adjust second year") 
inpre2=tmp_path+city+str(year[0])+"u_nu"
inpre1=tmp_path+city+str(year[1])+"u_nu"
incur=tmp_path+city+str(year[2])+"u_nu"
inpos=tmp_path+city+str(year[3])+"u_nu"
inraster="\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos+"\'"    
outraster=tmp_path+city+str(year[1])+"c"
gp.Combine_sa(inraster, outraster)
outadj=tmp_path+city+str(year[1])+"adj1"
field1=city+str(year[0])+"U_NU"
field2=city+str(year[2])+"U_NU"
field3=city+str(year[3])+"U_NU"
expression=field1+" = "+field2+" and "+field1+" = "+field3
gp.Con_sa(outraster, inpre2, outadj, inpre1, expression)

print("adjust first year")
inpre4=tmp_path+city+str(year[0])+"u_nu"
inpre3=tmp_path+city+str(year[1])+"u_nu"
inpre2=tmp_path+city+str(year[2])+"u_nu"
inpre1=tmp_path+city+str(year[3])+"u_nu"
incur=tmp_path+city+str(year[4])+"u_nu"
inpos=tmp_path+city+str(year[5])+"u_nu"
inraster="\'"+inpre4+"\'"+";"+"\'"+inpre3+"\'"+";"+"\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos+"\'"    
outraster=tmp_path+city+str(year[0])+"c"
gp.Combine_sa(inraster, outraster)
outadj=tmp_path+city+str(year[0])+"adj1"
field1=city+str(year[1])+"U_NU"
field2=city+str(year[2])+"U_NU"
field3=city+str(year[3])+"U_NU"
field4=city+str(year[4])+"U_NU"
field5=city+str(year[5])+"U_NU"
expression=field1+"=0"+" and "+field2+"=0"+" and "+field3+"=0"+" and "+field4+"=0"+" and "+field5+"=0"
gp.Con_sa(outraster, 0, outadj, inpre4, expression)


j=i-4
while j>1:
    print("adjust "+ str(year[j]))
    inpre2=tmp_path+city+str(year[j-2])+"u_nu"
    inpre1=tmp_path+city+str(year[j-1])+"u_nu"
    incur=tmp_path+city+str(year[j])+"u_nu"
    inpos1=tmp_path+city+str(year[j+1])+"u_nu"
    inpos2=tmp_path+city+str(year[j+2])+"u_nu"
    inraster="\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos1+"\'"+";"+"\'"+inpos2+"\'"
    outraster=tmp_path+city+str(year[j])+"c"
    gp.Combine_sa(inraster, outraster)
    outadj=tmp_path+city+str(year[j])+"adj1"
    field1=city+str(year[j-2])+"U_NU"
    field2=city+str(year[j-1])+"U_NU"
    field3=city+str(year[j+2])+"U_NU"
    field4=city+str(year[j+1])+"U_NU"
    expression=field1+" = "+field2+" and "+field1+" = "+field3+" and "+field3+" = "+field4
    gp.Con_sa(outraster, inpre1, outadj, incur, expression)
    j=j-1

print ("re-adjusting")
k=1
while k<4:
    print("adjust 2000")
    i=Nyr
    inpre2=tmp_path+city+str(year[i-5])+"adj"+str(k)
    inpre1=tmp_path+city+str(year[i-4])+"adj"+str(k)
    incur=tmp_path+city+str(year[i-3])+"adj"+str(k)
    inpos1=tmp_path+city+str(year[i-2])+"adj"+str(k)
    inpos2=tmp_path+city+str(year[i-1])+"adj"+str(k)
    inraster="\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos1+"\'"+";"+"\'"+inpos2+"\'"
    outraster=tmp_path+city+str(year[i-3])+"c"
    gp.Combine_sa(inraster, outraster)
    outadj=tmp_path+city+"2000adj"+str(k+1)
    field1=city+str(year[i-5])+"adj"+str(k)
    field2=city+str(year[i-4])+"adj"+str(k)
    field3=city+str(year[i-2])+"adj"+str(k)
    field4=city+str(year[i-1])+"adj"+str(k)
    expression=field1+" = "+field2+" and "+field1+" = "+field3+" and "+field3+" = "+field4
    gp.Con_sa(outraster, inpre1, outadj, incur, expression)

    print("adjust 2005") 
    inpre2=tmp_path+city+str(year[i-4])+"adj"+str(k)
    inpre1=tmp_path+city+str(year[i-3])+"adj"+str(k)
    incur=tmp_path+city+str(year[i-2])+"adj"+str(k)
    inpos=tmp_path+city+str(year[i-1])+"adj"+str(k)
    inraster="\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos+"\'"    
    outraster=tmp_path+city+str(year[i-2])+"c"
    gp.Combine_sa(inraster, outraster)
    outadj=tmp_path+city+"2005adj"+str(k+1)
    field1=city+str(year[i-4])+"adj"+str(k)
    field2=city+str(year[i-3])+"adj"+str(k)
    field3=city+str(year[i-1])+"adj"+str(k)
    expression=field1+" = "+field2+" and "+field1+" = "+field3
    gp.Con_sa(outraster, inpre1, outadj, incur, expression)

    print("adjust 2010")
    inpre4=tmp_path+city+str(year[i-6])+"adj"+str(k)
    inpre3=tmp_path+city+str(year[i-5])+"adj"+str(k)
    inpre2=tmp_path+city+str(year[i-4])+"adj"+str(k)
    inpre1=tmp_path+city+str(year[i-3])+"adj"+str(k)
    incur=tmp_path+city+str(year[i-2])+"adj"+str(k)
    inpos=tmp_path+city+str(year[i-1])+"adj"+str(k)
    inraster="\'"+inpre4+"\'"+";"+"\'"+inpre3+"\'"+";"+"\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos+"\'"    
    outraster=tmp_path+city+str(year[i-1])+"c"
    gp.Combine_sa(inraster, outraster)
    outadj=tmp_path+city+"2010adj"+str(k+1)
    field1=city+str(year[i-6])+"adj"+str(k)
    field2=city+str(year[i-5])+"adj"+str(k)
    field3=city+str(year[i-4])+"adj"+str(k)
    field4=city+str(year[i-3])+"adj"+str(k)
    field5=city+str(year[i-2])+"adj"+str(k)
    expression=field1+"=1"+" and "+field2+"=1"+" and "+field3+"=1"+" and "+field4+"=1"+" and "+field5+"=1"
    gp.Con_sa(outraster, 1, outadj, inpos, expression)

    print("adjust second year") 
    inpre2=tmp_path+city+str(year[0])+"adj"+str(k)
    inpre1=tmp_path+city+str(year[1])+"adj"+str(k)
    incur=tmp_path+city+str(year[2])+"adj"+str(k)
    inpos=tmp_path+city+str(year[3])+"adj"+str(k)
    inraster="\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos+"\'"    
    outraster=tmp_path+city+str(year[1])+"c"
    gp.Combine_sa(inraster, outraster)
    outadj=tmp_path+city+str(year[1])+"adj"+str(k+1)
    field1=city+str(year[0])+"adj"+str(k)
    field2=city+str(year[2])+"adj"+str(k)
    field3=city+str(year[3])+"adj"+str(k)
    expression=field1+" = "+field2+" and "+field1+" = "+field3
    gp.Con_sa(outraster, inpre2, outadj, inpre1, expression)

    print("adjust first year")
    inpre4=tmp_path+city+str(year[0])+"adj"+str(k)
    inpre3=tmp_path+city+str(year[1])+"adj"+str(k)
    inpre2=tmp_path+city+str(year[2])+"adj"+str(k)
    inpre1=tmp_path+city+str(year[3])+"adj"+str(k)
    incur=tmp_path+city+str(year[4])+"adj"+str(k)
    inpos=tmp_path+city+str(year[5])+"adj"+str(k)
    inraster="\'"+inpre4+"\'"+";"+"\'"+inpre3+"\'"+";"+"\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos+"\'"    
    outraster=tmp_path+city+str(year[0])+"c"
    gp.Combine_sa(inraster, outraster)
    outadj=tmp_path+city+str(year[0])+"adj"+str(k+1)
    field1=city+str(year[1])+"adj"+str(k)
    field2=city+str(year[2])+"adj"+str(k)
    field3=city+str(year[3])+"adj"+str(k)
    field4=city+str(year[4])+"adj"+str(k)
    field5=city+str(year[5])+"adj"+str(k)
    expression=field1+"=0"+" and "+field2+"=0"+" and "+field3+"=0"+" and "+field4+"=0"+" and "+field5+"=0"
    gp.Con_sa(outraster, 0, outadj, inpre4, expression)


    j=i-4
    while j>1:
        print("adjust "+ str(year[j]))
        inpre2=tmp_path+city+str(year[j-2])+"adj"+str(k)
        inpre1=tmp_path+city+str(year[j-1])+"adj"+str(k)
        incur=tmp_path+city+str(year[j])+"adj"+str(k)
        inpos1=tmp_path+city+str(year[j+1])+"adj"+str(k)
        inpos2=tmp_path+city+str(year[j+2])+"adj"+str(k)
        inraster="\'"+inpre2+"\'"+";"+"\'"+inpre1+"\'"+";"+"\'"+incur+"\'"+";"+"\'"+inpos1+"\'"+";"+"\'"+inpos2+"\'"
        outraster=tmp_path+city+str(year[j])+"c"
        gp.Combine_sa(inraster, outraster)
        outadj=tmp_path+city+str(year[j])+"adj"+str(k+1)
        field1=city+str(year[j-2])+"adj"+str(k)
        field2=city+str(year[j-1])+"adj"+str(k)
        field3=city+str(year[j+2])+"adj"+str(k)
        field4=city+str(year[j+1])+"adj"+str(k)
        expression=field1+" = "+field2+" and "+field1+" = "+field3+" and "+field3+" = "+field4
        gp.Con_sa(outraster, inpre1, outadj, incur, expression)
        j=j-1
    k=k+1

i=0
while i<Nyr:
    inPreUfile= tmp_path+city+str(year[i])+"adj"+str(k)
    output=out_path+city+str(year[i])+"adj"
    gp.copy_management(inPreUfile,output)
    #gp.RasterToOtherFormat_conversion(inPreUfile,out_path,"GRID")
    i=i+1
__import__('shutil').rmtree(tmp_path)         
print 'Congratulations! \n'               
del gp
