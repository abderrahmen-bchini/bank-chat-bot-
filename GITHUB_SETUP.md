# GitHub Setup & Configuration

## Branching Strategy - Git Flow

We use **Git Flow** to prevent direct pushes to `main` and ensure code quality:

```
main              ← Production-ready code (protected, requires PR)
develop           ← Integration branch (default, requires PR)
feature/US-XX-*   ← Feature branches (one per user story)
fix/*             ← Bug fix branches
```

**Why this approach?**
- Protects `main` from untested code
- All code reviewed before merging
- Clear separation between development and production
- Enables parallel work on multiple features
- Easy to track which code is deployed

## Using GitHub Desktop

We use **GitHub Desktop** for easier branch management:

### Creating a Feature Branch

1. Open GitHub Desktop
2. Click **Current Branch** → **New Branch**
3. Name: `feature/US-XX-short-description`
4. Choose **develop** as the base branch
5. Click **Create Branch**
6. Click **Publish branch**

### Making Changes

1. Make your code changes locally
2. GitHub Desktop shows modified files
3. Write commit message: `feat(scope): description`
4. Click **Commit to feature/US-XX-...**
5. Click **Push origin**

### Creating a Pull Request

1. After pushing, click **Create Pull Request**
2. GitHub opens your browser
3. Write PR description
4. Add reviewers
5. Submit PR
6. Team member reviews and approves
7. Click **Squash and merge** on GitHub

### Pulling Latest Changes

1. Click **Current Branch**
2. Select `develop`
3. Click **Fetch origin**
4. Click **Pull origin** to get latest code

### Why GitHub Desktop?

- Visual branch management (no terminal needed)
- Easy push/pull operations
- Clear file change visualization
- Straightforward PR workflow
- Perfect for team collaboration

---

## Step 1: Git Setup

```bash
cd bank-chat-bot-

git config user.email "your-email@example.com"
git config user.name "Your Name"

git checkout -b develop
git add .
git commit -m "chore: set up repo structure, README, templates, and gitignore"
git push origin develop
git push origin main
```

(If using GitHub Desktop, you can skip these commands - GitHub Desktop handles all this)

## Step 2: Repository Settings

Navigate to **Settings** and configure:

### Default Branch
- Go to **Branches**
- Set `develop` as the default branch

### Branch Protection Rules
- Rule for `main` branch:
  - Require a pull request before merging
  - Require at least 1 approval
  - Require status checks to pass
  - Require branches to be up to date before merging

- Rule for `develop` branch:
  - Require a pull request before merging
  - Require at least 1 approval

### Collaborators
- Go to **Collaborators & teams**
- Add team members with appropriate roles

## Step 3: Create Labels

Go to **Issues** → **Labels** and create the following labels:

### Epic Labels
- **epic** — Epic user story group (color: #0366d6 - blue)
- **epic: infrastructure** (color: #1f6feb)
- **epic: ingestion** (color: #1f6feb)
- **epic: rag** (color: #1f6feb)
- **epic: auth** (color: #1f6feb)
- **epic: ui** (color: #1f6feb)

### Status Labels
- **status: backlog** (color: #cfcfcf - gray)
- **status: in-progress** (color: #fbca04 - yellow)
- **status: blocked** (color: #ee0701 - red)
- **status: in-review** (color: #0075ca - blue)
- **status: done** (color: #28a745 - green)

### Sprint Labels
- **sprint-1** (color: #a2eeef)
- **sprint-2** (color: #a2eeef)
- **sprint-3** (color: #a2eeef)
- **sprint-4** (color: #a2eeef)
- **sprint-5** (color: #a2eeef)

### Type Labels
- **type: user-story** (color: #7057ff - purple)
- **type: bug** (color: #d73a49 - red)
- **type: enhancement** (color: #a2eeef - cyan)
- **type: documentation** (color: #0075ca - blue)
- **type: chore** (color: #ffc274 - orange)

### Priority Labels
- **priority: high** (color: #d73a49 - red)
- **priority: medium** (color: #fbca04 - yellow)
- **priority: low** (color: #0075ca - blue)

---

## 📋 Step 4: Create GitHub Issues

Go to **Issues** → **New Issue** and create one issue per user story:

### Sprint 1 (Epic 1 - Done)
- [ ] US-01: GitHub repo with branching strategy
- [ ] US-02: Notion documentation pipeline
- [ ] US-03: Defined system architecture

**Labels for each**: `sprint-1`, `type: user-story`, `epic: infrastructure`, `status: done`

### Sprint 2 (Epic 2 - Current)
- [ ] US-04: Upload PDF/DOCX/TXT files
- [ ] US-05: Extract and clean text
- [ ] US-06: Split documents into chunks
- [ ] US-07: Generate embeddings
- [ ] US-08: Store embeddings in Qdrant

**Labels for each**: `sprint-2`, `type: user-story`, `epic: ingestion`, `status: backlog`
(Mark US-04 as `status: in-progress`)

### Sprint 3 (Epic 3 - Planned)
- [ ] US-09: Natural language Q&A
- [ ] US-10: Embed query and search
- [ ] US-11: Inject context into LLM
- [ ] US-12: Hallucination check
- [ ] US-13: Source citation

**Labels for each**: `sprint-3`, `type: user-story`, `epic: rag`, `status: backlog`

### Sprint 4 (Epic 4 - Planned)
- [ ] US-14: User login
- [ ] US-15: Role-based access
- [ ] US-16: Query logging
- [ ] US-17: On-premise deployment

**Labels for each**: `sprint-4`, `type: user-story`, `epic: auth`, `status: backlog`

### Sprint 5 (Epic 5 - Planned)
- [ ] US-18: Web interface
- [ ] US-19: Admin panel
- [ ] US-20: One-command deployment
- [ ] US-21: Performance testing

**Labels for each**: `sprint-5`, `type: user-story`, `epic: ui`, `status: backlog`

---

## 🎨 Step 5: Set Up GitHub Projects (Kanban Board)

1. Go to **Projects** tab
2. Click **New Project**
3. Select **Board** view
4. Name: "Sprint 2 Board" (or "Backlog")
5. Create columns:
   - 📋 Backlog
   - 🚀 Sprint Planned
   - 🔄 In Progress
   - 👀 In Review
   - ✅ Done

6. Add issues to the board:
   - Drag Sprint 2 issues from Backlog → Sprint Planned
   - Move US-04 → In Progress

---

## 📚 Step 6: Documentation

### Update README Team Section
Edit `README.md` and fill in:
```markdown
| **Project Lead** | [Your Name] | [your-email@example.com] |
| **Backend Lead** | [Name] | [email] |
| **Frontend Lead** | [Name] | [email] |
| **DevOps/Infra** | [Name] | [email] |
| **Supervisor** | [Name] | [email] |

**University**: [Your University]
**Department**: Software Engineering
**Capstone Period**: [Start Date] - [End Date]
```

### Create Docs Directory Structure
```bash
mkdir -p docs/diagrams
# docs/ARCHITECTURE.md (already created)
# docs/API.md (already created)
```

---

## 🔗 Step 7: Configure Webhooks (Optional)

For Notion/Discord notifications on issue updates:

1. Go to **Settings** → **Webhooks**
2. Add Notion or Discord webhook URL
3. Select events: Issues, Pull Requests
4. Activate

---

## ✅ Step 8: Verification Checklist

- [ ] `main` branch exists and is protected
- [ ] `develop` branch exists and is default
- [ ] `.gitignore` is in place
- [ ] README.md updated with full documentation
- [ ] `.github/` templates in place
- [ ] `docker-compose.yml` configured
- [ ] `.env.example` created
- [ ] All 21 issues created in GitHub
- [ ] Labels created (35+)
- [ ] Project board set up
- [ ] CONTRIBUTING.md explains workflow
- [ ] ARCHITECTURE.md documents design
- [ ] BACKLOG.md lists all user stories
- [ ] Branch protection rules enabled
- [ ] Team members added as collaborators

---

## 🚀 First Feature Branch

Ready to start Sprint 2? Create your first feature branch:

```bash
# Make sure you're on develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/US-04-pdf-upload

# Make your changes...
# git add, git commit, git push

# Create Pull Request on GitHub with:
# Title: [US-04] Add PDF file upload endpoint
# Description: Closes #XX (issue number)
# Reviewers: @team-member
```

---

## 📞 Support & Questions

- 📖 Review `CONTRIBUTING.md` for dev guidelines
- 🏗️ Review `ARCHITECTURE.md` for system design
- 📋 Check `BACKLOG.md` for story details
- 💬 Ask in GitHub Discussions or Notion

---

**Congratulations! Your GitHub is now professionally configured! 🎉**

Next: Start working on Sprint 2 (US-04: PDF Upload)
