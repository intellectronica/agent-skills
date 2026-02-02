#!/usr/bin/env bun
import { parseArgs } from "node:util";
import { Redis } from "@upstash/redis";

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  options: {
    url: { type: "string" },
    token: { type: "string" },
    help: { type: "boolean", short: "h" },
    // SET options
    ex: { type: "string" },
    px: { type: "string" },
    exat: { type: "string" },
    pxat: { type: "string" },
    nx: { type: "boolean" },
    xx: { type: "boolean" },
    keepttl: { type: "boolean" },
    get: { type: "boolean" },
    // ZRANGE/ZADD options
    withscores: { type: "boolean" },
    byscore: { type: "boolean" },
    bylex: { type: "boolean" },
    rev: { type: "boolean" },
    limit: { type: "string" },
    // ZADD-specific options
    gt: { type: "boolean" },
    lt: { type: "boolean" },
    ch: { type: "boolean" },
    // JSON input for complex objects
    json: { type: "boolean" },
  },
  allowPositionals: true,
});

function printHelp() {
  console.log(`Usage: bun run upstash-client.ts [options] <command> [args...]

Connection Options:
  --url <url>      Upstash REST URL (or UPSTASH_REDIS_REST_URL env var)
  --token <token>  Upstash REST token (or UPSTASH_REDIS_REST_TOKEN env var)
  -h, --help       Show this help

SET Options:
  --ex <seconds>   Set expiration in seconds
  --px <ms>        Set expiration in milliseconds
  --exat <ts>      Set expiration as Unix timestamp (seconds)
  --pxat <ts>      Set expiration as Unix timestamp (milliseconds)
  --nx             Only set if key does not exist
  --xx             Only set if key already exists
  --keepttl        Retain existing TTL
  --get            Return old value

ZADD Options:
  --nx             Only add new elements
  --xx             Only update existing elements
  --gt             Only update when new score > current score
  --lt             Only update when new score < current score
  --ch             Return number of changed elements

ZRANGE Options:
  --withscores     Include scores in output
  --byscore        Interpret range as score range
  --bylex          Interpret range as lexicographical range
  --rev            Reverse order
  --limit <off,count>  Limit results (e.g., --limit 0,10)

General:
  --json           Parse next argument as JSON (for complex objects)

Commands:

  STRING:
    GET <key>
    SET <key> <value> [--ex N] [--px N] [--nx] [--xx]
    MGET <key1> [key2...]
    MSET <key1> <val1> [key2 val2...]
    INCR <key>
    INCRBY <key> <increment>
    DECR <key>
    DECRBY <key> <decrement>
    APPEND <key> <value>
    STRLEN <key>

  HASH:
    HGET <key> <field>
    HSET <key> <field1> <val1> [field2 val2...]
    HMGET <key> <field1> [field2...]
    HGETALL <key>
    HDEL <key> <field1> [field2...]
    HEXISTS <key> <field>
    HKEYS <key>
    HVALS <key>
    HLEN <key>
    HINCRBY <key> <field> <increment>
    HSETNX <key> <field> <value>

  LIST:
    LPUSH <key> <val1> [val2...]
    RPUSH <key> <val1> [val2...]
    LPOP <key> [count]
    RPOP <key> [count]
    LRANGE <key> <start> <stop>
    LLEN <key>
    LINDEX <key> <index>
    LSET <key> <index> <value>
    LREM <key> <count> <value>
    LTRIM <key> <start> <stop>
    LINSERT <key> <BEFORE|AFTER> <pivot> <value>

  SET:
    SADD <key> <member1> [member2...]
    SREM <key> <member1> [member2...]
    SMEMBERS <key>
    SISMEMBER <key> <member>
    SCARD <key>
    SPOP <key> [count]
    SRANDMEMBER <key> [count]
    SINTER <key1> [key2...]
    SUNION <key1> [key2...]
    SDIFF <key1> [key2...]

  SORTED SET:
    ZADD <key> <score1> <member1> [score2 member2...] [--nx] [--xx] [--gt] [--lt] [--ch]
    ZREM <key> <member1> [member2...]
    ZSCORE <key> <member>
    ZRANK <key> <member>
    ZREVRANK <key> <member>
    ZRANGE <key> <start> <stop> [--withscores] [--byscore] [--bylex] [--rev]
    ZRANGEBYSCORE <key> <min> <max> [--withscores] [--limit off,count]
    ZCARD <key>
    ZCOUNT <key> <min> <max>
    ZINCRBY <key> <increment> <member>
    ZPOPMIN <key> [count]
    ZPOPMAX <key> [count]

  KEY:
    DEL <key1> [key2...]
    EXISTS <key1> [key2...]
    EXPIRE <key> <seconds>
    EXPIREAT <key> <timestamp>
    TTL <key>
    PTTL <key>
    PERSIST <key>
    KEYS <pattern>
    SCAN <cursor> [MATCH pattern] [COUNT count]
    TYPE <key>
    RENAME <key> <newkey>
    RENAMENX <key> <newkey>

  SERVER:
    DBSIZE
    FLUSHDB
    PING
    ECHO <message>

Examples:
  # Basic string operations
  bun run upstash-client.ts SET mykey "hello world"
  bun run upstash-client.ts GET mykey
  bun run upstash-client.ts SET session:123 "data" --ex 3600

  # Hash operations (field/value pairs)
  bun run upstash-client.ts HSET user:1 name "John" email "john@example.com" age 30
  bun run upstash-client.ts HGET user:1 name
  bun run upstash-client.ts HGETALL user:1

  # List operations
  bun run upstash-client.ts LPUSH tasks "task1" "task2" "task3"
  bun run upstash-client.ts LRANGE tasks 0 -1

  # Set operations
  bun run upstash-client.ts SADD tags "javascript" "redis" "nodejs"
  bun run upstash-client.ts SMEMBERS tags

  # Sorted set operations (score member pairs)
  bun run upstash-client.ts ZADD leaderboard 1000 "player1" 1500 "player2"
  bun run upstash-client.ts ZRANGE leaderboard 0 -1 --withscores --rev

  # Multiple keys
  bun run upstash-client.ts MSET key1 "val1" key2 "val2" key3 "val3"
  bun run upstash-client.ts MGET key1 key2 key3

  # With explicit credentials
  bun run upstash-client.ts --url https://... --token AX... GET mykey`);
}

if (values.help || positionals.length === 0) {
  printHelp();
  process.exit(values.help ? 0 : 1);
}

const url = values.url || process.env.UPSTASH_REDIS_REST_URL;
const token = values.token || process.env.UPSTASH_REDIS_REST_TOKEN;

if (!url || !token) {
  console.error("Error: Missing credentials");
  console.error("Provide --url and --token, or set UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN");
  process.exit(1);
}

const redis = new Redis({ url, token });
const [rawCmd, ...args] = positionals;
const cmd = rawCmd.toUpperCase();

// Helper to parse a value (try JSON, fall back to string/number)
function parseValue(val: string): any {
  if (values.json) {
    try {
      return JSON.parse(val);
    } catch {
      return val;
    }
  }
  // Try to parse as number
  const num = Number(val);
  if (!isNaN(num) && val.trim() !== "") {
    return num;
  }
  // Try to parse as JSON object/array
  if ((val.startsWith("{") && val.endsWith("}")) || (val.startsWith("[") && val.endsWith("]"))) {
    try {
      return JSON.parse(val);
    } catch {
      return val;
    }
  }
  return val;
}

// Helper to convert pairs to object: [k1, v1, k2, v2] -> {k1: v1, k2: v2}
function pairsToObject(pairs: string[]): Record<string, any> {
  const obj: Record<string, any> = {};
  for (let i = 0; i < pairs.length; i += 2) {
    if (i + 1 < pairs.length) {
      obj[pairs[i]] = parseValue(pairs[i + 1]);
    }
  }
  return obj;
}

// Helper to convert score/member pairs: [s1, m1, s2, m2] -> [{score: s1, member: m1}, ...]
function scoreMemberPairs(pairs: string[]): Array<{ score: number; member: string }> {
  const result: Array<{ score: number; member: string }> = [];
  for (let i = 0; i < pairs.length; i += 2) {
    if (i + 1 < pairs.length) {
      result.push({ score: Number(pairs[i]), member: pairs[i + 1] });
    }
  }
  return result;
}

// Build SET options
function buildSetOptions(): Record<string, any> | undefined {
  const opts: Record<string, any> = {};
  if (values.ex) opts.ex = Number(values.ex);
  if (values.px) opts.px = Number(values.px);
  if (values.exat) opts.exat = Number(values.exat);
  if (values.pxat) opts.pxat = Number(values.pxat);
  if (values.nx) opts.nx = true;
  if (values.xx) opts.xx = true;
  if (values.keepttl) opts.keepttl = true;
  if (values.get) opts.get = true;
  return Object.keys(opts).length > 0 ? opts : undefined;
}

// Build ZADD options
function buildZaddOptions(): Record<string, any> | undefined {
  const opts: Record<string, any> = {};
  if (values.nx) opts.nx = true;
  if (values.xx) opts.xx = true;
  if (values.gt) opts.gt = true;
  if (values.lt) opts.lt = true;
  if (values.ch) opts.ch = true;
  return Object.keys(opts).length > 0 ? opts : undefined;
}

// Build ZRANGE options
function buildZrangeOptions(): Record<string, any> | undefined {
  const opts: Record<string, any> = {};
  if (values.withscores) opts.withScores = true;
  if (values.byscore) opts.byScore = true;
  if (values.bylex) opts.byLex = true;
  if (values.rev) opts.rev = true;
  if (values.limit) {
    const [offset, count] = values.limit.split(",").map(Number);
    opts.offset = offset;
    opts.count = count;
  }
  return Object.keys(opts).length > 0 ? opts : undefined;
}

// Parse SCAN arguments: SCAN cursor [MATCH pattern] [COUNT count]
function parseScanArgs(args: string[]): { cursor: number; options?: { match?: string; count?: number } } {
  const cursor = Number(args[0]) || 0;
  const options: { match?: string; count?: number } = {};

  for (let i = 1; i < args.length; i++) {
    const arg = args[i].toUpperCase();
    if (arg === "MATCH" && i + 1 < args.length) {
      options.match = args[++i];
    } else if (arg === "COUNT" && i + 1 < args.length) {
      options.count = Number(args[++i]);
    }
  }

  return { cursor, options: Object.keys(options).length > 0 ? options : undefined };
}

async function execute(): Promise<any> {
  // STRING COMMANDS
  switch (cmd) {
    case "GET":
      return redis.get(args[0]);

    case "SET": {
      const opts = buildSetOptions();
      return opts
        ? redis.set(args[0], parseValue(args[1]), opts)
        : redis.set(args[0], parseValue(args[1]));
    }

    case "SETNX":
      return redis.setnx(args[0], parseValue(args[1]));

    case "SETEX":
      return redis.setex(args[0], Number(args[1]), parseValue(args[2]));

    case "PSETEX":
      return redis.psetex(args[0], Number(args[1]), parseValue(args[2]));

    case "MGET":
      return redis.mget(...args);

    case "MSET":
      return redis.mset(pairsToObject(args));

    case "MSETNX":
      return redis.msetnx(pairsToObject(args));

    case "INCR":
      return redis.incr(args[0]);

    case "INCRBY":
      return redis.incrby(args[0], Number(args[1]));

    case "INCRBYFLOAT":
      return redis.incrbyfloat(args[0], Number(args[1]));

    case "DECR":
      return redis.decr(args[0]);

    case "DECRBY":
      return redis.decrby(args[0], Number(args[1]));

    case "APPEND":
      return redis.append(args[0], args[1]);

    case "STRLEN":
      return redis.strlen(args[0]);

    case "GETRANGE":
      return redis.getrange(args[0], Number(args[1]), Number(args[2]));

    case "SETRANGE":
      return redis.setrange(args[0], Number(args[1]), args[2]);

    // HASH COMMANDS
    case "HGET":
      return redis.hget(args[0], args[1]);

    case "HSET":
      return redis.hset(args[0], pairsToObject(args.slice(1)));

    case "HSETNX":
      return redis.hsetnx(args[0], args[1], parseValue(args[2]));

    case "HMSET":
      return redis.hset(args[0], pairsToObject(args.slice(1)));

    case "HMGET":
      return redis.hmget(args[0], ...args.slice(1));

    case "HGETALL":
      return redis.hgetall(args[0]);

    case "HDEL":
      return redis.hdel(args[0], ...args.slice(1));

    case "HEXISTS":
      return redis.hexists(args[0], args[1]);

    case "HKEYS":
      return redis.hkeys(args[0]);

    case "HVALS":
      return redis.hvals(args[0]);

    case "HLEN":
      return redis.hlen(args[0]);

    case "HINCRBY":
      return redis.hincrby(args[0], args[1], Number(args[2]));

    case "HINCRBYFLOAT":
      return redis.hincrbyfloat(args[0], args[1], Number(args[2]));

    case "HSCAN": {
      const cursor = Number(args[1]) || 0;
      const scanOpts: { match?: string; count?: number } = {};
      for (let i = 2; i < args.length; i++) {
        if (args[i].toUpperCase() === "MATCH" && i + 1 < args.length) scanOpts.match = args[++i];
        if (args[i].toUpperCase() === "COUNT" && i + 1 < args.length) scanOpts.count = Number(args[++i]);
      }
      return redis.hscan(args[0], cursor, Object.keys(scanOpts).length > 0 ? scanOpts : undefined);
    }

    // LIST COMMANDS
    case "LPUSH":
      return redis.lpush(args[0], ...args.slice(1).map(parseValue));

    case "RPUSH":
      return redis.rpush(args[0], ...args.slice(1).map(parseValue));

    case "LPUSHX":
      return redis.lpushx(args[0], ...args.slice(1).map(parseValue));

    case "RPUSHX":
      return redis.rpushx(args[0], ...args.slice(1).map(parseValue));

    case "LPOP":
      return args.length > 1 ? redis.lpop(args[0], Number(args[1])) : redis.lpop(args[0]);

    case "RPOP":
      return args.length > 1 ? redis.rpop(args[0], Number(args[1])) : redis.rpop(args[0]);

    case "LRANGE":
      return redis.lrange(args[0], Number(args[1]), Number(args[2]));

    case "LLEN":
      return redis.llen(args[0]);

    case "LINDEX":
      return redis.lindex(args[0], Number(args[1]));

    case "LSET":
      return redis.lset(args[0], Number(args[1]), parseValue(args[2]));

    case "LREM":
      return redis.lrem(args[0], Number(args[1]), parseValue(args[2]));

    case "LTRIM":
      return redis.ltrim(args[0], Number(args[1]), Number(args[2]));

    case "LINSERT":
      return redis.linsert(
        args[0],
        args[1].toLowerCase() as "before" | "after",
        parseValue(args[2]),
        parseValue(args[3])
      );

    case "LPOS":
      return redis.lpos(args[0], parseValue(args[1]));

    case "LMOVE":
      return redis.lmove(
        args[0],
        args[1],
        args[2].toUpperCase() as "LEFT" | "RIGHT",
        args[3].toUpperCase() as "LEFT" | "RIGHT"
      );

    // SET COMMANDS
    case "SADD":
      return redis.sadd(args[0], ...args.slice(1).map(parseValue));

    case "SREM":
      return redis.srem(args[0], ...args.slice(1).map(parseValue));

    case "SMEMBERS":
      return redis.smembers(args[0]);

    case "SISMEMBER":
      return redis.sismember(args[0], parseValue(args[1]));

    case "SMISMEMBER":
      return redis.smismember(args[0], args.slice(1).map(parseValue));

    case "SCARD":
      return redis.scard(args[0]);

    case "SPOP":
      return args.length > 1 ? redis.spop(args[0], Number(args[1])) : redis.spop(args[0]);

    case "SRANDMEMBER":
      return args.length > 1 ? redis.srandmember(args[0], Number(args[1])) : redis.srandmember(args[0]);

    case "SINTER":
      return redis.sinter(...args);

    case "SINTERSTORE":
      return redis.sinterstore(args[0], ...args.slice(1));

    case "SUNION":
      return redis.sunion(...args);

    case "SUNIONSTORE":
      return redis.sunionstore(args[0], ...args.slice(1));

    case "SDIFF":
      return redis.sdiff(...args);

    case "SDIFFSTORE":
      return redis.sdiffstore(args[0], ...args.slice(1));

    case "SMOVE":
      return redis.smove(args[0], args[1], parseValue(args[2]));

    case "SSCAN": {
      const cursor = Number(args[1]) || 0;
      const scanOpts: { match?: string; count?: number } = {};
      for (let i = 2; i < args.length; i++) {
        if (args[i].toUpperCase() === "MATCH" && i + 1 < args.length) scanOpts.match = args[++i];
        if (args[i].toUpperCase() === "COUNT" && i + 1 < args.length) scanOpts.count = Number(args[++i]);
      }
      return redis.sscan(args[0], cursor, Object.keys(scanOpts).length > 0 ? scanOpts : undefined);
    }

    // SORTED SET COMMANDS
    case "ZADD": {
      const zaddOpts = buildZaddOptions();
      const members = scoreMemberPairs(args.slice(1));
      return zaddOpts
        ? redis.zadd(args[0], zaddOpts, ...members)
        : redis.zadd(args[0], ...members);
    }

    case "ZREM":
      return redis.zrem(args[0], ...args.slice(1));

    case "ZSCORE":
      return redis.zscore(args[0], args[1]);

    case "ZMSCORE":
      return redis.zmscore(args[0], ...args.slice(1));

    case "ZRANK":
      return redis.zrank(args[0], args[1]);

    case "ZREVRANK":
      return redis.zrevrank(args[0], args[1]);

    case "ZRANGE": {
      const opts = buildZrangeOptions();
      return opts
        ? redis.zrange(args[0], args[1], args[2], opts)
        : redis.zrange(args[0], args[1], args[2]);
    }

    case "ZRANGEBYSCORE": {
      const opts: { withScores?: boolean; offset?: number; count?: number } = {};
      if (values.withscores) opts.withScores = true;
      if (values.limit) {
        const [offset, count] = values.limit.split(",").map(Number);
        opts.offset = offset;
        opts.count = count;
      }
      return Object.keys(opts).length > 0
        ? redis.zrange(args[0], args[1], args[2], { byScore: true, ...opts })
        : redis.zrange(args[0], args[1], args[2], { byScore: true });
    }

    case "ZREVRANGE": {
      const opts = buildZrangeOptions();
      return redis.zrange(args[0], args[1], args[2], { rev: true, ...opts });
    }

    case "ZREVRANGEBYSCORE": {
      const opts: { withScores?: boolean; offset?: number; count?: number } = {};
      if (values.withscores) opts.withScores = true;
      if (values.limit) {
        const [offset, count] = values.limit.split(",").map(Number);
        opts.offset = offset;
        opts.count = count;
      }
      return redis.zrange(args[0], args[2], args[1], { byScore: true, rev: true, ...opts });
    }

    case "ZCARD":
      return redis.zcard(args[0]);

    case "ZCOUNT":
      return redis.zcount(args[0], args[1], args[2]);

    case "ZINCRBY":
      return redis.zincrby(args[0], Number(args[1]), args[2]);

    case "ZPOPMIN":
      return args.length > 1 ? redis.zpopmin(args[0], Number(args[1])) : redis.zpopmin(args[0]);

    case "ZPOPMAX":
      return args.length > 1 ? redis.zpopmax(args[0], Number(args[1])) : redis.zpopmax(args[0]);

    case "ZREMRANGEBYRANK":
      return redis.zremrangebyrank(args[0], Number(args[1]), Number(args[2]));

    case "ZREMRANGEBYSCORE":
      return redis.zremrangebyscore(args[0], args[1], args[2]);

    case "ZINTERSTORE":
      return redis.zinterstore(args[0], Number(args[1]), ...args.slice(2));

    case "ZUNIONSTORE":
      return redis.zunionstore(args[0], Number(args[1]), ...args.slice(2));

    case "ZSCAN": {
      const cursor = Number(args[1]) || 0;
      const scanOpts: { match?: string; count?: number } = {};
      for (let i = 2; i < args.length; i++) {
        if (args[i].toUpperCase() === "MATCH" && i + 1 < args.length) scanOpts.match = args[++i];
        if (args[i].toUpperCase() === "COUNT" && i + 1 < args.length) scanOpts.count = Number(args[++i]);
      }
      return redis.zscan(args[0], cursor, Object.keys(scanOpts).length > 0 ? scanOpts : undefined);
    }

    // KEY COMMANDS
    case "DEL":
      return redis.del(...args);

    case "UNLINK":
      return redis.unlink(...args);

    case "EXISTS":
      return redis.exists(...args);

    case "EXPIRE":
      return redis.expire(args[0], Number(args[1]));

    case "EXPIREAT":
      return redis.expireat(args[0], Number(args[1]));

    case "PEXPIRE":
      return redis.pexpire(args[0], Number(args[1]));

    case "PEXPIREAT":
      return redis.pexpireat(args[0], Number(args[1]));

    case "TTL":
      return redis.ttl(args[0]);

    case "PTTL":
      return redis.pttl(args[0]);

    case "PERSIST":
      return redis.persist(args[0]);

    case "KEYS":
      return redis.keys(args[0]);

    case "SCAN": {
      const { cursor, options } = parseScanArgs(args);
      return options ? redis.scan(cursor, options) : redis.scan(cursor);
    }

    case "TYPE":
      return redis.type(args[0]);

    case "RENAME":
      return redis.rename(args[0], args[1]);

    case "RENAMENX":
      return redis.renamenx(args[0], args[1]);

    case "COPY":
      return redis.copy(args[0], args[1]);

    case "DUMP":
      return redis.dump(args[0]);

    case "OBJECT": {
      const subcmd = args[0].toUpperCase();
      if (subcmd === "ENCODING") return redis.objectEncoding(args[1]);
      if (subcmd === "FREQ") return redis.objectFreq(args[1]);
      if (subcmd === "IDLETIME") return redis.objectIdletime(args[1]);
      if (subcmd === "REFCOUNT") return redis.objectRefcount(args[1]);
      throw new Error(`Unknown OBJECT subcommand: ${subcmd}`);
    }

    case "RANDOMKEY":
      return redis.randomkey();

    case "TOUCH":
      return redis.touch(...args);

    // SERVER COMMANDS
    case "DBSIZE":
      return redis.dbsize();

    case "FLUSHDB":
      return redis.flushdb();

    case "FLUSHALL":
      return redis.flushall();

    case "PING":
      return args.length > 0 ? redis.ping(args[0]) : redis.ping();

    case "ECHO":
      return redis.echo(args[0]);

    case "TIME":
      return redis.time();

    case "INFO":
      return redis.info(args[0]);

    // JSON COMMANDS (if using Upstash JSON)
    case "JSON.SET":
      return (redis as any).json.set(args[0], args[1], parseValue(args[2]));

    case "JSON.GET":
      return (redis as any).json.get(args[0], args.length > 1 ? args[1] : "$");

    case "JSON.DEL":
      return (redis as any).json.del(args[0], args.length > 1 ? args[1] : "$");

    default:
      throw new Error(`Unknown or unsupported command: ${cmd}`);
  }
}

try {
  const result = await execute();

  if (result === null || result === undefined) {
    console.log("(nil)");
  } else if (typeof result === "object") {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(result);
  }
} catch (err) {
  console.error(`Error: ${err instanceof Error ? err.message : err}`);
  process.exit(1);
}
