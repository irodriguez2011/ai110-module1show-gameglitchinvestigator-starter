# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I use Claude as a tool for thos project.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
When I asked Claude to fix the high/low bug, it also found that the app was turning the secret number into a string on every other attempt. That meant Python was comparing the numbers lexicographically, like words in a dictionary, so "9" > "10" came out True because it only looks at the first character. Claude suggested converting both the guess and the secret to integers before comparing them, so 9 < 10 like it should be. I verified it by running pytest with a test that checks a guess of 9 against a secret of "10" returns "Too Low", and by playing the game with the Developer Debug Info open to make sure the hints were right on every attempt.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
When I ran pytest I got a "No module named 'logic_utils'" error, so Claude added a new pytest.ini file to fix the import path. But the error was coming from Python 3.14, and this project uses Python 3.13 in the .venv. Claude had also been running the tests with 3.14, which is why it didn't catch that. I didn't keep the pytest.ini because it was an extra file that only covered up the real problem, and running `python -m pytest` inside the .venv already finds logic_utils.py without it. I deleted pytest.ini, activated the .venv, checked `python --version` showed 3.13, and ran `python -m pytest`, and all 23 tests passed.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed when there was a pytest test for it that passed and the game also behaved right when I played it. One test I ran was `test_new_game_after_win_lets_you_play_again`, which wins a game and then clicks New Game. It passing showed me that the new `start_new_game()` function really resets the game, because the old New Game button never reset the status and the game stayed stuck on "You already won." I also found a bug myself where pressing Enter didn't submit my guess, so we added `test_enter_submits_guess`. AppTest can't press a real Enter key, so the test checks that the guess box and Submit button are inside a form (which is what makes Enter work) and that submitting the form gives the right hint. I also tested it by hand in the browser. Claude helped me write the tests using Streamlit's AppTest, which runs the app without a browser and clicks the buttons for you. It also explained why my first pytest run failed with "No module named 'logic_utils'" and the difference between `pytest` and `python -m pytest`.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button or type something, Streamlit runs the whole Python file again from top to bottom. That means normal variables get reset every time, so the game would forget the secret number and your attempts. Session state is like a notebook that Streamlit keeps between reruns, so anything you save in `st.session_state` is still there after the next click. The tricky part is that you also have to reset it yourself when you want a fresh start, which is why New Game was broken.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - Asking the AI to explain its changes, like why it changed the Hard range or how `st.empty()` works, instead of just accepting them. That's how I caught changes I didn't fully agree with.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would check which Python version and environment the AI is using at the start, because it ran the tests with Python 3.14 instead of the project's 3.13 .venv. I would also avoid editing a file while the AI is changing it, since I accidentally overwrote its comments in app.py.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI generated code can look finished and still have a lot of hidden bugs, so I need to test it and play with it myself instead of trusting it. AI is really helpful for finding and explaining bugs, but I still have to question its suggestions and check that they fit my project.
