# Changelog

This project follows [Semantic Versioning](https://semver.org). It stays below 1.0 while the Claude Code mod API it runs on is in early access.

## 0.3.0 — renamed to Prompt Clarify

- The plugin is now named `prompt-clarify`, shown as "Prompt Clarify", so it can be listed in Anthropic's plugin directory, where the name "clarify" is already taken. The `/clarify` command and the `--clarify` marker work as before.
- If you installed it as `clarify`, uninstall that (`claude plugin uninstall clarify`) and install `prompt-clarify` from the same marketplace. Claude Code keeps plugin options by plugin name, so pick your rewrite model again if it wasn't `sonnet`.
- Added a privacy policy, [PRIVACY.md](PRIVACY.md), linked from the README and from the manifest's `privacyPolicyUrl`. The manifest also links GitHub issues as `supportUrl`.

## 0.2.0 — first public release

- If the engine refuses to send the rewrite request (for example, a model your account or organization blocks), the original draft now goes back in the prompt box. Before, a `--clarify` submission could be dropped with no draft restored.
- If anything unexpected fails during a `--clarify` rewrite, the status line is cleared and the original draft is copied to the clipboard.
- Added README, MIT license, marketplace file and manifest metadata.

## 0.1.0

- `/clarify <request>` and a trailing `--clarify` marker rewrite a draft and put it back in the prompt box, unsent.
- The rewrite model can be set to haiku, sonnet (default) or opus.
