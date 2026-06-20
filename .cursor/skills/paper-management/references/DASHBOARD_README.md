# Reading Progress Dashboard 📊

A beautiful, auto-updating HTML dashboard for tracking your research paper reading progress.

## Overview

The dashboard provides a clean, visual interface for monitoring:
- 📚 Papers in your reading queue
- ✅ Completed papers
- 📈 Reading progress with TODO completion percentages
- 🎯 Statistics: total papers, completion rates, TODO items
- 🏷️ Tags and priorities for each paper

## Features

### Visual Design
- **Modern gradient interface** with purple/blue theme
- **Responsive layout** that works on desktop and mobile
- **Interactive cards** with hover effects
- **Progress bars** showing TODO completion for each paper
- **Priority badges** (high, medium, low) with color coding
- **Statistics dashboard** with key metrics at a glance

### Automatic Updates
The dashboard automatically regenerates when you:
- Add a new paper
- Mark a paper as read
- Create or update TODO lists
- Complete TODO items
- Move papers between lists

### Manual Regeneration
You can also manually update the dashboard:

```bash
# Using the CLI
python research.py dashboard

# Or run the generator directly
python paper_management/generate_dashboard.py
```

## Dashboard Sections

### 📊 Statistics Cards
Shows at-a-glance metrics:
- Total papers in your library
- Papers read
- Papers to read
- TODOs completed vs. total

### 📖 Currently Reading / To Read
Each paper card shows:
- **Title** (clickable link to the paper)
- **Authors**
- **Priority badge** (high/medium/low)
- **Tags** relevant to the paper
- **Added date**
- **Notes preview** (first 200 characters)
- **Progress bar** showing TODO completion percentage
- **TODO items** with checkboxes (completed items are checked and strikethrough)
- **Links to notes files** (if any exist)

### ✅ Completed Papers
Similar to the reading list, but for finished papers:
- Shows completion date instead of priority
- Links to any notes you've created
- Retains all metadata (authors, tags, etc.)

### Footer
Shows when the dashboard was last updated.

## File Structure

```
/workspace/
├── reading_progress.html              # The dashboard (open in browser)
├── paper_management/
│   ├── generate_dashboard.py          # Dashboard generator script
│   ├── papers/
│   │   ├── to_read.json               # Papers you're reading
│   │   ├── read.json                  # Completed papers
│   │   └── paper_todos.json           # TODO lists per paper
│   └── notes/
│       └── *.md                       # Your paper notes
```

## How It Works

1. **Data Source**: Reads from JSON files in `paper_management/papers/`
2. **Progress Calculation**: Computes completion percentage from TODO items
3. **Note Detection**: Finds markdown files in `notes/` folder matching paper titles
4. **HTML Generation**: Creates a standalone HTML file with embedded CSS
5. **Auto-refresh**: Triggered automatically after data changes

## Viewing the Dashboard

1. **Local Browser**: Simply open `reading_progress.html` in any web browser
2. **File Protocol**: Works with `file://` URLs, no web server needed
3. **Refresh**: Reload the page after making changes to see updates

## Customization

The dashboard styling is embedded in the HTML file. To customize:

1. Edit `paper_management/generate_dashboard.py`
2. Modify the CSS in the `<style>` section
3. Regenerate with `python research.py dashboard`

### Color Scheme
- Primary gradient: `#667eea` to `#764ba2` (purple-blue)
- High priority: Red (`#c53030`)
- Medium priority: Orange (`#d97706`)
- Low priority: Blue (`#1890ff`)

### Modifying Layout
The layout uses CSS Grid for the statistics section and flexbox for paper cards. Both are responsive and mobile-friendly.

## Tips

1. **Keep TODOs Updated**: The progress bars are based on TODO completion
2. **Use Priorities**: High priority papers stand out with red badges
3. **Add Notes**: The dashboard links to note files automatically
4. **Tag Papers**: Tags help categorize and filter papers visually

## Troubleshooting

### Dashboard not updating?
```bash
# Manually regenerate
python research.py dashboard
```

### Empty dashboard?
- Check that you have papers in `paper_management/papers/to_read.json`
- Add a paper: `python research.py papers add "paper_url_or_name"`

### Progress not showing?
- Create a TODO list: `python research.py todos create "Paper Title"`
- Add items: `python research.py todos add "Paper Title" "Read section 1"`

## Integration with Cursor Skills

The dashboard automatically updates when using Cursor skills:
- When you add papers via the paper management skill
- When you manage TODOs via the TODO skill
- After marking papers as read or completed

No manual intervention needed!

## Future Enhancements

Potential features for the dashboard:
- [ ] Charts/graphs for reading trends over time
- [ ] Filtering and sorting options
- [ ] Search functionality
- [ ] Export to PDF
- [ ] Reading time estimates
- [ ] Note previews with excerpts
- [ ] Tag cloud visualization
- [ ] Reading streak tracking

## Example Screenshots

The dashboard includes:
- Clean header with gradient background
- Four statistic cards showing key metrics
- Paper cards with all metadata visible
- Progress bars and TODO checklists
- Responsive design for all screen sizes

Open `reading_progress.html` in your browser to see it in action!
