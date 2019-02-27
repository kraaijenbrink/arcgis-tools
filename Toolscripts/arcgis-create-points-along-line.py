#-------------------------------------------------------------------------------
# Purpose:     Creates points on lines at a specified distance, interval, or
#              percentage using a fixed or field-based value. Points can be
#              created starting from the beginning, or end of the line.
#
# Author:      Ian Broad
# Website:     www.ianbroad.com
#
# Created:     05/06/2015
#-------------------------------------------------------------------------------

import arcpy

arcpy.env.overwriteOutput = True

line = arcpy.GetParameterAsText(0)
create_from = arcpy.GetParameterAsText(1)
choice = arcpy.GetParameterAsText(2)
use_field = arcpy.GetParameterAsText(3)
field = arcpy.GetParameterAsText(4)
distance = float(arcpy.GetParameterAsText(5))
end_points = arcpy.GetParameterAsText(6)
output = arcpy.GetParameterAsText(7)

if "in_memory" in output:
    mem_name = output.split("\\")[-1]
else:
    mem_name = "mem_point"

mem_point = arcpy.CreateFeatureclass_management("in_memory", mem_name, "POINT", "", "DISABLED", "DISABLED", line)
arcpy.AddField_management(mem_point, "LineOID", "TEXT")
arcpy.AddField_management(mem_point, "Value", "TEXT")

result = arcpy.GetCount_management(line)
features = int(result.getOutput(0))

arcpy.SetProgressor("step", "Creating Points on Lines...", 0, features, 1)

fields = ["SHAPE@", "OID@"]

if use_field == "YES":
    fields.append(field)

reverse = False
if create_from == "END":
   reverse = True
   reversed_points = []

with arcpy.da.SearchCursor(line, (fields)) as search:
    with arcpy.da.InsertCursor(mem_point, ("SHAPE@", "LineOID", "Value")) as insert:
        for row in search:
            try:
                line_geom = row[0]
                length = float(line_geom.length)
                count = distance
                oid = str(row[1])
                start = arcpy.PointGeometry(line_geom.firstPoint)
                end = arcpy.PointGeometry(line_geom.lastPoint)

                if reverse == True:
                   for part in line_geom:
                       for p in part:
                           reversed_points.append(p)

                   reversed_points.reverse()
                   array = arcpy.Array([reversed_points])
                   line_geom = arcpy.Polyline(array)

                if use_field == "YES":
                    count = float(row[2])
                    distance = float(row[2])

                if choice == "DISTANCE":
                    point = line_geom.positionAlongLine(count, False)
                    insert.insertRow((point, oid, count))

                elif choice == "INTERVAL":
                    while count <= length:
                      point = line_geom.positionAlongLine(count, False)
                      insert.insertRow((point, oid, count))
                      count += distance

                elif choice == "PERCENTAGE":
                    point = line_geom.positionAlongLine(count, True)
                    insert.insertRow((point, oid, count))

                elif choice == "START/END POINTS":
                    insert.insertRow((start, oid, 0))
                    insert.insertRow((end, oid, str(length)))

                if end_points == "START":
                    insert.insertRow((start, oid, 0))

                elif end_points == "END":
                    insert.insertRow((end, oid, str(length)))

                elif end_points == "BOTH":
                    insert.insertRow((start, oid, 0))
                    insert.insertRow((end, oid, str(length)))

                arcpy.SetProgressorPosition()

            except Exception as e:
                arcpy.AddMessage(str(e.message))

if "in_memory" in output:
    arcpy.SetParameter(8, mem_point)
else:
    arcpy.CopyFeatures_management(mem_point, output)
    arcpy.Delete_management(mem_point)

arcpy.ResetProgressor()
arcpy.GetMessages()


