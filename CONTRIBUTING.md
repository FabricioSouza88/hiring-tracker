# Contribuindo

1. **Branching**: `feat/*`, `fix/*`, `chore/*`.
2. **Commits**: Conventional Commits.
3. **Code style**: Será aplicado (`ruff`, `black`, `mypy`) quando iniciarmos o código.
4. **Migrations**: Para mudanças de schema, crie um novo arquivo SQL incremental em `migrations/sql` e rode o `migrator`.
5. **PRs**: Inclua descrição, screenshots do Streamlit quando aplicável e instruções de teste.
