import random
class LSH:
    def __init__(self, num_bands: int, rows_per_band: int):
        """
        Initialize the Locality Sensitive Hashing (LSH) object.
        
        Args:
            num_bands (int): Number of bands to divide signatures into.
            rows_per_band (int): Number of rows (hash values) in each band.
        """
        self.num_bands = num_bands
        self.rows_per_band = rows_per_band
        
        # Dictionary to store buckets with similar signature bands
        self.buckets = {}
    
    def create_bucket_hash(self, band_idx, band_signature):
        """
        Create a hash that generates a readable code.
        
        Returns:
            str: A unique hash code
        """
        # Combine band index and signature values
        hash_code = band_idx
        for val in band_signature:
            hash_code = (hash_code * 31 + val) % (2**63 - 1)
        
        # Ensure the hash is positive and limit to 6 digits
        bucket_code = hash_code % 1000000
        
        # Format as LSH-NNNNNN
        return f"LSH-{bucket_code:06d}"
    
    def build_buckets(self, signatures: dict):
        """
        Build hash buckets by dividing signatures into bands.
        
        This method populates the buckets with user IDs that have similar 
        signature bands. It helps in quickly finding similar items by 
        reducing the search space.
        
        Args:
            signatures (dict): Dictionary with user IDs as keys and signature arrays as values.
        Returns:
                None
        """
        # Reset buckets to ensure clean slate
        self.buckets = {}
        
        # Iterate through each user's signature
        for user_id, signature in signatures.items():
            # Divide signature into bands
            for band_idx in range(self.num_bands):
                # Calculate start and end indices for the current band
                start = band_idx * self.rows_per_band
                end_index = start + self.rows_per_band
                
                # Extract band signature and convert to tuple for hashing
                band_signature = tuple(signature[start:end_index])
                
                # Create bucket key using custom hash function
                bucket_key = self.create_bucket_hash(band_idx, band_signature)
                
                # Add user ID to the corresponding bucket
                if bucket_key not in self.buckets:
                    self.buckets[bucket_key] = []
                self.buckets[bucket_key].append(user_id)
    
    def query(self, query_signature: list, query_user_id: int):
        """
        Find candidate similar users using LSH buckets.
        
        This method identifies users with at least one matching signature band, 
        providing potential similar candidates quickly.
        
        Args:
            query_signature (list): Signature array of the query user
            query_user_id (int): ID of the user making the query
        
        Returns:
            list: List of candidate user IDs similar to the query user
        """
        # Set to store unique candidate user IDs
        candidates = set()
        
        # Iterate through each band of the query signature
        for band_idx in range(self.num_bands):

            # Calculate start and end indices for the current band
            start_index = band_idx * self.rows_per_band
            end_index = start_index + self.rows_per_band
            
            # Extract band signature and convert to tuple
            band_signature = tuple(query_signature[start_index:end_index])
            
            # Create bucket key using custom hash function
            bucket_key = self.create_bucket_hash(band_idx, band_signature)
            
            # Add users from the matching bucket (if exists)
            if bucket_key in self.buckets:
                candidates.update(self.buckets[bucket_key])
        
        # Remove the query user from candidates to avoid self-matching
        candidates.discard(query_user_id)
        
        return list(candidates)
    
    def view_buckets(self, num_buckets: int = 10):
        """
        Display the contents of a specified number of random buckets.
        
        This method is useful for debugging and understanding 
        how signatures are distributed across buckets.
        
        Args:
            num_buckets (int, optional): Number of random buckets to display. 

        Returns:
            None
        """
        # Select random bucket IDs
        random_bucket_ids = random.sample(list(self.buckets.keys()), num_buckets)

        # Display the selected random buckets
        for bucket_id in random_bucket_ids:
            similar_users = self.buckets[bucket_id]
            print(f"Bucket {bucket_id}: {similar_users}")