## Milestone 4 Reflection

As we are in the final stage of app development, we have implemented every feature we planned to since the planning stage of the project. We have created a U.S. job market dashboard for Data Science and related jobs that provides users with information surrounding the following:

- Top 10 high paying jobs
- Mean salary based on years of experience 
- A map of the job distribution
- Mean salary per company size 

We also included filtering options for company size, job titles, and experience level that affect all graphs aside from the Top 10 High Paying Jobs bar chart. 

A reoccurring theme in the feedback given to us by the TA and our peers was that for our top and bottom graphs (bar chart and boxplot), the x axes were difficult to see, as they did not quite fit their designated space and scrolling was challenging. We have since improved the fit of our charts and scrolling is no longer required; the axes are consistently visible. Another important piece of feedback we incorporated to improve our app was that we added a "clear all" option to the job title filtering and "any level" and "reset" options to our experience level filter. We believe this change makes our app functional and easy to use for as many purposes as possible, no matter the preferences the user has. These core changes help improve the functionality and ease of use of our final dashboard.

Some feedback that we implemented to improve the aesthetics of our app included adding more colours (we changed the colour of the bars in our Top 10 High Paying Jobs chart and the colour gradient in our Job Distribution map). For readability, we increased font sizes nearly everywhere, with the exception of our side panel which already used a large font. To help users gain a deeper understanding of the boxplot, we also added a couple descriptive lines below the chart title that explain what the whiskers and other features of the boxplot indicate.

Though we believe our app is very user friendly and simple to use and interpret, we occasionally run into a memory issue with Render, our deployment platform of choice. While running locally, the app can run as long as you like without issue but through Render, there is a 502 error that sometimes occurs after multiple filters have been changed repeatedly. Due to the limitations of free deployment, this is unfortunately not something we can control.