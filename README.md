<p align="center"><img src="assets/banner.png" alt="clarify: rough request in, clear prompt back in your prompt box, unsent" width="800"></p>

# clarify

A Claude Code plugin that turns a rough request into a clear prompt. It puts the rewrite back in your prompt box **without sending it**, so you read it, edit it, and press Enter yourself.

End any prompt with `--clarify`:

```
fix the login loop on safari, dont touch the api --clarify
```

Your prompt box then holds something like this, unsent:

```
Fix the login redirect loop that happens in Safari. Do not change the API.
Before editing, find where the redirect is triggered and explain the cause.
```

<p align="center"><img src="assets/before-after.png" alt="A rough draft ending in --clarify becomes a clearer draft in the prompt box, waiting for Enter" width="800"></p>

## Install

At the prompt of a Claude Code terminal session:

```
/plugin install clarify --marketplace luchasarie/claude-clarify
```

Answer `y` to add the marketplace, then pick a scope (user scope makes it work in every session). The command works right away, with no restart.

From a shell:

```
claude plugin install clarify --marketplace luchasarie/claude-clarify
```

In the desktop app, where `/plugin` doesn't run: click **+** next to the prompt box, then **Plugins**, **Add marketplace** with `luchasarie/claude-clarify`, then **Add plugin**.

**Requirements:** a Claude Code build that supports plugin hooks modules (mods). It was tested on Claude Code 2.1.305. The mod API is in early access and can change between releases, so if it stops loading after a Claude Code update, please open an issue.

## Usage

| You type | What happens |
| --- | --- |
| `<request> --clarify` (or `-clarify`) | The prompt isn't sent. The rewrite replaces it in the prompt box. |
| `/clarify <request>` | Same result, as a slash command. |

Press Enter to send the rewrite, or edit it first. If you change your mind, just clear the box.

The marker only counts when it's the **last word** of the prompt. These are left alone and sent as normal:

- `explain the --clarify flag` (the marker isn't at the end)
- slash commands and `!` shell commands, such as `/review --clarify`
- a marker inside an open code fence or an open double quote

If the rewrite fails (timeout, API error, empty reply), your original draft goes back in the prompt box. If you've started typing something new in the meantime, the plugin doesn't overwrite it: the rewrite is copied to your clipboard instead.

## Configuration

One option: **model**, the model that does the rewrite. It can be `haiku`, `sonnet` (default) or `opus`. You set it when you install. To change it later, use the plugin's row in the config menu, or run:

```
claude plugin configure clarify
```

Haiku is the fastest and cheapest. Opus rewrites best on long or tangled requests.

## Privacy and cost

- Your request goes to the model through your own Claude Code session, with your account's credentials. It counts toward your usage like any other request.
- The plugin sends nothing anywhere else, stores nothing, and has no telemetry.
- The request is sent as a JSON field with instructions to rewrite it and never act on it. Each rewrite is capped at 1,200 output tokens with a 30-second timeout.

## How it works

Everything lives in one file, [`hooks/register.ts`](hooks/register.ts):

- A `prompt.submit` hook spots a trailing `--clarify`. It drops the submission, so nothing reaches the conversation, and rewrites the text with `$.model.complete`.
- The rewrite goes into the prompt box with `$.prompt.fill`, but only if the box still holds your draft or is empty.
- `/clarify` is a registered command that runs the same rewrite.

The system prompt tells the model to keep your language, names, paths, commands and constraints, and to keep small requests small. If something important is ambiguous, it asks a short question in the rewrite instead of making something up.

## Uninstall

```
claude plugin uninstall clarify
```

## Development

```
git clone https://github.com/luchasarie/claude-clarify
cd claude-clarify
claude --plugin-dir .            # run a session with the mod loaded
claude plugin validate .         # manifest and hooks checks
claude plugin test .             # runs tests/*.test.ts
```

Type definitions are generated into `.claude-plugin/types/` the first time Claude Code loads the plugin (this folder is git-ignored). After that, `npx tsc -p .` type-checks the plugin.

## Acknowledgements

The idea, rewriting a draft before sending it and handing it back for review, comes from [pi-clarify](https://github.com/dodo-reach/pi-clarify) by dodo-reach. This is an independent implementation for Claude Code.

## License

[MIT](LICENSE)
