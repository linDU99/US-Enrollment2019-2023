## US-Enrollment2019-2023
### College enrollment 2019-2023
- Create an interactive dash application framed from an explanatory perspective with Plotly Dash
- Explore enrollment trends of US degree-granting institutions (colleges, universities, and technical and vocational institutions).
- Display enrollment changes across groups:
    - Education level: Undergraduate (UG) vs. Graduate (GR)
    - Gender: Women vs. Men
    - Study status: Full-Time (FT) vs. Part-Time (PT)

#### Data: 
The enrollment data are from the Integrated Postsecondary Education Data System (IPEDS) provided by the U.S. National Center for Education Statistics (NCES).
Source: https://nces.ed.gov/ipeds/summarytables 
- Limited to all Title IV degree-granting institutions in the U.S.: N ≥ 3838
- The numbers of enrollment are summary data of all institutes included.
- The enrollments are the fall terms of 2019 to 2023. 
- Enrollment App: The default model includes the enrollment of all groups. Groups' data can be selected by clicking the checkbox. 

#### Directory Structure:
1. data: The enrollment data files
2. notebooks: The Jupyter Notebook files for data exploration and creating the dash App
3. src: The python scripts for creating the dash App
4. visuals: The image of enrollment dash App 
   
#### Findings: 
- **Undergraduates:** Overall enrollment decreased continuously from Fall 2019 to Fall 2022. In Fall 2023, enrollment rebounded to approximately the 2020 level.
- **Graduates:** The total enrollment increased consistently from Fall 2019 to Fall 2021. Since then, it has fluctuated around 3.2 million students. 
- **By Gender:** More than 57% of undergraduates and approximately 61% of graduates were female. Across all institutions (n ≥ 3,838), female enrollment exceeded male enrollment by at least 2.9 million students.
- **By study status:** Overall, more than 60% of enrolled students were full-time.
  
