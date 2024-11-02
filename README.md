# GitHub User Analysis in Seattle

- We scraped data from GitHub's API using python to analyze user profiles of developers based in Seattle with more than 200 followers, focusing on followers and public repositories.
- An interesting finding was that longer bios tended to correlate with fewer followers, which suggests that brevity may be more appealing.
- Based on our analysis, seattle developers should create more public repositories, as we found that each additional repository leads to approximately 2.5 more followers on average.

## How the Data Was Collected
To gather the data, we used the GitHub REST API in python, which allows access to various user details. We specifically searched for users in Seattle with over 200 followers. For each user, we collected information on their profiles, including their number of followers, public repositories, and company affiliations.

## Key Findings
One of the most surprising insights was the correlation between bio length and follower count. After analyzing the data, we found that users with longer bios had fewer followers on average. This was evident from our statistical analysis, which indicated a negative slope when we performed regression on followers versus bio word count. This finding suggests that concise and engaging bios might resonate more with users and attract more followers.

Based on this surprising insight, our actionable recommendation for seattle developers is to focus on creating more public repositories. Our regression analysis showed that for every additional repository, users gained about 2.5 additional followers. This relationship indicates that increasing repository visibility could significantly enhance a developer's follower count and overall presence on GitHub.

2. **Statistical Analysis**:
   - **Correlation Coefficient**: The Pearson correlation between followers and public repositories was calculated, yielding a value of 0.203, indicating a weak positive relationship.
   - **Regression Analysis**: We performed linear regression to determine the impact of public repositories on follower counts, finding a slope of 2.499, which suggests that additional repositories can help users gain more followers.



