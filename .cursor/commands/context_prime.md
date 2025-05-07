# Context Prime Command

## Purpose
This command helps AI tools quickly understand the codebase structure and essential components to provide more accurate assistance.

## Command Execution Steps

1. **Read Project README**
   ```
   cat README.md
   ```

2. **Identify Project Structure**
   ```
   find . -type f -not -path "*/node_modules/*" -not -path "*/dist/*" -not -path "*/.git/*" | sort
   ```

3. **Examine Key Configuration Files**
   ```
   cat package.json
   cat tsconfig.json || cat .eslintrc.js || cat webpack.config.js || echo "No common config files found"
   ```

4. **Check Entry Points**
   ```
   cat src/index.js || cat src/main.js || cat src/app.js || cat src/index.ts || echo "No common entry points found"
   ```

5. **Understand Project Dependencies**
   ```
   cat package.json | grep -A 50 "dependencies"
   ```

6. **Review Directory Structure**
   ```
   find . -type d -maxdepth 2 -not -path "*/node_modules/*" -not -path "*/dist/*" -not -path "*/.git/*"
   ```

7. **Examine AI Docs for Context**
   ```
   find ./ai_docs -type f | xargs cat
   ```

8. **Review Latest Spec Documents**
   ```
   find ./specs -type f -name "*.md" | xargs cat
   ```

## Analysis Request

After gathering this information, please:

1. Summarize the project's purpose and architecture
2. Identify the main technologies and frameworks used
3. Outline the key components and their relationships
4. Note any patterns, conventions, or special considerations
5. Summarize current work in progress based on spec documents

This will establish the necessary context for productive collaboration on this project.