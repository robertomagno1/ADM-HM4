import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


class KMeansVisualizer:
    def __init__(self, data, centroids_history, labels_history):
        """
        Visualizes the results of the K-Means++ algorithm with history.

        Args:
        - data: Original dataset (2D NumPy array)
        - centroids_history: List of centroid positions for each iteration
        - labels_history: List of cluster assignments for each iteration
        """
        # Initialize the data, centroids history, and labels history
        self.data = data
        self.centroids_history = centroids_history
        self.labels_history = labels_history
        self.iteration_data = []
        
        # Prepares data for visualization
        self._prepare_visualization_data()
    
    def _prepare_visualization_data(self):
        """
        Prepares the data for each iteration for interactive visualization.
        """
        # Loop through each iteration of centroids and labels
        for iteration, (centroids, labels) in enumerate(zip(self.centroids_history, self.labels_history)):
            # For each data point, store its feature values, cluster assignment, and centroid position
            for i, point in enumerate(self.data):
                self.iteration_data.append({
                    'Iteration': iteration + 1,  # Iteration number
                    'Feature1': point[0],         # Feature 1 (e.g., x-coordinate in PCA space)
                    'Feature2': point[1],         # Feature 2 (e.g., y-coordinate in PCA space)
                    'Cluster': labels[i],         # Cluster assignment
                    'Centroid_X': centroids[labels[i]][0],  # X position of the assigned centroid
                    'Centroid_Y': centroids[labels[i]][1]   # Y position of the assigned centroid
                })
    
    def create_visualization(self):
        """
        Creates the interactive visualization of the evolution of the clusters.
        """
        # Convert the iteration data into a DataFrame for easier handling
        df_iterations = pd.DataFrame(self.iteration_data)
        
        # Define a color map for the clusters
        color_map = px.colors.qualitative.Plotly
        
        # Prepare frames for animation
        frames = []
        for iteration in df_iterations['Iteration'].unique():
            # Filter the data for the current iteration
            df_frame = df_iterations[df_iterations['Iteration'] == iteration]
            
            # Scatter plot of the data points
            scatter = go.Scatter(
                x=df_frame['Feature1'], 
                y=df_frame['Feature2'],
                mode='markers',
                marker=dict(
                    size=10, 
                    color=[color_map[c % len(color_map)] for c in df_frame['Cluster']],  # Color based on cluster
                    line=dict(width=1, color='DarkSlateGrey')  # Add border to points
                ),
                name=f'Points - Iteration {iteration}'  # Label for the scatter plot
            )
            
            # Scatter plot of the centroids
            centroids = go.Scatter(
                x=df_frame['Centroid_X'], 
                y=df_frame['Centroid_Y'],
                mode='markers',
                marker=dict(
                    symbol='x',  # Mark centroids with an 'x' symbol
                    size=15,     # Size of the centroids
                    color='red', # Centroids are marked in red
                    line=dict(width=2)  # Add border to centroid points
                ),
                name=f'Centroids - Iteration {iteration}'  # Label for the centroid plot
            )
            
            # Create a frame for the current iteration
            frame = go.Frame(
                data=[scatter, centroids],
                name=f'frame{iteration}'  # Name of the frame
            )
            frames.append(frame)
        
        # Create the initial figure with a subplot
        fig = make_subplots(
            rows=1, cols=1, 
            subplot_titles=('Evolution of K-Means++ Clustering')
        )
        first_frame = frames[0]
        fig.add_trace(first_frame.data[0])  # Add scatter plot for the first frame
        fig.add_trace(first_frame.data[1])  # Add centroid plot for the first frame
        
        # Set up animation for the frames
        fig.frames = frames
        fig.update_layout(
            title='Evolution of K-Means++ Clustering',
            xaxis_title='Feature 1',
            yaxis_title='Feature 2',
            height=800,
            updatemenus=[{
                'type': 'buttons',  # Add buttons for animation control
                'showactive': False,
                'buttons': [
                    {
                        'label': 'Play',  # Button to start animation
                        'method': 'animate',
                        'args': [None, {
                            'frame': {'duration': 1000, 'redraw': True},  # Set duration for each frame
                            'fromcurrent': True,
                            'transition': {'duration': 300}  # Transition duration between frames
                        }]
                    },
                    {
                        'label': 'Pause',  # Button to pause animation
                        'method': 'animate',
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    },
                    {
                        'label': 'Reset',  # Button to reset animation to the first frame
                        'method': 'animate',
                        'args': [None, {
                            'frame': {'duration': 1000, 'redraw': True},
                            'mode': 'immediate',
                            'fromcurrent': False,
                            'transition': {'duration': 300}
                        }]
                    }
                ]
            }]
        )
        
        return fig
