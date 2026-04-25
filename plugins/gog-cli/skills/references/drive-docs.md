# Drive, Docs, Sheets, Slides, Forms, and Apps Script Reference

Use this for Google Drive files and Google editor content operations.

## Drive

List/search:

```bash
gog drive ls
gog drive ls --parent <folderId>
gog drive ls --all
gog drive ls --query "mimeType='application/pdf' and trashed=false"
gog drive search "quarterly report" --max 20
gog drive search "invoice filetype:pdf" --json
gog drive get <fileId>
gog drive url <fileId1> <fileId2>
```

Download/export:

```bash
gog drive download <fileId> --out ./file.pdf
gog drive download <docFileId> --format pdf --out ./doc.pdf
gog drive download <sheetFileId> --format xlsx --out ./sheet.xlsx
gog drive download <slideFileId> --format pptx --out ./deck.pptx
```

Upload/create/replace:

```bash
gog drive upload ./report.pdf --parent <folderId>
gog drive upload ./report.pdf --name "Q2 Report.pdf"
gog drive upload ./report.md --convert-to doc --parent <folderId>
gog drive upload ./data.csv --convert-to sheet
gog drive upload ./deck.pptx --convert-to slides
gog drive upload ./report.md --convert-to doc --keep-frontmatter
gog drive upload ./updated.pdf --replace <fileId> --name "Updated.pdf"
gog drive mkdir "New Folder" --parent <folderId>
```

`--replace` preserves the Drive file ID, shared link, and permissions.

File operations:

```bash
gog drive copy <fileId> "Copy Name" --parent <folderId>
gog drive move <fileId> --parent <newFolderId>
gog drive rename <fileId> "New Name"
gog drive delete <fileId>
gog drive delete <fileId> --permanent
```

Prefer normal delete, which moves to trash. Use `--permanent` only when explicitly requested.

Sharing:

```bash
gog drive share <fileId> --to user --email user@example.com --role writer
gog drive share <fileId> --to user --email user@example.com --role commenter
gog drive share <fileId> --to domain --domain example.com --role reader
gog drive share <fileId> --to anyone --role reader
gog drive permissions <fileId>
gog drive unshare <fileId> <permissionId>
```

Public/domain sharing may prompt or require `--force`; explain the effect first.

Shared drives and comments:

```bash
gog drive drives
gog drive drives --query "name contains 'Team'"
gog drive comments list <fileId>
gog drive comments get <fileId> <commentId>
gog drive comments create <fileId> "Please review"
gog drive comments update <fileId> <commentId> "Updated comment"
gog drive comments reply <fileId> <commentId> "Done"
gog drive comments delete <fileId> <commentId>
```

Drive query examples:

```bash
gog drive ls --query "name contains 'Report'"
gog drive ls --query "'<folderId>' in parents and trashed=false"
gog drive ls --query "mimeType='application/vnd.google-apps.spreadsheet'"
gog drive ls --query "modifiedTime > '2026-04-01T00:00:00'"
```

## Docs

Create/copy/read/export:

```bash
gog docs create "Meeting Notes"
gog docs copy <docId> "Copy of Meeting Notes"
gog docs info <docId>
gog docs cat <docId>
gog docs cat <docId> -N
gog docs export <docId> --format pdf --out ./doc.pdf
gog docs export <docId> --format docx --out ./doc.docx
gog docs export <docId> --format md --out ./doc.md
gog docs export <docId> --format html --out ./doc.html
```

Write/import:

```bash
gog docs write <docId> --text "Plain text"
gog docs write <docId> --file ./brief.txt --replace
gog docs write <docId> --file ./brief.md --replace --markdown
gog docs write <docId> --file - --replace
gog docs write <docId> --file ./appendix.md --append --markdown
gog docs create "Brief" --file ./brief.md --pageless
```

Tabs and structure:

```bash
gog docs list-tabs <docId>
gog docs structure <docId>
gog docs write <docId> --file ./tab.md --replace --markdown --tab-id <tabId>
```

Edit text:

```bash
gog docs find-replace <docId> "{{NAME}}" "Ada"
gog docs find-replace <docId> "{{BODY}}" --content-file ./body.md --format markdown
gog docs find-replace <docId> "{{LOGO}}" --content-file ./logo.md --format markdown --first
gog docs insert <docId> "Intro text" --index 1
gog docs delete <docId> --start 10 --end 20
gog docs clear <docId>
```

Sed-style rich editing:

```bash
gog docs sed <docId> 's/status/{b c=green}approved/g' --dry-run
gog docs sed <docId> -f edits.sed
echo 's/title/{h=1}Quarterly Report/' | gog docs sed <docId>
```

Read `references/sedmat.md` for the full sedmat DSL: bold/italic, colours, links, images, headings, tables, checkboxes, and regex captures.

Docs comments:

```bash
gog docs comments list <docId>
gog docs comments add <docId> "Please revise this paragraph"
gog docs comments reply <docId> <commentId> "Updated"
gog docs comments resolve <docId> <commentId>
gog docs comments delete <docId> <commentId>
```

## Sheets

Create/copy/export:

```bash
gog sheets create "Budget 2026" --sheets "Q1,Q2"
gog sheets create "Budget 2026" --parent <folderId>
gog sheets copy <spreadsheetId> "Budget Copy"
gog sheets export <spreadsheetId> --format xlsx --out ./budget.xlsx
gog sheets metadata <spreadsheetId>
```

Values:

```bash
gog sheets get <spreadsheetId> 'Sheet1!A1:D10'
gog sheets update <spreadsheetId> 'Sheet1!A1:B2' '[["Name","Age"],["Ada",30]]'
gog sheets append <spreadsheetId> 'Sheet1!A:B' '[["Grace",35]]'
gog sheets clear <spreadsheetId> 'Sheet1!A1:D10'
```

Formatting and layout:

```bash
gog sheets format <spreadsheetId> 'Sheet1!A1:D1' --bold --bg-color '#FFCC00' --h-align center
gog sheets number-format <spreadsheetId> 'Sheet1!B2:B100' --pattern '$#,##0.00'
gog sheets merge <spreadsheetId> 'Sheet1!A1:D1'
gog sheets unmerge <spreadsheetId> 'Sheet1!A1:D1'
gog sheets freeze <spreadsheetId> --sheet Sheet1 --rows 1 --cols 0
gog sheets resize-columns <spreadsheetId> 'Sheet1!A:C' --width 160
gog sheets resize-rows <spreadsheetId> 'Sheet1!1:10' --height 36
gog sheets read-format <spreadsheetId> 'Sheet1!A1:B2'
gog sheets read-format <spreadsheetId> 'Sheet1!A1:B2' --effective
```

Rows, columns, tabs:

```bash
gog sheets insert <spreadsheetId> Sheet1 rows 2 --count 3
gog sheets insert <spreadsheetId> Sheet1 cols 3 --after
gog sheets add-tab <spreadsheetId> "Summary" --index 0
gog sheets rename-tab <spreadsheetId> "Sheet1" "Raw"
gog sheets delete-tab <spreadsheetId> "Old" --force
```

Notes, links, find/replace:

```bash
gog sheets notes <spreadsheetId> 'Sheet1!A1:B10'
gog sheets update-note <spreadsheetId> 'Sheet1!A1' --note "Check this"
gog sheets update-note <spreadsheetId> 'Sheet1!A1' --note ''
gog sheets links <spreadsheetId> 'Sheet1!A1:B10'
gog sheets find-replace <spreadsheetId> "old" "new" --sheet Sheet1
```

Named ranges:

```bash
gog sheets named-ranges list <spreadsheetId>
gog sheets named-ranges get <spreadsheetId> MyRange
gog sheets named-ranges add <spreadsheetId> MyRange 'Sheet1!A1:B2'
gog sheets named-ranges update <spreadsheetId> MyRange --name BetterRange
gog sheets named-ranges delete <spreadsheetId> BetterRange
```

Charts:

```bash
gog sheets chart list <spreadsheetId>
gog sheets chart get <spreadsheetId> <chartId> --json > chart.json
gog sheets chart create <spreadsheetId> --spec-json @chart.json --sheet Sheet1 --anchor E10
gog sheets chart update <spreadsheetId> <chartId> --spec-json '{"title":"New Title"}'
gog sheets chart delete <spreadsheetId> <chartId>
```

A1 range reminders:

| Format | Meaning |
| --- | --- |
| `Sheet1!A1` | one cell |
| `Sheet1!A1:B2` | rectangular range |
| `Sheet1!A:A` | column |
| `Sheet1!1:1` | row |
| `Sheet1` | whole sheet |
| `A1:B2` | default sheet |

## Slides

Create/copy/export:

```bash
gog slides create "Q2 Review"
gog slides copy <presentationId> "Q2 Review Copy"
gog slides info <presentationId>
gog slides export <presentationId> --format pptx --out ./deck.pptx
gog slides export <presentationId> --format pdf --out ./deck.pdf
```

Generate/edit decks:

```bash
gog slides create-from-markdown "Status Deck" --content-file ./deck.md
gog slides create-from-template <templateId> "Monthly Report" --replace "month=April" --replace "revenue=$1.2M"
gog slides create-from-template <templateId> "Monthly Report" --replacements replacements.json
gog slides add-slide <presentationId> ./slide.png --notes "Speaker notes"
gog slides replace-slide <presentationId> <slideId> ./replacement.png
gog slides update-notes <presentationId> <slideId> --notes-file ./notes.txt
```

Inspect/render:

```bash
gog slides list-slides <presentationId>
gog slides read-slide <presentationId> <slideId>
gog slides read-slide <presentationId> <slideId> --recursive --json
gog slides thumbnail <presentationId> <slideId>
gog slides thumbnail <presentationId> <slideId> --out ./slide.png
gog slides thumbnail <presentationId> <slideId> --size medium --format jpeg --out ./slide.jpg
gog slides delete-slide <presentationId> <slideId>
```

## Forms

```bash
gog forms create --title "Weekly Check-in" --description "Friday async update"
gog forms get <formId>
gog forms update <formId> --title "Weekly Sync" --quiz true
gog forms add-question <formId> --title "What shipped?" --type paragraph --required
gog forms move-question <formId> 3 1
gog forms delete-question <formId> 2 --force
gog forms responses list <formId> --max 20
gog forms responses get <formId> <responseId>
gog forms watch create <formId> --topic projects/<project>/topics/<topic>
gog forms watch list <formId>
gog forms watch renew <formId> <watchId>
gog forms watch delete <formId> <watchId>
```

## Apps Script

```bash
gog appscript create --title "Automation Helpers"
gog appscript create --title "Bound Script" --parent-id <driveFileId>
gog appscript get <scriptId>
gog appscript content <scriptId>
gog appscript run <scriptId> myFunction --params '["arg1", 123, true]'
gog appscript run <scriptId> myFunction --dev-mode
```

## Scripting examples

Download every PDF in a folder:

```bash
gog --json drive ls --parent <folderId> --query "mimeType='application/pdf'" | \
  jq -r '.files[].id' | \
  xargs -n 1 -I {} gog drive download {} --out ./pdfs/
```

Export all docs returned by a query:

```bash
gog --json drive ls --query "mimeType='application/vnd.google-apps.document' and trashed=false" | \
  jq -r '.files[] | @tsv "\(.id)\t\(.name)"' | \
  while IFS=$'\t' read -r id name; do
    gog docs export "$id" --format pdf --out "./pdfs/${name}.pdf"
  done
```
