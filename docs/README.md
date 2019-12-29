# Setup to Generate Docs From Docstrings

1. Install sphinx
   ```
   pip install Sphinx
   ```
2. Move to docs folder
   ```
   cd docs
   ```
3. Update docs if needed (OPTIONAL)
   ```
   sphinx-apidoc -o . ../evalai
   ```
4. Generate HTML Using Provided theme
   ```
   make html
   ```