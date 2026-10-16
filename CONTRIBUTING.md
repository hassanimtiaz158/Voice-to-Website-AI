# Contributing to Voice-to-Website AI

Welcome to the **Voice-to-Website AI** project!

This document defines our Git workflow, branch strategy, commit conventions, pull request (PR) process, code review rules, and collaboration standards. All team members must follow these guidelines to keep the codebase organized, stable, and easy to maintain.

## 1. Project Overview

Voice-to-Website AI is an AI-powered platform that allows users to create and customize websites using voice or text instructions.

The platform aims to include:

- Voice and text input for website generation.
- Speech recognition and LLM-powered code generation.
- An AI coding agent that modifies and validates website code.
- GitHub integration for version control.
- A live website preview.
- A human-assisted production deployment workflow.

Our team has five members. We will collaborate using Git, GitHub branches, pull requests, code reviews, and automated checks.

## 2. Our Branching Strategy

We use three permanent branches and temporary feature branches.

| Branch      | Purpose                                                | Stability          |
| ----------- | ------------------------------------------------------ | ------------------ |
| `main`      | Production-ready code and approved releases.           | Highest            |
| `staging`   | Integration testing and pre-release quality assurance. | High               |
| `dev`       | Integration branch for ongoing development.            | Active development |
| `feature/*` | New functionality developed independently.             | Temporary          |
| `fix/*`     | Bug fixes.                                             | Temporary          |
| `hotfix/*`  | Urgent production fixes.                               | Temporary          |

### `main` — Production Branch

- Contains only approved, stable code.
- Represents the production-ready version of the project.
- No direct pushes are allowed after branch protection is enabled.
- Changes must arrive through a reviewed pull request from `staging`.
- Production deployments must follow the project's release and deployment procedure.

### `staging` — Testing Branch

- Contains code selected for integration testing before release.
- Used to test whether multiple features work together.
- QA checks, integration tests, and manual testing should happen here.
- Only merge changes into `main` after the required checks and approval succeed.
- Avoid adding unfinished features directly to this branch.

### `dev` — Development Integration Branch

- The default base branch for day-to-day development.
- Receives completed features and bug fixes through pull requests.
- The team integrates and tests features here before moving them to `staging`.
- Do not push unfinished work directly to this branch.

### `feature/*` — Feature Branches

Temporary branches for developing new functionality.

Examples:

- `feature/voice-input`
- `feature/ai-code-generation`
- `feature/code-editor`
- `feature/live-preview`
- `feature/github-integration`
- `feature/user-authentication`

Create feature branches from the latest `dev` branch.

### `fix/*` — Bug Fix Branches

Use these branches to fix non-urgent bugs.

Examples:

- `fix/voice-transcription-error`
- `fix/preview-rendering`
- `fix/api-validation`

Create them from `dev` unless the issue specifically requires a different target.

### `hotfix/*` — Urgent Production Fixes

Use these branches only for urgent problems affecting production.

Examples:

- `hotfix/authentication-security`
- `hotfix/production-crash`

For a production hotfix, branch from `main`. After the fix is approved and released, merge or otherwise propagate it into `staging` and `dev` so the problem does not return in future releases.

## 3. Our Development Workflow

The normal development process is:

`feature branch → PR to dev → PR from dev to staging → PR from staging to main`

### Step 1: Get the Latest Development Code

Clone the repository once:

```bash
git clone https://github.com/hassanimtiaz158/Voice-to-Website-AI.git
cd Voice-to-Website-AI
```

For subsequent work, update your local `dev` branch:

```bash
git switch dev
git pull origin dev
```

If you have not cloned the repository yet, use the clone command before running these commands.

### Step 2: Create a New Branch

Always create a separate branch for your task.

```bash
git switch -c feature/voice-input
```

Replace `feature/voice-input` with a short, descriptive name for your task.

The command creates the branch and switches to it.

Before starting work, confirm your current branch:

```bash
git branch --show-current
```

Expected output:

```text
feature/voice-input
```

Do not develop directly on `main`, `staging`, or `dev`.

### Step 3: Make Your Changes

Work only on files related to your assigned task.

Check your changes regularly:

```bash
git status
git diff
```

Before committing, review the changes and ensure you have not included unnecessary files, credentials, local environment files, or unrelated modifications.

### Step 4: Stage and Commit Changes

Stage the files you want to commit:

```bash
git add path/to/file
```

Or, after reviewing all changes:

```bash
git add .
```

Commit your work using the team's commit convention:

```bash
git commit -m "feat: add voice input component"
```

A commit records a snapshot of your changes in Git.

### Step 5: Push Your Branch to GitHub

```bash
git push -u origin feature/voice-input
```

The `-u` option sets the upstream branch, making later pushes easier.

For subsequent updates:

```bash
git push
```

### Step 6: Open a Pull Request

On GitHub:

1. Open the repository.
2. Select **Pull requests**.
3. Click **New pull request**.
4. Select your feature branch as the source.
5. Select `dev` as the target.
6. Add a descriptive title and explain your changes.
7. Link any relevant issue.
8. Submit the pull request for review.

**Important:** The normal target for feature branches is `dev`, not `main` or `staging`.

### Step 7: Review and Merge

- A teammate reviews the code.
- Automated checks must pass.
- The author addresses requested changes.
- At least one other team member approves the PR.
- An authorized maintainer merges it into `dev`.

After the feature is integrated, the temporary branch can be deleted.

### Step 8: Move Code Through Staging and Production

When `dev` contains a suitable group of completed features:

1. Open a PR from `dev` to `staging`.
2. Run integration tests and QA checks.
3. Fix any issues found during testing.
4. Once approved, open a PR from `staging` to `main`.
5. Merge only after the required reviews and checks pass.
6. Deploy according to the approved deployment procedure.

## 4. Commit Message Convention

We use a simplified Conventional Commits style:

```text
type: short description
```

Write commit messages in lowercase where practical, start with an appropriate type, and describe what the commit changes.

| Type       | Purpose                                                    | Example                               |
| ---------- | ---------------------------------------------------------- | ------------------------------------- |
| `feat`     | Add a new feature.                                         | `feat: add voice input component`     |
| `fix`      | Fix a bug.                                                 | `fix: handle empty voice transcripts` |
| `docs`     | Update documentation.                                      | `docs: update setup instructions`     |
| `chore`    | Routine maintenance or project setup.                      | `chore: configure project structure`  |
| `test`     | Add or update tests.                                       | `test: add voice parser tests`        |
| `refactor` | Improve code structure without changing intended behavior. | `refactor: simplify prompt builder`   |
| `style`    | Formatting-only changes.                                   | `style: format frontend components`   |
| `perf`     | Improve performance.                                       | `perf: reduce preview rendering time` |
| `ci`       | Change continuous integration workflows.                   | `ci: add automated test workflow`     |
| `build`    | Change build tools or dependencies.                        | `build: configure frontend build`     |

### Good Commit Messages

```text
feat: add website generation endpoint
fix: handle invalid API responses
docs: add local development guide
chore: add initial repository structure
test: cover prompt validation
```

### Avoid These Messages

```text
changes
update
final
work
new code
fix stuff
```

Each commit should ideally represent one logical change. Smaller, focused commits are easier to review and debug.

## 5. Pull Request Rules

Every pull request should meet these requirements:

- Have a clear title using the commit-style prefixes where appropriate.
- Explain what changed and why.
- Describe how the change was tested.
- Link a related GitHub issue when one exists.
- Include screenshots or a short demonstration for significant UI changes.
- Avoid unrelated changes and unnecessary generated files.
- Ensure relevant tests, linting, and build checks pass.
- Request review from at least one teammate other than the author.

### Suggested PR Title Examples

```text
feat: implement voice input
fix: resolve preview rendering error
docs: document backend setup
chore: configure CI pipeline
```

### Pull Request Checklist

Before requesting review, verify:

- [ ] My branch is based on the latest appropriate base branch.
- [ ] My changes are limited to the intended task.
- [ ] I have reviewed my own diff.
- [ ] Relevant tests pass.
- [ ] The application builds successfully when applicable.
- [ ] I have not committed secrets or personal environment files.
- [ ] Documentation has been updated where necessary.
- [ ] I have explained the changes and testing steps in the PR.

## 6. Code Review Rules

Reviewers should check:

- Correctness and expected behavior.
- Readability and maintainability.
- Security and validation of user input.
- Error handling and useful error messages.
- Appropriate tests and documentation.
- Unnecessary complexity, duplication, and unrelated changes.

Reviewers should explain requested changes clearly and respectfully.

The author should address feedback and request another review when necessary. Do not approve your own PR as a substitute for an independent review.

## 7. Keeping Your Branch Updated

If `dev` receives new changes while you are working:

```bash
git fetch origin
git switch dev
git pull origin dev
git switch feature/voice-input
git merge dev
```

Resolve any conflicts, run the relevant tests, and then push your updated feature branch:

```bash
git push
```

If your team prefers rebasing, use it consistently and only when you understand the implications. Do not force-push shared branches.

## 8. Resolving Merge Conflicts

When Git reports a conflict:

1. Open each conflicted file.
2. Find conflict markers such as `<<<<<<<`, `=======`, and `>>>>>>>`.
3. Decide which changes should be kept and combine them correctly.
4. Remove the conflict markers.
5. Run tests and inspect the resulting changes.
6. Stage the resolved files.
7. Complete the merge commit if Git requests it.

Commands:

```bash
git status
git add path/to/resolved-file
git commit
git push
```

Do not resolve conflicts by blindly accepting all changes from one side. If the intended behavior is unclear, coordinate with the teammate who wrote the affected code.

## 9. Git Safety Rules

- Never commit API keys, passwords, tokens, private keys, or production credentials.
- Keep `.env` and other local secret files out of version control.
- Provide `.env.example` containing placeholder values for required configuration.
- Add dependencies through the appropriate package manager and commit the relevant dependency manifests and lockfiles.
- Never use `git push --force` on shared or protected branches.
- Do not delete or rewrite shared branch history without explicit maintainer approval.
- Avoid committing large generated files, build output, local caches, or virtual environments unless the project specifically requires them.
- Use `.gitignore` for operating-system files, IDE files, build artifacts, local environments, and other unnecessary files.
- Never merge code you have not reviewed or tested to the best of your ability.

If a secret is accidentally committed, removing it from the latest commit alone may not be enough. Revoke or rotate the exposed credential immediately and notify the maintainer.

## 10. Testing and Quality Standards

Before opening a PR:

- Run the tests relevant to your changes.
- Run the project's configured linting and formatting tools.
- Verify that the application builds when applicable.
- Test error cases, not just successful scenarios.
- Document any known limitations or manual testing that remains.

As the project grows, we should add automated checks for:

- Backend tests.
- Frontend linting and build validation.
- API validation and integration tests.
- AI generation and error-handling behavior.
- Security-sensitive operations.
- Deployment and configuration checks.

Use the actual commands documented in the relevant frontend or backend directory. Do not assume a test command exists until it has been configured.

## 11. Team Collaboration

For our five-person team:

- Each member should own clearly assigned tasks.
- Use GitHub Issues to track features, bugs, and technical tasks.
- Assign an issue before starting substantial work when practical.
- Avoid two members independently modifying the same component without coordination.
- Communicate changes to shared interfaces, API contracts, and database schemas.
- Ask for help early when blocked.
- Update the relevant issue or PR with progress and remaining work.
- Share knowledge so that important parts of the system are not understood by only one member.

A suggested task lifecycle is:

`Issue → Assignment → Branch → Implementation → Tests → PR → Review → Merge`

## 12. Initial Repository Setup

Because the repository starts with an empty project structure, initialize it with a tracked file before pushing branches.

Create `README.md` and `CONTRIBUTING.md`, then run:

```bash
git add README.md CONTRIBUTING.md
git commit -m "docs: add project and contribution guides"
git branch -M main
git push -u origin main
```

If `origin/main` already contains commits, inspect the remote before renaming or pushing; coordinate with the repository owner to avoid overwriting or diverging from existing history.

Next, create the permanent branches:

```bash
git switch -c dev
git push -u origin dev

git switch -c staging
git push -u origin staging

git switch dev
```

If a branch already exists locally or remotely, inspect its status rather than recreating it blindly.

After creating the branches, configure GitHub branch protection or rulesets for `main`, `staging`, and `dev` as appropriate.

Recommended protections:

- Require pull requests before merging.
- Require at least one approval from another team member.
- Require relevant CI checks when available.
- Require conversations to be resolved before merging.
- Prevent force pushes and branch deletion.
- Restrict who can merge into production where practical.

Repository administrators should configure these rules according to the team's GitHub plan and repository settings.


## 14. Final Rule

**Never push feature work directly to `main`.**

Use feature branches and pull requests, keep changes focused, review teammates' code, protect secrets, and test before merging. The purpose of this workflow is to make collaboration safer, improve code quality, and maintain a reliable project as Voice-to-Website AI grows.

Thank you for contributing to Voice-to-Website AI!
