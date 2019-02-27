# Script to construct the centerline for a polygon through the creation of a thiessen skeleton
# Philip Kraaijenbrink
# 20151107

import arcpy

# Script arguments
InputPolygonFeatures = arcpy.GetParameterAsText(0)
ApplyDensification = arcpy.GetParameterAsText(1)
DensificationDistance = arcpy.GetParameterAsText(2)
CleanupTolerance = arcpy.GetParameterAsText(3)
ApplyTrimming = arcpy.GetParameterAsText(4)
TrimIterations = arcpy.GetParameterAsText(5)
MaximumDangleLength = arcpy.GetParameterAsText(6)
ApplySmoothing = arcpy.GetParameterAsText(7)
SmoothingTolerance = arcpy.GetParameterAsText(8)
OutputCenterlineFeature = arcpy.GetParameterAsText(9)


### Generate skeleton ###

arcpy.CopyFeatures_management(InputPolygonFeatures,'in_memory/densified_poly')                                                          # copy features to memory
if str(ApplyDensification)=='true':																										# densify polygon vertices if checked
	arcpy.Densify_edit('in_memory/densified_poly', "DISTANCE", DensificationDistance, "#", "#")
arcpy.FeatureVerticesToPoints_management('in_memory/densified_poly', 'in_memory/vertices', "ALL")										# Get vertices as points
arcpy.CreateThiessenPolygons_analysis('in_memory/vertices', 'in_memory/thiessen_polys', "ONLY_FID")										# Create Thiessen polygons for the points
arcpy.FeatureToLine_management('in_memory/thiessen_polys', 'in_memory/thiessen_lines', "", "ATTRIBUTES")								# Get the outlines from the Thiessen polygons
arcpy.Clip_analysis('in_memory/thiessen_lines', 'in_memory/densified_poly', 'in_memory/thiessen_lines_clipped', "")						# Clip the thiessen polygons to the input polygon
arcpy.FeatureToLine_management('in_memory/densified_poly', 'in_memory/input_poly_outline', "", "ATTRIBUTES")							# Get the outline of the input polygon
arcpy.Erase_analysis('in_memory/thiessen_lines_clipped', 'in_memory/input_poly_outline', 'in_memory/skeleton_singleparts', "")			# Erase the line coincident to the input polygon outline from the skeleton
arcpy.Dissolve_management('in_memory/skeleton_singleparts', 'in_memory/skeleton', "", "", "MULTI_PART", "DISSOLVE_LINES")				# Merge the skeleton parts to a single line
arcpy.Integrate_management('in_memory/skeleton', CleanupTolerance)																		# Clean topo errors of the skeleton

# Trim the skeleton dangles iteratively to get centerline
if str(ApplyTrimming)=='true':
	for i in range(0, int(TrimIterations)):
		arcpy.MultipartToSinglepart_management('in_memory/skeleton', 'in_memory/skeleton_prep')
		arcpy.TrimLine_edit('in_memory/skeleton_prep', MaximumDangleLength, "DELETE_SHORT")
		arcpy.Delete_management('in_memory/skeleton')
		arcpy.Dissolve_management('in_memory/skeleton_prep', 'in_memory/skeleton', "", "", "MULTI_PART", "DISSOLVE_LINES")

# Smooth the centerline
if str(ApplySmoothing)=='true':
	arcpy.SmoothLine_cartography('in_memory/skeleton', 'in_memory/skeleton_smoothed', "PAEK", SmoothingTolerance, '#', '#')
	arcpy.Delete_management('in_memory/skeleton')
	arcpy.CopyFeatures_management('in_memory/skeleton_smoothed','in_memory/skeleton')

# save output to disk
arcpy.CopyFeatures_management('in_memory/skeleton', OutputCenterlineFeature)


