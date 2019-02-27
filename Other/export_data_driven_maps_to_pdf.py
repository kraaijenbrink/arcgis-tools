# Export the current map document for all data driven pages.
# P.D.A. Kraaijenbrink, 20150429



################### SETTINGS ###################

# output path
outDir = r"d:/outmaps"

# output name (excl. extension)
outName = "outprefix"


# PDF output settings
dpiOut = 600
imageQ = "BEST"
colSpace = "RGB"
compressVec = True
compressImage = "LZW"
picSymbol = "RASTERIZE_BITMAP"
convMarkers = False
embFonts = True
layerAttr = "LAYERS_ONLY"
geoRef = True
comprJPEG = 80



################### PROCESSING ###################

# Load required modules
import arcpy, os

# Define the map document
mxd = arcpy.mapping.MapDocument("CURRENT")

# loop over data driven pages and export each to pdf map
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
	outPath = os.path.join(outDir,outName + '_page-' + str(pageNum) + '.pdf')
	mxd.dataDrivenPages.currentPageID = pageNum
	print "Exporting page {0} of {1}".format(str(mxd.dataDrivenPages.currentPageID), str(mxd.dataDrivenPages.pageCount))
	arcpy.mapping.ExportToPDF(map_document=mxd, out_pdf=outPath, data_frame='PAGE_LAYOUT', resolution=dpiOut, image_quality=imageQ, colorspace=colSpace, compress_vectors=compressVec, image_compression=compressImage, picture_symbol=picSymbol, convert_markers=convMarkers, embed_fonts=embFonts, layers_attributes=layerAttr,georef_info=geoRef, jpeg_compression_quality=comprJPEG)
del mxd

	
	
#EOF
