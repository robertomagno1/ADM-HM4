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
