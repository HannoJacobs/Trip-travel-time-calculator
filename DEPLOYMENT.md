# GitHub Pages Deployment Guide

Follow these steps to deploy your Travel Time Calculator to GitHub Pages:

## 1. Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., `Trip-travel-time-calculator`)
5. Make sure it's set to **Public** (required for free GitHub Pages)
6. Don't initialize with README (we already have files)
7. Click "Create repository"

## 2. Upload Your Files

### Option A: Using Git Command Line
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Travel Time Calculator web app"

# Add GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/Trip-travel-time-calculator.git

# Push to GitHub
git push -u origin main
```

### Option B: Using GitHub Web Interface
1. On your new repository page, click "uploading an existing file"
2. Drag and drop all these files:
   - `index.html`
   - `styles.css`
   - `calculator.js`
   - `app.js`
   - `README_WEBSITE.md`
   - `.nojekyll`
   - `_config.yml`
3. Write a commit message like "Add Travel Time Calculator web app"
4. Click "Commit changes"

## 3. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on the "Settings" tab
3. Scroll down to "Pages" in the left sidebar
4. Under "Source", select "Deploy from a branch"
5. Choose "main" branch and "/ (root)" folder
6. Click "Save"

## 4. Access Your Website

After a few minutes, your website will be available at:
```
https://YOUR_USERNAME.github.io/Trip-travel-time-calculator
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## 5. Custom Domain (Optional)

If you want to use a custom domain:

1. In your repository, create a file named `CNAME`
2. Add your domain name (e.g., `travel-calculator.yourdomain.com`)
3. Configure your domain's DNS to point to GitHub Pages
4. Update the Pages settings to use your custom domain

## 6. Updates and Maintenance

To update your website:
1. Make changes to your local files
2. Commit and push changes to GitHub
3. GitHub Pages will automatically rebuild and deploy

## Troubleshooting

### Website Not Loading
- Wait 5-10 minutes after enabling Pages
- Check that the repository is public
- Ensure `index.html` is in the root directory

### Styles Not Loading
- Make sure `.nojekyll` file exists
- Check that CSS and JS file paths are correct
- Clear your browser cache

### JavaScript Errors
- Open browser developer tools (F12)
- Check the Console tab for error messages
- Ensure all file paths are relative (no leading `/`)

## File Structure

Your repository should have this structure:
```
Trip-travel-time-calculator/
├── index.html          # Main webpage
├── styles.css          # Styling
├── calculator.js       # Calculation logic
├── app.js             # User interface
├── README_WEBSITE.md  # Documentation
├── .nojekyll          # GitHub Pages config
├── _config.yml        # Jekyll config (optional)
└── DEPLOYMENT.md      # This file
```

## Support

If you encounter issues:
1. Check GitHub Pages documentation
2. Verify all files are uploaded correctly
3. Test locally by opening `index.html` in a browser
4. Check browser developer tools for errors

Your Travel Time Calculator should now be live and accessible to anyone with the URL! 