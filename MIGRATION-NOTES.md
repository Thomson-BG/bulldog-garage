# Bulldog Garage — Migration Notes

Pages rebuilt in the new design: 5

## Legacy links that were already dead on the old site (0)
These targets returned 404 on cte-auto.net and were omitted from the new boards:
## iSpring "(Published)" quizzes — recovered via remapping

Eight quizzes on the old site were published with iSpring's **online** player,
which streamed the quiz engine (`player.js`) and content from iSpring's servers.
Those servers are gone, so only an empty shell of each was archivable. Each has
been remapped to a working Flash quiz that covers the same material:

- Safety Test Parts 1–5  →  the original Flash Safety Test SWFs (fully recovered)
- AST 1B Electrical Final (Published)  →  Electrical review quiz (Conductors/Insulators)
- Suspension–Steering Final (Published)  →  Steering System Fundamentals quiz

All quiz links now point to working assessments.

## Why quizzes need the site hosted

Flash quizzes run through the bundled Ruffle emulator, and Ruffle's engine
(plus the SWF files) load over the network. Browsers — including ChromeOS on
school Chromebooks — block that loading on the `file://` protocol for security.
The fix is to host the site at a web address (see start-server.html / "Host it
once"). Once hosted, all quizzes and videos work with no per-device setup.
