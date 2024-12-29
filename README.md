# Algorithmic Methods for Data Mining - Homework 5 ✈️

This is a GitHub repository created to submit the fifth homework of the Algorithmic Methods for Data Mining (ADM) course for the MSc. in Data Science at the Sapienza University of Rome. This project involves analyzing U.S. airport flight networks, exploring the graph's structure, centralities, communities, and routes, with an emphasis on implementing algorithms from scratch and evaluating their performance.
---

### Files and Directories
```
.

├── .gitattributes         # Manages Git LFS settings for large files (e.g., Jupyter Notebooks)
├── .gitignore             # Specifies files and folders to exclude from version control
├── README.md              # Project documentation
├── functions/             # Directory for Python modules
│   ├── analysis.py         # Analyzes graph features (size, density, hubs, etc.)
│   └── summarize.py        # Summarizes graph analysis into reports
├── funtions2/             # Auxiliary functions
│   └── function2.py        # Helper module for additional tasks
├── libs/                  # Directory for reusable Python code
│   └── function_ex_2.py    # Functions for Q2 (Nodes' Contribution)
├── adm_hm5_(Q4).ipynb     # Notebook for the Q4 Airline Network Partitioning problem
├── algorithm.ipynb        # Notebook for the algorithmic question
├── flight_network_map.html # HTML file with an interactive visualization of flight routes
├── main (ex1_ex2).ipynb   # Notebook combining analysis for exercises 1 and 2
├── main.ipynb             # General notebook containing other exercises
├── merged1and2.ipynb      # Merged notebook for exercises 1 and 2
└── usa-airport-dataset.zip # Compressed dataset of USA flight data

# Project Overview

This project analyzes the flight network of U.S. airports and focuses on various analytical tasks. It includes the following components:

---

## 1. Flight Network Analysis

**Objectives**:
- Compute graph features such as size, density, and degree distributions.
- Identify hubs (airports with high connectivity).
- Visualize key metrics like histograms and graphs for better insights.

**Visualizations**:
- Degree distribution histograms (in-degree and out-degree).
- Interactive map visualizing flight routes across the network.

---

## 2. Nodes' Contribution (Centrality)

**Centrality Measures**:
- **Betweenness Centrality**: Identifies airports that often appear on the shortest paths between other nodes.
- **Closeness Centrality**: Evaluates how accessible an airport is within the network.
- **Degree Centrality**: Measures the number of direct connections an airport has.
- **PageRank**: Highlights the "importance" of an airport based on incoming connections.

**Outputs**:
- Distribution plots for each centrality measure.
- A ranked list of the top 5 airports for each centrality measure.

---

## 3. Best Routes

**Task**:
- Determine the **optimal routes** between cities based on flight distances and stops.

**Features**:
- Handles multiple airports per city to provide comprehensive comparisons.
- Outputs a table with the best routes or reports `"No route found"` if no valid path exists.

---

## 4. Airline Network Partitioning

**Objective**:
- Divide the flight network into two disconnected subgraphs by removing the minimal number of flights.

**Outputs**:
- Visualizations of the original network and partitioned subgraphs.
- A list of flights removed to achieve the partition.

---

## 5. Community Detection

**Analysis**:
- Identify communities of interconnected airports (grouped by cities) based on network connectivity.

**Visualizations**:
- Color-coded communities on the graph to highlight distinct groups.
- Evaluate whether two specific cities belong to the same community.

---

## 6. Bonus: Connected Components on MapReduce

**Objective**:
- Using **PySpark** and the **MapReduce paradigm**, identify connected components (groups of airports connected either directly or indirectly).

**Steps**:
1. Compute the number of connected components.
2. Measure the size of each component.
3. Identify and output the airports in the largest connected component.

**Comparison**:
- Compare the results and execution time with those obtained using **GraphFrames**.
- Discuss any differences in performance and accuracy.

---

## Dataset

The analysis is based on a **U.S. airport dataset**, which includes:
- **Origin and destination airports**: Routes between airports in the U.S.
- **Traffic data**: Number of flights, passengers, and distances.
- **Geographic data**: Latitude and longitude for each airport.

**File**: `usa-airport-dataset.zip`

---

## Implementation Details

### 1. Flight Network Analysis
**Graph Properties**:
- Compute the number of nodes (airports) and edges (routes).
- Measure the network density and classify it as sparse or dense.

**Visualizations**:
- In-degree and out-degree histograms.
- Interactive map of flight routes for geographic insights.

---

### 2. Nodes' Contribution (Centrality)

**Key Features**:
- **Centrality Measures**: Betweenness, Closeness, Degree, and PageRank.
- **Comparison**: Generate visualizations and rankings for top airports.

---

### 3. Best Routes
- Calculate the shortest flight distance for all possible airport pairs between two cities.
- Provide a clear table showing optimal routes.

---

### 4. Airline Network Partitioning
- Minimize the number of flights removed to split the network into two disconnected subgraphs.
- Visualize the process and results.

---

### 5. Community Detection
- Group cities into communities based on flight connectivity.
- Visualize the communities with distinct colors and analyze the relationship between cities.

---

### Bonus: Connected Components on MapReduce
- Implement a **MapReduce** solution to identify connected components.
- Output:
  - Number and size of components.
  - Airports in the largest connected component.
- Compare with **GraphFrames** results.

---

## Results and Insights

### Summary:
- **Flight Network**:
  - Visualized the U.S. airport network and identified key hubs.
  - Highlighted busiest routes and under/over-utilized connections.

- **Centrality**:
  - Ranked airports by their importance in the network.
  - Delivered insights on critical nodes that maintain network flow.

- **Best Routes**:
  - Determined optimal routes under constraints.

- **Partitioning**:
  - Successfully divided the network into two balanced subgraphs.

- **Communities**:
  - Revealed clusters of connected cities for optimized operations.

---

## Important Notes

1. **Notebook Loading**:
   - If a notebook does not render properly on GitHub, try:
     - [NBViewer](https://nbviewer.org/) for online rendering.
     - Downloading the notebook and opening it locally.

2. **Responsible LLM Usage**:
   - AI tools (e.g., ChatGPT, Claude AI) were used responsibly for coding assistance.
   - All outputs and results were manually validated to ensure correctness.

---

**Authors**: Roberto Magno Mazzotta , xxxx, xxxx  
**Email**:  
- Roberto: magnomazzotta.2200470@studenti.uniroma1.it  
- xxx 
- xxx 

*Master's in Data Science, Sapienza University of Rome*  
