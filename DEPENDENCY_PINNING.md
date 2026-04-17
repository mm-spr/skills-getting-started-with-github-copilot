# Dependency Pinning Policy

## Overview
This project enforces pinned dependencies for all builds and CI/CD pipelines to ensure reproducible, secure, and predictable builds. All dependencies must be locked to specific versions to prevent unexpected breaking changes or security vulnerabilities.

## Python Dependencies

### Policy
- All Python packages in `requirements.txt` must use exact version pinning with the `==` operator
- Versions must be at least 3 days old unless explicitly required for security patches or critical bugfixes
- Example: `fastapi==0.104.1` (not `fastapi>=0.100.0` or unpinned `fastapi`)

### Current Dependencies (Pinned)
```
fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.2
watchfiles==0.20.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

### Installation
Always install dependencies with pinned versions to prevent accidental updates:
```bash
pip install -r requirements.txt
```

### Updating Dependencies
When updating dependencies:
1. Update versions in `requirements.txt` using exact pinning (`==`)
2. Verify the version is at least 3 days old (check PyPI release history)
3. Test thoroughly in development before committing
4. Update `requirements.txt` and run tests in CI/CD before merging

Example update process:
```bash
# Check version release dates on PyPI
# Update requirements.txt with new pinned version
pip install -r requirements.txt
# Run tests to verify compatibility
pytest
```

## GitHub Actions

### Policy
- All GitHub Actions must use pinned versions
- Use specific semantic versions (major.minor.patch format preferred)
- Never use branch names like `main` or tags like `latest`
- For official GitHub actions, major version pinning (e.g., `@v6`) is acceptable as GitHub maintains backward compatibility

### Current Actions (Pinned)

**Official GitHub Actions:**
- `actions/checkout@v6` - Pinned to major version (GitHub maintains compatibility)
- `actions/github-script@v7` - Pinned to major version

**Community Actions:**
- `GrantBirki/comment@v2.1.1` - Pinned to specific patch version (recommended)
- `peter-evans/find-comment@v3` - Pinned to major version
- `tj-actions/changed-files@v47` - Pinned to specific patch version
- `skills/action-keyphrase-checker@v1` - Pinned to major version
- `skills/exercise-toolkit/.github/workflows/*@v0.8.1` - Pinned to specific patch version

### Best Practices
1. **Always specify versions explicitly** - Never use `@latest` or branch names
2. **For official GitHub actions** - Use major version (e.g., `@v6`) for automatic maintenance updates within the major version
3. **For community/third-party actions** - Use specific patch versions (e.g., `@v2.1.1`) for maximum stability
4. **Review updates carefully** - Test new action versions in development before updating in production workflows

### Updating Actions
When updating GitHub Actions:
1. Review the changelog/release notes
2. Update the version reference in the workflow file
3. Test the workflow in a non-production branch
4. Verify all checks pass before merging to main

Example:
```yaml
- name: Checkout
  uses: actions/checkout@v6  # Pinned version
```

## CI/CD Considerations

### Build Reproducibility
- All builds must use pinned dependencies
- The CI/CD pipeline enforces this by using `pip install -r requirements.txt` (not `pip install --upgrade`)
- This ensures every build produces identical results

### Security Patches
- Pinned dependencies should be reviewed and updated regularly (weekly/monthly)
- Security patches should be prioritized and applied immediately
- Urgent security fixes can bypass the 3-day-old requirement

### Automation
Consider automating dependency updates with:
- **Dependabot** - GitHub's native dependency update automation
- **Renovate** - Advanced dependency management tool
- **pip-audit** - Scan dependencies for known vulnerabilities

Example Dependabot configuration would check for outdated pins and create PRs.

## Verification

### Check Python Dependencies
```bash
# Verify all dependencies are pinned
grep -E '^[a-zA-Z0-9_-]+==' requirements.txt
```

### Check GitHub Actions
```bash
# Verify no unpinned actions (no @latest or @main)
grep -r "uses: .*@latest\|uses: .*@main" .github/workflows/
# Should return no results
```

## References
- [PyPI Best Practices](https://packaging.python.org/tutorials/installing-packages/)
- [GitHub Actions - Action Versioning](https://docs.github.com/en/actions/creating-actions/about-actions#using-release-management-for-actions)
- [OWASP - Dependency Management](https://owasp.org/www-community/attacks/Dependency_and_System_Library_Hijacking)
