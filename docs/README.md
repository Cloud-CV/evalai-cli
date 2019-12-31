# Setup to Generate Docs From Docstrings

1. Install sphinx
   ```
   pip install Sphinx
   ```
2. Install Theme
   ```
   pip install sphinx-rtd-theme
   ```
3. Move to docs folder
   ```
   cd docs
   ```
4. Update docs if needed (OPTIONAL)
   ```
   sphinx-apidoc -o . ../evalai
   ```
5. Generate HTML Using Provided theme
   ```
   make html
   ```