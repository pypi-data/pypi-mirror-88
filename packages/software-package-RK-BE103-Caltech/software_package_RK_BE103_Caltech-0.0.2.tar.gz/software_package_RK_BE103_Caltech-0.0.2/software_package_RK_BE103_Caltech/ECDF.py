import numpy as np


def ecdf_vals(data):
    '''Generate the coordinates to plot an ECDF in "dots" style
        
        Parameters
        ----------
        data : Pandas Series or 1D Numpy array, containing tidy data for plotting
        
        Returns
        -------
        unique : returns the x values for plotting an ECDF
        norm_cum_counts : returns the y values for plotting an ECDF
        
    '''
    if len(np.shape(data)) > 1:
        raise RuntimeError('Input data must be one dimensional')
    
    unique, counts = np.unique(data, return_counts=True)
    norm_cum_counts = np.cumsum(counts) / np.sum(counts)
    
    return unique, norm_cum_counts