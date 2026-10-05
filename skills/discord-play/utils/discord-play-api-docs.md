# `discord.play` api docs

only the shapes and the common blunders. errors from `play_start`/`play_test` name the exact problem; fix it with a small `edit`.

## app shape

```js
import { app, step, text, embed, button, row, grid, after } from "@teapilot/discord-play";

export default app({
  init(ctx) { return step({ x: 0 }, after(2000, "tick")); },   // state, or step(state, ...effects)
  update(state, action, ctx) {
    if (action.kind === "button" && action.id === "right") return { ...state, x: state.x + 1 };
    if (action.kind === "timer" && action.id === "tick") return step(state, after(2000, "tick"));
    return state;
  },
  view(state, ctx) {
    return {
      content: text("**score** 0", grid(["🟦🟦🟥"])),
      rows: [row(button("left", "◀"), button("right", "▶", { style: "primary" }))],
    };
  },
});
```

- `view()` returns one message: `{ content?, embeds?, rows? }`. nothing else is read; `text`, `controls`, `embed` keys are ignored.
- sandboxed: synchronous, no `async`, no imports besides the sdk, no fs/network. state must be plain json.

## controls

- controls only exist inside `rows`: `rows: [row(...controls)]`. there is no top-level `controls` on the app or the view.
- `button(id, label, { style, emoji, disabled, opens })`, positional, not `button({ id, label })`.
- `select(id, ["a", "b"], { placeholder, min, max })`; a select sits alone in its row.
- `modal(id, title, [field(id, label, { style: "paragraph" })])` goes in a button's `opens`; it arrives as `{ kind: "modal", id, fields }`.
- limits: 5 rows, 5 buttons per row, control ids unique per view (`[A-Za-z0-9_.:-]`).
- every state needs a usable control, a pending timer or a consult, or `play_start` rejects the app.
- actions: `{ kind: "button" | "select" | "modal", id, user }` (select adds `values`), `{ kind: "timer", id }`, `{ kind: "consult", id, text }`.

## builders

- `text(...lines)` joins lines with `\n`, skipping falsy ones, and returns a **string**: use it as `content`, never as a wrapper object.
- `embed({ title, description, color, fields, footer, image })` takes an **options object**: `embed({ description: board })`, not `embed(board)`. goes in `embeds: [...]`.
- `grid(cells, palette)` turns rows of codes into an emoji board: `grid(["#.#"], { "#": "🟫", ".": "⬛" })`.
- `meter(value, max, width)` draws a bar; `spoiler(s)` hides text; `colors.red` etc. for embed colours.

## timers and effects

effects ride on `step(state, ...effects)` from `init` or `update`.

- `after(ms, id)`: **ms first**. one-shot, min 2000 ms; a game loop re-schedules `after(...)` in its own timer handler. there is no `timer()` builder.
- `cancel(id)`, `finish(summary)` (ends the app), `ephemeral(content)` (private reply to whoever acted), `consult(id, prompt)` (asks the model; answer arrives as a `consult` action).

## sizes

- `content` ≤ 2000 chars; embed description ≤ 4096, all embeds ≤ 6000. 🟦-style emoji are 2 chars each (a 24×15 board is ~735). render a camera window, not the whole level.
- state ≤ 64k chars; keep big static data (levels, maps) in code constants or a text asset, not state.
- text assets: `play_start({ file, title, assets: { level: "assets/level.txt" } })`, then `ctx.readText("level")` in the app.

## tools

- `play_test({ file, actions, expect })` dry-runs without posting. runs are limited per request: always pass `expect` assertions, and check the view it prints has your controls.
- `play_start({ file, title })` validates (it presses every control itself) and posts.
- `play_update({ id?, reset?, timers? })` reloads a running app from its file after an `edit`; `timers` starts a loop the new code adds.
- `play_inspect`, `play_list`, `play_resend`, `play_stop` for running apps.
