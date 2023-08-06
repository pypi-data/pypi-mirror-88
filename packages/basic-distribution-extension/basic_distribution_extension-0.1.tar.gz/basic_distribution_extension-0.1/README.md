# Basic Distribution Extension

*basic-distribution-extension* is a Python module that makes it easy to initialize, add, calculate, and plot probability distributions. In addition, users are able to retrive useful characteristics (e.g. mean, standard deviation probability, sample size) of the distribution with one-line command. Currently, this module only supports Gaussian and Binomial distributions.

1. [Installation](#installation)
2. [Dependencies](#dependencies)
3. [Example Usage](#example)

## Installation <a name="installation"></a>

Users can install basic-distribution-extension using ``pip``   :

    pip install -U basic-distribution-extension

## Dependencies <a name="dependencies"></a>
basic-distribution-extension requires
- Python (>=3.0)
- math
- matplotlib

## Example Usage <a name="example"></a>
## Import Modules
    from basic_distribution_extension import Gaussian, Binomial

### Create distribution
    gaussian_one = Gaussian(5,2)
    binomial_one = Binomial(0.4,20)

### Read Data File
    gaussian_one = Gaussian()
    gaussian_one.read_data_file('numbers.txt')
    binomial_one.read_data_file('numbers.txt')

### Calculate mean given the data file
    gaussian_one.calculate_mean()
    binomial_one.calculate_mean()

### Calculate standard deviation
    gaussian_one.calculate_stdev()
    binomial_one.calculate_stdev()

### Calculate probability density for a given point
    gaussian_one.pdf(25)
    binomial_one.pdf(25)

### Add two distributions
    gaussian_one = Gaussian(5,2)
    gaussian_two = Gaussian(10,1)
    gaussian_sum = gaussian_one + gaussian_two

    binomial_one = Binomial(0.4,20)
    binomial_two = Binomial(0.4,60)
    binomial_sum = binomial_one + binomial_two

### Output the characteristics of distributions
    gaussian_sum
    binomial_sum

### Plot data
    gaussian_one.plot_histogram()
    binomial_one.plot_bar()


### Plot the probability density function 
    gaussian_one.plot_histogram_pdf()
    binomial_one.plot_bar_pdf()