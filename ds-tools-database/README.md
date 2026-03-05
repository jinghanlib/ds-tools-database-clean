# DS Tools Database

A searchable, filterable web repository of 257+ digital scholarship tools built with [Eleventy](https://www.11ty.dev/) and deployed on Netlify.

## Features

- **Responsive card grid** with tool images
- **Category filters** (25 categories)
- **Fuzzy search** using Fuse.js
- **Direct links** to external tools
- **Mobile-friendly design**
- **Static site** - no server or database required

## Quick Start

### Prerequisites

- Node.js 18+ (recommended: 20+)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The site will be available at `http://localhost:8080`

### Build for Production

```bash
npm run build
```

The built site will be in the `_site` directory.

## Project Structure

```
ds-tools-database/
├── src/
│   ├── _data/
│   │   └── tools.json          # Tool data (257 entries)
│   ├── _includes/
│   │   └── layouts/
│   │       └── base.njk        # Base HTML template
│   ├── assets/
│   │   ├── css/style.css       # Styles
│   │   ├── js/search.js        # Search/filter functionality
│   │   └── images/             # Tool screenshots (257 images)
│   └── index.njk               # Homepage with grid
├── .eleventy.js                # Eleventy config
├── netlify.toml                # Netlify deployment config
└── package.json
```

## Deployment to Netlify

1. Push this repository to GitHub
2. Connect the repo to Netlify
3. Netlify will auto-detect the settings from `netlify.toml`
4. Your site will be live!

### Manual Netlify Settings (if needed)

- **Build command:** `npm install && npx @11ty/eleventy`
- **Publish directory:** `_site`
- **Node version:** 20

## Data Format

Tools are stored in `src/_data/tools.json`:

```json
{
  "tools": [
    {
      "id": 1,
      "name": "Tool Name",
      "slug": "tool-name",
      "url": "https://example.com",
      "categories": ["Category 1", "Category 2"],
      "description": "Tool description...",
      "image": "/assets/images/tool-name.png",
      "updated": "5/19/2024 11:42am"
    }
  ],
  "categories": ["AI", "Data Sources", "Mapping Tools", ...]
}
```

## Adding New Tools

1. Add tool entry to `src/_data/tools.json`
2. Add tool screenshot to `src/assets/images/`
3. Rebuild the site

## Categories

The database includes 25 categories:
- 3D
- AI
- Consultation Services
- Creative Coding Tools
- Data Sources
- Digital Media Production Tools
- Digital Publishing
- Example Projects
- External Aggregated Resources
- Funding for Individuals
- Funding for Institutions
- Infrastructure
- Learning Resources
- Mapping Tools
- Network Analysis Tools
- Open Source / Open Access
- Research Tools
- Storytelling Tools
- Text Analysis Tools
- VR/AR/MR/XR
- Visualization Tools
- Web Archiving Tools
- Web IDE & Notebooks
- Web Scraping Tools
- Website Builder & CMS Tools

## License

MIT
