# Drive, Docs, Sheets, and Slides Reference

Comprehensive guide to Google Drive and document operations with `gog`.

## Google Drive

### Listing Files

```bash
# List files in root
gog drive ls

# List in specific folder
gog drive ls --parent <folderId>

# Filter with query
gog drive ls --query "mimeType='application/pdf'"

# Limit results
gog drive ls --max 20

# Paginate
gog drive ls --page <nextPageToken>
```

### Searching Files

```bash
# Text search
gog drive search "quarterly report"

# Limit results
gog drive search "budget" --max 10
```

### File Information

```bash
# Get file metadata
gog drive get <fileId>

# Get web URLs
gog drive url <fileId1> <fileId2>
```

### Downloading Files

```bash
# Download file
gog drive download <fileId>

# Specify output path
gog drive download <fileId> --out ~/Downloads/file.pdf
```

### Uploading Files

```bash
# Upload to root
gog drive upload ~/Documents/report.pdf

# Upload with custom name
gog drive upload ~/Documents/report.pdf --name "Q4 Report.pdf"

# Upload to specific folder
gog drive upload ~/Documents/report.pdf --parent <folderId>
```

### Creating Folders

```bash
# Create folder in root
gog drive mkdir "New Folder"

# Create in specific location
gog drive mkdir "Subfolder" --parent <folderId>
```

### File Operations

```bash
# Delete file (to trash)
gog drive delete <fileId>

# Move file
gog drive move <fileId> --parent <newFolderId>

# Copy file
gog drive copy <fileId>
gog drive copy <fileId> --name "Copy of File"
gog drive copy <fileId> --parent <folderId>

# Rename file
gog drive rename <fileId> "New Name"
```

### Sharing Files

```bash
# Share with anyone (link sharing)
gog drive share <fileId> --anyone --role reader

# Share with specific person
gog drive share <fileId> --email user@example.com --role writer

# Make discoverable
gog drive share <fileId> --anyone --role reader --discoverable

# List permissions
gog drive permissions <fileId>

# Remove sharing
gog drive unshare <fileId> <permissionId>
```

### Shared Drives

```bash
# List shared drives
gog drive drives

# Search shared drives
gog drive drives --query "name contains 'Team'"
```

### Comments

```bash
# List comments
gog drive comments <fileId>

# Add comment
gog drive comments add <fileId> --content "This needs review"

# Reply to comment
gog drive comments reply <fileId> <commentId> --content "Done!"

# Resolve comment
gog drive comments resolve <fileId> <commentId>

# Delete comment
gog drive comments delete <fileId> <commentId>
```

---

## Google Sheets

### Creating Spreadsheets

```bash
# Create empty spreadsheet
gog sheets create "Budget 2024"

# Create with named sheet
gog sheets create "Budget 2024" --sheet "Q1"
```

### Getting Spreadsheet Info

```bash
# Get spreadsheet metadata
gog sheets get <spreadsheetId>

# Get sheet metadata
gog sheets metadata <spreadsheetId>
```

### Reading Data

```bash
# Read range
gog sheets read <spreadsheetId> "Sheet1!A1:D10"

# Read entire sheet
gog sheets read <spreadsheetId> "Sheet1"

# JSON output
gog sheets read <spreadsheetId> "Sheet1!A1:D10" --json
```

### Writing Data

```bash
# Write values (overwrites)
gog sheets write <spreadsheetId> "Sheet1!A1:B2" \
  --values '[["Name","Age"],["Alice",30]]'

# Update values
gog sheets update <spreadsheetId> "Sheet1!A1:B2" \
  --values '[["Name","Age"],["Bob",25]]'
```

### Appending Data

```bash
# Append rows
gog sheets append <spreadsheetId> "Sheet1!A:B" \
  --values '[["Charlie",35],["Diana",28]]'
```

### Clearing Data

```bash
# Clear range
gog sheets clear <spreadsheetId> "Sheet1!A1:D10"
```

### Formatting Cells

```bash
# Bold text
gog sheets format <spreadsheetId> "Sheet1!A1:D1" --bold

# Multiple formatting options
gog sheets format <spreadsheetId> "Sheet1!A1:D1" \
  --bold \
  --italic \
  --bg-color "#FFCC00" \
  --fg-color "#000000" \
  --font-size 14 \
  --h-align center

# Number formatting
gog sheets format <spreadsheetId> "Sheet1!B2:B100" \
  --number-format "$#,##0.00"
```

### Range Format (A1 Notation)

| Format | Description |
|--------|-------------|
| `Sheet1!A1` | Single cell |
| `Sheet1!A1:B2` | Range |
| `Sheet1!A:A` | Entire column |
| `Sheet1!1:1` | Entire row |
| `Sheet1` | Entire sheet |
| `A1:B2` | Default sheet |

---

## Google Docs

### Creating Documents

```bash
gog docs create "Meeting Notes"
```

### Getting Document Info

```bash
gog docs get <documentId>
```

### Exporting Documents

```bash
# Export as PDF
gog docs export <documentId> --format pdf --out ~/Documents/notes.pdf

# Export as Word
gog docs export <documentId> --format docx --out ~/Documents/notes.docx

# Other formats
gog docs export <documentId> --format txt
gog docs export <documentId> --format html
gog docs export <documentId> --format md
```

---

## Google Slides

### Creating Presentations

```bash
gog slides create "Q4 Review"
```

### Getting Presentation Info

```bash
gog slides get <presentationId>
```

### Exporting Presentations

```bash
# Export as PDF
gog slides export <presentationId> --format pdf --out ~/Documents/slides.pdf

# Export as PowerPoint
gog slides export <presentationId> --format pptx --out ~/Documents/slides.pptx
```

---

## Drive Query Syntax

The `--query` parameter uses Google Drive query syntax:

| Query | Description |
|-------|-------------|
| `name = 'Report'` | Exact name match |
| `name contains 'Report'` | Name contains |
| `mimeType = 'application/pdf'` | File type |
| `'folderId' in parents` | In specific folder |
| `trashed = false` | Not in trash |
| `starred = true` | Starred files |
| `sharedWithMe = true` | Shared with me |
| `modifiedTime > '2024-01-01'` | Modified after date |

### Common MIME Types

| Type | MIME Type |
|------|-----------|
| Folder | `application/vnd.google-apps.folder` |
| Document | `application/vnd.google-apps.document` |
| Spreadsheet | `application/vnd.google-apps.spreadsheet` |
| Presentation | `application/vnd.google-apps.presentation` |
| PDF | `application/pdf` |

### Example Queries

```bash
# PDFs only
gog drive ls --query "mimeType='application/pdf'"

# Recent files
gog drive ls --query "modifiedTime > '2024-12-01'"

# Starred spreadsheets
gog drive ls --query "starred=true and mimeType='application/vnd.google-apps.spreadsheet'"
```

---

## Scripting Examples

### Backup Folder

```bash
# Download all files from a folder
gog drive ls --parent <folderId> --json | \
  jq -r '.files[].id' | \
  xargs -I {} gog drive download {} --out ~/backup/
```

### Bulk Upload

```bash
# Upload all PDFs in directory
for f in ~/Documents/*.pdf; do
  gog drive upload "$f" --parent <folderId>
done
```

### Export All Docs as PDF

```bash
gog drive ls --query "mimeType='application/vnd.google-apps.document'" --json | \
  jq -r '.files[] | "\(.id) \(.name)"' | \
  while read id name; do
    gog docs export "$id" --format pdf --out "~/pdfs/${name}.pdf"
  done
```
