import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import pairwise_distances
import scipy.sparse as sp


# Prime Number Helper
def next_prime(n):
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

# Create Characteristic Matrix
def create_characteristic_matrix(ratings, all_movies, user_movies):
    n_users = len(user_movies)
    n_movies = len(all_movies)
    movie_to_index = {movie: i for i, movie in enumerate(all_movies)}

    characteristic_matrix = np.zeros((n_movies, n_users))

    for user, movies in user_movies.items():
        for movie in movies:
            characteristic_matrix[movie_to_index[movie], user - 1] = 1

    return characteristic_matrix

# Generate MinHash Signatures
def generate_minhash_signatures(characteristic_matrix, n_hashes):
    n_movies, n_users = characteristic_matrix.shape
    hash_params = [(np.random.randint(1, n_movies), np.random.randint(0, n_movies)) for _ in range(n_hashes)]
    mod_prime = next_prime(n_movies)

    signature_matrix = np.full((n_hashes, n_users), np.inf)

    for row in range(n_movies):
        hashes = [(a * row + b) % mod_prime for a, b in hash_params]
        for col in range(n_users):
            if characteristic_matrix[row, col] == 1:
                signature_matrix[:, col] = np.minimum(signature_matrix[:, col], hashes)

    return signature_matrix

# LSH Bucket Creation
def lsh_bucket_creation(signature_matrix, n_bands):
    n_hashes, n_users = signature_matrix.shape
    rows_per_band = n_hashes // n_bands
    buckets = {}

    for band_idx in range(n_bands):
        start_row = band_idx * rows_per_band
        end_row = start_row + rows_per_band

        band_hashes = tuple(map(tuple, signature_matrix[start_row:end_row, :].T))

        for user_idx, band_hash in enumerate(band_hashes):
            if band_hash not in buckets:
                buckets[band_hash] = []
            buckets[band_hash].append(user_idx)

    return buckets

# Debugging Buckets
def debug_lsh_buckets(buckets):
    print("\n=== Debug: LSH Buckets ===")
    for bucket, users in list(buckets.items())[:5]:  # Print first 5 buckets
        print(f"Bucket {hash(bucket)}: Users: {users}")

# Recommend Movies Using LSH
def recommend_movies_lsh(target_user_idx, user_movies, buckets, ratings, top_n=5):
    similar_users = set()
    for users in buckets.values():
        if target_user_idx in users:
            similar_users.update(users)
    similar_users.discard(target_user_idx)

    if not similar_users:
        print(f"No similar users found for User {target_user_idx + 1}.")
        return []

    similar_users_movies = pd.DataFrame(
        [
            (user, movie, ratings.loc[(ratings["userId"] == user + 1) & (ratings["movieId"] == movie), "rating"].mean())
            for user in similar_users
            for movie in user_movies[user + 1]
        ],
        columns=["userId", "movieId", "avg_rating"]
    )

    similar_users_movies = similar_users_movies.groupby("movieId")["avg_rating"].mean().reset_index()
    similar_users_movies = similar_users_movies.sort_values(by="avg_rating", ascending=False)

    recommended_movies = similar_users_movies[~similar_users_movies["movieId"].isin(user_movies[target_user_idx + 1])]

    return recommended_movies.head(top_n)["movieId"].tolist()

def locality_sensitive_hashing_workflow(ratings, n_hashes=100, n_bands=20, top_n=5):
    all_movies = set(ratings["movieId"].unique())
    user_movies = ratings.groupby("userId")["movieId"].apply(set).to_dict()

    characteristic_matrix = create_characteristic_matrix(ratings, all_movies, user_movies)
    signature_matrix = generate_minhash_signatures(characteristic_matrix, n_hashes)
    buckets = lsh_bucket_creation(signature_matrix, n_bands)

    debug_lsh_buckets(buckets)

    for user_idx in range(len(user_movies)):
        print(f"\nGenerating recommendations for User {user_idx + 1}...")
        recommended_movies = recommend_movies_lsh(
            target_user_idx=user_idx,
            user_movies=user_movies,
            buckets=buckets,
            ratings=ratings,
            top_n=top_n,
        )
        print(f"Recommended movies for User {user_idx + 1}: {recommended_movies}")

def plot_probability_curve(n=100, band_values=[5, 10, 20, 25, 50]):
    s = np.linspace(0, 1, 100)

    plt.figure(figsize=(10, 6))
    for b in band_values:
        r = n // b
        probability = 1 - (1 - s**r)**b
        plt.plot(s, probability, label=f"$b = {b}, r = {r}$")

    plt.title(f"Probability for $n = {n}$ hash functions and different values of $b$")
    plt.xlabel("Similarity $s$")
    plt.ylabel("Probability")
    plt.legend()
    plt.grid(True)
    plt.show()

