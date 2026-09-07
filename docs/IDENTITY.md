# Identity cleanup — open, unresolved

Parked, but flagged here because the vault depends on it.

---

## The problem

Different emails for different things, accumulated over years, no master
account. No clear picture of what is signed in where.

## Why it belongs to this project

The vault stands on four accounts:

| Account | If you lose access to its email |
|---|---|
| **Backblaze** | The off-site backup is gone. Not "locked" — gone. |
| **Tailscale** | You cannot reach your own vault from anywhere. |
| **GitHub** | You lose the scripts. Recoverable, annoying. |
| **Apple ID** | The migration source. Recoverable, painful. |

The first one is the problem. A vault whose off-site copy hangs off an email
address you have half-forgotten is not actually protected — it just looks
protected, which is worse.

## When to deal with it

**Before creating the Backblaze and Tailscale accounts** in the real build.
Making them on a deliberately chosen address costs nothing now and is
genuinely painful to change later — Backblaze in particular.

That is the moment to fix it. Not before, not after.

## Roughly what "fixed" looks like

- One master email that owns everything infrastructural
- A password manager holding the full inventory, so the question "what am I
  signed into" has an answer
- Two-factor on the master account, with recovery codes printed on paper and
  stored with the vault passphrase
- Old addresses forwarded, not deleted, until nothing depends on them

Not a today problem. A before-you-buy-hardware problem.
