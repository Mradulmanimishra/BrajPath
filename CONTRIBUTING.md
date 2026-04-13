# Contributing to BrajPath

🙏 **Radhe Radhe!** Thank you for your interest in contributing to BrajPath.

## How to Contribute

1. **Fork** the repository.
2. **Clone** your fork locally.
3. **Create a branch** for your feature or bugfix.
4. **Develop**:
   - Ensure you use `uv` for dependency management.
   - Run `pytest` before submitting.
5. **Submit a Pull Request** with a clear description of your changes.

## Code Standards
- We use **Ruff** for linting.
- Follow the **Registry-based Handler Pattern** in `app/services/state_machine.py`.
- Document new service functions in `app/services/temple_service.py`.

## Local Setup
```bash
uv sync
uv run python -m scripts.run_seed
uv run pytest
```
