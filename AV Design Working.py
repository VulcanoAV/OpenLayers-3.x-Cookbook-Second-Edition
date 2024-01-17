import arcpy
import os

fc = "Design_lines_20240101"
gdbloc = r"C:\Admin\ArcGIS\GeoDatabase\AV.gdb"
desc = arcpy.Describe(fc)
workspaceloc = "AV.gdb"

arcpy.env.workspace = workspaceloc

list1 = []
list2 = []
outList = []
grouplist = []

# append values to list
rows = arcpy.SearchCursor(fc)
for row in rows:
    list1.append((row.package_id,row.discipline_code,row.milestone_code,row.suitability_code,row.fileupdateddate,row.revision))

del row, rows
'''
for row in rows:
    list2.append((row.package_id,row.discipline_code,row.milestone_code,row.suitability_code,row.fileupdateddate,row.revision))

del row, rows
'''

# create unique list by excluding duplicates
for n in list1:
    if n not in outList:
        outList.append(n)
'''       
# create unique from published list by excluding duplicates
for n in list2:
    if n not in outList:
        outList.append(n)        
'''
# create layer files
for a,b,c,d,e,f in outList:
    featlyr = a + "_" + b + "_" + c + "_" + d + "_" + f + "_" + desc.shapeType
    featlyrgdb = "design_" + a.replace("-","_") + "_" + b + "_" + c + "_" + d + "_" + f + "_" + desc.shapeType
    testquery = ("\"package_id\" = " + "'" + a + "'" + " And " + "\"discipline_code\" = " + "'" + b + "'" + " And " +"\"milestone_code\" = " + "'" + c + "'" + " And " + "\"suitability_code\" = " + "'" + d + "'")

    arcpy.management.MakeFeatureLayer(fc, featlyr, testquery)

    arcpy.env.addOutputsToMap = False    
    arcpy.conversion.FeatureClassToFeatureClass(featlyr, gdbloc, featlyrgdb)
    arcpy.management.Append(featlyr, os.path.join(gdbloc, c + "_" + d + "_" + desc.shapeType))
    arcpy.env.addOutputsToMap = True  