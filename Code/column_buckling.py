import numpy as np
from matplotlib import pyplot as plt
from skin_stress import skin_stress
import scipy as sp
from scipy import interpolate
from load_case import LoadCase

class design_option_column:
    '''a class for column buckling of the stringers for a design option'''
    def __init__(self, a_stringer: float, n_stringers, a_t: float, lengths: list, t_s, t_f: float, t_r: float, option = 0):
        #define the variables
        self.a_stringer = a_stringer
        self.n_stringers = n_stringers
        self.a = np.sqrt(a_stringer*a_t/2)
        self.t_s = t_s
        self.t_f = t_f
        self.t_r = t_r
        self.load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
        self.option = option

        #check if lengths were specified
        if lengths is None:
            self.lengths = self.calc_lengths()
        else:
            self.lengths = np.array(lengths)


        #calculate the y coordinate of the ribs
        self.ribs = []
        for i in range(len(self.lengths)):
            self.ribs.append(np.sum(self.lengths[:i+1]))

        #get the critical stresses
        crit_stress = self.crit_stress()

        #interpolate the critical stresses
        if len(self.lengths)==1:
            crit_stress = np.append(crit_stress, crit_stress)
            self.ribs = np.append(self.ribs, self.ribs[0]+1)

        self.critical_stress = sp.interpolate.interp1d(self.ribs, crit_stress, kind = "next", fill_value="extrapolate")

    def calc_lengths(self) -> list:
        '''calculates the required lengths of the stringers'''
        #define the variables
        k = 4
        e = 68e9

        #initialize the variables
        rib_lengths = []
        y = 0

        #find the lengths
        while y<12:
            stress = skin_stress(y, self.t_f, self.t_r, self.t_s(y), self.a_stringer, self.load, self.n_stringers(y), 1)
            if not y:
                print(stress)
            length = np.sqrt(k * np.pi**2*e*self.a**2 / (6*stress))
            rib_lengths.append(length)

            #update the y coordinate
            y+=length

        return np.array(rib_lengths)

    def crit_stress(self) -> float:
        '''calculates the critical stress'''
        #define the variables
        k = 4 #both ends clamped - very much non-conservative
        #k = 1 #both ends pinned - cpnservative
        e = 68e9

        #calculate the critical stress
        crit_stress = k * np.pi**2*e*self.a**2 / (6*self.lengths**2)

        #return the critical stress
        return crit_stress
    
    def test(self) -> bool:
        '''tests whether the design option satisfies the column buckling requirement'''
        y_axis = np.linspace(0,12,100)

        critical = self.critical_stress(y_axis)

        actual = []
        for y in y_axis:
            if self.critical_stress(y)/skin_stress(y, self.t_f, self.t_r, self.t_s(y), self.a_stringer, self.load, self.n_stringers(y), 1) < 1:
                return False
        return True
    
    def generate_plot(self):
        '''generates the plot of the margin of safety for column buckling'''
        #define the y-axis
        y_axis = np.linspace(0,12,1000)

        #calculate the critical stress
        critical = self.critical_stress(y_axis)

        #calculate the actual stress at each y location
        actual = []
        for y in y_axis:
            actual.append(skin_stress(y, self.t_f, self.t_r, self.t_s(y), self.a_stringer, self.load, self.n_stringers(y), 1))
        actual = np.array(actual)

        #calculate the factor
        factor = critical/actual

        #plot the values
        plt.plot(y_axis, factor)
        plt.yscale("log")
        plt.xlim(0,12)
        plt.ylim(1)
        plt.xlabel("Spanwise location [m]")
        plt.ylabel("Margin of Safety [-]")
        plt.grid(1)

        #define the name of the file
        # option = 3-(self.n_stringers==2)
        name = f"./Figures/mos_col_option_{self.option}.svg"
        # plt.show()
        #save the plot
        plt.savefig(name, format="svg")

        #clear the plot
        plt.cla()

def main():
    a_stringer = (35*10**-3)**2
    t_f = 5.5*10**-3 #m
    t_r = 4*10**-3 #m

    #OPTION1:
    m = 0.362
    n = lambda x: 6 if x< 7.49 else 4 if x<8.7 else 2
    ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.785, 8.08, 8.385, 8.7, 9.06, 9.435, 9.735, 12])
    t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 7.1e-3, 5.6e-3])
    y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 7.49, 9.435, 12])
    t_s = sp.interpolate.interp1d(y_lst, t_lst, kind="next", fill_value="extrapolate")

    
    lengths = np.zeros(len(ribs_list))
    for i in range(0,len(ribs_list)):
        if i == 0:
            lengths[i] = ribs_list[i]
        else:
            lengths[i] = ribs_list[i]-ribs_list[i-1]
    # option_1 = design_option_column(m*a_stringer, n, 10, lengths,t_s,t_f,t_r,1)

    #OPTION2:
    m = 0.362
    # n = lambda x: 6 if x<8.885 else 4 if x< 9.41 else 2
    # ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.65, 7.81, 7.975, 8.145, 8.305, 8.47, 8.66, 8.885, 9.145, 9.41, 9.745, 10.105, 12])
    # t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 4.4e-3, 5.2e-3])
    # y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 8.145, 8.885, 12])
    # t_s = sp.interpolate.interp1d(y_lst, t_lst, kind="next", fill_value="extrapolate")
    n= lambda x:2
    t_s = lambda x: 13.7e-3
    m=0.08
    lengths = np.zeros(len(ribs_list))
    for i in range(0,len(ribs_list)):
        if i == 0:
            lengths[i] = ribs_list[i]
        else:
            lengths[i] = ribs_list[i]-ribs_list[i-1]
    option_2 = design_option_column(m*a_stringer, n, 10, None,t_s,t_f,t_r,1)

    #OPTION3:
    m = 0.265
    n = lambda x: 4 if x<8.62 else 2
    ribs_list = np.array([0, 0.345, 0.69, 1.02, 1.35, 1.655, 1.96, 2.25, 2.535, 2.815, 3.09, 3.36, 3.63, 3.895, 4.155, 4.41, 4.665, 4.92, 5.175, 5.41, 5.645, 5.88, 6.115, 6.335, 6.555, 6.775, 6.995, 7.2, 7.405, 7.615, 7.825, 8.02, 8.215, 8.415, 8.62, 8.975, 9.34, 9.59, 9.85, 10.13, 12])
    # t_lst = np.array([13.3e-3, 12.5e-3, 11.4e-3, 10.4e-3, 10.0e-3, 9.5e-3, 9.2e-3, 8.7e-3, 7.7e-3, 6.8e-3, 6.0e-3, 5.3e-3, 7.0e-3, 4.8e-3])
    # y_lst = np.array([0.69, 1.35, 1.96, 2.535, 3.09, 3.63, 4.155, 5.175, 6.115, 6.995, 7.825, 8.62, 9.34, 12])


    #[13.6e-3, 12.7e-3, 7.0e-3, 3.2e-3, 2.1e-3, 2.0e-3, 2.0e-3]
    #[13.6e-3, 12.3e-3, 10.9e-3, 9.9e-3, 9.2e-3, 7.9e-3, 6.5e-3, 4.4e-3, 2.8e-3, 2e-3, 1.7e-3, 1.5e-3]
     
    #[0.71, 4.25, 7.11, 8.30, 9.37, 10.34, 12]
    #[0.94,1.78,2.36,2.86,3.68,4.71,6.14,7.43,8.59,9.13,9.64,12]
    # t_s = sp.interpolate.interp1d(y_lst, t_lst, kind="next", fill_value="extrapolate")
    t_s = lambda x: 13.7e-3
    n= lambda x: 4
    m=0.265
    
    lengths = np.zeros(len(ribs_list))
    for i in range(0,len(ribs_list)):
        if i == 0:
            lengths[i] = ribs_list[i]
        else:
            lengths[i] = ribs_list[i]-ribs_list[i-1]
    # load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)    #define option 2
    option_3 = design_option_column(m*a_stringer, n, 10, None,t_s,t_f,t_r,2)
    #define option 3

    #generate the plots
    # option_1.generate_plot()
    option_2.generate_plot()
    option_3.generate_plot()
    # option_3.generate_plot()

if __name__=="__main__":
    main()