#!/usr/bin/env python3

import argparse
import sys
import os
import requests
import time
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

# === .env laden ===
load_dotenv()

# === Argumente parsen ===
parser = argparse.ArgumentParser(description="Synchronisiert alle Projekte aus Todoist nach Clockify (nur Ergänzung, keine Löschung).")
parser.add_argument("--clockify-workspace", required=True, help="Workspace in Clockify")
parser.add_argument("--todoist-api-key", required=False, help="API-Key für Todoist")
parser.add_argument("--clockify-api-key", required=False, help="API-Key für Clockify")
parser.add_argument("--no-background", action="store_true")
args = parser.parse_args()

# API-Keys aus Kommandozeile oder .env lesen
TODOIST_API_KEY = args.todoist_api_key or os.getenv("TODOIST_API_KEY")
CLOCKIFY_API_KEY = args.clockify_api_key or os.getenv("CLOCKIFY_API_KEY")
NO_BACKGROUND = args.no_background or False
CLOCKIFY_WORKSPACE_NAME = "privat"

if not TODOIST_API_KEY or not CLOCKIFY_API_KEY:
    print("""
Dieses Script überträgt alle Todoist-Projekte nach Clockify, sofern sie dort noch nicht vorhanden sind.

Erforderliche Parameter:
  --clockify-workspace  Name des Workspaces in Clockify, in den die Projekte importiert werden sollen.

Optionale Parameter:
  --no-background       Programm nach einer Ausführung sofort beenden (anderenfalls alle 60 Minuten erneut synchronisieren)
  --todoist-api-key     Dein API-Key für Todoist (oder Umgebungsvariable TODOIST_API_KEY)
  --clockify-api-key    Dein API-Key für Clockify (oder Umgebungsvariable CLOCKIFY_API_KEY)

Beispiel:
  python sync_projects.py --workspace "My Workspace" --todoist-api-key abc123 --clockify-api-key xyz456
  oder über .env-Datei mit:
  TODOIST_API_KEY=abc123
  CLOCKIFY_API_KEY=xyz456

""")
    sys.exit(1)
    
# === Clockify-HTTP-Hilfsfunktionen ===
CLOCKIFY_API_BASE = "https://api.clockify.me/api/v1"
CLOCKIFY_HEADERS = {"X-Api-Key": CLOCKIFY_API_KEY, "Content-Type": "application/json"}

def get_clockify_workspaces():
    response = requests.get(f"{CLOCKIFY_API_BASE}/workspaces", headers=CLOCKIFY_HEADERS)
    response.raise_for_status()
    return response.json()

def get_clockify_projects(workspace_id):
    response = requests.get(f"{CLOCKIFY_API_BASE}/workspaces/{workspace_id}/projects", headers=CLOCKIFY_HEADERS)
    response.raise_for_status()
    return response.json()

def add_clockify_project(workspace_id, project_name):
    data = {"name": project_name, "isPublic": False}
    response = requests.post(f"{CLOCKIFY_API_BASE}/workspaces/{workspace_id}/projects", headers=CLOCKIFY_HEADERS, json=data)
    response.raise_for_status()
    return response.json()

# === TODOIST & CLOCKIFY INITIALISIEREN ===
todoist = TodoistAPI(TODOIST_API_KEY)

while True:

    # 1. Todoist-Projekte abrufen
    try:
        todoist_projects = next(todoist.get_projects())
    except Exception as e:
        print(f"Fehler beim Abrufen der Todoist-Projekte: {e}")
        sys.exit(1)

    # 2. Clockify: Workspace und vorhandene Projekte abrufen
    workspace = next((w for w in get_clockify_workspaces() if w["name"] == CLOCKIFY_WORKSPACE_NAME), None)
    if not workspace:
        print(f"Clockify-Workspace '{CLOCKIFY_WORKSPACE_NAME}' nicht gefunden.")
        sys.exit(1)

    workspace_id = workspace["id"]

    try:
        clockify_projects = get_clockify_projects(workspace_id)
        existing_clockify_projects = {p["name"] for p in clockify_projects}
    except Exception as e:
        print(f"Fehler beim Abrufen der Clockify-Projekte: {e}")

    # 3. Todoist-Projekte nach Clockify übertragen
    for project in todoist_projects:
        if project.name not in existing_clockify_projects:
            try:
                add_clockify_project(workspace_id, project.name)
                print(f"Projekt '{project.name}' in Clockify angelegt.")
            except Exception as e:
                print(f"Fehler beim Anlegen von Projekt '{project.name}': {e}")
        else:
            print(f"Projekt '{project.name}' existiert bereits in Clockify.")

    print("Projektsynchronisation abgeschlossen.")

    if NO_BACKGROUND:
        break

    time.sleep(3600)