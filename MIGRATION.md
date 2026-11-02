# Migrating from 0.1.2 to 0.1.3

Upgrade the package in the environment that runs your CLI or MCP server. If using the MCP extra, allow the compatible patched SDK range `mcp>=1.30.0,<2`; resolve conflicting constraints before upgrading. The server remains stdio-based and requires no account for local use. Run the `doctor` command after upgrading.
