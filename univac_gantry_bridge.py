#!/usr/bin/env python3
"""
Revolutionary Technology - Legacy Systems Integration
Bridges the Univac-IX Mainframe emulation to a web-based KVM GUI via Gantry 5.
"""

import typer
import yaml
import subprocess
from pathlib import Path

app = typer.Typer(
    name="UnivacGantryBridge", 
    help="Deploy Univac Sperry KVM GUI to Gantry 5",
    add_completion=False
)

REPO_ROOT = Path(__file__).parent

@app.command()
def build_kvm_particle(
    particle_name: str = typer.Option("univac_sperry_kvm", help="Name of the Gantry 5 particle"),
    host_ip: str = typer.Option("192.168.1.100", help="IP address of the Univac-IX server"),
    port: int = typer.Option(5900, help="VNC/KVM Port")
):
    """
    Generates a Gantry 5 YAML configuration file for the Univac KVM Viewer.
    Drop this into your Gantry 'custom/particles' directory.
    """
    # Gantry 5 Particle YAML structure for a remote KVM connection
    config = {
        "name": particle_name,
        "description": "Univac Sperry Legacy KVM Terminal",
        "type": "particle",
        "icon": "fa-terminal",
        "configuration": {
            "caching": {"type": "static"},
            "fields": {
                "server_ip": {
                    "type": "input.text",
                    "default": host_ip,
                    "label": "Univac-IX Host IP"
                },
                "connection_port": {
                    "type": "input.text",
                    "default": port,
                    "label": "VNC/KVM Port"
                },
                "terminal_theme": {
                    "type": "select",
                    "default": "amber",
                    "options": {
                        "amber": "Sperry Amber Monochrome", 
                        "green": "Classic Phosphor Green",
                        "modern": "High-Contrast Modern"
                    },
                    "label": "Terminal Display Theme"
                },
                "encryption": {
                     "type": "select",
                     "default": "tls1.3",
                     "options": {"none": "Unencrypted (Local Only)", "tls1.3": "TLS 1.3 (Secure)"},
                     "label": "Connection Encryption"
                }
            }
        }
    }
    
    out_path = REPO_ROOT / f"{particle_name}.yaml"
    with open(out_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
    typer.secho(f"Gantry 5 KVM particle configuration saved to {out_path}", fg=typer.colors.GREEN)
    typer.echo("\nINSTRUCTIONS FOR DEPLOYMENT:")
    typer.echo("1. Copy this YAML file to your CMS: user/data/gantry5/themes/[YOUR_THEME]/particles/")
    typer.echo("2. Ensure the paired .html.twig file is placed in the same directory.")

@app.command()
def test_mainframe_connection(
    host_ip: str = typer.Argument("192.168.1.100")
):
    """
    Pings the Univac-IX host to verify the KVM port is open before web deployment.
    """
    typer.echo(f"Initiating diagnostic ping to Univac-IX at {host_ip}...")
    
    # Simple ping check using standard system tools
    try:
        # -c 1 means send 1 packet. Adjust for Windows (-n 1) if necessary.
        result = subprocess.run(["ping", "-c", "1", "-W", "2", host_ip], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            typer.secho("SUCCESS: Univac-IX Host is reachable.", fg=typer.colors.GREEN)
        else:
            typer.secho(f"WARNING: Host {host_ip} is unreachable. Check network routing.", fg=typer.colors.YELLOW)
    except FileNotFoundError:
        typer.secho("Ping utility not found. Skipping network diagnostic.", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
