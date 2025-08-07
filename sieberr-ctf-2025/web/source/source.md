1. Since the challenge description was "Is there anything hidden in this webpage?", I guessed that there must be something hidden in the developer tools.

2. By inspecting the webpage, I found a hint:    
``` <!-- Welcome to the Inspect Element Challenge -->
    <!-- Maybe there's a secret hidden here? 🤔 -->
    <!-- Psst: Don't check out the route at /supersecretroute -->```
So I checked out that route, and found another hint "Where do web crawlers look to index your page?"

3. Hence, I checked the route /robots.txt and found the flag there: `sctf{chrome_devtools_are_really_useful}`