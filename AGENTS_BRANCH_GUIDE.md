# Agents Systems Codebase Branch

## Overview

A new Git branch called `agents-systems-only` has been created that contains **only** the core agent systems code from this repository, along with comprehensive documentation on how to run and test each system.

## What's in the New Branch?

The `agents-systems-only` branch contains:

### 📁 Agent Systems
1. **Deep Research System** (`1_deep_research/deep_research/`)
   - Multi-agent research system using LangGraph
   - Planner, Search, Writer, and Push agents
   - Gradio web interface

2. **Engineering Team** (`2_engineering_team/engineering_team/`)
   - CrewAI-based software development team
   - Engineering Lead, Backend Engineer, Frontend Engineer, Test Engineer
   - YAML-based configuration

3. **Trading Floor** (`3_trading_floor/`)
   - AI trading system with autonomous agents
   - Multiple trader personalities (Warren, George, Ray, Cathie)
   - MCP servers for market data and account management
   - Web interface for monitoring

### 📚 Documentation
- **README.md** - Comprehensive guide covering all systems
- **QUICKSTART.md** - 5-minute quick start guide
- **TESTING.md** - Detailed testing strategies and examples
- **ARCHITECTURE.md** - In-depth architecture and design patterns

### 🔧 Configuration
- **pyproject.toml** - All Python dependencies
- **.gitignore** - Proper exclusions
- **.python-version** - Python version specification
- **LICENSE** - Original license preserved

## How to Access the Branch

### Option 1: Clone Only the Agents Branch

```bash
# Clone the repository with only the agents-systems-only branch
git clone --single-branch --branch agents-systems-only https://github.com/tywade1980/action.git agents-codebase
cd agents-codebase
```

### Option 2: Checkout from Existing Clone

```bash
# If you already have the repository
cd action
git fetch origin
git checkout agents-systems-only
```

### Option 3: View on GitHub

Navigate to: `https://github.com/tywade1980/action/tree/agents-systems-only`

## What's Removed?

The following items from the main branch are **NOT** included in the agents-systems-only branch:
- Lab notebooks (moved to separate notebooks if needed)
- Workshop materials
- Setup guides for the workshop
- Assets and images
- Output examples
- Troubleshooting notebooks

This keeps the branch focused purely on the **runnable agent systems code** and **documentation**.

## Quick Start (Once on the Branch)

After checking out the `agents-systems-only` branch:

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
uv sync

# 3. Set up API keys
echo "OPENAI_API_KEY=your_key_here" > .env

# 4. Run a system
cd 1_deep_research/deep_research
uv run python deep_research.py
```

See **QUICKSTART.md** in the branch for more details.

## Documentation Overview

### README.md
- Complete overview of all three agent systems
- Prerequisites and installation instructions
- Detailed "How to Run" sections for each system
- Comprehensive "How to Test" sections with examples
- Architecture patterns explanation
- Troubleshooting guide

### QUICKSTART.md
- 5-minute quick start guide
- Minimal setup instructions
- Simple commands to run each system
- Basic testing examples
- Common issues and solutions

### TESTING.md
- Unit testing strategies
- Integration testing examples
- End-to-end test scenarios
- Performance testing guidelines
- Manual testing checklists
- Debugging and troubleshooting

### ARCHITECTURE.md
- Detailed architecture explanations for each system
- Design patterns used
- Component diagrams
- Communication patterns
- Technology stack details
- Security considerations
- Future enhancement ideas

## Running Each System

### 1. Deep Research System
```bash
cd 1_deep_research/deep_research
uv run python deep_research.py
# Opens web interface at http://localhost:7860
```

### 2. Engineering Team
```bash
cd 2_engineering_team/engineering_team
uv tool install crewai
uv run crewai run
# Follow prompts to specify development task
```

### 3. Trading Floor
```bash
# Terminal 1: Market Server
cd 3_trading_floor
uv run python market_server.py

# Terminal 2: Accounts Server
uv run python accounts_server.py

# Terminal 3: Trading Floor
uv run python trading_floor.py

# Terminal 4: Web Interface (optional)
uv run python app.py
# Opens at http://localhost:7860
```

## Testing Examples

### Deep Research
```bash
cd 1_deep_research/deep_research
uv run python -c "
from research_manager import ResearchManager
import asyncio

async def test():
    manager = ResearchManager()
    result = []
    async for chunk in manager.run('What is AI?'):
        result.append(chunk)
    print('Test passed:', len(''.join(result)), 'chars')

asyncio.run(test())
"
```

### Engineering Team
```bash
cd 2_engineering_team/engineering_team
uv run crewai run
# Enter test task: "Create a hello world function with tests"
# Check output/ directory
```

### Trading Floor
```bash
cd 3_trading_floor
uv run python -c "from database import Database; db = Database(); print('OK')"
uv run python -c "from market import is_market_open; print(is_market_open())"
uv run python -c "from accounts import read_account; print(read_account('Warren')[:50])"
```

## Why a Separate Branch?

This separate branch provides:

1. **Clean Codebase** - Only production-ready agent systems
2. **Easy Distribution** - Share just the code without workshop materials
3. **Clear Documentation** - Focused docs for running the systems
4. **Easy Deployment** - Ready to clone and run
5. **Version Control** - Track agent code separately from workshop content

## Branch Maintenance

The `agents-systems-only` branch is:
- Independent (orphan branch with no shared history)
- Self-contained (all dependencies included)
- Documented (comprehensive guides included)
- Runnable (all systems tested and working)

To update the branch with new features:
```bash
# Make changes on a feature branch
git checkout -b feature/new-agent agents-systems-only
# ... make changes ...
git commit -m "Add new agent feature"
git push origin feature/new-agent
# Create PR to merge into agents-systems-only
```

## Getting Help

If you're on the `agents-systems-only` branch:

1. Read **QUICKSTART.md** for immediate help
2. Check **README.md** for detailed instructions
3. Consult **TESTING.md** if tests are failing
4. Review **ARCHITECTURE.md** to understand the design

For issues or questions:
- Check the documentation in the branch
- Review code comments
- Experiment with the examples
- Refer to framework documentation (LangGraph, CrewAI, OpenAI Agents)

## Summary

The `agents-systems-only` branch provides:

✅ **Three complete agent systems** ready to run  
✅ **Comprehensive documentation** for setup, running, and testing  
✅ **Clean codebase** without workshop materials  
✅ **Clear instructions** for each system  
✅ **Testing strategies** with examples  
✅ **Architecture documentation** explaining design decisions  

To get started: **checkout the branch** and open **QUICKSTART.md**!

---

**Branch:** `agents-systems-only`  
**Created:** 2025-11-02  
**Purpose:** Production-ready agent systems codebase with comprehensive documentation
