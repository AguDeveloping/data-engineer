#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para respaldar la configuraciu00f3n de Metabase y exportar dashboards.
Este script utiliza la API REST de Metabase para exportar dashboards, colecciones y configuraciones.
"""

import requests
import json
import os
import datetime
import argparse
import sys

# Configuraciu00f3n por defecto
METABASE_URL = "http://localhost:3000"
OUTPUT_DIR = "../exports"

def login_to_metabase(url, username, password):
    """Iniciar sesiu00f3n en Metabase y obtener token de sesiu00f3n"""
    login_url = f"{url}/api/session"
    payload = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(login_url, json=payload)
        response.raise_for_status()
        return response.json()["id"]
    except requests.exceptions.RequestException as e:
        print(f"Error al iniciar sesiu00f3n en Metabase: {e}")
        sys.exit(1)

def get_dashboards(url, session_token):
    """Obtener todos los dashboards disponibles"""
    dashboards_url = f"{url}/api/dashboard"
    headers = {"X-Metabase-Session": session_token}
    
    try:
        response = requests.get(dashboards_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener dashboards: {e}")
        return []

def export_dashboard(url, session_token, dashboard_id):
    """Exportar un dashboard especu00edfico"""
    dashboard_url = f"{url}/api/dashboard/{dashboard_id}"
    headers = {"X-Metabase-Session": session_token}
    
    try:
        response = requests.get(dashboard_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al exportar dashboard {dashboard_id}: {e}")
        return None

def get_collections(url, session_token):
    """Obtener todas las colecciones disponibles"""
    collections_url = f"{url}/api/collection"
    headers = {"X-Metabase-Session": session_token}
    
    try:
        response = requests.get(collections_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener colecciones: {e}")
        return []

def export_collection_items(url, session_token, collection_id):
    """Exportar los elementos de una colecciu00f3n"""
    collection_items_url = f"{url}/api/collection/{collection_id}/items"
    headers = {"X-Metabase-Session": session_token}
    
    try:
        response = requests.get(collection_items_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al exportar elementos de la colecciu00f3n {collection_id}: {e}")
        return None

def get_cards(url, session_token):
    """Obtener todas las tarjetas (preguntas) disponibles"""
    cards_url = f"{url}/api/card"
    headers = {"X-Metabase-Session": session_token}
    
    try:
        response = requests.get(cards_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener tarjetas: {e}")
        return []

def export_card(url, session_token, card_id):
    """Exportar una tarjeta (pregunta) especu00edfica"""
    card_url = f"{url}/api/card/{card_id}"
    headers = {"X-Metabase-Session": session_token}
    
    try:
        response = requests.get(card_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al exportar tarjeta {card_id}: {e}")
        return None

def create_output_directory(output_dir):
    """Crear directorio de salida si no existe"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = os.path.join(output_dir, f"metabase_export_{timestamp}")
    
    os.makedirs(export_dir, exist_ok=True)
    os.makedirs(os.path.join(export_dir, "dashboards"), exist_ok=True)
    os.makedirs(os.path.join(export_dir, "collections"), exist_ok=True)
    os.makedirs(os.path.join(export_dir, "cards"), exist_ok=True)
    
    return export_dir

def save_json(data, file_path):
    """Guardar datos en formato JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def export_all(url, session_token, output_dir):
    """Exportar todos los elementos de Metabase"""
    export_dir = create_output_directory(output_dir)
    
    # Exportar dashboards
    print("Exportando dashboards...")
    dashboards = get_dashboards(url, session_token)
    save_json(dashboards, os.path.join(export_dir, "dashboards_list.json"))
    
    for dashboard in dashboards:
        dashboard_id = dashboard["id"]
        dashboard_name = dashboard["name"]
        print(f"  - Exportando dashboard: {dashboard_name} (ID: {dashboard_id})")
        
        dashboard_data = export_dashboard(url, session_token, dashboard_id)
        if dashboard_data:
            file_name = f"{dashboard_id}_{dashboard_name.replace(' ', '_')}.json"
            save_json(dashboard_data, os.path.join(export_dir, "dashboards", file_name))
    
    # Exportar colecciones
    print("\nExportando colecciones...")
    collections = get_collections(url, session_token)
    save_json(collections, os.path.join(export_dir, "collections_list.json"))
    
    for collection in collections:
        collection_id = collection["id"]
        collection_name = collection["name"]
        print(f"  - Exportando colecciu00f3n: {collection_name} (ID: {collection_id})")
        
        collection_items = export_collection_items(url, session_token, collection_id)
        if collection_items:
            file_name = f"{collection_id}_{collection_name.replace(' ', '_')}.json"
            save_json(collection_items, os.path.join(export_dir, "collections", file_name))
    
    # Exportar tarjetas (preguntas)
    print("\nExportando tarjetas (preguntas)...")
    cards = get_cards(url, session_token)
    save_json(cards, os.path.join(export_dir, "cards_list.json"))
    
    for card in cards:
        card_id = card["id"]
        card_name = card["name"]
        print(f"  - Exportando tarjeta: {card_name} (ID: {card_id})")
        
        card_data = export_card(url, session_token, card_id)
        if card_data:
            file_name = f"{card_id}_{card_name.replace(' ', '_')}.json"
            save_json(card_data, os.path.join(export_dir, "cards", file_name))
    
    print(f"\nExportaciu00f3n completa. Archivos guardados en: {export_dir}")
    return export_dir

def main():
    parser = argparse.ArgumentParser(description='Respaldar configuraciu00f3n y dashboards de Metabase')
    parser.add_argument('--url', default=METABASE_URL, help='URL de Metabase (por defecto: http://localhost:3000)')
    parser.add_argument('--username', required=True, help='Nombre de usuario de Metabase')
    parser.add_argument('--password', required=True, help='Contraseu00f1a de Metabase')
    parser.add_argument('--output-dir', default=OUTPUT_DIR, help='Directorio de salida para los respaldos')
    
    args = parser.parse_args()
    
    try:
        print(f"Iniciando sesiu00f3n en Metabase ({args.url})...")
        session_token = login_to_metabase(args.url, args.username, args.password)
        
        print("Exportando configuraciu00f3n de Metabase...")
        export_dir = export_all(args.url, session_token, args.output_dir)
        
        print("\nRespaldo completado exitosamente.")
        print(f"Todos los datos han sido exportados a: {export_dir}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
