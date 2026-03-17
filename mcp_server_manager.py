"""
MCP Server Manager

Unified manager for starting, stopping, and monitoring all MCP servers:
- Accounting MCP Server (port 8001)
- Social Media MCP Server (port 8002)
- Personal MCP Server (port 8003)
- Business MCP Server (port 8004)

Provides centralized control for the multi-domain MCP architecture.
"""

import asyncio
import logging
import os
import signal
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List
import subprocess
import time
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPServerConfig:
    """Configuration for an MCP server"""
    
    def __init__(self, name: str, file: str, port: int, 
                 domain: str, required: bool = True):
        self.name = name
        self.file = file
        self.port = port
        self.domain = domain
        self.required = required
        self.url = f"http://localhost:{port}"
        self.health_endpoint = f"{self.url}/health"


class MCPServerManager:
    """
    Manages lifecycle and health monitoring of all MCP servers.
    """
    
    def __init__(self):
        # Define MCP server configurations
        self.servers: Dict[str, MCPServerConfig] = {
            "Accounting": MCPServerConfig(
                name="Accounting MCP Server",
                file="accounting_mcp_server.py",
                port=8001,
                domain="Accounting",
                required=True
            ),
            "Social Media": MCPServerConfig(
                name="Social MCP Server",
                file="social_mcp_server.py",
                port=8002,
                domain="Social Media",
                required=True
            ),
            "Personal": MCPServerConfig(
                name="Personal MCP Server",
                file="personal_mcp_server.py",
                port=8003,
                domain="Personal",
                required=True
            ),
            "Business": MCPServerConfig(
                name="Business MCP Server",
                file="business_mcp_server.py",
                port=8004,
                domain="Business",
                required=True
            )
        }
        
        # Track running processes
        self.processes: Dict[str, subprocess.Popen] = {}
        
        # HTTP client for health checks
        self.http_timeout = httpx.Timeout(5.0)
        
        logger.info("MCP Server Manager initialized")
    
    def start_server(self, domain: str, background: bool = True) -> bool:
        """
        Start a specific MCP server.
        
        Args:
            domain: Domain name (Accounting, Social Media, Personal, Business)
            background: Whether to run in background
            
        Returns:
            True if started successfully, False otherwise
        """
        if domain not in self.servers:
            logger.error(f"Unknown domain: {domain}")
            return False
        
        config = self.servers[domain]
        
        # Check if already running
        if domain in self.processes:
            if self.processes[domain].poll() is None:
                logger.info(f"{config.name} is already running")
                return True
            else:
                # Process ended, clean up
                del self.processes[domain]
        
        # Check if server file exists
        if not os.path.exists(config.file):
            logger.error(f"Server file not found: {config.file}")
            return False
        
        try:
            # Start the server
            cmd = [sys.executable, config.file]
            
            if background:
                # Run in background (Windows compatible)
                creationflags = 0
                if os.name == 'nt':  # Windows
                    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=creationflags
                )
            else:
                process = subprocess.Popen(cmd)
            
            self.processes[domain] = process
            
            # Wait a moment for server to start
            time.sleep(2)
            
            # Verify server is running
            if self.check_server_health(domain):
                logger.info(f"✅ {config.name} started successfully on port {config.port}")
                return True
            else:
                logger.warning(f"⚠️ {config.name} started but health check failed")
                return True  # Still consider it started, may need more time
                
        except Exception as e:
            logger.error(f"Failed to start {config.name}: {str(e)}")
            return False
    
    def start_all_servers(self) -> Dict[str, bool]:
        """
        Start all MCP servers.
        
        Returns:
            Dictionary mapping domain to start status
        """
        results = {}
        
        logger.info("=" * 60)
        logger.info("Starting all MCP servers...")
        logger.info("=" * 60)
        
        for domain in self.servers:
            logger.info(f"\nStarting {domain} domain server...")
            results[domain] = self.start_server(domain)
        
        # Wait for all servers to initialize
        logger.info("\nWaiting for servers to initialize...")
        time.sleep(3)
        
        # Final health check
        logger.info("\n" + "=" * 60)
        logger.info("Final Health Check")
        logger.info("=" * 60)
        
        for domain in self.servers:
            status = "✅ Healthy" if self.check_server_health(domain) else "❌ Unhealthy"
            logger.info(f"{domain}: {status}")
        
        return results
    
    def stop_server(self, domain: str) -> bool:
        """
        Stop a specific MCP server.
        
        Args:
            domain: Domain name
            
        Returns:
            True if stopped successfully, False otherwise
        """
        if domain not in self.servers:
            return False
        
        if domain not in self.processes:
            logger.warning(f"{domain} server is not running")
            return True
        
        try:
            process = self.processes[domain]
            
            # Send terminate signal
            if os.name == 'nt':  # Windows
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                process.terminate()
            
            # Wait for graceful shutdown
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if not responding
                process.kill()
                process.wait()
            
            del self.processes[domain]
            
            logger.info(f"✅ {self.servers[domain].name} stopped")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping {domain} server: {str(e)}")
            return False
    
    def stop_all_servers(self) -> Dict[str, bool]:
        """
        Stop all MCP servers.
        
        Returns:
            Dictionary mapping domain to stop status
        """
        results = {}
        
        logger.info("=" * 60)
        logger.info("Stopping all MCP servers...")
        logger.info("=" * 60)
        
        for domain in list(self.processes.keys()):
            results[domain] = self.stop_server(domain)
        
        return results
    
    def check_server_health(self, domain: str) -> bool:
        """
        Check health of a specific MCP server.
        
        Args:
            domain: Domain name
            
        Returns:
            True if healthy, False otherwise
        """
        if domain not in self.servers:
            return False
        
        config = self.servers[domain]
        
        try:
            with httpx.Client(timeout=self.http_timeout) as client:
                response = client.get(config.health_endpoint)
                response.raise_for_status()
                
                data = response.json()
                return data.get("status") == "healthy"
                
        except Exception:
            return False
    
    def get_all_health_status(self) -> Dict[str, Any]:
        """
        Get health status of all MCP servers.
        
        Returns:
            Dictionary with health status for each domain
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "servers": {}
        }
        
        for domain, config in self.servers.items():
            is_healthy = self.check_server_health(domain)
            is_running = domain in self.processes and self.processes[domain].poll() is None
            
            status["servers"][domain] = {
                "health": "healthy" if is_healthy else "unhealthy",
                "running": is_running,
                "port": config.port,
                "url": config.url
            }
        
        return status
    
    def get_cross_domain_topology(self) -> str:
        """
        Get ASCII art representation of cross-domain topology.
        
        Returns:
            String with topology diagram
        """
        topology = """
╔══════════════════════════════════════════════════════════════════╗
║              CROSS-DOMAIN MCP SERVER TOPOLOGY                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ┌─────────────────────────────────────────────────────────┐    ║
║  │                    BUSINESS DOMAIN                       │    ║
║  │              (Business MCP Server - :8004)               │    ║
║  │                                                          │    ║
║  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │    ║
║  │  │   Meetings   │  │     CRM      │  │    Sales     │  │    ║
║  │  └──────────────┘  └──────────────┘  └──────────────┘  │    ║
║  └─────────────────────────────────────────────────────────┘    ║
║         │                    │                    │              ║
║         │                    │                    │              ║
║         ▼                    ▼                    ▼              ║
║  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      ║
║  │   PERSONAL   │    │  ACCOUNTING  │    │ SOCIAL MEDIA │      ║
║  │  (:8003)     │    │   (:8001)    │    │   (:8002)    │      ║
║  │              │    │              │    │              │      ║
║  │ Appointments │    │  Invoicing   │    │   Facebook   │      ║
║  │  Reminders   │    │   Expenses   │    │  Instagram   │      ║
║  │    Travel    │    │   Reports    │    │   Twitter    │      ║
║  └──────────────┘    └──────────────┘    └──────────────┘      ║
║                                                                  ║
║  Integration Flow:                                               ║
║  • Business → Personal: Work-life balance flags                 ║
║  • Business → Accounting: Financial task flags                  ║
║  • Business → Social Media: Marketing task flags                ║
║  • Personal → Accounting: Expense categorization                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
        return topology
    
    def print_status(self):
        """Print formatted status of all servers"""
        status = self.get_all_health_status()
        
        print("\n" + "=" * 70)
        print("MCP SERVER STATUS")
        print("=" * 70)
        print(f"Timestamp: {status['timestamp']}")
        print("-" * 70)
        
        print(f"\n{'Domain':<15} {'Status':<12} {'Running':<10} {'Port':<8} {'URL'}")
        print("-" * 70)
        
        for domain, info in status["servers"].items():
            status_icon = "✅" if info["health"] == "healthy" else "❌"
            running_icon = "Yes" if info["running"] else "No"
            print(f"{domain:<15} {status_icon} {info['health']:<10} {running_icon:<10} {info['port']:<8} {info['url']}")
        
        print("\n" + "=" * 70)
        print(self.get_cross_domain_topology())


# Convenience functions
def start_all():
    """Start all MCP servers"""
    manager = MCPServerManager()
    manager.start_all_servers()
    manager.print_status()


def stop_all():
    """Stop all MCP servers"""
    manager = MCPServerManager()
    manager.stop_all_servers()
    print("\n✅ All MCP servers stopped")


def check_health():
    """Check health of all MCP servers"""
    manager = MCPServerManager()
    manager.print_status()


# Example usage when run directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Server Manager")
    parser.add_argument(
        "action",
        choices=["start", "stop", "health", "status"],
        help="Action to perform"
    )
    parser.add_argument(
        "--domain",
        choices=["Accounting", "Social Media", "Personal", "Business"],
        help="Specific domain to act on (optional)"
    )
    
    args = parser.parse_args()
    
    manager = MCPServerManager()
    
    if args.action == "start":
        if args.domain:
            manager.start_server(args.domain)
        else:
            manager.start_all_servers()
        manager.print_status()
        
    elif args.action == "stop":
        if args.domain:
            manager.stop_server(args.domain)
        else:
            manager.stop_all_servers()
            
    elif args.action == "health":
        manager.print_status()
        
    elif args.action == "status":
        manager.print_status()
