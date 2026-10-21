import { expect, test } from 'claude-code/testing'

import { cleanRewrite, stripMarker } from '../hooks/register'

const usage = { input_tokens: 1, output_tokens: 1, cache_creation_input_tokens: 0, cache_read_input_tokens: 0 }

test('the marker is honoured only as the last token, outside code and commands', async () => {
  expect(stripMarker('fix the login bug --clarify')).toBe('fix the login bug')
  expect(stripMarker('fix the login bug -clarify  ')).toBe('fix the login bug')
  expect(stripMarker('explain the --clarify flag')).toBeUndefined()
  expect(stripMarker('/review --clarify')).toBeUndefined()
  expect(stripMarker('!ls --clarify')).toBeUndefined()
  expect(stripMarker('```\nrun --clarify')).toBeUndefined()
  expect(stripMarker('--clarify')).toBeUndefined()
})

test('wrapper noise is stripped from the rewrite', async () => {
  expect(cleanRewrite('```text\nDo X.\n```')).toBe('Do X.')
  expect(cleanRewrite('Rewritten prompt: Do X.')).toBe('Do X.')
})

test('/clarify puts the rewrite in the prompt box and sends nothing', async ($, on) => {
  const filled: string[] = []
  let asked = ''
  on('model.complete', ($, e) => {
    asked = e.prompt
    return { value: { isAnswered: true, text: 'Fix the login redirect loop in app/auth.ts.', usage } }
  })
  on('prompt.read', () => ({ value: { text: '', cursor: 0 } }))
  on('ui.status', () => ({ value: undefined }))
  on('prompt.fill', ($, e) => {
    filled.push(e.text)
    return { isFilled: true }
  })
  const out = await $.command.run({
    command: 'clarify',
    args: 'fix login thing in auth',
    origin: { kind: 'plugin', name: 'test' },
    presentation: { isFullscreen: false, columns: 80 },
  })
  expect(JSON.parse(asked)).toEqual({ request_to_rewrite: 'fix login thing in auth' })
  expect(filled).toEqual(['Fix the login redirect loop in app/auth.ts.'])
  expect(out.text).toContain('Draft clarified')
})

test('a submit that is not the person\'s own passes through untouched', async ($, on) => {
  const seen: string[] = []
  on('prompt.submit', ($, e) => {
    seen.push(e.text)
    return { text: e.text }
  })
  await $.prompt.submit({ text: 'do the thing --clarify', wait: false, origin: { kind: 'plugin', name: 'test' } })
  expect(seen).toEqual(['do the thing --clarify'])
})

test('a model the engine refuses restores the draft instead of losing it', async ($, on) => {
  const filled: string[] = []
  on('model.complete', () => {
    throw new Error('model blocked')
  })
  on('prompt.read', () => ({ value: { text: '', cursor: 0 } }))
  on('ui.status', () => ({ value: undefined }))
  on('prompt.fill', ($, e) => {
    filled.push(e.text)
    return { isFilled: true }
  })
  const out = await $.command.run({
    command: 'clarify',
    args: 'fix login thing in auth',
    origin: { kind: 'plugin', name: 'test' },
    presentation: { isFullscreen: false, columns: 80 },
  })
  expect(filled).toEqual(['fix login thing in auth'])
  expect(out.text).toContain('Clarify failed (')
  expect(out.text).toContain('original draft restored')
})
