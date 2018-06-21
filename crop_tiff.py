#created by Zhanlin Liu
#crop images using raster mask

import rasterio
from rasterio.tools.mask import mask
# the polygon GeoJSON geometry
geoms = [{'type': 'Polygon', 'coordinates': [[(  -2849.167, 425588.544), (  -2849.167, 422497.143), (    235.212, 425588.544), (    235.212, 422497.143)]]}]
# load the raster, mask it by the polygon and crop it
with rasterio.open("cea.tif") as src:
    out_image, out_transform = mask(src, geoms, crop=True)
out_meta = src.meta.copy()

# save the resulting raster  
out_meta.update({"driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
"transform": out_transform})

with rasterio.open("masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)

##########################

import fiona
import rasterio
import rasterio.mask

with fiona.open("box.shp", "r") as shapefile:
    features = [feature["geometry"] for feature in shapefile]


with rasterio.open("RGB.byte.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, features,
                                                        crop=True)
    out_meta = src.meta.copy()

with rasterio.open("masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)

    