# Script to construct the outline for a raster with nodata
# Philip Kraaijenbrink
# 20151107

import arcpy

arcpy.CheckOutExtension("spatial")

# Script arguments
InputRaster    = arcpy.GetParameterAsText(0)
OutputPolygons = arcpy.GetParameterAsText(1)


# process
temprast = arcpy.sa.Int(InputRaster) * 0 + 1
arcpy.RasterToPolygon_conversion(temprast, OutputPolygons, "NO_SIMPLIFY", 'Value')
