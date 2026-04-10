# Contributing

## Git Flow & Branching Strategy

We protect the `main` branch by requiring all code to go through feature branches and pull requests. This ensures:
- No untested code reaches production
- Code is reviewed before merging
- Multiple team members can work in parallel
- Easy rollback if needed

**Branch structure:**
- `main` — Production code (protected)
- `develop` — Integration branch
- `feature/US-XX-*` — Feature branches
- `fix/*` — Bug fix branches

## Using GitHub Desktop (Recommended)

GitHub Desktop makes branching and PR management easy:

### Step 1: Clone the Repository
1. Open GitHub Desktop
2. Click **File** → **Clone Repository**
3. Select the repository
4. Click **Clone**

### Step 2: Create Feature Branch
1. Click **Current Branch** tab
2. Click **New Branch**
3. Name: `feature/US-XX-description`
4. Base branch: `develop`
5. Click **Create Branch**
6. Click **Publish branch**

### Step 3: Make Changes
1. Edit files in your editor
2. GitHub Desktop shows changes automatically
3. Write clear commit message: `feat(scope): description`
4. Click **Commit to feature/US-XX-...**
5. Click **Push origin** button

### Step 4: Create Pull Request
1. Click **Create Pull Request**
2. GitHub opens browser with PR form
3. Add description: `Closes #XX`
4. Request reviewers
5. Click **Create Pull Request**

### Step 5: Code Review
1. Team member reviews code on GitHub
2. Address feedback with new commits
3. Push additional commits
4. After approval, click **Squash and merge** on GitHub

### Step 6: Update Local Repository
1. Switch to `develop` branch in GitHub Desktop
2. Click **Fetch origin**
3. Click **Pull origin**

## Using Git Commands (Alternative)

If you prefer command line:

```bash
# Setup
git clone https://github.com/abderrahmen-bchini/bank-chat-bot-.git
cd bank-chat-bot-

# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/US-XX-short-description

# Make changes, then commit
git add .
git commit -m "feat(scope): description"

# Push branch
git push origin feature/US-XX-short-description

# Create PR on GitHub website
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 16+ (for frontend)
- GitHub Desktop (recommended) or Git CLI

### Setup

```bash
git clone https://github.com/abderrahmen-bchini/bank-chat-bot-.git
cd bank-chat-bot-

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend (new terminal)
cd frontend
npm install
```

## Development

### Backend

```bash
cd backend
python -m uvicorn api.main:app --reload
```

### Frontend

```bash
cd frontend
npm start
```

### Tests

```bash
pytest tests/
npm test  # (frontend/)
```

## Commit Convention

```
feat(scope): description
fix(scope): description
docs: description
test(scope): description
refactor: description
chore: description
```

**Examples:**
```
feat(ingestion): add PDF text extraction
fix(api): resolve authentication timeout
docs(readme): add setup instructions
test(retrieval): add search tests
```

## Pull Request Guidelines

1. Create feature branch from `develop`
2. Implement changes with tests
3. Commit with clear messages
4. Push to origin
5. Create PR on GitHub
6. Link issue: `Closes #XX`
7. Request team member review
8. Address feedback
9. After approval: squash and merge

## Code Standards

- Write clean, readable code
- Add docstrings to functions and classes
- Keep functions focused (<50 lines)
- Comment complex logic only
- Follow PEP 8 (Python), ESLint (JavaScript)

## Testing Requirements

- Write tests for new features
- Run full test suite before PR
- Aim for >80% coverage on new code
- Test edge cases and errors

## Reporting Issues

### Bug Report
- Use bug_report_template.md
- Include steps to reproduce
- Describe expected vs actual behavior
- Add logs/screenshots

### Feature Request
- Use feature_request_template.md
- Explain the use case
- Describe expected behavior
- Suggest implementation (optional)

## Definition of Done

- Code written and tested
- Tests pass
- Code reviewed and approved
- Documentation updated
- PR merged to `develop`
- Tagged with sprint label

---

See [README.md](README.md) for documentation links.
