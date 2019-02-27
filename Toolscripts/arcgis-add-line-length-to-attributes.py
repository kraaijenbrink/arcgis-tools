# Python script that add line length attribute column to polyline or line feature layers
# Philip Kraaijenbrink

import arcpy

# Get parameters from ArcMap
InputLineFeatures = arcpy.GetParameterAsText(0)
FieldName = arcpy.GetParameterAsText(1)
LengthType = arcpy.GetParameterAsText(2)

# Add a field to the attribute table
arcpy.AddField_management(InputLineFeatures,FieldName,"DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")

# Calculate the geometry
arcpy.CalculateField_management(InputLineFeatures,FieldName,"!shape.length@" + LengthType + "!","PYTHON_9.3","#")