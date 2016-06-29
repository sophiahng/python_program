# -*- coding: cp936 -*-
import arcgisscripting,sys,os,os.path
import math
import string
gp=arcgisscripting.create()
gp.Workspace= "E:/LUCCexpiriment/"
gp.overwriteoutput=1
os.makedirs(r'E:/arcgis/tmp')
in_path = "E:/haikou/"
tmp_path= "E:/arcgis/tmp/"
out_path = "E:/haikou/LUCC/"

city="hk_"
year=[1975,1990,1995,2000,2005,2010]
Nyr=len(year)
i=1
while i<Nyr:
    inPreUfile= in_path+city+str(year[i-1])+"_ufin"
    inPosUfile= in_path+city+str(year[i])+"_ufin"
    
    # combined
    try:
    # Set local variables
      outcombined = tmp_path+"Combined"+str(year[i-1])

    # Check out Spatial Analyst extension license
      gp.CheckOutExtension("Spatial")
      print ("===========processing Period:"+str(year[i-1])+"-"+str(year[i])+"==========")
      print ("conversion to grid")
      gp.RasterToOtherFormat_conversion(inPreUfile,tmp_path,"GRID")
      gp.RasterToOtherFormat_conversion(inPosUfile,tmp_path,"GRID")
    # Process: Combine...
      inPreUfile= tmp_path+city+str(year[i-1])+"_ufin"
      inPosUfile= tmp_path+city+str(year[i])+"_ufin"
      inraster="\'"+inPreUfile+"\'"+";"+"\'"+inPosUfile+"\'"
      print ("combined")
      outraster=tmp_path+str(year[i-1])+"times"
      gp.Times_sa(inPreUfile, 10, outraster)
      gp.Plus_sa(outraster, inPosUfile, outcombined)
      #gp.Combine_sa(inraster, outcombined)
    except:
    # If an error occurred while running a tool, then print the messages.
      print gp.GetMessages()
      print ("outcombined here")
    try:
      InWhereClause = "value=1 or value=11"
      Outcombined2 = tmp_path+"Combined2"+str(year[i-1])

      print ("extracting Expanded urban and existed urban")
    # Process: ExtractByAttributes
      gp.ExtractByAttributes_sa(outcombined, InWhereClause, Outcombined2)
    except:
    # If an error occurred while running a tool, then print the messages.
      print gp.GetMessages()

    try:
        
      OutPolygonFeatures = tmp_path+str(year[i-1])+".shp"
      
    # Process: RasterToPolygon_conversion
      print ("raster to polygon")
      gp.RasterToPolygon_conversion(Outcombined2, OutPolygonFeatures, "NO_SIMPLIFY")
      outselectEP= tmp_path+str(year[i-1])+"EP.shp"
      print("Expand urban")
      gp.select_analysis(OutPolygonFeatures, outselectEP, ' "GRIDCODE" = 1 ')
      outselectEX= tmp_path+str(year[i-1])+"EX.shp"
      print ("Existed urban")
      gp.select_analysis(OutPolygonFeatures, outselectEX, ' "GRIDCODE" = 11 ')
      gp.addfield (outselectEX, "area", "double", "9")
      expression = "float(!shape.area!)"
      gp.CalculateField_management(outselectEX, "area", expression, "PYTHON")
      
    except:
    # If an error occurred while running a tool, then print the messages.
      print gp.GetMessages()

    try:
      print ("intersect")
      outintersect= tmp_path+str(year[i-1])+"intersect.shp"
      inraster="\'"+outselectEP+"\'"+";"+"\'"+outselectEX+"\'"
      gp.Intersect_analysis(inraster, outintersect, "#",1.5, "line")
    except:
    # If an error occurred while running a tool, then print the messages.
      print gp.GetMessages()
    try:
      print ("calculate perimeter and length")
      gp.addfield (outselectEP, "Peri", "double", "9")
      expression = "float(!shape.Length!)"
      gp.CalculateField_management(outselectEP, "Peri", expression, "PYTHON")
      gp.addfield (outintersect, "length", "double","9")
      gp.CalculateField_management(outintersect, "length", expression, "PYTHON")
      outstat = tmp_path+ "intersect_stats"+str(year[i-1])
    except:
    # If an error occurred while running a tool, then print the messages.
      print gp.GetMessages()
    try:
      print ("Sum length and connect to Expanded urban, time cosumming.....")
      statF="FID_"+str(year[i-1])+"EP"
      gp.Statistics(outintersect, outstat,"length sum",statF)
      gp.joinfield (outselectEP, "FID", outstat, statF, "SUM_length")
      gp.addfield (outselectEP, "E", "double")
      gp.CalculateField_management(outselectEP, "E", "[SUM_length]/[Peri]", "VB")
      outputep=out_path+city+str(year[i-1])+"EP.shp"
      gp.CopyFeatures(outselectEP,outputep)
      print ("Stats...")
      gp.addfield (outputep, "area", "double", "9")
      expression = "float(!shape.area!)"
      gp.CalculateField_management(outputep, "area", expression, "PYTHON")
      gp.addfield (outputep, "areaE", "double","9")
      gp.CalculateField_management(outputep, "areaE", "[area]*[E]", "VB")
      outputex=out_path+city+str(year[i-1])+"EX.shp"
      gp.CopyFeatures(outselectEX,outputex)
    except:
    # If an error occurred while running a tool, then print the messages.
      print gp.GetMessages()  
    i=i+1
__import__('shutil').rmtree(tmp_path)
os.makedirs(r'E:/LUCCexpiriment/tmp')          
print 'Congratulations! \n'               
del gp
