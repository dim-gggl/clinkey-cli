# Clinkey CLI - Release Notes

## Version 1.2.0 (2025-11-15)

### Overview
This release marks a significant evolution of Clinkey with enhanced security, improved code architecture, comprehensive testing infrastructure, and a refreshed user interface. The project has matured with professional development workflows and CI/CD automation.

---

### 🔒 Security Enhancements

#### Cryptographically Secure Random Generation
- **Breaking Change**: Replaced `random` module with `secrets` module for password generation
  - Ensures cryptographically strong randomness suitable for security-sensitive applications
  - All passwords now generated using `secrets.choice()` instead of `random.choice()`
  - See [clinkey_cli/main.py](clinkey_cli/main.py)

#### Enhanced Input Validation
- Added security constants for safe bounds:
  - `MAX_PASSWORD_LENGTH = 128`: Maximum password length limit
  - `MAX_BATCH_SIZE = 500`: Maximum batch generation limit
  - `MIN_PASSWORD_LENGTH = 16`: Recommended minimum length
  - `SAFE_SEPARATOR_CHARS`: Validated set of printable non-whitespace separators
- Comprehensive input sanitization to prevent edge cases and potential exploits

---

### 🎨 User Interface Improvements

#### New ASCII Art Logo System
- Created dedicated [clinkey_cli/logos.py](clinkey_cli/logos.py) module for visual branding
- Implemented animated logo transitions for interactive mode
- 8 different logo animation frames (`LOGO`, `LOGO1`-`LOGO8`) for dynamic welcome screen
- Improved visual consistency with Rich-powered rendering
- Updated panel borders and color scheme for better terminal aesthetics

#### Enhanced Interactive Experience
- Redesigned welcome screen with animated logo display
- Improved prompts with clearer formatting and visual hierarchy
- Better table rendering for password output
- Consistent color palette throughout the interface

---

### 📝 Code Quality & Documentation

#### Comprehensive Docstrings
- **Full NumPy-style documentation** added to all public APIs:
  - Module-level docstrings with detailed descriptions
  - Class docstrings with complete Attributes and Methods sections
  - Function docstrings with Parameters, Returns, Raises, and Examples sections
- Enhanced code comments throughout core logic
- Improved inline documentation for complex algorithms

#### Code Architecture Improvements
- New [clinkey_cli/const.py](clinkey_cli/const.py) module for security and validation constants
- Cleaner separation of concerns between modules
- Better type hints coverage
- Reduced code duplication through helper methods

---

### 🧪 Testing Infrastructure

#### Complete Test Suite
- **New comprehensive test suite** in `tests/` directory:
  - [tests/test_main.py](tests/test_main.py): Core password generation logic tests
  - [tests/test_cli.py](tests/test_cli.py): CLI interface and integration tests
  - [tests/conftest.py](tests/conftest.py): Shared pytest fixtures
  - [tests/__init__.py](tests/__init__.py): Package initialization

#### Test Configuration
- Added [pytest.ini](pytest.ini) with standard test discovery settings
- Configured coverage tracking in [pyproject.toml](pyproject.toml)
- Test execution options for strict mode and concise output
- Coverage targets: ≥80% overall, ≥95% for core modules

---

### ⚙️ Development Workflow & CI/CD

#### GitHub Actions Workflows
New automated CI/CD pipelines in `.github/workflows/`:

1. **[quality.yml](.github/workflows/quality.yml)**: Code quality checks
   - Black formatting verification
   - isort import ordering
   - Flake8 linting
   - MyPy type checking
   - Pylint static analysis

2. **[tests.yml](.github/workflows/tests.yml)**: Automated testing
   - Pytest execution with coverage reporting
   - Multi-Python version compatibility (3.10, 3.11, 3.12)
   - Coverage threshold enforcement

3. **[security.yml](.github/workflows/security.yml)**: Security scanning
   - Bandit security issue detection
   - Dependency vulnerability scanning
   - Automated security audits

#### Pre-commit Hooks
- Added [.pre-commit-config.yaml](.pre-commit-config.yaml) with comprehensive hooks:
  - File formatting (trailing whitespace, end-of-file fixes)
  - Syntax validation (YAML, JSON, TOML)
  - Code formatting (Black, isort)
  - Linting (Flake8)
  - Type checking (MyPy)
  - Security scanning (Bandit)

---

### 📦 Distribution & Dependencies

#### Homebrew Formula Updates
- Updated [Formula/clinkey-cli.rb](Formula/clinkey-cli.rb) to version 1.2.0
- **Vendored Click and Rich dependencies** for better Homebrew compatibility:
  - Click resource (version 8.1.7) bundled in formula
  - Rich resource (version 14.1.0) bundled in formula
- Lowered Click constraint from `>=8.3.0` to `>=8.1.7` for broader compatibility
- Switched to `virtualenv_install_with_resources` installation method
- Updated SHA256 checksum for new release tarball
- Enhanced installation reliability in Homebrew environments

#### Dependency Management
- Clarified dependency separation in [pyproject.toml](pyproject.toml):
  - **Runtime dependencies**: Click (>=8.3.0), Rich (>=14.1.0)
  - **Development dependencies**: pytest, black, isort, flake8, mypy, pylint, bandit, etc.
  - **Build dependencies**: build package
- Removed build tools from runtime dependencies
- Updated `uv.lock` for dependency resolution

---

### 🔧 Configuration & Tooling

#### Project Configuration Refinements
- Updated [.gitignore](.gitignore) for better coverage and test artifacts exclusion
- Enhanced tool configurations in [pyproject.toml](pyproject.toml):
  - Black: Line length 79, Python 3.10-3.14 targets
  - isort: Black profile, proper first-party package detection
  - MyPy: Python 3.14 compatibility, type checking settings
  - Pylint: 79 character line length, disabled docstring warnings
  - pytest: Verbose mode, strict markers, concise tracebacks
  - Coverage: Source tracking, precision reporting

---

### 🐛 Bug Fixes & Minor Improvements

- Fixed potential security issues with weak random number generation
- Improved error messages with better context and examples
- Enhanced password generation algorithm for better pronounceability
- Added missing syllables to complex syllable sets (`TRY`, `TSY`)
- Better handling of edge cases in batch generation
- Improved file writing robustness

---

### 📊 Project Metrics

**Code Quality Achievements:**
- Test Coverage: Comprehensive suite covering core functionality
- Type Hints: 100% coverage on public APIs
- Documentation: Complete NumPy-style docstrings
- Security: Cryptographically secure random generation
- CI/CD: Full automation with quality gates

**Lines of Code Changes:**
- Core logic improvements: ~150 lines added/modified in [main.py](clinkey_cli/main.py)
- CLI enhancements: ~100 lines added/modified in [cli.py](clinkey_cli/cli.py)
- New modules: ~170 lines in [logos.py](clinkey_cli/logos.py) + [const.py](clinkey_cli/const.py)
- Test suite: ~400+ lines of comprehensive tests
- CI/CD configuration: ~100 lines of workflow definitions

---

### 🔄 Migration Guide

#### For End Users
**No breaking changes for command-line usage.** All existing commands and options work identically:

```bash
# All existing commands continue to work
clinkey                          # Interactive mode
clinkey -l 20 -t strong         # Direct mode
clinkey -l 24 --no-sep -n 5     # Batch generation
```

#### For Developers/API Users
**⚠️ Random Module Change**: If you were using Clinkey programmatically and relied on seeded randomness for testing:

```python
# OLD (no longer works for reproducibility)
import random
random.seed(42)
clinkey = Clinkey()
password = clinkey.generate_password()  # Will be different each time now

# NEW (use secrets for security, mock for testing)
from unittest.mock import patch
clinkey = Clinkey()

# For testing with predictable output
with patch('secrets.choice', side_effect=lambda seq: seq[0]):
    password = clinkey.generate_password()
```

**Recommended**: Update any tests that relied on `random.seed()` to use proper mocking.

---

### 🎯 What's Next

Future considerations for upcoming releases:
- Additional password generation presets
- Internationalization (i18n) support
- Plugin system for custom syllable sets
- Password strength estimation
- Export formats (JSON, CSV)
- Shell completion scripts (bash, zsh, fish)

---

### 🙏 Acknowledgments

Special thanks to the Python community for excellent tools:
- Click team for the elegant CLI framework
- Rich team for beautiful terminal rendering
- pytest team for comprehensive testing tools
- The entire Python security community

---

### 📚 Documentation

- **User Guide**: See [README.md](README.md)
- **Project Instructions**: See [CLAUDE.md](CLAUDE.md)
- **Contributing**: Check `.AGENTS/` directory for development workflows
- **License**: MIT License

---

### 🔗 Links

- **PyPI Package**: https://pypi.org/project/clinkey-cli/
- **GitHub Repository**: https://github.com/dim-gggl/clinkey-cli
- **Homebrew Tap**: `dim-gggl/clinkey-cli/clinkey-cli`
- **Issue Tracker**: https://github.com/dim-gggl/clinkey-cli/issues

---

**Full Changelog**: v1.1.0...v1.2.0
