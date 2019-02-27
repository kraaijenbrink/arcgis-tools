# Python script that adds polygon areas to the attribute table of a polygon shapefile.
# Philip Kraaijenbrink

import arcpy

# Get parameters from ArcMap
InputPolyFeatures = arcpy.GetParameterAsText(0)
FieldName = arcpy.GetParameterAsText(1)
AreaType = arcpy.GetParameterAsText(2)

# Add a field to the attribute table
arcpy.AddField_management(InputPolyFeatures,FieldName,"DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")

# Calculate the geometry
arcpy.CalculateField_management(InputPolyFeatures,FieldName,"!shape.area@" + AreaType + "!","PYTHON_9.3","#")