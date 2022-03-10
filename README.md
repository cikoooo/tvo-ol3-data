# tvo-ol3-data

##This is the repository for the code I used to collect data of Olkiluoto 3 Nuclear facility and its energy production during its implementation.

TVO-OL3.py collects data from TVO's websites, and transforms it into a DataFrame. The DataFrame is stored as a csv (couple of times...). Not the most elegant solution, but it works.
DF_to_Google stores the data into Google Sheets. I visualised the data with Tableau and stored the data into Google Sheets because Google Sheets updates the data once in a day to Tableau.
So it was a good fit.

directly_to_sheets is the same idea as TVO-OL3.py, but this works only with Google Sheets, with no dummy csv-files.

Check out the viz from (Tableau)[https://public.tableau.com/app/profile/cikoooo/viz/OL3-tuotantokoekytnaikana/Tabula]

