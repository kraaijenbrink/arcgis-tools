# Script to convert vertices of a shapefile to points and add calculate distance, angle, curvature and inflextion statistics to the attribute table
# Philip Kraaijenbrink
# 20151109

import arcpy
import math

# Script input arguments
InputLineFeatures = arcpy.GetParameterAsText(0)
ApplyDensification = arcpy.GetParameterAsText(1)
DensificationDistance = arcpy.GetParameterAsText(2)
OutputPointFeatures = arcpy.GetParameterAsText(3)


#####################################################

# Densify lines if desired
arcpy.CopyFeatures_management(InputLineFeatures,'in_memory/densified_lines')                                         
if str(ApplyDensification)=='true':																					 
	arcpy.Densify_edit('in_memory/densified_lines', "DISTANCE", DensificationDistance, "#", "#")
	
# Get vertices as points and covert to multipoint
vertexlayer = 'in_memory/vertices'
arcpy.FeatureVerticesToPoints_management('in_memory/densified_lines', vertexlayer, "ALL")

# add columns to the attribute table
arcpy.AddField_management(vertexlayer,"x","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(vertexlayer,"y","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(vertexlayer,"distance","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(vertexlayer,"dist2prv","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(vertexlayer,"angle2pr","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(vertexlayer,"curve","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(vertexlayer,"infl_pnt","SHORT","#","#","#","#","NULLABLE","NON_REQUIRED","#")

# populate the xy fields
arcpy.CalculateField_management(vertexlayer,"x","!shape.centroid.x!","PYTHON_9.3","#")
arcpy.CalculateField_management(vertexlayer,"y","!shape.centroid.y!","PYTHON_9.3","#")

# calculate the other fields
desc = arcpy.Describe(vertexlayer)  
vertexlayerName = desc.name
rows = arcpy.UpdateCursor(vertexlayer)


# get current entries
entries = []
for row in rows:
	entries.append((row.getValue("x"),row.getValue("y"),row.getValue("ORIG_FID")))

# update distance and angle columns
i = 0
rows = arcpy.UpdateCursor(vertexlayer)
for row in rows:
	# Set first vertex to 0 distance and angle
	if i==0:
		d=0.0
		d2p = 0.0
		a=0.0
		c=0.0
		infl=0
	# Reset first vertex of new line (i.e. change in ORIG_FID) to 0 distance and angle
	elif entries[i][2] != entries[i-1][2]:
		d=0.0	
		d2p = 0.0
		a=0.0
		c=0.0
		infl=0
	# For second to last vertex or when changing ORIG_FID, do not calculate the angle
	elif i==len(entries)-1:
		d = math.sqrt((entries[i][0]-entries[i-1][0])**2 + (entries[i][1]-entries[i-1][1])**2) + d_old
		d2p = math.sqrt((entries[i][0]-entries[i-1][0])**2 + (entries[i][1]-entries[i-1][1])**2)
		a=0.0
		c=0.0
		infl=0
	elif entries[i][2] != entries[i+1][2]:
		d = math.sqrt((entries[i][0]-entries[i-1][0])**2 + (entries[i][1]-entries[i-1][1])**2) + d_old
		d2p = math.sqrt((entries[i][0]-entries[i-1][0])**2 + (entries[i][1]-entries[i-1][1])**2)
		a=0.0
		c=0.0
		infl=0
	# For all else, calculate cumulative distance and the angle with respect to previous vertex
	else:
		
		# calucalate distance and cum. distance
		d2p = math.sqrt((entries[i][0]-entries[i-1][0])**2 + (entries[i][1]-entries[i-1][1])**2)
		d = math.sqrt((entries[i][0]-entries[i-1][0])**2 + (entries[i][1]-entries[i-1][1])**2) + d_old
		
		# the vectors from a points to its two neighbours
		x1 = entries[i-1][0] - entries[i][0]
		y1 = entries[i-1][1] - entries[i][1]
		x2 = entries[i+1][0] - entries[i][0]
		y2 = entries[i+1][1] - entries[i][1]
		
		# Determine counterclockwise angle between the vectors
		a = ((2*math.pi % math.atan2(x1*y2-x2*y1,x1*x2+y1*y2)) * (180/math.pi))
		a = a+180 if a<0 else -a

		# calculate curvature
		d2n = (entries[i+1][0]-entries[i][0])**2 + (entries[i+1][1]-entries[i][1])**2
		c = a / (d2p+d2n)
		
		# determine if point is an inflection point
		infl = 1 if ((a_old < 0) & (a >=0)) | ((a_old > 0) & (a <=0)) else 0
		
		
	# populate the attribute table
	row.setValue('distance',d)
	row.setValue('dist2prv',d2p)
	row.setValue('angle2pr',a)
	row.setValue('curve',c)
	row.setValue('infl_pnt',infl)
	rows.updateRow(row)
	
	# remember current vals for next iteration
	d_old   = d
	d2p_old = d2p
	a_old   = a
	c_old   = a
	infl_old = infl
	
	# update counter
	i+=1
	
# write to disk
arcpy.CopyFeatures_management(vertexlayer,OutputPointFeatures)

#EOF