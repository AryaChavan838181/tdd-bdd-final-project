# Product Catalogue REST API — TDD & BDD Final Project

Complete, GitHub-ready **Python** solution for the IBM/Coursera assignment. The seven files requested by the grading rubric are included in their exact relative locations. A minimal supporting Flask application and administrative UI are included so the project is self-contained; this is **not a verbatim copy of the official IBM starter**.

## Required GitHub file URLs

Replace `USERNAME` with your GitHub username. Create a repository named `tdd-bdd-final-project` with default branch `main`.

| Assignment tasks | Link |
|---|---|
| Task 1 (Q1) | `https://github.com/USERNAME/tdd-bdd-final-project/blob/main/tests/factories.py` |
| Task 2 (Q2–Q8) | `https://github.com/USERNAME/tdd-bdd-final-project/blob/main/tests/test_models.py` |
| Task 3 (Q9–Q15) | `https://github.com/USERNAME/tdd-bdd-final-project/blob/main/tests/test_routes.py` |
| Task 4 (Q16–Q19) | `https://github.com/USERNAME/tdd-bdd-final-project/blob/main/service/routes.py` |
| Task 5 (Q20) | `https://github.com/USERNAME/tdd-bdd-final-project/blob/main/features/steps/load_steps.py` |
| Task 6 (Q21–Q27) | `https://github.com/USERNAME/tdd-bdd-final-project/blob/main/features/products.feature` |
| Task 7 (Q28–Q31) | `https://github.com/USERNAME/tdd-bdd-final-project/blob/main/features/steps/web_steps.py` |

For multiple questions in a task, **repeat the same file URL** for each question. Do not link to the ZIP archive itself.

## Upload to GitHub

1. Create a new **empty** GitHub repository named `tdd-bdd-final-project` (do not initialize with README).
2. Extract this ZIP. Open a terminal **inside the extracted `tdd-bdd-final-project` folder**.
3. Run:

   ```bash
   git init
   git add .
   git commit -m "Complete TDD BDD final project"
   git branch -M main
   git remote add origin https://github.com/USERNAME/tdd-bdd-final-project.git
   git push -u origin main
   ```

4. Verify the seven URLs on GitHub, then submit them to Coursera.

## Run locally

Requires Python 3.10+ and, for BDD, Chrome or Chromium.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python app.py
```

In a second terminal, after the server starts:

```bash
behave features/products.feature
```

Use `DATABASE_URI` to override the default local SQLite database.

## Validation status

All Python source files compile successfully in the creation environment, and their declared task functions/scenarios are checked. The full Flask/Behave/Selenium test suite has **not** been executed here because this environment does not have all of those dependencies and a browser. Run the tests before submitting. No grade is guaranteed.

Starter project reference: https://github.com/ibm-developer-skills-network/xgcyk-tdd-bdd-final-project-template
