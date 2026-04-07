# Survey Sensors & Multispectral Cameras

> **Forge cross-reference:** 36 entries in `sensors` category  
> **Related handbook chapters:** LiDAR & Mapping Payloads, Sensor Payload Integration, Optical Flow

## The Sensors Category

The `sensors` category in Forge covers precision data-collection payloads that go beyond standard FPV cameras — survey RGB cameras, multispectral imagers, hyperspectral sensors, and related precision measurement hardware. These are the payloads that enable agriculture analytics, infrastructure inspection, environmental monitoring, and precision mapping.

This is distinct from thermal cameras (separate category) and LiDAR (separate category). Where those are covered in depth in their own chapters, this chapter covers the RGB survey and multispectral ecosystem.

## Multispectral Cameras

Multispectral cameras capture light across multiple discrete wavelength bands beyond standard RGB. The additional bands — near-infrared (NIR), red-edge, and sometimes thermal — enable vegetation analysis impossible with standard cameras.

**Why bands matter:** Healthy vegetation absorbs red light and strongly reflects NIR. Dead or stressed vegetation reflects red and absorbs NIR. The NDVI (Normalized Difference Vegetation Index) formula `(NIR - Red) / (NIR + Red)` produces a health map from those two bands. You can't calculate NDVI with a standard camera.

### MicaSense RedEdge-P (AgEagle)
MicaSense (acquired by AgEagle Aerial Systems, Wichita KS, USA — NDAA ✓) produces the industry-standard multispectral cameras for precision agriculture. The RedEdge-P captures 5 bands: Blue, Green, Red, Red Edge, NIR. 21MP panchromatic band for RGB reference. Integrates with DJI Zenmuse X7 gimbal or standard payload mounts.

**Why RedEdge dominates:** 10+ years of field deployment, industry-standard data format, integration with Pix4D/DroneDeploy/Agisoft Metashape, and a large agronomist/researcher community built around its output. If you need multispectral data that downstream customers can process, RedEdge is the safest choice.

### MicaSense Altum-PT (AgEagle)
The premium offering. Adds a FLIR Lepton 3.5 thermal band to the 5-band multispectral stack, plus a 12MP panchromatic sensor. All 7 bands captured simultaneously, spatially co-registered — eliminating the parallax errors that occur when merging separate thermal and multispectral captures.

**Use case:** Irrigation stress mapping, disease detection, precision variable-rate application requiring thermal anomaly correlation with spectral data.

### Sentera 6X (John Deere)
Sentera (Minneapolis MN, USA — acquired by John Deere 2025, NDAA ✓) produces multi-sensor cameras positioned as a MicaSense alternative. The 6X captures 6 bands including NDRE (Normalized Difference Red Edge) support. Native John Deere Operations Center integration post-acquisition.

**Competitive position:** Sentera offers some price advantage over MicaSense, with comparable data quality. John Deere acquisition provides integration into the largest precision agriculture platform ecosystem.

## High-Resolution Survey Cameras

### Sony ILX-LR1
Sony's 61MP full-frame sensor in a drone-optimized body (248g, no LCD, single interface). Designed for photogrammetry mapping where maximum resolution reduces required flight altitude for a given GSD (ground sampling distance).

**Integration:** Typically mounted in a nadir-facing gimbal on M300/M350/M400 or large custom platforms. Controlled via Sony Remote Camera SDK over Ethernet/USB. Native Pix4Dmapper support.

**Use case:** Large-area survey where flight time is limited and resolution matters. 61MP full-frame at 100m AGL produces 0.5cm/pixel GSD — comparable to RTK drone surveys at much lower altitude.

### Phase One Industrial Cameras
Phase One (Denmark — NDAA ✓) produces the highest-resolution commercially available drone cameras (iXM-100, iXM-50). 100MP medium format. Primary use in large-area survey, corridor mapping, and precision industrial inspection where single-pass resolution requirements exceed what smaller sensors can provide.

**Price point:** $30,000+. Enterprise/government procurement only.

## NDAA Summary

| Product | Manufacturer | Origin | NDAA |
|---|---|---|---|
| RedEdge-P / Altum-PT | AgEagle (MicaSense) | USA | ✓ |
| Sentera 6X | John Deere | USA | ✓ |
| Sony ILX-LR1 | Sony | Japan | ✓ Allied |
| Phase One iXM | Phase One | Denmark | ✓ EU/NATO |
| DJI Zenmuse P1/L3 | DJI | China | ✗ |
| RoboSense RS-Helios | RoboSense | China | ✗ |

Survey sensors are a cleaner NDAA category than consumer FPV hardware. The professional precision agriculture camera market is dominated by US manufacturers (AgEagle, John Deere). The main NDAA risk is in the integrated platform — a NDAA-compliant sensor on a DJI Matrice 300 still creates a procurement problem for federal programs due to the FCC Covered List status of DJI platforms.

## Processing Pipeline

Multispectral data requires calibrated processing:

1. **Calibration panel:** Image the MicaSense calibration reflectance panel (Lambertian white reference) before and after each flight
2. **Radiometric calibration:** Convert raw sensor values to reflectance using calibration panel data and DLS (Downwelling Light Sensor) readings
3. **Point cloud / orthomosaic:** Standard SfM photogrammetry (Pix4D, Metashape) to create georeferenced orthomosaic
4. **Index calculation:** Compute NDVI, NDRE, etc. in Pix4D, QGIS, or ArcGIS Pro using the aligned band outputs

Without proper radiometric calibration, multispectral data is not comparable across flights or between platforms. This is the most common failure mode in DIY multispectral programs.
