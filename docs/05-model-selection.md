# Model and tier selection

Rule of thumb: match model weight to task weight, and re-decide per task,
not once per project. Claude.ai and Claude Code both let you switch models
mid-session - use that.

## A rough triage

### Fast, lighter model
Alert triage, quick lookups, checking whether a transaction matches a known
pattern, formatting or summarizing a document you already trust. These are
high-volume, low-ambiguity tasks - throughput matters more than depth, and
errors are cheap to catch on a re-read.

### Your strongest available model
Drafting SAR/STR narrative structure (not filing - structuring the write-up),
typology research synthesis, regulatory gap analysis, rule-tuning hypothesis
generation. These involve genuine reasoning over ambiguous, multi-factor
evidence where a subtly wrong conclusion is expensive.

### Whichever model has the largest context/reasoning budget
Long-running exploratory work - reading through a full typology report,
cross-referencing multiple regulatory instruments, iterating on a detection
script. Do not split a task like this across a fast model's shorter attention
just to save time - you will pay it back in re-explaining context.

## Cost and latency are real constraints - plan around them, do not ignore them

If your institution is on a metered API rather than a flat Claude.ai seat,
the fast/cheap tier for high-volume triage is not optional - it is what makes
routing hundreds of alerts through an LLM economically sane at all. Reserve
the expensive tier for the fraction of cases that actually need deep
reasoning, and let a cheaper pass do the initial sort.

## Do not over-fit to one specific model name

Model names and tiers change faster than this document will be updated.
The categories above (fast/cheap, strongest-available, long-context) are the
durable distinction - check your current provider's docs for which specific
model currently fills which slot.
