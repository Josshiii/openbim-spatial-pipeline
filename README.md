# OpenBIM Automated Data Extraction & Telemetry Pipeline

![Language](https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=flat-square)
![Schema](https://img.shields.io/badge/OpenBIM-IFC2x3%20%2F%20IFC4-00A8FF?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## Executive Summary
In complex BIM/VDC ecosystems, architectural and structural models frequently suffer from inconsistent naming conventions, unmapped parameters, and inaccessible property layers due to CAD vendor lock-in. 

This repository provides an automated, headless **OpenBIM data processing pipeline** designed to audit IFC (Industry Foundation Classes) models without proprietary dependencies. It parses structural topology, resolves multi-layered material associations (`IfcRelAssociatesMaterial`), normalizes erratic user-input naming schemas, and exports structured, analytics-ready datasets for CDE (Common Data Environment) compliance audits.

---

## Technical Architecture & Workflow

[ Input: Raw IFC Model ] -> [ Geometry & Schema Validation ]
│
├──> [ Naming Normalization Engine ]
├──> [ Material & Layer Set Resolution ]
└──> [ Property Set (PSet) Quantification ]
│
[ Output: JSON Schema ] <────────┴──> [ Output: CSV Analytics Table ]

---

## Key Features

- **Vendor-Agnostic Parsing:** Direct interpretation of IFC2x3 and IFC4 schemas using native `ifcopenshell` bindings without requiring Autodesk Revit, ArchiCAD, or Solibri licenses.
- **Erratic String Normalization:** Automated regex-based cleansing of alphanumeric entity names, stripping typographic errors, trailing spaces, and CAD-generated special characters (`$` or unnamed identifiers).
- **Deep Material Layer Resolution:** Traverses relational bindings (`IfcMaterial`, `IfcMaterialLayerSetUsage`, and `IfcMaterialList`) to extract surface textures and assigned physical materials into flat, auditable strings.
- **Data Completeness Validation:** Checks physical representation availability (`Has_Geometry`) and quantifies assigned property sets (`IfcRelDefinesByProperties`) to identify LOD/LOIN compliance gaps.

---

## Installation & Quick Start

### 1. Requirements
Ensure Python 3.10+ is installed in your environment. Install required open-source dependencies:

```bash
pip install ifcopenshell pandas openpyxl
