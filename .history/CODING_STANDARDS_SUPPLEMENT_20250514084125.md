# Coding Standards Supplement

This document implements Section 23 of `AI_CODING_BASELINE_RULES.md`—see that file for context, exceptions, and overall process.

<!-- id: CQM-01, priority: MUST, tags: [code-quality,maintainability], last_reviewed: 2025-05-13 -->
## 23.1 Code Quality, Readability, and Maintainability
- MUST: Write clear, self-documenting code with meaningful identifiers and straightforward control flow.
- MUST: Adhere to language and framework-specific style guides (e.g., PEP 8 for Python) and enforce compliance via linters and formatters.
- SHOULD: Keep functions and methods small, focused on a single responsibility.
- SHOULD: Refactor duplicate or similar code to eliminate repetition and follow the DRY principle.
- SHOULD: Use comments judiciously to explain intent and rationale rather than restate code; include docstrings for public modules, classes, and methods.
- MAY: Provide illustrative code snippets for complex algorithms or patterns to aid understanding.
- MUST: Review and test code for readability and maintainability before merging.

<!-- id: DAP-01, priority: SHOULD, tags: [design,architecture], last_reviewed: 2025-05-13 -->
## 23.2 Design and Architecture Principles
- MUST: Design components to be modular with single responsibilities (SRP).
- SHOULD: Promote code reuse and reduce coupling through abstraction and interfaces (DIP, ISP).
- SHOULD: Design for extensibility (OCP) allowing new functionality with minimal changes.
- SHOULD: Implement and document design patterns (Factory, Observer, Strategy, Decorator) with rationale.
- SHOULD: Follow SOLID principles for flexible, maintainable design.
- SHOULD: Employ dependency injection to provide components with dependencies externally.

<!-- id: EH-01, priority: MUST, tags: [error-handling,robustness], last_reviewed: 2025-05-13 -->
## 23.3 Error Handling and Robustness
- MUST: Implement comprehensive error handling using language-appropriate constructs to catch and manage exceptions.
- MUST: Define and use custom exception types for application-specific error conditions.
- MUST: Log all exceptions and significant error states with sufficient context (stack trace, parameters).
- MUST: Rigorously validate all external inputs at component boundaries to prevent errors and vulnerabilities.

<!-- id: PERF-01, priority: SHOULD, tags: [performance,scalability], last_reviewed: 2025-05-13 -->
## 23.4 Performance and Scalability
- SHOULD: Choose efficient algorithms and data structures appropriate for task and data sizes.
- SHOULD: Utilize appropriate concurrency mechanisms (asyncio, threading, multiprocessing) for parallelism.
- SHOULD: Profile code to identify bottlenecks before optimizing critical paths.
- MUST: Manage system resources efficiently, ensuring proper cleanup of resources (context managers, finally blocks).
- SHOULD: Establish and rerun performance benchmarks after significant changes.

<!-- id: QA-01, priority: SHOULD, tags: [testing,qa], last_reviewed: 2025-05-13 -->
## 23.5 Testing and Quality Assurance
- MUST: Implement comprehensive unit tests covering new and modified code.
- MUST: Write integration tests for interactions between components or services.
- SHOULD: Aim for high test coverage of business logic and critical paths.
- MUST: Structure code to be easily testable (SRP, DI, limited global state).

<!-- id: SBP-01, priority: MUST, tags: [security], last_reviewed: 2025-05-13 -->
## 23.6 Security Best Practices
- MUST: Validate and sanitize all inputs from untrusted sources to prevent injection and traversal attacks.
- MUST: Enforce the principle of least privilege for processes and services.
- MUST: Regularly scan and update dependencies to patch known vulnerabilities.
- MUST: Protect sensitive data with encryption at rest and in transit, and avoid logging sensitive information.

<!-- id: CICD-02, priority: SHOULD, tags: [cicd,automation], last_reviewed: 2025-05-13 -->
## 23.7 CI/CD (Continuous Integration & Continuous Deployment)
- SHOULD: Automate build, test, and deployment processes through CI/CD pipelines.
- SHOULD: Maintain consistency between development, testing, and production environments.
- SHOULD: Integrate containerization and declarative configs to reduce environment drift.

<!-- id: PY-01, priority: SHOULD, tags: [python], last_reviewed: 2025-05-13 -->
## 23.8 Python-Specific Development Guidelines
- MUST: Adhere to PEP 8 style guide for Python code formatting.
- SHOULD: Use type hints for function arguments and return values where they improve clarity.
- MUST: Include docstrings for all public modules, classes, functions, and methods.
- SHOULD: Use linters (Flake8, Pylint) and formatters (Black, isort) via pre-commit hooks.
- SHOULD: Leverage Pythonic idioms (list comprehensions, context managers).
- SHOULD: Use Abstract Base Classes and decorators for interfaces and cross-cutting concerns.
- MUST: Catch specific exceptions and ensure resource cleanup with context managers.
- SHOULD: Utilize asyncio for I/O-bound concurrency and multiprocessing for CPU-bound tasks.
- SHOULD: Write tests with pytest or unittest, using mocking and measuring coverage.
- MUST: Isolate dependencies in virtual environments and pin versions in requirements.txt.
- SHOULD: Avoid unsafe use of pickle and sanitize inputs in web contexts.
