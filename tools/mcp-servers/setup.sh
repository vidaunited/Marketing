#!/usr/bin/env bash
# Axanta ERP MCP Server — one-command setup for Claude Code
# Usage: bash tools/mcp-servers/setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Axanta ERP MCP Server Setup ==="
echo ""

# 1. Install Python dependencies
echo "[1/3] Installing dependencies..."
pip install -q -r "$SCRIPT_DIR/requirements.txt"

# 2. Check for .env or prompt for credentials
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo ""
    echo "[2/3] No .env file found. Creating one..."
    echo ""
    read -rp "Axanta URL (e.g. https://tempcanteen.axantacloud.com): " axanta_url
    read -rp "Database name (e.g. tempcanteen): " axanta_db
    read -rp "User email: " axanta_user
    read -rsp "API key: " axanta_key
    echo ""

    cat > "$SCRIPT_DIR/.env" <<EOL
AXANTA_URL="${axanta_url}"
AXANTA_DB="${axanta_db}"
AXANTA_USER="${axanta_user}"
AXANTA_KEY="${axanta_key}"
EOL
    echo "  Created .env file at $SCRIPT_DIR/.env"
else
    echo "[2/3] .env file found, using existing credentials."
fi

# 3. Register MCP server with Claude Code
echo "[3/3] Registering MCP server with Claude Code..."

# Source .env to get variables
set -a
source "$SCRIPT_DIR/.env"
set +a

claude mcp add axanta-erp \
    -e AXANTA_URL="$AXANTA_URL" \
    -e AXANTA_DB="$AXANTA_DB" \
    -e AXANTA_USER="$AXANTA_USER" \
    -e AXANTA_KEY="$AXANTA_KEY" \
    -- python3 "$SCRIPT_DIR/axanta_mcp_server.py"

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Start Claude Code and ask about your ERP data:"
echo '  "What are today'"'"'s sales?"'
echo '  "Check inventory for Red Bull"'
echo '  "Show unpaid invoices"'
echo '  "List customers in Kuwait City"'
echo ""
echo "Run /mcp in Claude Code to verify the server is connected."
