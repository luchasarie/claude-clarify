# Privacy policy

Prompt Clarify is a Claude Code plugin. All of its code is in [`hooks/register.ts`](hooks/register.ts), and it runs inside your own Claude Code session.

## What it processes

Only the draft you ask it to rewrite: a prompt that ends with `--clarify` (or `-clarify`), or the text after `/clarify`. Prompts without the marker pass through untouched. Before it puts the rewrite in your prompt box, the plugin reads the box to check that it still holds your draft or is empty. It doesn't read your files, your conversation or anything else.

## Where it goes

The draft is sent to the Claude model you choose in the plugin's settings (`haiku`, `sonnet` or `opus`). It goes through Claude Code's own model call, with your account's credentials and whatever provider your Claude Code is set up to use, the same way any prompt you send does. The provider's own privacy terms apply to that request.

The rewrite comes back to your prompt box. If you've typed something new there meanwhile, or something unexpected fails, the rewrite or your original draft is copied to your clipboard instead.

## What it doesn't do

- It stores nothing itself: no files, no logs, no history.
- It makes no other network requests and sends nothing to the author or to any third party.
- It has no telemetry, analytics or tracking.

The only setting it keeps is the model you choose, and Claude Code stores that in your own settings.

## Contact

Questions or concerns: open an issue at <https://github.com/luchasarie/claude-clarify/issues>.

If this policy changes, the change is recorded in this file and in the [changelog](CHANGELOG.md).
