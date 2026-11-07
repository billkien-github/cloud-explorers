---
name: revise-script
description: Revise a Cloud Explorers episode's beat sheet (.md) and Fountain screenplay (.fountain) after a /review round at the script gate, keeping both files in sync, self-checking with measurements and state tables, then preparing the next review round. Use when the user types /revise-script, or asks to fix, update or revise a script or beat sheet after review.
argument-hint: <EPxxx> [notes, e.g. "Blockers only" or "apply suggestions 2, 5"]
---

# Revise a script after review

General rules for fixing and for when to re-run review live in `.claude/skills/review/SKILL.md`, section "Sửa và review lại" (read it first). This skill is the concrete procedure for the script gate: the beat sheet `03_CONTENT/Scripts/EPxxx_<name>.md` and the `.fountain` file of the same name. Yardsticks for self-checking: `03_CONTENT/README.md`, sections "Cỡ" and "Soát trước khi review kịch bản"; the Character Bible for characters, gadgets and acting limits. The project works in Vietnamese: write all edits to the beat sheet, the Fountain file, the round list and the report to the user in Vietnamese.

Why this exists: most errors in a later round come from the previous fix, especially when layout measurements are not worked out as numbers, prop states are not traced line by line, and the beat sheet is fixed one way while the Fountain file is fixed another (EP000E round 2: all 7 Blockers of round 1 were fixed, but 6 new Blockers appeared, all of these two kinds).

## Inputs

- Results of the review round just run (in the chat), including the merged issue list from step 5 of the review skill.
- Issue lists of earlier rounds, if any (files in the session scratchpad created by step 7 below).
- User notes: which Suggestions (Gợi ý) to apply, creative decisions already made.

If there are no review results yet, stop and suggest running `/review EPxxx` first. If a review round is still running, wait for every reviewer to finish before starting.

## Steps

1. **Build an issue table.** One row per Blocker (Chặn) and Should-fix (Nên sửa): severity, reviewer, location (file, line), root cause, intended fix. Issues sharing a root cause go in one row (e.g. "backpack loses continuity" raised by three reviewers). Keep Suggestions in a separate list.

2. **Ask the user once before editing** (batch the questions): which Suggestions to apply (multi-select); places where two reviewers contradict each other; issues whose fix is a creative decision or changes something locked in another episode (length, a gadget rule, the look of a location that already has an image). Issues with one clear fix under existing rules: fix them without asking.

3. **Rules first, wording second.** An issue that adds or changes a rule: write it in the owning file first (gadgets, characters, acting limits: Character Bible; Wonder Hub, Chronicle Engine, Season 0, writing rules: `03_CONTENT/README.md`; episode-specific rules: the "Luật nhân quả" and "Bố trí" sections of the beat sheet). A threshold rule must cover every case (one, some, all meeting the condition; once triggered, does it hold or release) and state the measuring point (where on the object it is measured).

4. **Revise the beat sheet**, section by section: Luật nhân quả → Bố trí (measurements) → Gài trước, trả sau → Các cảnh (Thời gian column matching the new length) → links to the previous and next episode → Sản xuất (a size for every new item) → checklist (add an item for each kind of error just found). The status line at the top says which draft this is and which review round it was revised after.

5. **Revise the Fountain file to match the revised beat sheet**, scene by scene, not only the flagged lines:
   - Layout, safety, reach and size constraints belong in action lines; `/* */` notes only explain the numbers and never replace an action line (previz follows action lines).
   - Dialogue in the "Các cảnh" table and in the Fountain file is word-for-word identical.
   - A new item gets its size in the action line where it first appears.
   - `Draft date` names the new draft.

6. **Self-check with tables** (the most important step; work them out in your head or in the scratchpad, never in the repo):
   - **Threshold table:** every threshold rule × every place a character or object stands (including the waiting pose before a countdown, where they stand in earlier scenes before the rule is used, and the moment a moving object such as a rising platform crosses the threshold): work out distance, height offset and body width (`02_ASSET_LIBRARY/MODELING.md`, "Bảng cỡ") as numbers; record the result (lit or dark, caught or not, overlapping or not) and compare with what the action line says. A rule that triggers as soon as its condition is met: the line where the condition is met must be the line where the event happens. EP000E examples: the door opens when the four sockets light; Lumo stood on top of Piko; Piko caught a ring just by taking position, before the countdown.
   - **State table:** every prop with a state (worn or set down where, open or closed, goggles on cap or eyes, held at what height, who is holding it) in Fountain line order, before and after each line; objects never move on their own. Things only the audience sees: note hidden or visible on every line where a character comes near.
   - **Gadget and machine use table:** for each use, check every clause in the Character Bible (naming the machine, setting the pack down before turning, the ritual before looking, tying the pouch…). A machine fault only shows up on a test run.
   - **Acting limits:** grep each character's name in the Fountain file, read every verb attached, compare with the Character Bible (a legless character does not "step", a flying character does not "sit", no body parts the character lacks, short arms do not reach past their limit).
   - **Both files in sync:** every beat in the "Các cảnh" table appears in the Fountain file and vice versa; measurements in the Fountain file match the "Bố trí" table; one sound effect is never used for two different meanings.
   - **Episode links:** end-of-episode state against the opening of the next episode; locations and props against the previous episode (`03_CONTENT/README.md`, section "Soát trước khi review kịch bản").
   - **Length:** add up the beats of each scene in the Fountain file against the Thời gian column; over the user's target, merge connecting lines that carry no gag before cutting gags.
   - Grep every name, measurement and line of dialogue just changed across all `.md` and `.fountain` files in the repo, and fix places still quoting the old version (README status, `MODELING.md`, other episodes' beat sheets).

7. **Write the round's issue list** to the session scratchpad (not the repo), named `<episode code>_luot<N>.md`: the Blockers and Should-fixes (severity, reviewer, a faithful summary of what the reviewer said, with the key quote) and the Suggestions applied. The re-review round hands this file to the reviewers per step 3 of section "Chạy" in the review skill.

8. **Learn from the round and choose how to re-run** per steps 4 and 5 of "Sửa và review lại" in the review skill. If a kind of error already has a rule and still recurs, make that rule clearer in `03_CONTENT/README.md`, or add a step to this skill.

9. **Report back to the user:** where each issue was fixed (grouped by root cause), which rule changed in which owning file, which Suggestions were applied, what is still uncertain, and how the next review round will run (full group or confirmation round). Update the "Trạng thái" section of `README.md`.
