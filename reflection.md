# Reflection on the Week 7 Codex CLI Assignment

The hardest part of this assignment was reviewing the results and checking that they were correct. 
Codex made the mechanics surprisingly easy, it handled commands and created the requested files. 
But the results depended on how clearly I described what I wanted, 
so I had to be specific about the analysis and the way it should be presented.

The work developed through several prompts. I began by asking for an inspection of the Ames housing data. 
That first attempt failed because pandas was unavailable, 
but Codex continued the inspection with Python’s built-in `csv` module. 
I then refined the analysis request to include each neighborhood’s sale count and 
to flag neighborhoods with fewer than 10 sales as small samples without excluding them. 
When I reviewed the first chart, I noticed it was missing a horizontal price axis. 
I prompted Codex to add a zero-based currency axis while keeping the chart’s values, counts, ordering, and colors.

Checking the analysis also required more than looking at the summary. 
The median positions and values for MeadowV and StoneBr were reviewed with ChatGPT’s assistance; 
I didn't independently verify them myself. 
That distinction matters when describing how much checking I personally performed.

I used a separate ChatGPT conversation to clarify a few technical
steps and check whether I was following
the workflow correctly. The analytical code and outputs were
produced in Codex CLI using my Clemson Edu account.

This experience taught me that using AI for analytical work still leaves substantial responsibility with the user. 
The instructions shape what the tool produces, and the user must review whether 
the output answers the question and whether its details are correct. Next time, 
I would be more careful and precise about what I ask for, then plan time to verify the results 
and presentation instead of assuming that a smooth workflow guarantees a correct result.
