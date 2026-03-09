#!/bin/bash
# Essential View Builder MCP - Setup Script
# Verifies Python 3.11+ with mcp package is available.

set -euo pipefail

echo "🚀 Setting up Essential View Builder MCP..."

# 1. Check for Python 3.11
PY="/usr/local/bin/python3.11"
if [[ ! -x "$PY" ]]; then
    echo "❌ Error: Python 3.11 not found at $PY"
    echo "   Please install Homebrew python@3.11:"
    echo "   brew install python@3.11"
    exit 1
fi

echo "✅ Found Python: $PY"

# 2. Verify mcp package is installed
if ! "$PY" -c "import mcp" 2>/dev/null; then
    echo "❌ Error: 'mcp' package not found in Python 3.11"
    echo "   Installing mcp package..."
    "$PY" -m pip install --user mcp
    
    # Verify again
    if ! "$PY" -c "import mcp" 2>/dev/null; then
        echo "❌ Failed to install mcp. Please install manually:"
        echo "   $PY -m pip install mcp"
        exit 1
    fi
fi

echo "✅ MCP package is installed"

# 3. Make start_server.sh executable
chmod +x start_server.sh

echo ""
echo "✨ Setup complete!"
echo ""
echo "To add this MCP to Claude Desktop, add the following to your config:"
echo "(Usually at: ~/Library/Application Support/Claude/claude_desktop_config.json)"
echo ""
echo "{"
echo "  \"mcpServers\": {"
echo "    \"essential-view-builder\": {"
echo "      \"command\": \"/bin/bash\","
echo "      \"args\": [\"$(pwd)/start_server.sh\"]"
echo "    }"
echo "  }"
echo "}"
echo ""
echo "You can now start using the Essential View Builder tools in Claude!"
