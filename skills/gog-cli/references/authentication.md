# gogcli Authentication Guide

Complete guide to authentication, credentials, and account management.

## Credential Storage

Tokens are secured using OS-native keystores:
- **macOS**: Keychain
- **Linux**: Secret Service (GNOME Keyring, KWallet)
- **Windows**: Credential Manager

An encrypted on-disk fallback is available when native keyring is unavailable.

### Keyring Backend Configuration

```bash
# Check current backend
gog config get keyring_backend

# Force specific backend
gog config set keyring_backend keychain  # macOS
gog config set keyring_backend file      # Encrypted file fallback

# Environment variable override
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD=your-encryption-password
```

---

## OAuth Client Credentials

Before adding accounts, store OAuth client credentials from Google Cloud Console.

### Creating OAuth Credentials

1. Go to Google Cloud Console > APIs & Services > Credentials
2. Create OAuth 2.0 Client ID (Desktop application type)
3. Download the JSON credentials file
4. Enable required APIs (Gmail, Calendar, Drive, etc.) in API Library

### Storing Credentials

```bash
# Store default credentials
gog auth credentials ~/Downloads/client_secret.json

# Store from stdin
cat client_secret.json | gog auth credentials -

# Store named client (for multiple organisations)
gog --client work auth credentials ~/Downloads/work-client.json
gog --client personal auth credentials ~/Downloads/personal-client.json

# Store with domain mapping (auto-select for matching email domains)
gog --client work auth credentials ~/Downloads/work.json --domain example.com

# List stored credentials
gog auth credentials list
```

---

## Adding Accounts

```bash
# Add account with interactive browser flow
gog auth add user@gmail.com

# Add with specific services
gog auth add user@gmail.com --services gmail,calendar,drive

# Add all available services
gog auth add user@gmail.com --services all

# Add with readonly access
gog auth add user@gmail.com --readonly

# Add with specific Drive scope
gog auth add user@gmail.com --drive-scope file      # Per-file access only
gog auth add user@gmail.com --drive-scope readonly  # Read-only
gog auth add user@gmail.com --drive-scope full      # Full access (default)

# Browserless flow (for headless systems)
gog auth add user@gmail.com --manual

# Force new consent (re-authorise)
gog auth add user@gmail.com --force-consent
```

### Available Services

```bash
# Show available services
gog auth services

# Show as markdown
gog auth services --markdown
```

Common services:
- `user` - Basic profile info (default)
- `gmail` - Email access
- `calendar` - Calendar access
- `drive` - Google Drive
- `contacts` - Contacts and People
- `tasks` - Tasks
- `classroom` - Google Classroom
- `chat` - Google Chat (Workspace)
- `sheets` - Google Sheets
- `docs` - Google Docs
- `slides` - Google Slides

---

## Managing Multiple Accounts

### Account Selection

```bash
# Use specific account for one command
gog --account work@example.com gmail search "is:unread"

# Set default account via environment
export GOG_ACCOUNT=work@example.com

# Set default account in config
gog config set default_account work@example.com
```

### Account Aliases

```bash
# Create alias
gog auth alias set work work@example.com
gog auth alias set personal me@gmail.com

# Use alias
gog --account work gmail search "is:unread"

# List aliases
gog auth alias list

# Remove alias
gog auth alias unset work
```

### Client Selection

```bash
# Use specific client for one command
gog --client work auth add user@example.com

# Set via environment
export GOG_CLIENT=work

# Auto-select by domain (configured during credential storage)
# Accounts at @example.com will automatically use the "work" client
```

---

## Service Accounts (Workspace)

For automated access without user interaction, use service accounts with domain-wide delegation.

### Setup

1. Create service account in Google Cloud Console
2. Enable domain-wide delegation
3. Grant required scopes in Google Workspace Admin
4. Download service account key JSON

```bash
# Configure service account for impersonation
gog auth service-account set admin@example.com --key ~/service-account.json

# Check status
gog auth service-account status

# Use impersonated account
gog --account admin@example.com gmail search "is:unread"
```

### Google Keep (Workspace Only)

Keep API requires service account authentication:

```bash
gog auth keep user@example.com --key ~/service-account.json
```

---

## Account Status

```bash
# List all authenticated accounts
gog auth list

# List with token validation check
gog auth list --check

# Show detailed auth status
gog auth status

# List stored tokens
gog auth tokens list
```

---

## Removing Accounts

```bash
# Remove account
gog auth remove user@gmail.com

# Delete specific token
gog auth tokens delete user@gmail.com
```

---

## Client Selection Hierarchy

When determining which OAuth client to use, `gog` follows this priority:

1. `--client` command flag
2. `GOG_CLIENT` environment variable
3. Account-specific mapping (`account_clients` in config)
4. Domain-based mapping (`client_domains` in config)
5. Domain-matching credentials file (`credentials-<domain>.json`)
6. Default client (`credentials.json`)

---

## Troubleshooting

### Token Expired

```bash
# Re-authenticate
gog auth add user@gmail.com --force-consent
```

### Wrong Scopes

If receiving permission errors, the token may have insufficient scopes:

```bash
# Re-add with required services
gog auth add user@gmail.com --services gmail,calendar,drive --force-consent
```

### Keyring Issues

```bash
# Check keyring backend
gog config get keyring_backend

# Force file backend
gog config set keyring_backend file

# Or use environment variable
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD=your-secure-password
```

### Multiple Client Confusion

```bash
# See which client is being used
gog auth status

# Explicitly specify client
gog --client work gmail search "is:unread"
```
