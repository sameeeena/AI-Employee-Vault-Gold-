"""
Accounting MCP Server

FastAPI service that connects to Odoo Community via JSON-RPC API
to perform accounting operations like creating invoices, recording expenses,
and fetching financial reports.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import hashlib
import aiofiles
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for startup/shutdown events"""
    # Startup
    logger.info("Initializing Accounting MCP Server...")
    if not await odoo_client.auth_manager.authenticate():
        logger.error("Failed to authenticate with Odoo on startup")
    else:
        logger.info("Successfully connected to Odoo")
    yield
    # Shutdown (cleanup if needed)
    logger.info("Shutting down Accounting MCP Server...")


app = FastAPI(title="Accounting MCP Server", version="1.0.0", lifespan=lifespan)


class OdooConfig:
    """Configuration for Odoo connection"""
    def __init__(self):
        self.url = os.getenv("ODOO_URL", "http://localhost:8069")
        self.db = os.getenv("ODOO_DB", "odoo_db")
        self.username = os.getenv("ODOO_USERNAME", "admin")
        self.password = os.getenv("ODOO_PASSWORD", "admin")


class JSONRPCResponse(BaseModel):
    """Standard response model"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: str


class InvoiceRequest(BaseModel):
    partner_id: int
    product_ids: list[int]
    quantities: list[float]
    prices: list[float]
    journal_id: Optional[int] = None
    date: Optional[str] = None
    reference: Optional[str] = None


class ExpenseRequest(BaseModel):
    partner_id: int
    product_id: int
    quantity: float
    price_unit: float
    account_id: int
    date: Optional[str] = None
    reference: Optional[str] = None


class FinancialReportRequest(BaseModel):
    date_from: str
    date_to: str
    company_id: Optional[int] = None


class AuthenticationManager:
    """Handles Odoo authentication and session management"""

    def __init__(self):
        self.config = OdooConfig()
        self.uid = None
        self.session_id = None

    async def authenticate(self) -> bool:
        """Authenticate with Odoo and get UID"""
        url = f"{self.config.url}/jsonrpc"

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [
                    self.config.db,
                    self.config.username,
                    self.config.password,
                    {}
                ]
            },
            "id": int(datetime.now(timezone.utc).timestamp())
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

                result = response.json()
                if 'result' in result and result['result']:
                    self.uid = result['result']
                    logger.info(f"Authentication successful, UID: {self.uid}")
                    return True
                else:
                    logger.error("Authentication failed")
                    return False
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False

    async def ensure_authenticated(self) -> bool:
        """Ensure we have a valid session, authenticate if needed"""
        if not self.uid:
            return await self.authenticate()
        return True


class OdooAPIClient:
    """Odoo API client using JSON-RPC"""

    def __init__(self):
        self.auth_manager = AuthenticationManager()

    async def call_method(self, model: str, method: str, args: list, kwargs: dict = None) -> Dict[str, Any]:
        """Make a JSON-RPC call to Odoo"""
        if kwargs is None:
            kwargs = {}

        if not await self.auth_manager.ensure_authenticated():
            raise HTTPException(status_code=401, detail="Authentication failed")

        url = f"{self.auth_manager.config.url}/jsonrpc"

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.auth_manager.config.db,
                    self.auth_manager.uid,
                    self.auth_manager.config.password,
                    model,
                    method,
                    args,
                    kwargs
                ]
            },
            "id": int(datetime.now(timezone.utc).timestamp())
        }

        # Log the request
        await self.log_request(model, method, args, kwargs)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

                result = response.json()

                # Log the response
                await self.log_response(model, method, result)

                if 'error' in result:
                    raise HTTPException(status_code=500, detail=result['error'])

                return result.get('result', {})

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            await self.log_error(model, method, str(e))
            raise HTTPException(status_code=e.response.status_code, detail=error_msg)

        except httpx.RequestError as e:
            error_msg = f"Request error occurred: {str(e)}"
            logger.error(error_msg)
            await self.log_error(model, method, str(e))
            raise HTTPException(status_code=500, detail=error_msg)

        except Exception as e:
            error_msg = f"Unexpected error occurred: {str(e)}"
            logger.error(error_msg)
            await self.log_error(model, method, str(e))
            raise HTTPException(status_code=500, detail=error_msg)

    async def log_request(self, model: str, method: str, args: list, kwargs: dict):
        """Log the API request to accounting_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        request_id = hashlib.md5(f"{timestamp}_{model}_{method}".encode()).hexdigest()[:8]

        log_entry = f"""
## Request Log - {request_id}
- **Timestamp:** {timestamp}
- **Model:** {model}
- **Method:** {method}
- **Args:** {json.dumps(args, default=str)}
- **Kwargs:** {json.dumps(kwargs, default=str)}

"""

        async with aiofiles.open("accounting_log.md", "a", encoding="utf-8") as log_file:
            await log_file.write(log_entry)

    async def log_response(self, model: str, method: str, result: Any):
        """Log the API response to accounting_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        log_entry = f"""- **Response:** {json.dumps(result, default=str)[:500]}...

---

"""

        async with aiofiles.open("accounting_log.md", "a", encoding="utf-8") as log_file:
            await log_file.write(log_entry)

    async def log_error(self, model: str, method: str, error: str):
        """Log errors to accounting_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        log_entry = f"""
## Error Log
- **Timestamp:** {timestamp}
- **Model:** {model}
- **Method:** {method}
- **Error:** {error}

---

"""

        async with aiofiles.open("accounting_log.md", "a", encoding="utf-8") as log_file:
            await log_file.write(log_entry)


# Initialize the API client
odoo_client = OdooAPIClient()


@app.post("/create_invoice", response_model=JSONRPCResponse)
async def create_invoice(request: InvoiceRequest):
    """Create a new invoice in Odoo"""
    try:
        # Prepare invoice values
        invoice_vals = {
            'partner_id': request.partner_id,
            'move_type': 'out_invoice',
            'invoice_date': request.date or datetime.now().strftime('%Y-%m-%d'),
            'ref': request.reference,
        }

        # Prepare line items
        line_items = []
        for i, product_id in enumerate(request.product_ids):
            line_items.append((0, 0, {
                'product_id': product_id,
                'quantity': request.quantities[i],
                'price_unit': request.prices[i],
            }))

        invoice_vals['invoice_line_ids'] = line_items

        # Create the invoice
        result = await odoo_client.call_method(
            model='account.move',
            method='create',
            args=[invoice_vals]
        )

        # Post the invoice to validate it
        await odoo_client.call_method(
            model='account.move',
            method='action_post',
            args=[[result]]
        )

        return JSONRPCResponse(
            success=True,
            data={"invoice_id": result},
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )

    except Exception as e:
        logger.error(f"Error creating invoice: {str(e)}")
        return JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )


@app.post("/record_expense", response_model=JSONRPCResponse)
async def record_expense(request: ExpenseRequest):
    """Record an expense in Odoo"""
    try:
        # Prepare expense values
        expense_vals = {
            'partner_id': request.partner_id,
            'move_type': 'in_invoice',
            'invoice_date': request.date or datetime.now().strftime('%Y-%m-%d'),
            'ref': request.reference,
            'invoice_line_ids': [(0, 0, {
                'product_id': request.product_id,
                'quantity': request.quantity,
                'price_unit': request.price_unit,
                'account_id': request.account_id,
            })]
        }

        # Create the expense entry
        result = await odoo_client.call_method(
            model='account.move',
            method='create',
            args=[expense_vals]
        )

        # Post the expense to validate it
        await odoo_client.call_method(
            model='account.move',
            method='action_post',
            args=[[result]]
        )

        return JSONRPCResponse(
            success=True,
            data={"expense_id": result},
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )

    except Exception as e:
        logger.error(f"Error recording expense: {str(e)}")
        return JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )


@app.post("/fetch_profit_loss", response_model=JSONRPCResponse)
async def fetch_profit_loss(request: FinancialReportRequest):
    """Fetch profit and loss statement"""
    try:
        # Search for moves in the specified date range
        domain = [
            ('date', '>=', request.date_from),
            ('date', '<=', request.date_to),
            ('state', '=', 'posted'),
            ('move_type', 'in', ['out_invoice', 'in_invoice', 'entry'])
        ]

        if request.company_id:
            domain.append(('company_id', '=', request.company_id))

        moves = await odoo_client.call_method(
            model='account.move',
            method='search_read',
            args=[domain, ['id', 'name', 'date', 'amount_total', 'move_type']],
            kwargs={'order': 'date'}
        )

        # Calculate profit/loss from invoices directly
        total_income = 0.0
        total_expenses = 0.0
        
        for move in moves:
            amount = move.get('amount_total', 0) or 0
            move_type = move.get('move_type', '')
            
            # Customer invoices = income
            if move_type == 'out_invoice':
                total_income += amount
            # Vendor bills = expenses
            elif move_type == 'in_invoice':
                total_expenses += amount
        
        net_profit = total_income - total_expenses

        result = {
            "period": f"{request.date_from} to {request.date_to}",
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "moves_count": len(moves),
            "moves_summary": moves[:10]  # Limit for readability
        }

        return JSONRPCResponse(
            success=True,
            data=result,
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )

    except Exception as e:
        logger.error(f"Error fetching profit/loss: {str(e)}")
        return JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )


@app.post("/fetch_balance_sheet", response_model=JSONRPCResponse)
async def fetch_balance_sheet(request: FinancialReportRequest):
    """Fetch balance sheet"""
    try:
        # Get all posted moves up to the end date
        domain = [
            ('date', '<=', request.date_to),
            ('state', '=', 'posted'),
        ]

        if request.company_id:
            domain.append(('company_id', '=', request.company_id))

        moves = await odoo_client.call_method(
            model='account.move',
            method='search_read',
            args=[domain, ['id', 'name', 'date', 'amount_total', 'move_type']],
            kwargs={}
        )

        # Simplified balance sheet calculation
        # In a real implementation, you'd query account balances from account.account
        # For now, we'll return the moves summary
        
        result = {
            "as_of_date": request.date_to,
            "moves_count": len(moves),
            "moves_summary": moves[:10],  # Limit for readability
            "note": "Full balance sheet requires chart of accounts configuration"
        }

        return JSONRPCResponse(
            success=True,
            data=result,
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )

    except Exception as e:
        logger.error(f"Error fetching balance sheet: {str(e)}")
        return JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "config": {
            "url": odoo_client.auth_manager.config.url,
            "db": odoo_client.auth_manager.config.db,
            "username": odoo_client.auth_manager.config.username
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)