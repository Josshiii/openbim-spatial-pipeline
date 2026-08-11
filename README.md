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
```

2. DeploymentClone the repository and insert your target IFC asset into the root directory:Bashgit clone [https://github.com/Josshiii/BIM_Data_Pipeline.git](https://github.com/Josshiii/BIM_Data_Pipeline.git)
cd BIM_Data_Pipeline

3. ExecutionRun the extractor against your target asset (modelo_prueba.ifc by default):Bashpython extractor.py
Structured Output Schema (bim_telemetry_matrix.json / .csv)The pipeline compiles an auditable table containing the following normalized fields per IFC instance:FieldData TypeDescriptionGlobalIdStringUniversal 22-character IFC unique identifier.IFC_ClassStringPrimary OpenBIM data schema type (e.g., IfcBeam, IfcSlab).Normalized_NameStringSanitized, uppercase alphanumeric identifier for database indexing.Raw_NameStringOriginal text string extracted from the authoring software.Object_TypeStringStructural/Architectural family or category designator.Assigned_MaterialsStringPipe-delimited list of physical materials or textures bound to the element.Property_Set_CountIntegerQuantitative sum of attached IfcPropertySet containers.Has_GeometryBooleanBoolean flag confirming physical 3D mesh representation.Professional ContextThis pipeline represents a core architectural module used in automated Virtual Design and Construction (VDC) data validation workflows, bridging the gap between computational systems engineering and spatial project execution.Author: Alberto Alvarez Gonzalez — Systems VDC Architect & BIM Coordinator
