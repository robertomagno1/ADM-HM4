import numpy as np
import random 

class MinHash:
    def __init__(self, n_hash_functions: int = 100, prime_number: int = 10513, type_function: str = 'linear'):
        """
        Initialize MinHash with a specified number of hash functions.
        
        Args:
            n_hash_functions: Number of hash functions to use for creating signatures (default is 100)
            prime: A higher prime number for the hash function (default is 10513)
            type_function: Type of hash function to use ('linear', 'universal', 'polynomial')
        """
        if n_hash_functions <= 0:
            raise ValueError("Number of hash functions must be greater than 0")
        
        if type_function not in ['linear', 'universal', 'polynomial']:
            raise ValueError("Invalid type_function. It must be one of 'linear', 'universal', 'polynomial'")
        
        self.n_hash_functions = n_hash_functions
        self.prime = prime_number
        self.type_function = type_function

        # Generate random coefficients for each hash function within the modulus range
        self.a = [random.randint(1, self.prime - 1) for _ in range(n_hash_functions)]
        self.b = [random.randint(0, self.prime - 1) for _ in range(n_hash_functions)]
        self.coefficients = [[random.randint(1, self.prime - 1) for _ in range(3)] for _ in range(n_hash_functions)]  # For polynomial hash

    def hash_function(self, x, a, b, i):
        """
        Apply the selected hash function based on type_function. 
        (linear, polynomial, universal)
        
        Args:
            x: The value to hash (movie ID)
            a, b: Random coefficients used in the hash function
            i: Index of the current hash function
        
        Returns:
            int: Hashed value
        """
        self.type_function= self.type_function.lower()

        if self.type_function in ('linear', 'l'):
            return (a * x + b) % self.prime
        
        elif self.type_function in ('polynomial', 'p'):
            coefficients = self.coefficients[i]
            hash_value = sum(coefficient * (x ** exponent) for exponent, coefficient in enumerate(coefficients)) % self.prime
            return hash_value
        
        elif self.type_function in ('universal', 'u'):
            m = 104729  # A larger prime modulus
            hash_value1 = (a * x + b) % self.prime # First hash function
            hash_value2 = (a * hash_value1 + b) % m # Second hash function for double hashing

            return (hash_value1 + hash_value2) % m # Combine both hash values to reduce collision probability
        
        else:
            raise ValueError(f"Unknown hash function type: {self.type_function}")

    def create_signature(self, movie_set):
        """
        Create MinHash signature for a set of movies.
        
        Args:
            movie_set: Set of movie IDs
            
        Returns:
            np.ndarray: MinHash signature (array of minimum hash values)
        """
        # Initialize signature array with infinity
        signature = np.full(self.n_hash_functions, np.inf)
        
        # For each movie ID, apply all hash functions
        for movie_id in movie_set:
            for i in range(self.n_hash_functions):
                hash_value = self.hash_function(movie_id, self.a[i], self.b[i],i)
                # Update the signature by taking the minimum hash value for each hash function
                signature[i] = min(signature[i], hash_value)
                
        return signature.astype(int)

    def jaccard_similarity(self, signature1, signature2):
        """
        Estimate Jaccard similarity between two MinHash signatures.
        
        Args:
            signature1: First MinHash signature
            signature2: Second MinHash signature
        
        Returns:
            float: Estimated Jaccard similarity (0-1)
        """
        # Count matching hash values
        matching_hashes = np.sum(signature1 == signature2)
        
        # Jaccard similarity estimation
        return matching_hashes / self.n_hash_functions


from tqdm import tqdm

def generate_signatures(user_movies: dict, num_hash_function: int,function_name: str):

    minhash=MinHash(num_hash_function,type_function=function_name)
     # Initialize an empty dictionary to store the MinHash signatures for each user.
    signatures = {}

    # Iterate over each user and their associated movie set in the `user_movies` dictionary.
    # Use tqdm to display a progress bar for tracking the loop's progress.

    for user_id, movies in tqdm(user_movies.items(), desc="Generating Signatures", total=len(user_movies)):
        signatures[user_id] = minhash.create_signature(movies)   # Generate a MinHash signature for the current user's movie set and store it.
    return signatures

def exact_jaccard_similarity(sig1, sig2):
    """
    sig1 : the signature of the user 1
    sig2 : the signature of the user 2
    """
    intersection = len(sig1 & sig2)
    union = len(sig1 | sig2)
    return intersection / union # Return Jaccard similarity value between 0 and 1



def compute_similarities(user_signatures, user_movies, max_results=10, similarity_threshold=0.6, hash_functions=100):
    # Initialize a counter to track the number of similar user pairs above the threshold
    similar_users_count=0
    # Set a random seed for reproducibility of results
    np.random.seed(213242)
    
    # Select 1000 random user IDs to compute similarities
    user_ids = np.random.choice(range(1, len(user_movies) + 1), 1000, replace=False)
    
    # Initialize dictionaries to store similarities and losses
    similarities, losses = {}, []
    
    for i in range(len(user_ids)):
        for j in range(i + 1, len(user_ids)):
        
            # Create MinHash instance for each comparison
            minhash = MinHash(n_hash_functions=hash_functions)
            
            # Estimate Jaccard similarity using MinHash signatures
            est_sim = minhash.jaccard_similarity(user_signatures[user_ids[i]], user_signatures[user_ids[j]])
            
            # Filter pairs above certain similarity threshold
            if est_sim > similarity_threshold:

                similar_users_count += 1  # Increment the counter for similar users

                # Compute exact Jaccard similarity
                exact_sim = exact_jaccard_similarity(user_movies[user_ids[i]], user_movies[user_ids[j]])
                
                # Calculate loss between estimated and exact similarities
                loss = abs(est_sim - exact_sim)
                losses.append(loss)
                
                # Store similarity information
                similarities[(user_ids[i], user_ids[j])] = (est_sim, exact_sim, loss)
    
    # Sort similarities by estimated similarity in descending order
    sorted_sims = sorted(similarities.items(), key=lambda x: x[1][0], reverse=True)[:max_results]
    
    # Print details of top similar user pairs
    for (user1, user2), (est_sim, exact_sim, loss) in sorted_sims:
        print(f"Users: ({user1}, {user2}) --> Estimated: {est_sim:.2f}, Exact: {exact_sim:.2f}, Loss: {loss:.2f}")
    
    # Calculate average loss
    avg_loss = np.mean(losses) 
    print(f"\nAverage Loss: {avg_loss:.4f}")
    print(f"\nNumber of similar user pairs (estimated similarity > {similarity_threshold}): {similar_users_count}, Number of non similar user pairs is {1000-similar_users_count}")
  