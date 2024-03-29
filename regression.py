import matplotlib.pylab as plt
import numpy as np
from scipy import stats

class Regression(object):

    def __init__(self, Xs, xlabel, Ys, ylabel):
        self.Xs = np.array(Xs)
        self.Ys = np.array(Ys)
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.Yhat = None
        self.R2 = None
        self.p_value = None
        self.std_err = None

    def compute(self):
        slope, intercept, r_value, p_value, std_err = stats.linregress(self.Xs, self.Ys)

        self.pearson = stats.pearsonr(self.Xs, self.Ys)[0]

        self.Yhat = intercept + slope * self.Xs
        self.R2 = r_value**2
        self.p_value = p_value
        self.std_err = std_err


    def plot(self, filename=None):
        plt.figure()

        plt.scatter(self.Xs, self.Ys, color='CadetBlue')
        plt.plot(self.Xs, self.Yhat, color='red', linewidth=2)

        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        s = '$R^2 = {:.02f}$\n$p = {:+.02f}$'.format(self.R2, self.pearson)
        plt.text(0.75, 0.25, s, transform=plt.gca().transAxes, fontsize=14,
                              bbox={'facecolor': 'yellow',
                                    'alpha': 0.8,
                                    'pad': 10})

        plt.show()



if __name__ == "__main__":
    Xs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 17, 3, 1, 64, 12, 12, 6, 27, 13, 15, 76, 58, 26, 47, 23, 86, 20, 13, 31, 55, 112, 87, 72, 85, 3, 40, 28, 0, 19, 163, 147, 108, 117, 84, 47, 1, 0, 0, 36, 19, 64, 80, 4, 54, 96, 124, 116, 124, 110, 44, 20, 8, 36, 0, 107, 122, 109, 51, 31, 110, 201, 167, 294, 238, 151, 118, 89, 13, 7, 54, 12, 100, 145, 250, 100, 102, 53, 105, 107, 163, 137, 81, 102, 180, 94, 30, 65, 56, 177, 267, 205, 167, 99, 43, 50, 79, 183, 125, 126, 106, 112, 119, 5, 10, 74, 73, 156, 204, 238, 164, 80, 81, 130, 49, 87, 78, 191, 146, 78, 36, 2, 0, 18, 155, 115, 125, 101, 266, 83, 122, 75, 60, 44, 65, 72, 6, 0, 0, 0, 9, 6, 57, 50, 168, 179, 135, 68, 63,1, 0, 1, 0, 1, 0, 64, 76, 176, 34, 16, 0, 9, 0, 12, 135, 164, 223, 2, 0, 13, 2, 40, 24, 13, 1, 0, 1, 0]
    Ys = [0.006, 0.0, 0.096, 0.489, 0.061, 0.004, 0.003, 0.335, 0.028, 0.017, 0.0, 0.01, 0.286, 0.147, 0.016, 0.399, 0.066, 0.112, 0.119, 0.143, 0.084, 0.221, 0.721, 0.669, 0.179, 0.366, 0.117, 0.49, 0.232, 0.176, 0.796, 1.331, 1.73, 0.918, 0.661, 0.486, 0.064, 0.355, 0.543, 0.002, 0.648, 7.064, 3.966, 2.359, 1.628, 0.996, 0.254, 0.015, 0.003, 0.002, 0.343, 0.57, 0.999, 1.181, 0.074, 1.2, 2.193, 4.351, 3.293, 2.173, 1.705, 1.069, 0.202, 0.084, 0.216, 0.005, 0.673, 0.853, 1.783, 1.674, 0.398, 2.888, 5.99, 4.441, 3.853, 2.951, 2.022, 2.001, 0.722, 0.119, 0.067, 0.441, 0.09, 0.724, 1.966, 5.229, 1.88, 1.666, 1.535, 2.336, 2.592, 2.948, 2.343, 1.121, 1.292, 1.917, 1.291, 0.586, 0.688, 0.772, 2.288, 3.273, 4.292, 3.786, 0.923, 0.919, 1.71, 2.121, 3.416, 1.715, 1.701, 1.739, 1.56, 3.057, 0.305, 0.231, 1.401, 1.669, 1.606, 2.741, 4.294, 3.752, 1.976, 0.676, 1.281, 1.897, 2.727, 2.516, 2.716, 3.551, 2.338, 0.991, 0.038, 0.013, 0.401, 2.727, 3.485, 1.984, 1.567, 3.671, 3.508, 2.972, 2.644, 1.356, 2.193, 7.424, 3.679, 0.403, 0.0, 0.009, 0.004, 0.796, 0.216, 1.037, 0.98, 3.091, 3.117, 3.388, 2.314, 1.652, 0.118, 0.055, 0.175, 0.007, 0.005, 0.051, 0.835, 1.611, 4.59, 1.463, 0.966, 0.0, 0.192, 0.006, 0.516, 1.301, 2.942, 4.167, 0.077, 0.015, 0.345, 0.065, 0.787, 0.53, 0.678, 0.042, 0.0, 0.041, 0.001]

    Xs = np.random.random(500)
    Ys = np.random.random(500)

    r = Regression(Xs, "XXX", Ys, "YYY")    
    r.compute()
    r.plot()


