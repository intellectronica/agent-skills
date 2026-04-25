# gogcli Authentication Reference

Use this when configuring accounts, diagnosing auth failures, or selecting the right credential mode.

## Install and credentials

```bash
brew install gogcli
gog auth credentials set ~/Downloads/client_secret_....json
gog auth credentials list
gog auth add you@example.com --services gmail,calendar,drive
gog auth list --check
gog auth status
```

OAuth client credentials must be a Google Cloud "Desktop app" client JSON. Enable only the APIs needed for the task.

## Services and scopes

Check the live service list before prescribing scopes:

```bash
gog auth services
gog auth services --markdown
```

Current user-service names include:

```text
gmail, calendar, chat, classroom, drive, docs, slides, contacts,
tasks, sheets, people, forms, appscript, ads
```

Workspace-only service-account services include:

```text
groups, keep, admin
```

Important details:

- `gog auth add` defaults to `--services user`.
- `--services all` is a backwards-compatible alias for `user`, not "every Google API".
- Docs uses Docs plus Drive scopes; Slides and Sheets also rely on Drive for copy/export flows.
- Re-run with `--force-consent` when adding services or changing scope shape and Google does not return a new refresh token.

Least-privilege examples:

```bash
gog auth add you@example.com --services gmail --gmail-scope readonly
gog auth add you@example.com --services drive --drive-scope readonly
gog auth add you@example.com --services drive --drive-scope file
gog auth add you@example.com --services gmail,drive --readonly
gog auth add you@example.com --services gmail --extra-scopes https://www.googleapis.com/auth/gmail.labels
```

## OAuth clients and account selection

Use named clients for separate Google Cloud projects, organisations, or consent screens:

```bash
gog --client work auth credentials set ~/Downloads/work-client.json
gog --client work auth add you@company.com --services gmail,calendar
gog --client work gmail search 'is:unread'
```

Domain mapping auto-selects a client for matching account emails:

```bash
gog --client work auth credentials set ~/Downloads/work.json --domain company.com
```

Client resolution order:

1. `--client` or `GOG_CLIENT`
2. `account_clients` config mapping
3. `client_domains` config mapping
4. credentials file named after the email domain
5. `default`

Account aliases:

```bash
gog auth alias set work you@company.com
gog --account work calendar events primary --today
gog auth alias list
gog auth alias unset work
```

`--account auto` asks gog to use the default account or the single stored token.

## Browser, manual, remote, and proxy auth

Normal local browser flow:

```bash
gog auth add you@example.com --services gmail,calendar
```

Manual flow for headless systems:

```bash
gog auth add you@example.com --services gmail --manual
```

Remote two-step flow:

```bash
gog auth add you@example.com --services gmail --remote --step 1
gog auth add you@example.com --services gmail --remote --step 2 --auth-url 'http://127.0.0.1:<port>/oauth2/callback?code=...&state=...'
```

Proxy/tunnel callback:

```bash
gog auth add you@example.com --listen-addr 0.0.0.0:8080 --redirect-host gog.example.com
gog auth manage --listen-addr 0.0.0.0:8080 --redirect-host gog.example.com
```

The redirect URI must match the OAuth client configuration.

## Direct tokens and ADC

Direct short-lived token:

```bash
gog --access-token "$(gcloud auth print-access-token)" gmail labels list
GOG_ACCESS_TOKEN="$(gcloud auth print-access-token)" gog drive ls
```

Application Default Credentials mode is useful for Workload Identity, Cloud Run, and local `gcloud` ADC flows:

```bash
GOG_AUTH_MODE=adc gog --json drive ls
```

Direct access tokens expire in about an hour and do not use stored refresh tokens.

## Keyring backend

Tokens are stored in a keyring backend:

- `auto` - platform default
- `keychain` - macOS Keychain
- `file` - encrypted on-disk store

```bash
gog auth keyring
gog auth keyring keychain
gog auth keyring file
gog auth keyring auto
```

Environment overrides:

```bash
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD='...'
export GOG_KEYRING_SERVICE_NAME=gogcli
```

Use `GOG_KEYRING_PASSWORD` for non-interactive file-backend runs.

## Service accounts

Workspace domain-wide delegation is required for Admin and Keep and useful for unattended Workspace automation.

Setup outline:

1. Create a Google Cloud service account.
2. Enable domain-wide delegation.
3. Enable the APIs needed.
4. Add the service account client ID and comma-separated scopes in Workspace Admin Console.
5. Store the JSON key for the impersonated subject.

```bash
gog auth service-account set admin@example.com --key ~/Downloads/service-account.json
gog auth service-account status admin@example.com
gog --account admin@example.com admin users list --domain example.com
```

Remove a key:

```bash
gog auth service-account unset admin@example.com
```

Keep can also accept per-command service-account flags:

```bash
gog keep --service-account ~/service-account.json --impersonate user@example.com list
```

## Account and token management

```bash
gog auth list
gog auth list --check
gog auth status
gog auth remove you@example.com
gog auth credentials remove work
gog auth tokens list
gog auth tokens delete you@example.com
```

Token export/import contains secrets. Do not use it unless the user explicitly requested it:

```bash
gog auth tokens export you@example.com --out token.json
gog auth tokens import token.json
```

## Troubleshooting

| Symptom | Likely cause | Next command |
| --- | --- | --- |
| `no credentials` | OAuth client JSON not stored | `gog auth credentials set <client.json>` |
| `insufficient scopes` or 403 | Token lacks service/scope | `gog auth add <email> --services <service> --force-consent` |
| Keychain prompts or headless failures | Backend cannot unlock | `gog auth keyring file` plus `GOG_KEYRING_PASSWORD` |
| Wrong account/client | Alias or client auto-selection | `gog auth status`; retry with `--account` and `--client` |
| Workspace endpoint fails for Gmail.com | Consumer account unsupported | Use Workspace account/admin delegation |
