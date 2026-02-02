---
name: upstash-redis-kv
description: Read and write to Upstash Redis-compatible key-value store via REST API. Use when there is a need to save or retrieve key-value data, use Redis features (caching, counters, lists, sets, hashes, sorted sets, etc.) for the current interaction, or when the user explicitly asks to use Upstash or Redis.
---

# Upstash Redis Key-Value Store

Interact with Upstash's Redis-compatible key-value store using the REST interface.

## Script Location

```bash
bun run scripts/upstash-client.ts <command> [args...]
```

**IMPORTANT**: Always run with `bun run`, not directly.

## Configuration

### Environment Variables

The script uses these environment variables by default:
- `UPSTASH_REDIS_REST_URL` - The Upstash REST API URL
- `UPSTASH_REDIS_REST_TOKEN` - The Upstash REST API token

### Overriding Credentials

If the user provides credentials from another source (conversation context, a file, etc.), use the `--url` and `--token` flags to override environment variables:

```bash
bun run scripts/upstash-client.ts --url "https://..." --token "AX..." GET mykey
```

**Priority**: Command-line flags > Environment variables

## Command Reference

### String Commands

```bash
# Get/Set
GET <key>
SET <key> <value> [--ex seconds] [--px ms] [--nx] [--xx] [--keepttl] [--get]
SETNX <key> <value>                    # Set if not exists
SETEX <key> <seconds> <value>          # Set with expiration

# Multiple keys (key/value pairs)
MGET <key1> [key2...]
MSET <key1> <val1> [key2 val2...]
MSETNX <key1> <val1> [key2 val2...]    # Set all if none exist

# Counters
INCR <key>
INCRBY <key> <increment>
INCRBYFLOAT <key> <increment>
DECR <key>
DECRBY <key> <decrement>

# String manipulation
APPEND <key> <value>
STRLEN <key>
GETRANGE <key> <start> <end>
SETRANGE <key> <offset> <value>
```

### Hash Commands

Hashes store field-value pairs. Pass fields and values as alternating arguments:

```bash
# Set hash fields (field/value pairs)
HSET <key> <field1> <val1> [field2 val2...]
HSETNX <key> <field> <value>           # Set field if not exists

# Get hash fields
HGET <key> <field>
HMGET <key> <field1> [field2...]
HGETALL <key>

# Hash operations
HDEL <key> <field1> [field2...]
HEXISTS <key> <field>
HKEYS <key>
HVALS <key>
HLEN <key>
HINCRBY <key> <field> <increment>
HINCRBYFLOAT <key> <field> <increment>
HSCAN <key> <cursor> [MATCH pattern] [COUNT count]
```

**Examples:**

```bash
# Store user data
bun run scripts/upstash-client.ts HSET user:1 name "John" email "john@example.com" age 30

# Get single field
bun run scripts/upstash-client.ts HGET user:1 name

# Get all fields
bun run scripts/upstash-client.ts HGETALL user:1

# Increment numeric field
bun run scripts/upstash-client.ts HINCRBY user:1 age 1
```

### List Commands

Lists are ordered collections. Values are pushed/popped from left (head) or right (tail):

```bash
# Push elements
LPUSH <key> <val1> [val2...]           # Push to head
RPUSH <key> <val1> [val2...]           # Push to tail
LPUSHX <key> <val1> [val2...]          # Push if list exists
RPUSHX <key> <val1> [val2...]

# Pop elements
LPOP <key> [count]
RPOP <key> [count]

# Access elements
LRANGE <key> <start> <stop>            # Get range (0 = first, -1 = last)
LLEN <key>
LINDEX <key> <index>

# Modify
LSET <key> <index> <value>
LREM <key> <count> <value>             # Remove count occurrences
LTRIM <key> <start> <stop>             # Keep only range
LINSERT <key> <BEFORE|AFTER> <pivot> <value>
LPOS <key> <value>
LMOVE <src> <dst> <LEFT|RIGHT> <LEFT|RIGHT>
```

**Examples:**

```bash
# Create a task queue
bun run scripts/upstash-client.ts RPUSH tasks "task1" "task2" "task3"

# Get all tasks
bun run scripts/upstash-client.ts LRANGE tasks 0 -1

# Pop task from front (FIFO queue)
bun run scripts/upstash-client.ts LPOP tasks

# Pop task from back (LIFO stack)
bun run scripts/upstash-client.ts RPOP tasks
```

### Set Commands

Sets store unique, unordered members:

```bash
# Add/remove members
SADD <key> <member1> [member2...]
SREM <key> <member1> [member2...]

# Query
SMEMBERS <key>
SISMEMBER <key> <member>
SMISMEMBER <key> <member1> [member2...]
SCARD <key>

# Random access
SPOP <key> [count]
SRANDMEMBER <key> [count]

# Set operations
SINTER <key1> [key2...]
SINTERSTORE <dest> <key1> [key2...]
SUNION <key1> [key2...]
SUNIONSTORE <dest> <key1> [key2...]
SDIFF <key1> [key2...]
SDIFFSTORE <dest> <key1> [key2...]
SMOVE <src> <dst> <member>
SSCAN <key> <cursor> [MATCH pattern] [COUNT count]
```

**Examples:**

```bash
# Add tags
bun run scripts/upstash-client.ts SADD article:1:tags "javascript" "redis" "nodejs"

# Check membership
bun run scripts/upstash-client.ts SISMEMBER article:1:tags "javascript"

# Get all members
bun run scripts/upstash-client.ts SMEMBERS article:1:tags

# Find common tags between articles
bun run scripts/upstash-client.ts SINTER article:1:tags article:2:tags
```

### Sorted Set Commands

Sorted sets store members with scores for ranking:

```bash
# Add members (score/member pairs)
ZADD <key> <score1> <member1> [score2 member2...] [--nx] [--xx] [--gt] [--lt] [--ch]

# Remove
ZREM <key> <member1> [member2...]
ZREMRANGEBYRANK <key> <start> <stop>
ZREMRANGEBYSCORE <key> <min> <max>

# Scores and ranks
ZSCORE <key> <member>
ZMSCORE <key> <member1> [member2...]
ZRANK <key> <member>                   # Rank (low to high)
ZREVRANK <key> <member>                # Rank (high to low)
ZINCRBY <key> <increment> <member>

# Range queries
ZRANGE <key> <start> <stop> [--withscores] [--rev] [--byscore] [--bylex]
ZRANGEBYSCORE <key> <min> <max> [--withscores] [--limit off,count]
ZREVRANGE <key> <start> <stop> [--withscores]
ZREVRANGEBYSCORE <key> <max> <min> [--withscores] [--limit off,count]

# Counting
ZCARD <key>
ZCOUNT <key> <min> <max>

# Pop
ZPOPMIN <key> [count]
ZPOPMAX <key> [count]

# Set operations
ZINTERSTORE <dest> <numkeys> <key1> [key2...]
ZUNIONSTORE <dest> <numkeys> <key1> [key2...]
ZSCAN <key> <cursor> [MATCH pattern] [COUNT count]
```

**Examples:**

```bash
# Create leaderboard (score member pairs)
bun run scripts/upstash-client.ts ZADD leaderboard 1000 "player1" 1500 "player2" 1200 "player3"

# Get top 3 with scores (highest first)
bun run scripts/upstash-client.ts ZRANGE leaderboard 0 2 --rev --withscores

# Get player's rank
bun run scripts/upstash-client.ts ZREVRANK leaderboard "player2"

# Increment player's score
bun run scripts/upstash-client.ts ZINCRBY leaderboard 100 "player1"

# Get players with scores between 1000 and 1500
bun run scripts/upstash-client.ts ZRANGEBYSCORE leaderboard 1000 1500 --withscores
```

### Key Commands

```bash
# Delete
DEL <key1> [key2...]
UNLINK <key1> [key2...]                # Async delete

# Existence/Type
EXISTS <key1> [key2...]
TYPE <key>

# Expiration
EXPIRE <key> <seconds>
EXPIREAT <key> <timestamp>
PEXPIRE <key> <milliseconds>
PEXPIREAT <key> <timestamp>
TTL <key>
PTTL <key>
PERSIST <key>                          # Remove expiration

# Rename
RENAME <key> <newkey>
RENAMENX <key> <newkey>

# Search
KEYS <pattern>                         # Use with caution in production
SCAN <cursor> [MATCH pattern] [COUNT count]

# Other
COPY <src> <dst>
DUMP <key>
TOUCH <key1> [key2...]
RANDOMKEY
OBJECT ENCODING|FREQ|IDLETIME|REFCOUNT <key>
```

**Examples:**

```bash
# Set key with 1 hour expiration
bun run scripts/upstash-client.ts SET session:abc "data"
bun run scripts/upstash-client.ts EXPIRE session:abc 3600

# Or in one command
bun run scripts/upstash-client.ts SET session:abc "data" --ex 3600

# Check TTL
bun run scripts/upstash-client.ts TTL session:abc

# Scan keys matching pattern
bun run scripts/upstash-client.ts SCAN 0 MATCH "user:*" COUNT 100
```

### Server Commands

```bash
PING [message]
ECHO <message>
DBSIZE
TIME
INFO [section]
FLUSHDB                                # Delete all keys in current DB (DANGEROUS)
FLUSHALL                               # Delete all keys in all DBs (DANGEROUS)
```

## Command Options

### SET Options

```bash
--ex <seconds>     # Expire in seconds
--px <ms>          # Expire in milliseconds
--exat <ts>        # Expire at Unix timestamp (seconds)
--pxat <ts>        # Expire at Unix timestamp (ms)
--nx               # Only set if key does not exist
--xx               # Only set if key exists
--keepttl          # Retain existing TTL
--get              # Return old value
```

### ZADD Options

```bash
--nx               # Only add new members
--xx               # Only update existing members
--gt               # Only update if new score > current
--lt               # Only update if new score < current
--ch               # Return number of changed elements
```

### ZRANGE Options

```bash
--withscores       # Include scores in output
--byscore          # Range by score instead of rank
--bylex            # Range by lexicographical order
--rev              # Reverse order
--limit off,count  # Limit results (e.g., --limit 0,10)
```

## Output Format

- **String values**: Printed directly
- **null/nil**: Prints `(nil)`
- **Objects/arrays**: Pretty-printed as JSON

## Confirmation Behaviour

### Default: Ask for Confirmation

Before executing any destructive operation (write, modify, or delete), you MUST ask the user for confirmation. This includes:

**Write operations:**
- SET, SETNX, SETEX, PSETEX, MSET, MSETNX
- HSET, HSETNX
- LPUSH, RPUSH, LPUSHX, RPUSHX, LSET, LINSERT
- SADD
- ZADD

**Modify operations:**
- INCR, INCRBY, INCRBYFLOAT, DECR, DECRBY
- APPEND, SETRANGE
- HINCRBY, HINCRBYFLOAT
- LREM, LTRIM, LMOVE
- ZINCRBY

**Delete operations:**
- DEL, UNLINK
- HDEL
- LPOP, RPOP
- SREM, SPOP, SMOVE
- ZREM, ZREMRANGEBYRANK, ZREMRANGEBYSCORE, ZPOPMIN, ZPOPMAX
- FLUSHDB, FLUSHALL (extra caution)

**TTL/Rename operations:**
- EXPIRE, EXPIREAT, PEXPIRE, PEXPIREAT, PERSIST
- RENAME, RENAMENX

Example confirmation prompt:
> "I'm about to HSET `user:1` with fields `{name: "John", email: "john@example.com"}`. Proceed?"

### YOLO Mode: Skip Confirmation

If the user indicates they do not want to be asked for confirmation, respect this for all subsequent operations. Indicators include:

- "YOLO mode"
- "Don't ask for confirmation"
- "You're free to make changes without asking"
- "Just do it"
- "No need to confirm"
- "Auto-approve" or "auto-confirm"
- Any similar phrasing indicating blanket approval

Once YOLO mode is activated, proceed with destructive operations without asking, but still inform the user what was done.

Example:
> Set `user:1` with `{name: "John", email: "john@example.com"}` - done.

## Error Handling

If credentials are missing or invalid, the script will exit with an error message. Ensure the user has configured either:
1. Environment variables (`UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`)
2. Or provides credentials via `--url` and `--token` flags

## When to Use This Skill

- User explicitly asks to store or retrieve data from Upstash/Redis
- Need to persist data across conversations or sessions
- Implementing caching for expensive operations
- Maintaining counters, rate limits, or statistics
- Storing user preferences or session data
- Building leaderboards or rankings (sorted sets)
- Managing queues or task lists (lists)
- Tagging or categorisation (sets)
- Storing structured objects (hashes)
- Any scenario requiring fast key-value storage
