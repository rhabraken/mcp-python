# MCP-Python

First copy the `.env.example` and rename the copy to `.env`

Run with

```
docker-compose up
```

This will launch postgres db at localhost:5432 and will fill it with dummy data.
You can then launch the mcp server with app/server.py. You need to install uv
first.

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Save this in your mcp server config:

```
{
  "mcpServers": {
    "my_database": {
      "command": "uv",
      "args": [
        "--directory",
        "/directory/where/you/installed/it/app/",
        "run",
        "server.py"
      ],
      "env": {
        "DB_URL": "postgresql://postgres:password@localhost:5432/mydatabase"
      }
    }
  }
}
```

Then download claude desktop and run it.
