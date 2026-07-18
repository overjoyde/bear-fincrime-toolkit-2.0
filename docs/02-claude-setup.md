# Setting up Claude.ai for TM/KYC work

## Projects, not one-off chats

Use **Claude.ai Projects**, not the default chat, for anything you will do more
than once. A Project gives you three things a bare chat does not:

- **Project instructions** - a persistent system prompt (this is what the
  files in `profiles/` are). Set once, applies to every chat in the project.
- **Project knowledge** - files Claude can reference across every
  conversation in the project, without you re-uploading or re-pasting them
  each time. This is where synthetic reference data, typology briefs, or
  the relevant `grounding/` files go.
- **Isolation** - a TM-analyst project and a reg-watch project should not
  share instructions or knowledge. Keep them as separate Projects, not tabs
  in the same one.

## Setting up a profile

1. Create a new Project.
2. Open `profiles/tm-analyst.md` (or whichever role fits) and paste the
   "Project Instructions" block into the Project's custom instructions field.
3. Upload the files that profile's "Recommended knowledge" section lists -
   typically the relevant `grounding/` file and a sample of synthetic output
   from `pipelines/`.
4. Start a new chat inside the project for each alert/case/task. Do not
   reuse one long-running chat across unrelated cases - context bleeds and
   quality degrades as the conversation grows.

## Custom instructions vs. Project instructions

Claude.ai also has account-level **custom instructions** (Settings ->
Profile). Keep those to genuinely global preferences (tone, output format
defaults). Anything role-specific belongs in the Project, not your account
settings - otherwise your TM-analyst instructions leak into unrelated chats.

## Model selection inside a Project

See `docs/05-model-selection.md` for the full breakdown. Short version: pick
the model per-message based on task weight, not once per project - Claude.ai
lets you switch models mid-conversation.

## What to attach vs. what to describe

Attach source documents as files (regulatory text, a typology report, a
synthetic CSV) rather than pasting them into the chat as text when they are
longer than a paragraph or two. It keeps the conversation history readable
and lets Claude cite specific passages back to you.
