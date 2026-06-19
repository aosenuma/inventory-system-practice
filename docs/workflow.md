# GitHub Workflow Guide

This guide explains how to collaborate on the Inventory System Practice project using Git and GitHub.

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, production-ready code |
| `develop` | Integration branch where features are merged |
| `feature/<name>` | New features or enhancements |
| `fix/<name>` | Bug fixes |
| `docs/<name>` | Documentation changes |

## Step-by-Step Workflow

### 1. Create an Issue

Before starting work, create a GitHub issue describing:

- What you want to accomplish
- Why it is needed
- Acceptance criteria (how to know it is done)

### 2. Create a Branch from `develop`

```bash
# Make sure develop is up to date
git checkout develop
git pull origin develop

# Create and switch to your feature branch
git checkout -b feature/add-product-export
```

Use a descriptive branch name that reflects the task.

### 3. Make Changes and Commit

Work on your changes, then stage and commit:

```bash
git add .
git commit -m "feat: add CSV export for products"
```

#### Commit Message Convention

| Prefix | Use for |
|--------|---------|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `docs:` | Documentation only |
| `refactor:` | Code changes that don't add features or fix bugs |
| `style:` | Formatting, whitespace |
| `test:` | Adding or updating tests |

Examples:

```
feat: add low stock email alert
fix: prevent negative stock values
docs: update API endpoint list
```

### 4. Push Your Branch

```bash
git push -u origin feature/add-product-export
```

### 5. Open a Pull Request

1. Go to the repository on GitHub
2. Click **"Compare & pull request"** (or **"New pull request"**)
3. Set the base branch to `develop`
4. Set the compare branch to your feature branch
5. Fill in the PR title and description:
   - What changed
   - Why it changed
   - How to test it
6. Link the related issue (e.g., "Closes #12")
7. Request review from a teammate

### 6. Code Review

- Reviewers leave comments on the PR
- Address feedback with new commits on the same branch
- Push updates: `git push`
- The PR updates automatically

### 7. Merge

Once approved and CI passes (if configured), merge the PR into `develop`.

### 8. Stay Updated with `develop`

While working on a long-running branch, sync with `develop` regularly:

```bash
git checkout develop
git pull origin develop
git checkout feature/your-branch
git merge develop
```

Or use rebase (optional, for cleaner history):

```bash
git checkout feature/your-branch
git rebase develop
```

## Resolving Merge Conflicts

Conflicts happen when two branches modify the same lines of code.

### Steps

1. Update your branch with the latest `develop`:
   ```bash
   git checkout feature/your-branch
   git merge develop
   ```

2. Git will show which files have conflicts. Open them and look for markers:
   ```
   <<<<<<< HEAD
   your changes
   =======
   changes from develop
   >>>>>>> develop
   ```

3. Edit the file to keep the correct code (or combine both changes)

4. Remove the conflict markers

5. Stage and commit:
   ```bash
   git add .
   git commit -m "fix: resolve merge conflict in products route"
   ```

6. Push your branch:
   ```bash
   git push
   ```

### Tips

- Communicate with teammates if you are editing the same files
- Keep PRs small and focused — easier to review and fewer conflicts
- Pull from `develop` often

## Example Full Workflow

```bash
# Start
git checkout develop
git pull origin develop
git checkout -b feature/add-search-autocomplete

# Work and commit
git add app/routes/pages.py templates/products/index.html
git commit -m "feat: add search autocomplete for products"

# Push and create PR on GitHub
git push -u origin feature/add-search-autocomplete

# After PR is merged, clean up
git checkout develop
git pull origin develop
git branch -d feature/add-search-autocomplete
```
