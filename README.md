# Algorithmic Methods for Data Mining - Homework 4 🎥

This is a GitHub repository created to submit the fourth homework of the **Algorithmic Methods for Data Mining (ADM)** course for the MSc. in Data Science at the Sapienza University of Rome.

---

### Files and Directories
```
.
├── libs/                 # Python modules for the function called in the main notebook

        ├──  LSH.py
        ├──  analysis_functions.py
        ├──  functions.py
        ├──  k_means.py
        ├──  k_means_plus_plus.py
        ├──  k_means_visualizer.py
        ├──  locality_sensitive_hashing.py
        ├──  lsh_functions.py
        ├──  minhash_functions.py
        ├──  minhash_similarity.py
        
├── .gitignore            # Git ignore file for excluding unnecessary files
├── README.md             # Project documentation
├── algorithm4.ipynb       # Notebook for the algorithmic problem
└── main.ipynb            # Main notebook combining all tasks

```
--- 


1. `README.md`: A markdown file that explains the content of the repository.

2. `main.ipynb`: A [Jupyter Notebook](link_notebook) file containing all the relevant exercises and reports belonging to the homework questions, the *Command Line Question*, and the *Algorithmic Question*.

3. ``libs/``: A folder including 4 Python modules used to solve the exercises in `main.ipynb`. The files included are:

    - `analysis_functions.py`: A Python file including a `DataHandler` class designed to handle data cleaning and feature engineering on Kaggle's [MovieLens 20M Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset?select=rating.csv).
      
    - `lsh_functions.py`: A Python file including a `LSH` class designed to build a Recommendation Engine with LSH using user data obtained from Kaggle's [MovieLens 20M Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset?select=rating.csv).
  
      
    - `locality_sensitive_hashing.py` : Here there is functions that  recommend movies for a target user based on similar users 

    - `k_means.py`: A Python file including class `KMeans` designed to perform Factor Analysis of Mixed Data on Kaggle's [MovieLens 20M Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset?select=rating.csv) and then perform parallelized k-Means andusing PySpark.
      
    - `k_means_plus_plus.py`:  Implementation of k-Means++ clustering.
  
    - `k_means_visualizer.py`: function to visualize the k_means iterations and metrics associated.
  
    -  `minhash_functions.py` : this function create buckets , signatures and charateristic matrix for minhash
      
    - ` minhash_similarity.py` : this compute minhash similarity and return top hash bucket 



4. `.algorithm4.ipynb ` : here there is the notebook for the algorithmic problem (exercise 4)
   
6. `.gitignore`: A predetermined `.gitignore` file that tells Git which files or folders to ignore in a Python project.


---

## Project Overview

This project explores movie recommendation systems and clustering techniques using the Kaggle [MovieLens 20M Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset?select=rating.csv). It is divided into three main components:
1. **Recommendation System with Locality-Sensitive Hashing (LSH)**: Matches similar users and recommends movies based on their preferences.
2. **Clustering Movies**: Groups movies into clusters based on engineered features for better analysis.
3. **Algorithmic Question**: Solves a strategy-based game problem with an optimal solution.



---

## Dataset

The Kaggle [MovieLens 20M Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset?select=rating.csv) was used for this project. It includes user ratings and movie metadata, enabling robust feature engineering and analysis.

---

## Implementation Details

### Recommendation System
1. **MinHashing**: Implemented a custom MinHash function to create user signatures.
2. **Locality-Sensitive Hashing (LSH)**: Clustered users into buckets and recommended movies based on similarity.
3. **Recommendation Logic**: Delivered personalized recommendations using weighted scoring.

### Clustering Movies
1. **Feature Engineering**: Derived multiple features, including genres, average ratings, and user tags.
2. **Clustering**:
   - Implemented K-means and K-means++ algorithms.
   - Used AI-recommended clustering methods for comparative analysis.
3. **Evaluation**: Assessed clustering quality using metrics such as Silhouette Score and WCSS.

### Algorithmic Problem
1. Developed solutions for a sequence-based game problem using recursion and dynamic programming.
2. Validated solutions with time complexity analysis and AI-assisted optimization.

---

## Results and Visualizations

### Recommendation System
- Successfully implemented a scalable recommendation engine.

### Clustering Movies
- Visualized movie groupings to uncover natural patterns.

### Algorithmic Problem
- Delivered an efficient solution validated through test cases.

---
## Important Note

If the Notebook doesn't load through Github please try all of these steps:

1. Try compiling the Notebook through its [NBViewer](mainjupiter_link).

2. Try downloading the Notebook and opening it in your local computer.

---

**This is the animatet output for the bonus question 3 :**

https://github.com/user-attachments/assets/07d52864-82f7-4c2f-9a38-ce6b83234195

**Author:** Roberto Magno Mazzotta , Gabriel Pinos,  Ata Berk Firat

**Email:** magnomazzotta.2200470@studenti.uniroma1.it , pinos.1965035@atudenti.uniroma1.it, ataberk77178@outlook.com 

*MSc. in Data Science, Sapienza University of Rome*
