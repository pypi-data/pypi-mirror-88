#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 15:40:31 2020

@author: asyntychaki
"""

import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution # The '.' is required only for Python 3


class Gaussian(Distribution):
    """ A Gaussian distribution class for calculating and 
	visualizing a Gaussian distribution.
    It inherits from the general distribution class.
	
	Attributes:
        n (float) representing the mean value of the distribution
        ev (float) representing the standard deviation of the distribution
        a_list (list of floats) a list of floats extracted from the data file
	"""
    
    def __init__(self, mu=0, sigma=1):
        
        Distribution.__init__(self, mu, sigma)
        
    
    def calculate_mean(self):
        """Method to calculate the mean of the data set.
		
        Args: None
        
		Returns: 
             mean of the data set
		"""
        
        self.mean = sum(self.data) / len(self.data)
        
        return self.mean
        
				
    
    def calculate_stdev(self, sample=True):
        """Method to calculate the standard deviation of the data set.
        
        Args: 
            sample (bool): whether the data represents a sample or population
        
        Returns: 
            float: standard deviation of the data set
        """

        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)
        
        sigma = 0
        for num in self.data:
            sigma += (num - self.calculate_mean())**2
        
        self.stdev = math.sqrt( sigma / n)
        
        return self.stdev
    
    
    
    	#def read_data_file(self, file_name, sample=True):
	#
	#	"""Function to read in data from a txt file. The txt file should have
	#	one number (float) per line. The numbers are stored in the data attribute. 
	#	After reading in the file, the mean and standard deviation are calculated
	#			
	#	Args:
	#		file_name (string): name of a file to read from
	#	
	#	Returns:
	#		None
	#	
	#	"""
	#	with open(file_name) as file:
	#		data_list = []
	#		line = file.readline()
	#		while line:
	#			data_list.append(int(line))
	#			line = file.readline()
	#	file.close()
	#
	#	self.data = data_list
	#	self.mean = self.calculate_mean()
	#	self.stdev = self.calculate_stdev(sample)
    
    
    
    def plot_histogram(self):
        """Method to output a histogram of the instance variable data.
        Args:  None    
        Returns: None
        """

        plt.hist(self.data)
        plt.xlabel = 'Count'
        plt.ylabel = 'Data'
        plt.title = 'Histogram of Data'
        
        
    def pdf(self, x):
        """Probability density function calculator for the gaussian distribution.
        Args:
            x (float): point for calculating the probability density function
        Returns:
            float: probability density function output
        """
        
        pdf = (1.0 / (self.stdev * math.sqrt(2*math.pi))) * math.exp(-0.5*((x - self.mean) / self.stdev) ** 2)
    
        return pdf
    
    
    def plot_histogram_pdf(self, n_spaces = 50):
        """Method to plot the normalized histogram of the data and a plot of the 
        probability density function along the same range
        Args:
            n_spaces (int): number of data points 
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """
                
        mu = self.mean
        sigma = self.stdev

        min_range = min(self.data)
        max_range = max(self.data)
        
         # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y


    def __add__(self, other):
        """Magic method to add together two Gaussian distributions. 
        It changes the meaning of the "+" symbol when it is used for Gaussian() objects. 
        Args:
            other (Gaussian): Gaussian instance
        Returns:
            Gaussian: Gaussian distribution 
        """

        # create a new Gaussian object
        result = Gaussian()
        
        # TODO: calculate the mean and standard deviation of the sum of two Gaussians
        result.mean = self.mean + other.mean 
        result.stdev = math.sqrt(self.stdev**2 + other.stdev**2)
        
        return result    
    
    
    def __repr__(self):
        """Magic method to output the characteristics of the Gaussian instance.
        It changes the meaning of the output when it is used for Gaussian() objects.
        (Compiling a Gaussian() object in a line, prints this out.)
        Args: None
        Returns:
            string: characteristics of the Gaussian
        """
        
        return 'mean {}, standard deviation {}'.format(self.mean, self.stdev)
    
    
    
    
    

