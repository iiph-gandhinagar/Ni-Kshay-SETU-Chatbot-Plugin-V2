# Contributing to Chatbot Opensource

Thank you for considering contributing to **Chatbot Opensource**! 🚀  
We appreciate your time and effort to help improve this project. Please follow the guidelines below to ensure a smooth contribution process.

---

## 🛠 Setting Up the Project

1. **Fork the repository**: Click on the `Fork` button at the top right of the GitLab repository page.
2. **Clone your forked repository**:
   ```bash
   git clone git@git.digiflux.io:hannahr/chatbot-opensource.git
   cd your-repo-name
3. **Ensure Python and all dependencies are installed.**
   - Install **Python 3.10** (required).
   - Install all dependencies using:
     ```bash
     pip install -r requirements.txt
     ```

4. **Set up environment variables:**
   - Copy the example environment file and configure your environment variables:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file with appropriate values.

5. **Start the server using:**
   ```bash
   PYTHONPATH=. uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload
   ```

## 📌 How to Contribute

###  Reporting Issues
If you find a bug, typo, or an improvement area:

- Check the **existing issues** to avoid duplicates.
- Open a **new issue** describing the problem.
- If you want to fix it yourself, **comment on the issue** and follow the steps below.

---

###  Proposing Changes (Feature/Enhancement)
- Open a **feature request issue** before making large changes.
- Discuss with maintainers before starting work.

---

###  Making Code Contributions

#### **Create a new branch:**
```bash
git checkout -b feature-name
```

## **Make your changes and test them.**

### **Commit your changes:**
```bash
git add .
git commit -m "Added feature XYZ"
```
### **Push your branch:**
```bash
git push origin feature-name
```
### **Open a Merge Request (MR):**

1. Go to your **GitLab repo** and create a **New Merge Request**.
2. Describe the changes and reference related issues if applicable.
3. Wait for approval from maintainers.
 

## ✅ Code Guidelines

- Follow consistent coding standards (e.g., **Prettier** for JS, **PEP8** for Python).
- Write **meaningful commit messages**.
- Ensure **your code does not break existing functionality**.
- **Run tests before submitting your code**.

## 🧪 Running Tests

The project has tests, run them before submitting changes:
```bash
python -m pytest --maxfail=5 --disable-warnings --cov=app --junitxml=report.xml tests/
```

## 🔄 Keeping Your Fork Updated

To avoid merge conflicts, regularly sync your fork with the main repo:
``` bash
git checkout main
git pull upstream main
git checkout feature-name
git merge main
```