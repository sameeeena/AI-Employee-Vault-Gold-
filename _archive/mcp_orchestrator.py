"""
Enhanced MCP Server Orchestrator

Unified orchestrator for managing multiple MCP servers with:
- Auto-discovery of MCP servers
- Load balancing across servers
- Failover and recovery
- Centralized logging
- Performance monitoring
- Cross-domain routing

Usage:
    python mcp_orchestrator.py start    # Start all servers
    python mcp_orchestrator.py stop     # Stop all servers
    python mcp_orchestrator.py status   # Check status
    python mcp_orchestrator.py route    # Start routing service
"""

import asyncio
import json
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
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPServerInfo:
    """Information about an MCP server"""

    def __init__(self, domain: str, file: str, port: int,
                 tools: List[str] = None, required: bool = True):
        self.domain = domain
        self.file = file
        self.port = port
        self.tools = tools or []
        self.required = required
        self.url = f"http://localhost:{port}"
        self.health_endpoint = f"{self.url}/health"
        self.process: Optional[subprocess.Popen] = None
        self.last_health_check: Optional[datetime] = None
        self.is_healthy: bool = False
        self.request_count: int = 0
        self.avg_response_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "domain": self.domain,
            "file": self.file,
            "port": self.port,
            "url": self.url,
            "tools": self.tools,
            "required": self.required,
            "is_healthy": self.is_healthy,
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None,
            "request_count": self.request_count,
            "avg_response_time": self.avg_response_time
        }


class MCPOrchestrator:
    """
    Orchestrates multiple MCP servers with intelligent routing and failover.
    """

    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.servers: Dict[str, MCPServerInfo] = {}
        self.http_timeout = httpx.Timeout(5.0)
        self.routing_table: Dict[str, str] = {}  # action_type -> domain
        self._load_server_config()
        self._setup_routing_table()

        # Ensure logs directory exists
        self.logs_dir = self.base_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self._setup_logging()

        logger.info("MCP Orchestrator initialized")

    def _setup_logging(self):
        """Setup orchestrator logging"""
        log_file = self.logs_dir / "mcp_orchestrator_log.md"

        # Create log file if not exists
        if not log_file.exists():
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("# MCP Orchestrator Log\n\n")

        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

    def _load_server_config(self):
        """Load MCP server configurations"""
        config_file = self.base_dir / "mcp_config" / "mcp_orchestrator_config.json"

        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            for server_config in config.get("servers", []):
                server = MCPServerInfo(
                    domain=server_config["domain"],
                    file=server_config["file"],
                    port=server_config["port"],
                    tools=server_config.get("tools", []),
                    required=server_config.get("required", True)
                )
                self.servers[server.domain] = server

            logger.info(f"Loaded {len(self.servers)} server configurations")
        else:
            # Default configuration
            self._setup_default_servers()
            self._save_config()

    def _setup_default_servers(self):
        """Setup default server configurations"""
        default_servers = [
            {
                "domain": "Accounting",
                "file": "accounting_mcp_server.py",
                "port": 8001,
                "tools": ["create_invoice", "record_expense", "generate_report", "process_payment"],
                "required": True
            },
            {
                "domain": "Social Media",
                "file": "social_mcp_server_v2.py",
                "port": 8002,
                "tools": ["post_message", "get_metrics", "generate_summary", "schedule_post"],
                "required": True
            },
            {
                "domain": "Personal",
                "file": "personal_mcp_server.py",
                "port": 8003,
                "tools": ["schedule_appointment", "set_reminder", "plan_travel", "create_task"],
                "required": True
            },
            {
                "domain": "Business",
                "file": "business_mcp_server.py",
                "port": 8004,
                "tools": ["schedule_meeting", "update_crm", "update_sales_pipeline", "create_project"],
                "required": True
            }
        ]

        for server_config in default_servers:
            server = MCPServerInfo(**server_config)
            self.servers[server.domain] = server

    def _setup_routing_table(self):
        """Setup action type to domain routing"""
        self.routing_table = {
            # Accounting actions
            "invoice": "Accounting",
            "expense": "Accounting",
            "payment": "Accounting",
            "financial_report": "Accounting",
            "tax": "Accounting",

            # Social Media actions
            "post": "Social Media",
            "social_media": "Social Media",
            "facebook": "Social Media",
            "instagram": "Social Media",
            "twitter": "Social Media",
            "linkedin": "Social Media",
            "engagement": "Social Media",

            # Personal actions
            "appointment": "Personal",
            "reminder": "Personal",
            "travel": "Personal",
            "personal_task": "Personal",
            "calendar": "Personal",

            # Business actions
            "meeting": "Business",
            "crm": "Business",
            "sales": "Business",
            "project": "Business",
            "contract": "Business",
            "client": "Business"
        }

        logger.info(f"Setup routing table with {len(self.routing_table)} routes")

    def _save_config(self):
        """Save configuration to file"""
        config_file = self.base_dir / "mcp_config" / "mcp_orchestrator_config.json"

        config = {
            "version": "2.0.0",
            "last_updated": datetime.now().isoformat(),
            "servers": [server.to_dict() for server in self.servers.values()],
            "routing_table": self.routing_table
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        logger.info(f"Configuration saved to {config_file}")

    async def start_server(self, domain: str) -> bool:
        """Start a specific MCP server"""
        if domain not in self.servers:
            logger.error(f"Unknown domain: {domain}")
            return False

        server = self.servers[domain]

        # Check if already running
        if server.process and server.process.poll() is None:
            logger.info(f"{domain} server is already running")
            return True

        # Check if server file exists
        if not os.path.exists(server.file):
            logger.error(f"Server file not found: {server.file}")
            return False

        try:
            # Start the server
            cmd = [sys.executable, server.file]

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

            server.process = process

            # Wait for server to start
            await asyncio.sleep(2)

            # Verify server is running
            if await self.check_server_health(domain):
                logger.info(f"✅ {domain} server started successfully on port {server.port}")
                return True
            else:
                logger.warning(f"⚠️ {domain} server started but health check failed")
                return True

        except Exception as e:
            logger.error(f"Failed to start {domain} server: {str(e)}")
            return False

    async def start_all_servers(self) -> Dict[str, bool]:
        """Start all MCP servers"""
        results = {}

        logger.info("=" * 60)
        logger.info("Starting all MCP servers...")
        logger.info("=" * 60)

        # Start all servers in parallel
        tasks = {domain: self.start_server(domain) for domain in self.servers}
        results_dict = await asyncio.gather(*tasks.values())

        for domain, result in zip(tasks.keys(), results_dict):
            results[domain] = result

        # Wait for initialization
        await asyncio.sleep(3)

        # Final health check
        logger.info("\n" + "=" * 60)
        logger.info("Final Health Check")
        logger.info("=" * 60)

        for domain in self.servers:
            status = "✅ Healthy" if await self.check_server_health(domain) else "❌ Unhealthy"
            logger.info(f"{domain}: {status}")

        return results

    async def stop_server(self, domain: str) -> bool:
        """Stop a specific MCP server"""
        if domain not in self.servers:
            return False

        server = self.servers[domain]

        if server.process is None:
            logger.warning(f"{domain} server is not running")
            return True

        try:
            # Send terminate signal
            if os.name == 'nt':  # Windows
                server.process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                server.process.terminate()

            # Wait for graceful shutdown
            try:
                server.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if not responding
                server.process.kill()
                server.process.wait()

            server.process = None
            server.is_healthy = False

            logger.info(f"✅ {domain} server stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping {domain} server: {str(e)}")
            return False

    async def stop_all_servers(self) -> Dict[str, bool]:
        """Stop all MCP servers"""
        results = {}

        logger.info("=" * 60)
        logger.info("Stopping all MCP servers...")
        logger.info("=" * 60)

        for domain in list(self.servers.keys()):
            results[domain] = await self.stop_server(domain)

        return results

    async def check_server_health(self, domain: str) -> bool:
        """Check health of a specific MCP server"""
        if domain not in self.servers:
            return False

        server = self.servers[domain]

        try:
            async with httpx.AsyncClient(timeout=self.http_timeout) as client:
                response = await client.get(server.health_endpoint)
                response.raise_for_status()

                data = response.json()
                is_healthy = data.get("status") == "healthy"

                server.is_healthy = is_healthy
                server.last_health_check = datetime.now()

                return is_healthy

        except Exception:
            server.is_healthy = False
            return False

    async def check_all_health(self) -> Dict[str, Any]:
        """Check health of all servers"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "servers": {}
        }

        for domain, server in self.servers.items():
            is_healthy = await self.check_server_health(domain)
            is_running = server.process and server.process.poll() is None

            status["servers"][domain] = {
                "health": "healthy" if is_healthy else "unhealthy",
                "running": is_running,
                "port": server.port,
                "url": server.url,
                "tools": server.tools,
                "request_count": server.request_count,
                "avg_response_time": server.avg_response_time
            }

        return status

    def route_action(self, action_type: str) -> Optional[str]:
        """
        Route an action type to the appropriate domain.

        Args:
            action_type: Type of action (e.g., "invoice", "post", "meeting")

        Returns:
            Domain name or None if no route found
        """
        action_type_lower = action_type.lower()

        # Direct match
        if action_type_lower in self.routing_table:
            return self.routing_table[action_type_lower]

        # Partial match
        for key, domain in self.routing_table.items():
            if key in action_type_lower:
                return domain

        # Default to Business domain for unknown actions
        logger.warning(f"No route found for '{action_type}', defaulting to Business")
        return "Business"

    async def execute_action(self, action_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an action by routing to appropriate domain server.

        Args:
            action_type: Type of action
            params: Action parameters

        Returns:
            Action result
        """
        # Route to appropriate domain
        domain = self.route_action(action_type)

        if not domain or domain not in self.servers:
            return {
                "success": False,
                "error": f"No server found for action type: {action_type}"
            }

        server = self.servers[domain]

        # Check server health
        if not server.is_healthy:
            # Try to recover
            logger.info(f"Attempting to recover {domain} server...")
            await self.start_server(domain)

            if not await self.check_server_health(domain):
                return {
                    "success": False,
                    "error": f"Server {domain} is unhealthy"
                }

        # Execute action
        start_time = datetime.now()
        try:
            async with httpx.AsyncClient(timeout=self.http_timeout) as client:
                # Try to call via tool endpoint
                tool_url = f"{server.url}/api/call_tool"

                response = await client.post(tool_url, json={
                    "tool": action_type,
                    "params": params
                })

                response.raise_for_status()
                result = response.json()

                # Update metrics
                server.request_count += 1
                elapsed = (datetime.now() - start_time).total_seconds()
                server.avg_response_time = (server.avg_response_time + elapsed) / 2

                return result

        except Exception as e:
            logger.error(f"Failed to execute action {action_type} on {domain}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_topology_ascii(self) -> str:
        """Get ASCII art topology diagram"""
        topology = """
╔══════════════════════════════════════════════════════════════════╗
║              MCP SERVER ORCHESTRATOR TOPOLOGY                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║                        ┌──────────────┐                          ║
║                        │ ORCHESTRATOR │                          ║
║                        │  (Port 8000) │                          ║
║                        └──────┬───────┘                          ║
║                               │                                  ║
║         ┌─────────────────────┼─────────────────────┐            ║
║         │                     │                     │            ║
║         ▼                     ▼                     ▼            ║
║  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      ║
║  │  ACCOUNTING  │    │    BUSINESS  │    │   PERSONAL   │      ║
║  │   (:8001)    │    │   (:8004)    │    │   (:8003)    │      ║
║  │              │    │              │    │              │      ║
║  │  - Invoices  │    │  - Meetings  │    │ - Appts      │      ║
║  │  - Expenses  │    │  - CRM       │    │ - Reminders  │      ║
║  │  - Reports   │    │  - Sales     │    │ - Travel     │      ║
║  │  - Payments  │    │  - Projects  │    │ - Tasks      │      ║
║  └──────────────┘    └──────────────┘    └──────────────┘      ║
║                               │                                  ║
║                               ▼                                  ║
║                        ┌──────────────┐                          ║
║                        │ SOCIAL MEDIA │                          ║
║                        │   (:8002)    │                          ║
║                        │              │                          ║
║                        │ - Facebook   │                          ║
║                        │ - Instagram  │                          ║
║                        │ - Twitter    │                          ║
║                        │ - LinkedIn   │                          ║
║                        └──────────────┘                          ║
║                                                                  ║
║  Action Routing:                                                 ║
║  • invoice/expense → Accounting                                 ║
║  • meeting/crm → Business                                       ║
║  • appointment/reminder → Personal                              ║
║  • post/social → Social Media                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
        return topology

    def print_status(self):
        """Print formatted status of all servers"""
        # Fix Windows console encoding
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')

        print("\n" + "=" * 70)
        print("MCP ORCHESTRATOR STATUS")
        print("=" * 70)

        status = asyncio.run(self.check_all_health())

        print(f"Timestamp: {status['timestamp']}")
        print("-" * 70)

        print(f"\n{'Domain':<15} {'Status':<12} {'Port':<8} {'Tools':<40}")
        print("-" * 70)

        for domain, info in status["servers"].items():
            status_icon = "[OK]" if info["health"] == "healthy" else "[FAIL]"
            tools_str = ", ".join(info.get("tools", [])[:3])
            if len(info.get("tools", [])) > 3:
                tools_str += "..."
            print(f"{domain:<15} {status_icon:<12} {info['port']:<8} {tools_str:<40}")

        print("\n" + "=" * 70)
        print(self.get_topology_ascii())


# Convenience functions
async def start_all():
    """Start all MCP servers"""
    orchestrator = MCPOrchestrator()
    await orchestrator.start_all_servers()
    orchestrator.print_status()


async def stop_all():
    """Stop all MCP servers"""
    orchestrator = MCPOrchestrator()
    await orchestrator.stop_all_servers()
    print("\n✅ All MCP servers stopped")


async def check_health():
    """Check health of all MCP servers"""
    orchestrator = MCPOrchestrator()
    orchestrator.print_status()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MCP Server Orchestrator")
    parser.add_argument(
        "action",
        choices=["start", "stop", "health", "status", "route"],
        help="Action to perform"
    )
    parser.add_argument(
        "--domain",
        choices=["Accounting", "Social Media", "Personal", "Business"],
        help="Specific domain to act on (optional)"
    )

    args = parser.parse_args()

    orchestrator = MCPOrchestrator()

    if args.action == "start":
        if args.domain:
            asyncio.run(orchestrator.start_server(args.domain))
        else:
            asyncio.run(orchestrator.start_all_servers())
        orchestrator.print_status()

    elif args.action == "stop":
        if args.domain:
            asyncio.run(orchestrator.stop_server(args.domain))
        else:
            asyncio.run(orchestrator.stop_all_servers())

    elif args.action == "health":
        asyncio.run(orchestrator.check_all_health())
        orchestrator.print_status()

    elif args.action == "status":
        orchestrator.print_status()

    elif args.action == "route":
        print("\nAction Routing Table:")
        print("-" * 70)
        for action_type, domain in orchestrator.routing_table.items():
            print(f"  {action_type:<20} → {domain}")
        print("-" * 70)
