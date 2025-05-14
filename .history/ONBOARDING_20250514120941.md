<!-- See [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md) for required practices. -->
# Onboarding: Your First PR in 5 Minutes

Welcome to the Home Automation Stack repo! This guide helps you get up and running, and submit your first change, in under 5 minutes.

## 1. Fork & Clone
```powershell
# Fork the repo on GitHub, then clone locally:
git clone https://github.com/<your-username>/home-automation-stack.git
Set-Location 'j:\workspace\Home automation stack'
```

## 2. Create a Branch
Use the branch naming convention:
```powershell
git checkout -b feature/<short-description>
```

## 3. Add In-File Banner
For **every** new file you create, add this as the first line:
```markdown
<!-- See [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md) for required practices. -->
```

## 4. Install CLI Tools
- **Docker & Docker Compose** (Desktop or CLI).
- **Python 3.11** + `pip` for local scripts/tests.
- **Node.js & npm** (for commitlint hooks).
- **Optional:** Create and activate a Python virtual environment for tool isolation:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 5. Set Up Pre-Commit & Linting
### Python
```powershell
pip install pre-commit flake8 black isort
pre-commit install
```
Create `.pre-commit-config.yaml` (if not present) to include your linters.

### Sample `.pre-commit-config.yaml`
```yaml
# Minimal pre-commit configuration
repos:
  - repo: https://github.com/psf/black
    rev: stable
    hooks:
      - id: black
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.3.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
      - id: check-banner
        args: ['--banner', '<!-- See [AI_CODING_BASELINE_RULES.md](./AI_CODING_BASELINE_RULES.md) for required practices. -->']
  - repo: https://gitlab.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

### Commitlint (Conventional Commits)
```powershell
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky
npx husky install
npx husky add .husky/commit-msg "npx --no-install commitlint --edit $1"
```
Create `commitlint.config.js` with:
```js
module.exports = { extends: ['@commitlint/config-conventional'] };
```

## 6. Build & Run the Stack
```powershell
docker-compose \
  -f "docker-compose.ai.yml" \
  -f "docker-compose.home.yml" \
  -f "docker-compose.utils.yml" up -d
```

## 7. Verify Functionality
- Run the full test suite for this workspace (Python and PowerShell):
  ```powershell
  pytest -q
  .\test_ovos_containers.ps1 # optional, if working with OVOS services
  ```
- For any Dockerized service, you can verify by hitting its health endpoint or UI as documented in its setup guide.

## 8. Run Local Checks
- **Banner Check**: Ensure all files start with the banner comment.
- **Linters**: `flake8`, `black --check .`, `isort --check-only .`
- **Tests**: `pytest -q`

## 9. Quick Reference: Top 10 MUSTs
Refer to your quick checklist for core requirements:
1. In-file banner (Section 0)
2. Docker Compose service names for inter-container refs (Section 1)
3. Required ENV vars set in Compose (Section 2)
4. Proper volume mounts and permissions (Section 3)
5. Robust healthchecks, no always-passing checks (Section 4)
6. Pin versions of base images and key dependencies (Section 5)
7. No hardcoded secrets—use Docker secrets or ENV vars (Section 10)
8. Explicit confirmation before destructive actions (Section 9)
9. Adhere to official documentation (Section 9)
10. Document deviations via exception process (Section 28)

## 10. Commit & Push
```powershell
git add .
git commit -m "feat(<scope>): short description of change"
git push -u origin feature/<short-description>
```

## 11. Create a Pull Request
On GitHub, open a PR against `main` and reference relevant issues or docs. A CI baseline job will run to verify compliance.

## 12. Checklist
- [ ] Fork and clone the repository
- [ ] Create a feature branch
- [ ] Add the in-file banner to new files
- [ ] Activate virtual environment and install tools
- [ ] Install and activate pre-commit and commitlint hooks
- [ ] Build and run the full stack
- [ ] Verify functionality using the test suite
- [ ] Run local linting and tests
- [ ] Commit with a Conventional Commit message
- [ ] Open a pull request for review

---
**Congratulations!** You’ve submitted your first PR, enforced baseline rules, and contributed to a stable, secure stack. 🎉
