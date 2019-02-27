# copy the symbology of the first layer to all other layers

import arcpy

# Set the current workspace
mxd = arcpy.mapping.MapDocument("CURRENT")

# Set layer to apply symbology to
layers = arcpy.mapping.ListLayers(mxd)

# apply first layers to other layers
template = layers[0]
targets  = layers[1:]

# Apply the symbology from the template to all targets
for lyr in targets:
    arcpy.ApplySymbologyFromLayer_management(lyr, template)