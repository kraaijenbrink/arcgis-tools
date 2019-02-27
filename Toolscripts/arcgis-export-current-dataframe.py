# Script to export the current data frame to a GeoTIFF in ArcMap, used to rip web and baselayers to tiffs
# Philip Kraaijenbrink, 20141031

import arcpy

# Script arguments
PixelSize = arcpy.GetParameterAsText(0)
OutputRaster = arcpy.GetParameterAsText(1)

# commands
mxd = arcpy.mapping.MapDocument("CURRENT")
DataFrame = arcpy.mapping.ListDataFrames(mxd)[0]
AspectRatio = DataFrame.extent.height / DataFrame.extent.width
PixelsWidth = int((DataFrame.extent.XMax - DataFrame.extent.XMin) / float(PixelSize))
arcpy.mapping.ExportToTIFF(mxd, OutputRaster, DataFrame, df_export_width=PixelsWidth, df_export_height=PixelsWidth*AspectRatio, color_mode="24-BIT_TRUE_COLOR", tiff_compression="LZW", geoTIFF_tags=True)
		
# End of script



