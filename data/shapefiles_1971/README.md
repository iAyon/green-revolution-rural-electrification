# India District Boundaries (Census of India 1971)

## Overview
This folder contains the standardized historical administrative district boundaries of India for the **1971 Census of India**, standardized to **EPSG:4326 (WGS84)**.

These boundaries are the official geographic units corresponding to the baseline round of the **NCAER Additional Rural Incomes Survey (ARIS-REDS 1971)** and the beginning of the **ICRISAT District-Level Database (1966–2011)**.

---

## File Formats Included
1. **ESRI Shapefile Bundle**:
   - `india_districts_1971.shp` (Geometry features)
   - `india_districts_1971.shx` (Shape positional index)
   - `india_districts_1971.dbf` (Attribute table: district names, state names, area)
   - `india_districts_1971.prj` (Coordinate Reference System definition: WGS84 / EPSG:4326)
   - `india_districts_1971.cpg` (Character encoding: UTF-8)
2. **GeoJSON**:
   - `india_districts_1971.geojson` (Single-file open web GIS standard)
3. **Downloadable Single Archive**:
   - `india_districts_1971_shapefile.zip` (572 KB compressed archive containing all shapefile components for quick distribution to collaborators)

---

## Historical Boundary Verification (1971 Pedigree)
- **District Count**: Exactly **357 districts** covering all 30 States & Union Territories of 1971 India.
- **Historical State Names**:
  - `Mysore` (State Code 16) — officially renamed *Karnataka* on November 1, 1973.
  - `Laccadive, Minicoy and Amindivi Islands` (Union Territory) — officially renamed *Lakshadweep* on November 1, 1973.
- **Pre-Division District Boundaries**:
  - **Haryana**: Contains the original 7 districts established upon state reorganization in 1966: `Hissar`, `Rohtak`, `Gurgaon`, `Karnal`, `Ambala`, `Jind`, and `Mohindergarh`. This precedes the post-1971 divisions (Sonipat and Bhiwani in Dec 1972, Kurukshetra in Jan 1973, Sirsa in 1975, Faridabad in 1979).
  - **Punjab**: Contains the 11 undivided 1971 districts: `Amritsar`, `Bhatinda`, `Ferozepur`, `Gurdaspur`, `Hoshiarpur`, `Jullundur`, `Kapurthala`, `Ludhiana`, `Patiala`, `Rupnagar`, and `Sangrur` (prior to Faridkot carving out in 1972).
  - **Uttar Pradesh**: All 54 historical 1971 districts.

---

## Provenance
- Sourced and reconstructed from the **Census of India 1971 Administrative Atlas** and boundary records curated by the *India State Stories* geographic boundary project (`ramSeraph/indian_admin_boundaries`).
- Open access under public research and attribution guidelines.

---

## Quick Usage Examples

### Python (`geopandas`)
```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Load 1971 district shapefile
gdf_1971 = gpd.read_file("data/shapefiles_1971/india_districts_1971.shp")

# Inspect columns
print(gdf_1971[["District", "State"]].head())

# Quick plot
fig, ax = plt.subplots(figsize=(8, 10))
gdf_1971.boundary.plot(ax=ax, linewidth=0.5, color="black")
plt.title("India 1971 District Boundaries (357 Districts)")
plt.show()
```

### R (`sf`)
```R
library(sf)
library(ggplot2)

# Load 1971 shapefile
districts_1971 <- st_read("data/shapefiles_1971/india_districts_1971.shp")

# Plot
ggplot(districts_1971) +
  geom_sf(fill = "white", color = "gray40", size = 0.2) +
  theme_minimal() +
  labs(title = "Census of India 1971 District Boundaries")
```
