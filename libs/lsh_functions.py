import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt
import seaborn as sns


def next_prime(n):
    """Find the next prime number greater than n."""
    def is_prime(k):
        if k < 2:
            return False
        for i in range(2, int(k**0.5) + 1):
            if k % i == 0:
                return False
        return True
    
    prime = n + 1
    while not is_prime(prime):
        prime += 1
    return prime


def create_characteristic_matrix(ratings, all_movies, user_movies):
    """Create the binary characteristic matrix."""
    n_users = len(user_movies)
    n_movies = len(all_movies)
    movie_to_index = {movie: i for i, movie in enumerate(all_movies)}

    characteristic_matrix = np.zeros((n_movies, n_users))

    for user, movies in user_movies.items():
        for movie in movies:
            characteristic_matrix[movie_to_index[movie], user - 1] = 1

    return characteristic_matrix


def generate_minhash_signatures(characteristic_matrix, n_hashes):
    """Generate MinHash signatures for the characteristic matrix."""
    n_movies, n_users = characteristic_matrix.shape

    # Generate random hash parameters
    hash_params = [(np.random.randint(1, n_movies), np.random.randint(0, n_movies)) for _ in range(n_hashes)]
    mod_prime = next_prime(n_movies)

    # Initialize the signature matrix with infinity
    signature_matrix = np.full((n_hashes, n_users), np.inf)

    # Compute MinHash signatures
    for row in range(n_movies):
        hashes = [(a * row + b) % mod_prime for a, b in hash_params]
        for col in range(n_users):
            if characteristic_matrix[row, col] == 1:
                signature_matrix[:, col] = np.minimum(signature_matrix[:, col], hashes)

    return signature_matrix


def compute_jaccard_similarity(signature_matrix, user1_idx, user2_idx):
    """Compute estimated Jaccard similarity between two users."""
    user1 = signature_matrix[:, user1_idx]
    user2 = signature_matrix[:, user2_idx]
    return np.mean(user1 == user2)


def compute_similarities(signature_matrix):
    """Compute pairwise similarity matrix for all users."""
    return 1 - pairwise_distances(signature_matrix.T, metric="hamming")


def recommend_movies(similarities, user_movies, target_user_idx, top_n=5):
    """Recommend movies for a target user based on similar users."""
    # Find the most similar users
    similar_users = np.argsort(similarities[target_user_idx])[-(top_n + 1):-1]

    # Aggregate recommended movies
    recommended_movies = set()
    for similar_user in similar_users:
        recommended_movies.update(user_movies[similar_user + 1])

    # Exclude movies already rated by the target user
    recommended_movies -= user_movies[target_user_idx + 1]

    return recommended_movies


def plot_probability_curve(n=100, band_values=[5, 10, 20, 25, 50]):
    """
    Plot the probability of a pair of users being hashed to the same bucket 
    as a function of their similarity for different banding configurations.
    """
    s = np.linspace(0, 1, 100)  # Range of similarity values from 0 to 1

    plt.figure(figsize=(10, 6))

    for b in band_values:
        r = n // b  # Calculate rows per band
        probability = 1 - (1 - s**r)**b
        plt.plot(s, probability, label=f"$b = {b}, r = {r}$")

    plt.title(f"Probability for $n = {n}$ hash functions and different values of $b$")
    plt.xlabel("Similarity $s$")
    plt.ylabel("Probability")
    plt.legend()
    plt.grid(True)
    plt.show()



def visualize_signature_matrix(signature_matrix, rows=10, cols=10):
    """
    Visualize a subset of the signature matrix using a heatmap.

    Args:
        signature_matrix: The generated signature matrix.
        rows: Number of rows to display in the heatmap.
        cols: Number of columns to display in the heatmap.
    """
    subset_signature_matrix = signature_matrix[:rows, :cols]

    plt.figure(figsize=(10, 8))
    sns.heatmap(subset_signature_matrix, annot=True, fmt=".0f", cmap="viridis")
    plt.title("Subset of the Signature Matrix")
    plt.xlabel("Users")
    plt.ylabel("Hash Functions")
    plt.show()


from scipy.sparse import coo_matrix

def create_sparse_interaction_matrix(merged_df):
    """
    Create a sparse interaction matrix from the dataset.
    
    Args:
        merged_df: Merged DataFrame containing 'userId' and 'movieId' columns.
    
    Returns:
        A sparse matrix where rows represent movieIds, columns represent userIds,
        and values are 1 for interactions.
    """
    # Create a sparse matrix using scipy
    interaction_sparse_matrix = coo_matrix(
        (np.ones(len(merged_df)), (merged_df['movieId'], merged_df['userId'])),
        shape=(merged_df['movieId'].max() + 1, merged_df['userId'].max() + 1)
    )
    return interaction_sparse_matrix


def generate_minhash_signatures_with_interaction(interaction_sparse_matrix, n_hashes, a_values, b_values):
    """
    Generate MinHash signatures for a sparse interaction matrix.

    Args:
        interaction_sparse_matrix: A sparse matrix of movie-user interactions.
        n_hashes: Number of hash functions to generate.
        a_values: Array of 'a' coefficients for hash functions.
        b_values: Array of 'b' coefficients for hash functions.

    Returns:
        A signature matrix of dimensions (n_hashes, n_users).
    """
    n_movies, n_users = interaction_sparse_matrix.shape
    mod_prime = next_prime(n_movies)

    # Initialize the signature matrix with infinity
    signature_matrix = np.full((n_hashes, n_users), np.inf)

    # Iterate through the non-zero entries in the sparse matrix
    for row, col in zip(interaction_sparse_matrix.row, interaction_sparse_matrix.col):
        # Compute hash values for the current row (movieId)
        hash_values = [(a * row + b) % mod_prime for a, b in zip(a_values, b_values)]
        # Update the signature matrix with the minimum hash values
        signature_matrix[:, col] = np.minimum(signature_matrix[:, col], hash_values)

    return signature_matrix

from scipy.sparse import coo_matrix

def create_sparse_interaction_matrix_from_binary(interaction_matrix):
    """
    Create a sparse interaction matrix from a binary matrix.
    
    Args:
        interaction_matrix: Binary matrix with movieId as index and userId as columns.
    
    Returns:
        A sparse matrix.
    """
    # Reset index to use row numbers for the sparse matrix
    interaction_matrix = interaction_matrix.reset_index()
    rows, cols = interaction_matrix.shape

    # Use the binary matrix to create a sparse matrix
    row_indices, col_indices = interaction_matrix.index, interaction_matrix.columns
    data = interaction_matrix.values.flatten()

    sparse_matrix = coo_matrix((data, (row_indices, col_indices)), shape=(rows, cols))
    return sparse_matrix