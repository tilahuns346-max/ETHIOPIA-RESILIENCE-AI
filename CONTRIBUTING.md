# Contributing to ETHIOPIA RESILIENCE AI

Welcome! Thank you for contributing to Ethiopia's national disaster management platform.

## Development Workflow
1. Fork and clone the repository.
2. Adhere to conventional commit formats:
   - `feat(...)`: New features
   - `fix(...)`: Bug fixes
   - `test(...)`: Unit/integration tests
   - `docs(...)`: Documentation updates
   - `chore(...)`: Routine housekeeping
3. Ensure all tests pass before opening a PR:
   `pytest backend/tests`
4. Safety First: Any changes modifying early warning alert logic must preserve the Human-in-the-Loop invariant (BR-01).

## Code Style
- Python: PEP 8 formatting (Black, Flake8).
- TypeScript: ESLint + Prettier.
- Localized texts: Always provide both English and Amharic strings.
