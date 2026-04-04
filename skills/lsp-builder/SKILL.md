---
name: lsp-builder
description: >
  Guides building Language Server Protocol (LSP) servers from scratch based on the LSP 3.17 specification.
  Use this skill when the user wants to create, debug, or extend an LSP server in any language.
  Trigger on mentions of "language server", "LSP", "language server protocol", "textDocument",
  "completion provider", "hover provider", "diagnostics", or any LSP method name.
  This skill covers the full server lifecycle: base protocol transport, capabilities negotiation,
  text document synchronization, language features, workspace features, and window features.
---

# LSP Builder Skill

A step-by-step guide for building Language Server Protocol servers. Reference: LSP 3.17 specification.

## When to Use This Skill

Use whenever a user asks to:
- Build a new language server or LSP implementation
- Add language features (hover, completion, go-to-definition, etc.) to an editor via LSP
- Debug or extend an existing LSP server
- Understand how LSP transport, capabilities, or features work

## Architecture Overview

An LSP server is a process that communicates with a client (editor) using JSON-RPC messages over a transport layer. The protocol has three layers:

1. **Transport** — How bytes move between client and server (stdio, sockets, pipes)
2. **Base Protocol** — JSON-RPC message framing with `Content-Length` headers
3. **Language Protocol** — Semantic requests/responses (hover, completion, diagnostics, etc.)

## Phase 1: Base Protocol Transport

Read `references/specification.md` sections on Base Protocol and Header Part.

The wire format is:
```
Content-Length: <byte-length-of-json>\r\n
\r\n
<json-rpc-message>
```

**Requirements:**
- Header is ASCII-encoded, terminated by `\r\n`
- Content is UTF-8 JSON-RPC 2.0
- `Content-Length` is mandatory; `Content-Type` defaults to `application/vscode-jsonrpc; charset=utf-8`

**Implementation steps:**
1. Open stdin/stdout (or socket) for bidirectional communication
2. Read headers until `\r\n\r\n` is found
3. Parse `Content-Length` value
4. Read exactly that many bytes as the JSON content
5. Parse JSON to determine message type (request, response, or notification)
6. Repeat

**Message types:**

| Type | Has `id`? | Has `method`? | Requires response? |
|------|-----------|---------------|-------------------|
| Request | yes | yes | yes |
| Response | yes | no | no |
| Notification | no | yes | no |

### Reference: Message Transport (Python)

```python
import json
import sys

def read_message():
    """Read one JSON-RPC message from stdin using Content-Length framing."""
    headers = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None  # EOF
        line = line.decode("ascii")
        if line == "\r\n":
            break
        name, value = line.strip().split(": ", 1)
        headers[name.lower()] = value
    content_length = int(headers["content-length"])
    body = sys.stdin.buffer.read(content_length)
    return json.loads(body.decode("utf-8"))

def write_message(msg):
    """Write one JSON-RPC message to stdout using Content-Length framing."""
    body = json.dumps(msg, separators=(",", ":")).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n"
    sys.stdout.buffer.write(header.encode("ascii"))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()
```

## Phase 2: Server Lifecycle

Read `references/specification.md` sections on Server Lifecycle.

The lifecycle sequence is strictly defined:

```
Client                          Server
  |                                |
  |--- initialize (request) ----->|
  |<-- initialize (response) -----|
  |--- initialized (notify) ----->|
  |                                |  (server is now ready)
  |                                |
  |  ... normal operation ...      |
  |                                |
  |--- shutdown (request) ------->|
  |<-- shutdown (response) -------|
  |--- exit (notify) ------------>|
  |                                |  (server exits)
```

### initialize Request

Method: `initialize`
- Client sends capabilities and workspace info
- Server responds with its capabilities
- **Must not** send other requests/notifications before receiving `initialize`

**InitializeParams** (from client):
```json
{
  "processId": 12345,
  "rootUri": "file:///path/to/workspace",
  "capabilities": { ... },
  "clientInfo": { "name": "VSCode", "version": "1.74.0" }
}
```

**InitializeResult** (server response):
```json
{
  "capabilities": {
    "textDocumentSync": 1,
    "completionProvider": { "triggerCharacters": [".", ":"] },
    "hoverProvider": true,
    "definitionProvider": true,
    "referencesProvider": true,
    "documentSymbolProvider": true,
    "codeActionProvider": true,
    "documentFormattingProvider": true
  },
  "serverInfo": { "name": "my-lang-server", "version": "0.1.0" }
}
```

### initialized Notification

Method: `initialized`
- Server can now register capabilities, send `window/showMessage`, etc.

### shutdown and exit

- `shutdown`: Server returns `null` result. Must stop processing new requests.
- `exit`: Server exits with code 0 (success) or 1 (if shutdown wasn't received).

### Reference: Lifecycle Dispatch (Python)

```python
def main():
    shutting_down = False
    while True:
        msg = read_message()
        if msg is None:
            break
        method = msg.get("method")
        msg_id = msg.get("id")    # Notifications have NO id
        params = msg.get("params", {})

        if msg_id is None:
            # This is a NOTIFICATION (no response required)
            if method == "exit":
                return 0 if shutting_down else 1
            # Other notifications: "initialized", "textDocument/didOpen", etc.
            handle_notification(method, params)
            continue

        # This is a REQUEST (must send a response)
        if method == "shutdown":
            shutting_down = True
            write_message({"jsonrpc": "2.0", "id": msg_id, "result": None})
            continue
        result = handle_request(method, params)
        write_message({"jsonrpc": "2.0", "id": msg_id, "result": result})
```

## Phase 3: Text Document Synchronization

Read `references/specification.md` sections on Text Document Synchronization.

The server MUST implement all three or none:
- `textDocument/didOpen` — **Notification** from client: document opened
- `textDocument/didChange` — **Notification** from client: content changed
- `textDocument/didClose` — **Notification** from client: document closed

These are **notifications**, not requests — they have no `id`. The server must NOT send responses to them.

**Configure via `textDocumentSync` capability:**

```json
{
  "textDocumentSync": {
    "openClose": true,
    "change": 2
  }
}
```

`change` values:
- `0` (None): No sync
- `1` (Full): Send entire document content on each change
- `2` (Incremental): Send only changed ranges

### Core Types

```typescript
interface Position {
    line: uinteger;        // 0-indexed
    character: uinteger;   // 0-indexed UTF-16 offset by default
}

interface Range {
    start: Position;
    end: Position;
}

interface TextDocumentIdentifier {
    uri: DocumentUri;      // e.g. "file:///path/to/file.py"
}

interface TextDocumentItem {
    uri: DocumentUri;
    languageId: string;
    version: integer;
    text: string;
}

interface VersionedTextDocumentIdentifier extends TextDocumentIdentifier {
    version: integer | null;
}
```

### Full Sync (change: 1)

The simplest approach. On each `didChange`, the client sends the entire document text:

```json
{
  "textDocument": { "uri": "file:///foo.py", "version": 2 },
  "contentChanges": [{ "text": "entire document content here" }]
}
```

Server just stores `contentChanges[-1]["text"]`.

### Incremental Sync (change: 2)

The client sends only the changed range. The server must apply these edits to its in-memory copy:

```json
{
  "textDocument": { "uri": "file:///foo.py", "version": 2 },
  "contentChanges": [{
    "range": {
      "start": { "line": 0, "character": 5 },
      "end": { "line": 0, "character": 10 }
    },
    "rangeLength": 5,
    "text": "world"
  }]
}
```

### Reference: Incremental Sync Implementation (Python)

```python
class DocumentStore:
    def __init__(self):
        self._docs = {}  # uri -> text

    def open(self, uri, text):
        self._docs[uri] = text

    def close(self, uri):
        self._docs.pop(uri, None)

    def apply_incremental(self, uri, changes):
        text = self._docs.get(uri, "")
        for change in changes:
            if "range" in change:
                text = self._apply_range(text, change)
            else:
                # Full content replacement
                text = change.get("text", text)
        self._docs[uri] = text

    @staticmethod
    def _apply_range(text, change):
        lines = text.split("\n")
        rng = change["range"]
        s_line = rng["start"]["line"]
        s_char = rng["start"]["character"]
        e_line = rng["end"]["line"]
        e_char = rng["end"]["character"]
        new_text = change.get("text", "")

        before = "\n".join(lines[:s_line])
        if s_line > 0:
            before += "\n"
        prefix = lines[s_line][:s_char] if s_line < len(lines) else ""
        suffix = lines[e_line][e_char:] if e_line < len(lines) else ""
        after = "\n".join(lines[e_line + 1:]) if e_line + 1 < len(lines) else ""

        result = before + prefix + new_text + suffix + after
        return result

    def get(self, uri):
        return self._docs.get(uri)
```

**Position encoding:** Lines are 0-indexed. Characters are 0-indexed UTF-16 offsets by default. Since 3.17, you can negotiate UTF-8 or UTF-32 via `positionEncoding` in capabilities.

## Phase 4: Language Features

Each feature requires:
1. Server advertises the capability in `initialize` response
2. Server implements the handler for the corresponding method

### Hover (`textDocument/hover`)

Return documentation for the symbol at a given position.

**Capability:** `"hoverProvider": true`
**Request:** `HoverParams` with `textDocument` and `position`
**Response:** `Hover` with `contents` (MarkupContent or MarkedString) and optional `range`

```typescript
interface Hover {
    contents: MarkedString | MarkedString[] | MarkupContent;
    range?: Range;
}

interface HoverParams extends TextDocumentPositionParams {
    // textDocument: TextDocumentIdentifier
    // position: Position
}
```

### Completion (`textDocument/completion`)

Provide code completions at a cursor position.

**Capability:**
```json
"completionProvider": {
  "triggerCharacters": ["."],
  "resolveProvider": true,
  "completionItem": { "labelDetailsSupport": true }
}
```
**Request:** `CompletionParams` with `textDocument`, `position`, `context`
**Response:** `CompletionList` with `items[]` and `isIncomplete` flag, or `CompletionItem[]`

**Important:** Always include `triggerCharacters` when advertising `completionProvider` — clients use this to know when to automatically request completions.

```typescript
interface CompletionItem {
    label: string;
    kind?: CompletionItemKind;  // 1=Text, 2=Method, ..., 14=Keyword, 6=Variable, ...
    detail?: string;
    documentation?: string | MarkupContent;
    deprecated?: boolean;
    preselect?: boolean;
    sortText?: string;
    filterText?: string;
    insertText?: string;
    insertTextFormat?: InsertTextFormat;  // 1=PlainText, 2=Snippet
    textEdit?: TextEdit | InsertReplaceEdit;
    additionalTextEdits?: TextEdit[];
    commitCharacters?: string[];
    command?: Command;
    data?: LSPAny;
}
```

**CompletionItemKind values (common):**
| Value | Kind | Value | Kind |
|-------|------|-------|------|
| 1 | Text | 7 | Interface |
| 2 | Method | 8 | Function |
| 3 | Function | 10 | Module |
| 5 | Class | 13 | Value |
| 6 | Variable | 14 | Keyword |
| | | 15 | Snippet |

### Go to Definition (`textDocument/definition`)

**Capability:** `"definitionProvider": true`
**Request:** `DefinitionParams`
**Response:** `Location`, `Location[]`, or `LocationLink[]`

```typescript
interface Location {
    uri: DocumentUri;
    range: Range;
}
```

### References (`textDocument/references`)

**Capability:** `"referencesProvider": true`
**Request:** `ReferenceParams` with `context.includeDeclaration`
**Response:** `Location[]`

### Diagnostics (Push Model)

The server sends diagnostics to the client via `textDocument/publishDiagnostics` notification. No request is needed — the server pushes whenever diagnostics change.

**Notification:** `PublishDiagnosticsParams` with `uri`, `version`, and `diagnostics[]`

```typescript
interface Diagnostic {
    range: Range;
    severity?: DiagnosticSeverity;  // 1=Error, 2=Warning, 3=Information, 4=Hint
    code?: integer | string;
    codeDescription?: { href: URI };
    source?: string;          // e.g. "my-lang-linter"
    message: string;
    tags?: DiagnosticTag[];   // 1=Unnecessary, 2=Deprecated
    relatedInformation?: DiagnosticRelatedInformation[];
    data?: LSPAny;
}
```

### Document Symbols (`textDocument/documentSymbol`)

**Capability:** `"documentSymbolProvider": true`
**Response:** `DocumentSymbol[]` (hierarchical) or `SymbolInformation[]` (flat)

```typescript
interface DocumentSymbol {
    name: string;
    detail?: string;
    kind: SymbolKind;      // 5=Class, 12=Function, 13=Variable, 14=Constant, ...
    tags?: SymbolTag[];
    deprecated?: boolean;
    range: Range;          // Full range of this symbol (including body)
    selectionRange: Range; // Range that should be selected (the name)
    children?: DocumentSymbol[];
}
```

**SymbolKind values (common):**
| Value | Kind | Value | Kind |
|-------|------|-------|------|
| 5 | Class | 12 | Function |
| 6 | Method | 13 | Variable |
| 7 | Property | 14 | Constant |
| 8 | Field | 23 | Struct |
| 10 | Enum | 26 | TypeParameter |
| 11 | Interface | | |

### Formatting (`textDocument/formatting`)

**Capability:** `"documentFormattingProvider": true`
**Request:** `DocumentFormattingParams` with `options` (tabSize, insertSpaces, etc.)
**Response:** `TextEdit[]`

```typescript
interface TextEdit {
    range: Range;
    newText: string;
}
```

### Code Actions (`textDocument/codeAction`)

**Capability:**
```json
"codeActionProvider": {
  "codeActionKinds": ["quickfix", "refactor"]
}
```
**Request:** `CodeActionParams` with `textDocument`, `range`, `context.diagnostics`
**Response:** `(Command | CodeAction)[]`

### Other Features (implement as needed)

| Feature | Method | Capability Key |
|---------|--------|---------------|
| Signature Help | `textDocument/signatureHelp` | `signatureHelpProvider` |
| Rename | `textDocument/rename` | `renameProvider` |
| Code Lens | `textDocument/codeLens` | `codeLensProvider` (has resolve) |
| Document Highlights | `textDocument/documentHighlight` | `documentHighlightProvider` |
| Document Links | `textDocument/documentLink` | `documentLinkProvider` (has resolve) |
| Folding Ranges | `textDocument/foldingRange` | `foldingRangeProvider` |
| Selection Ranges | `textDocument/selectionRange` | `selectionRangeProvider` |
| Semantic Tokens | `textDocument/semanticTokens/*` | `semanticTokensProvider` |
| Inlay Hints | `textDocument/inlayHint` | `inlayHintProvider` (has resolve) |
| Type Hierarchy | `textDocument/typeHierarchy/*` | `typeHierarchyProvider` |
| Call Hierarchy | `textDocument/callHierarchy/*` | `callHierarchyProvider` |

## Phase 5: Workspace Features

| Feature | Method | Capability Key |
|---------|--------|---------------|
| Symbol Search | `workspace/symbol` | `workspaceSymbolProvider` |
| Execute Command | `workspace/executeCommand` | `executeCommandProvider` |
| Configuration | `workspace/configuration` | N/A (server requests config) |
| Did Change Config | `workspace/didChangeConfiguration` | `textDocumentSync` options |
| File Operations | `workspace/didCreateFiles` etc. | `workspace.fileOperations` |

## Phase 6: Window Features (Server → Client)

These are notifications the server sends TO the client:

| Feature | Method | Direction |
|---------|--------|-----------|
| Show Message | `window/showMessage` | Server → Client |
| Log Message | `window/logMessage` | Server → Client |
| Progress | `$/progress` | Bidirectional |

## Error Handling

Use `ResponseError` with standard error codes:

```
-32700  Parse Error
-32600  Invalid Request
-32601  Method Not Found
-32602  Invalid Params
-32603  Internal Error
-32002  Server Not Initialized
-32800  Request Cancelled
-32801  Content Modified
-32802  Server Cancelled
-32803  Request Failed
```

## Implementation Checklist

When building a server, work through this order:

1. [ ] Set up transport (stdio, socket, or pipe)
2. [ ] Implement header parsing (`Content-Length` based message framing)
3. [ ] Implement JSON-RPC message dispatch (request/notification/response routing)
4. [ ] Implement `initialize` handler with capabilities
5. [ ] Implement `initialized` handler
6. [ ] Implement `shutdown` and `exit` handlers
7. [ ] Implement text document sync (`didOpen`, `didChange`, `didClose`)
8. [ ] Implement at least one language feature (hover is simplest)
9. [ ] Implement diagnostics (push via `textDocument/publishDiagnostics`)
10. [ ] Add more language features as needed
11. [ ] Implement workspace features if applicable
12. [ ] Test with an LSP client (VS Code extension, Emacs lsp-mode, Neovim LSP)

## Key References

Read `references/specification.md` for:
- Complete type definitions for every request/response/notification
- Detailed capability structures
- The full list of features with their client/server capability paths
- Registration options for dynamic capabilities
- Work done progress and partial result progress mechanisms
- Notebook document support (3.17)

## Common Pitfalls

- **Don't send requests before `initialize`** — Clients will reject them
- **Don't notify without being asked** — Only send `publishDiagnostics` after document sync
- **Positions are 0-indexed** — Both line and character start at 0
- **UTF-16 character offsets by default** — Unless you negotiate UTF-8/UTF-32 via `positionEncoding`
- **Every request needs a response** — Even if returning `null`
- **Notifications must NOT get responses** — They have no `id` field. `didOpen`, `didChange`, `didClose`, `initialized`, `exit` are all notifications
- **Cancellation returns error, not no response** — Use `RequestCancelled` error code
- **Always use Content-Length framing** — Never read raw lines from stdin; use binary readline + exact byte reads
- **Incremental sync needs careful position math** — Convert 0-indexed line/character to string offsets before splicing
