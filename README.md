# AI Employee Vault [Gold]

An intelligent automation system for business operations, social media management, accounting, and audit logging.

## Features

- **Social Media Automation** - Auto-post to Facebook and Instagram
- **Accounting Integration** - MCP server for accounting operations
- **Audit Logging** - Comprehensive logging and compliance tracking
- **Business MCP Server** - Multi-protocol server for business operations
- **Email Automation** - Verified email flow integration

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for MCP features)

### Setup

1. **Install dependencies:**
```bash
pip install -r audit_requirements.txt
```

2. **Configure environment:**
```bash
# Edit .env file with your API keys and credentials
```

3. **Run the system:**
```bash
# Start accounting MCP server
python accounting_mcp_server.py

# Or start business MCP server
python business_mcp_server.py
```

## Documentation

Detailed guides are available in the `documentation/` folder:

- [Architecture Documentation](documentation/ARCHITECTURE_DOCUMENTATION.md)
- [Facebook Setup Guide](documentation/COMPLETE_FACEBOOK_SETUP.md)
- [Accounting Quickstart](documentation/ACCOUNTING_QUICKSTART.md)
- [Social Media Quickstart](documentation/SOCIAL_MEDIA_QUICKSTART.md)
- [MCP Servers Guide](documentation/MULTI_MCP_SERVERS.md)

## Project Structure

```
AI Employee Vault [Gold]/
├── accounting_mcp_server.py    # Accounting MCP server
├── business_mcp_server.py      # Business MCP server
├── audit_logger.py             # Audit logging system
├── autopost_facebook.py        # Facebook auto-posting
├── check_facebook_pages.py     # Facebook page checker
├── .env                        # Environment variables (do not commit)
├── documentation/              # All documentation files
└── README.md                   # This file
```

## Security Notes

- Never commit your `.env` file
- Keep API keys and tokens secure
- Review audit logs regularly

## License

Proprietary - All rights reserved

## Support

For issues and questions, please refer to the documentation folder or contact support.
