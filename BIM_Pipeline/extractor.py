import ifcopenshell
import pandas as pd
import json
import time
from pathlib import Path
from typing import Dict, Any, List

def setup_environment() -> None:
    print("\n" + "="*70)
    print("OPENBIM SPATIAL & MATERIAL TELEMETRY PIPELINE")
    print("="*70)

def normalize_text(value: Any) -> str:
    if value is None:
        return "UNSPECIFIED"
    clean_str = str(value).strip()
    return clean_str if clean_str else "UNSPECIFIED"

def extract_material_data(element: Any) -> str:
    if not hasattr(element, "HasAssociations"):
        return "UNSPECIFIED"
    
    for association in element.HasAssociations:
        if association.is_a("IfcRelAssociatesMaterial"):
            mat_select = association.RelatingMaterial
            if not mat_select:
                continue
            
            if mat_select.is_a("IfcMaterial"):
                return normalize_text(getattr(mat_select, "Name", None))
            
            elif mat_select.is_a("IfcMaterialLayerSetUsage"):
                layer_set = mat_select.ForLayerSet
                if layer_set and layer_set.MaterialLayers:
                    layers = [
                        normalize_text(getattr(layer.Material, "Name", None))
                        for layer in layer_set.MaterialLayers
                        if layer.Material
                    ]
                    return " | ".join(filter(lambda x: x != "UNSPECIFIED", layers)) or "UNSPECIFIED"
            
            elif mat_select.is_a("IfcMaterialList"):
                materials = [
                    normalize_text(getattr(m, "Name", None))
                    for m in mat_select.Materials
                    if m
                ]
                return " | ".join(filter(lambda x: x != "UNSPECIFIED", materials)) or "UNSPECIFIED"
                
    return "UNSPECIFIED"

def extract_property_count(element: Any) -> int:
    count = 0
    if hasattr(element, "IsDefinedBy"):
        for definition in element.IsDefinedBy:
            if definition.is_a("IfcRelDefinesByProperties"):
                property_set = definition.RelatingPropertyDefinition
                if property_set.is_a("IfcPropertySet") and hasattr(property_set, "HasProperties"):
                    count += len(property_set.HasProperties)
    return count

def extract_topology(file_path: Path) -> List[Dict[str, Any]]:
    print(f"Target Asset       : {file_path.name}")
    
    try:
        model = ifcopenshell.open(str(file_path))
        print(f"Schema Definition  : {model.schema}")
    except Exception as error:
        print(f"Critical Error: Unable to read IFC structural file -> {error}")
        return []

    print("Executing topology and material extraction...\n")
    print("TOPOLOGY BREAKDOWN")
    print("-" * 70)
    
    elements = model.by_type('IfcProduct')
    data_list: List[Dict[str, Any]] = []
    type_counts: Dict[str, int] = {}
    material_catalog: set = set()

    for el in elements:
        entity_type = el.is_a()
        type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
        
        primary_material = extract_material_data(el)
        if primary_material != "UNSPECIFIED":
            for mat_item in primary_material.split(" | "):
                material_catalog.add(mat_item.strip())
        
        element_data = {
            "GlobalId": normalize_text(getattr(el, 'GlobalId', None)),
            "IFC_Class": entity_type,
            "Name": normalize_text(getattr(el, 'Name', None)),
            "ObjectType": normalize_text(getattr(el, 'ObjectType', None)),
            "Tag": normalize_text(getattr(el, 'Tag', None)),
            "Primary_Material": primary_material,
            "Property_Count": extract_property_count(el)
        }
        data_list.append(element_data)

    for entity_type, count in sorted(type_counts.items()):
        print(f"  {entity_type:<26} : {count:>5} entities detected")

    print("\nMETADATA & MATERIAL AUDIT")
    print("-" * 70)
    print(f"  Total Audited Entities     : {len(data_list)}")
    print(f"  Unique Materials Detected  : {len(material_catalog)}")
    if material_catalog:
        sample_mats = ", ".join(sorted(list(material_catalog))[:4])
        print(f"  Material Sample            : {sample_mats}...")

    return data_list

def export_data(data: List[Dict[str, Any]], output_name: str = "bim_spatial_telemetry") -> None:
    if not data:
        return

    print("\nEXPORTING DATA ARTIFACTS")
    print("-" * 70)
    
    try:
        json_path = Path(f"{output_name}.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"  Created JSON Telemetry     : {json_path.name}")

        csv_path = Path(f"{output_name}.csv")
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"  Created CSV Spreadsheet    : {csv_path.name}")
        
    except Exception as error:
        print(f"Serialization Error        : {error}")

def execute_pipeline(target_file: str) -> None:
    start_time = time.time()
    setup_environment()
    
    file_path = Path(target_file)
    if not file_path.exists():
        print(f"Error: Target asset '{target_file}' not found.")
        return

    extracted_data = extract_topology(file_path)
    export_data(extracted_data)

    elapsed_time = round((time.time() - start_time) * 1000, 2)
    print("-" * 70)
    print(f"PIPELINE COMPLETED: {len(extracted_data)} entities audited in {elapsed_time} ms.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    execute_pipeline('modelo_prueba.ifc')