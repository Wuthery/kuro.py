# kuro.py

Async API wrapper for KuroBBS and Waves game written in Python

## Usage

Basic usage example:

```python
import asyncio
import kuro

async def main() -> None:
    client = kuro.Client()
    login_result = await client.game_login("email@example.com", "password")
    print(login_result)

asyncio.run(main())
```

See [tests](tests) for more examples.

## Setting up the development environment

```bash
# Clone the repo
git clone https://github.com/Wuthery/kuro.py
cd kuro.py

# Install the dependencies
uv sync

# Install pre-commit
pre-commit install
```

## Running tests

1. Create a `.env` file in the root directory of the project and add your test account credentials:
    ```env
    TEST_EMAIL=""
    TEST_PASSWORD=""
    ```
2. Run the tests using pytest:
    ```bash
    pytest
    ```
