## Milestone 2 Reflection

For the initial dashboard we have created, we have implemented all features outlined in our proposal and sketch.

For our bar chart of the top 10 highest paying jobs, we created a helper function that groups raw job titles into standardized categories through a series of if/else statements. A limitation to this is that our created list of job types is limited, though we believe it covers a broad range of titles and is substantial enough to reasonably cover this dataset. This function was used to create a new column, `job_type`. This column was used in combination with the `mean_salary` column to find the top 10 highest paying jobs and create the corresponding bar chart.

For our boxplot of salaries per company size, we created a helper function to ensure all company sizes were given as an integer rather than a phrase such as "1 to 50" by finding the mean number of employees per company. We then created a new column, `company_size_numeric`, and combined this with `mean_salary` for each job posting and created the corresponding boxplot.

For our U.S. job distribution map, we extracted the state from each location given through separating each location into city, state, and country. For this plot, we also removed any remote jobs. After extracting each state, we created a new column, `state`, and a new variable titled job_count that groups jobs by state. We then created a density-based gradient based on job_count. 

For the scatterplot of salary vs years of experience, a helper function was created to extract the required years of experience from each job posting's description and find the average years required if it was provided in a range such as "5-7 years". However, this helper is not perfect as it sometimes returns unrelated numeric values that come from phrases like “60 miles". We have limited the maximum years of experience to 20 because of this, but our group is still working to find a better solution. A new column `years_experience`, was created from this and was combined with `mean_salary` to produce the scatterplot of salary vs years of experience.

Our side panel includes checkboxes and a search box for users to filter the dashboard by job title. We also included checkboxes for experience level for additional filtering. Also included is a slider that allows users to filter the dashboard according to company size.

Though we are happy with our progress and believe this is a solid initial dashboard, there are improvements that could be made. We could find a way to cover more job types to increase our bar chart’s accuracy and find a way to better ensure all years of experience are truly years of experience and not another number included in the job description. Finally, we should deploy our app on Heroku or an equivalent platform.
