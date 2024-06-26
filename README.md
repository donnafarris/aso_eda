# ASO EDA: Analysis of Tracked Artificial Space Objects

### Table Of Contents

- [ASO EDA: Analysis of Tracked Artificial Space Objects](#aso-eda-analysis-of-tracked-artificial-space-objects)
  - [Table Of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Project Proposal / Research Question](#project-proposal--research-question)
  - [Source of Data](#source-of-data)
  - [Data Cleaning and Transformation](#data-cleaning-and-transformation)
  - [Contextual Visualization(s)](#contextual-visualizations)
    - [Visualization](#visualization)
  - [Key Insights](#key-insights)
  - [Future Studies](#future-studies)
    - [Trends in Space Launches:](#trends-in-space-launches)
    - [Technological Advancements:](#technological-advancements)
    - [Orbital Dynamics:](#orbital-dynamics)
    - [Space Debris:](#space-debris)
    - [Mission Lifetimes:](#mission-lifetimes)

## Overview

Exploratory data analysis (EDA) on tracked artificial space objects (ASOs) to uncover patterns, trends, and insights.

## Project Proposal / Research Question

- **Research Question:** What are the trends and patterns in the launch and distribution of artificial space objects over time?
- **Objectives:**
  - Analyze the distribution of ASOs by country and organization.
  - Identify temporal trends in ASO launches.

## Source of Data

The primary data sources for this project are:

- [Celestrak](https://www.celestrak.com/)
  - Data Download:
  - [Raw SATCAT Data](https://celestrak.org/pub/satcat.csv)
    - [Documentation](https://celestrak.org/satcat/satcat-format.php)
- [GCAT (J. McDowell)](https://www.planet4589.org/space/gcat/)
  - Data Downloads:
    - [currentcat](https://planet4589.org/space/gcat/tsv/derived/currentcat.tsv)
    - [launch](https://planet4589.org/space/gcat/tsv/launch/launch.tsv)
    - [orgs](https://planet4589.org/space/gcat/tsv/tables/orgs.tsv)
    - [psatcat](https://planet4589.org/space/gcat/tsv/cat/psatcat.tsv)
    - [satcat](https://planet4589.org/space/gcat/tsv/cat/satcat.tsv)
  - [Documentation](https://planet4589.org/space/gcat/web/cat/index.html)
    - Note: Documentation for GCAT is partitioned based on category of data.
  - There are many more sources of useful data available through GCAT than what was used for this analysis.

## Data Cleaning and Transformation

To ensure the reproducibility of results, the following steps were taken:

1. **Data Collection:** Raw data was collected from the sources mentioned above.
2. **Data Cleaning:**
   - Parsed all data into .csv format.
     - Data from GCAT required dropping a line where the author had inserted a comment.
   - Removed duplicate entries.
   - Filled or removed missing values where applicable.
   - Ensured all columns contained only one data type.
   - Standardized date and time formats.
3. **Data Transformation:**
   - Extracted relevant features such as launch date, country, and object type.
   - Created new columns for derived metrics such as launch year and count.

## Contextual Visualization(s)

To understand the distribution and trends of ASOs, the following visualizations are included:

- Temporal trends in ASO launches.
- Annual number of ASO launches by country.
- Starlink satellites vs all other satellites.
- Satellite types launched over time.

### Visualization

[![Satellite Growth Over Time](img/sat_growth.png)](https://donnafarris.github.io/aso_eda/#:~:text=Satellite%20Growth%20Over,Count)

[![Annual Number of Launches By Country](img/annual_number_of_launches_by_country.png)](https://donnafarris.github.io/aso_eda/#:~:text=ASO%20Visualizations-,Annual%20Number%20of%20Launches%20by%20Country,Number%20of%20Launches,-Satellite%20Growth%20Over)

[![Satellite Types Launched Over Time](img/launches_by_sat_type.png)](https://donnafarris.github.io/aso_eda/#:~:text=Count-,Annual%20Number%20of%20Launches%20by%20Satellite%20Type,Number%20of%20Launches,-Number%20of%20Starlink)

[![Starlink Vs. All Others](img/starlink_vs_all_others.png)](https://donnafarris.github.io/aso_eda/#:~:text=Number%20of%20Launches-,Number%20of%20Starlink%20vs%20All%20Other%20Satellite%20Launches,-Jan%202020)

## Key Insights

- The majority of ASOs are launched by a few key countries, primarily the US, Russia, and China.
- China has been ramping up their launch numbers in recent years.
- There is a notable increase in the number of launches in recent years, driven by commercial satellite deployments.
- Over half of the satellites launched since 2019 are Starlink satellites.

## Future Studies

### Trends in Space Launches:

Analysis of launch dates, types of objects launched, and the countries responsible for launches can reveal trends over time, such as increases in satellite launches for communication or Earth observation.

### Technological Advancements:

Examining changes in the construction, mass, and dimensions of space objects can provide insights into technological advancements and innovations in spacecraft design.

### Orbital Dynamics:

Analysis of canonical orbits and other orbital parameters can shed light on the preferred orbits for different types of missions and the evolution of orbital mechanics over time.

### Space Debris:

Evaluating the number and characteristics of pieces (debris) can contribute to understanding the growing issue of space debris and its management.

### Mission Lifetimes:

Analyzing the lifetimes and end-of-mission statuses can help assess the longevity and success rates of different types of space missions.

---

**Citations**

McDowell, Jonathan C., 2020. General Catalog of Artificial Space Objects,
Release 1.5.5 , https://planet4589.org/space/gcat

CelesTrak. (n.d.). Satellite Catalog (SATCAT), https://celestrak.org/pub/satcat.csv
