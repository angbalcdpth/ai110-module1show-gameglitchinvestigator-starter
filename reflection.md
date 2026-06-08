# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the game the behavior was inconsistent: the secret number would appear to change between guesses, and hints did not reliably point higher or lower. The provided "New Game" control did not reliably reset the game state without a full page refresh. I also observed that hint logic and score updates were inconsistent across outcomes (sometimes no penalty was applied). These issues made narrowing the correct number impossible and broke the expected game flow.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used ChatGPT and GitHub Copilot as coding assistants during debugging and while writing tests. One correct suggestion was to persist the secret number in `st.session_state` so it isn't reinitialized on every rerun; I implemented that change and verified stability by repeated manual play-throughs and a focused unit test against the game logic. One misleading suggestion recommended reinitializing the secret number in a callback rather than using session state; when I tried that the number still changed on some interactions, which I validated during manual testing and by observing failing test cases until the session-state approach was applied.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed when a focused unit test covering the behavior passed and manual play-throughs showed consistent behavior across runs. For example, after stabilizing the secret number I wrote a test that exercises the hint logic with fixed secret-and-guess pairs and asserts the expected hint string; running it highlighted an off-by-one case that I fixed and then re-tested. I also added a test that asserts identical score penalties for "Too High" and "Too Low" guesses; that test caught the earlier alternating-penalty bug. AI helped by suggesting edge cases and test assertions, which I implemented and validated locally.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because it was being reinitialized on every Streamlit rerun instead of being stored persistently; each widget interaction triggers a rerun and without session-scoped storage the code produced a new random value. I explain Streamlit reruns like this: every user interaction causes Streamlit to re-run the script top-to-bottom to recompute the UI and outputs, and `st.session_state` is a small dictionary that survives those reruns so you can store values (like a secret number) that should persist across interactions. To stabilize the secret number I created and used a key in `st.session_state` (for example, `if 'secret' not in st.session_state: st.session_state['secret']=randint(...)`) so the random value is assigned only once per game and not on every rerun.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

I want to keep the habit of writing a small, focused unit test for every bug I fix and running tests before and after changes; this made it much easier to verify fixes and prevented regressions. Next time I work with AI I will ask for reasoning behind suggestions and request minimal reproducible examples before accepting generated changes, which will speed verification and reduce wasted iterations. This project reinforced that AI-generated code is a useful collaborator for brainstorming fixes and tests, but its suggestions must be validated with tests and manual checks — AI accelerates work but doesn't replace critical verification.

## Summary

- Fixed score-keeping logic so both “Too High” and “Too Low” outcomes now apply the same penalty.
- Updated `update_score` to remove alternating behavior for “Too High” and always deduct 5 points for non-winning guesses.
- Added a new test to verify consistent penalty behavior across outcomes.
- Moved hint-related tests into `test_game_logic.py` so game logic and hint behavior are validated together.
- Added tests and manual checks to confirm stable hint and scoring behavior across runs.
