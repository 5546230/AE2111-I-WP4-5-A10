from Weight_diagram import get_Weight
from interpolation import get_Lspan
import numpy as np


y_axis = np.linspace(0.5,11.98, 1000)


def get_resultant(y):
    return get_Lspan(y,10/180*np.pi,10,1.225)+get_Weight(y)

x_axis = np.linspace(0.5,11.98, 1000)


#plt.plot(y_axis,x_axis)# get_resultant(y_axis))
#plt.title("bla lift distribution")
#plt.ylabel("bla [N]")
#plt.xlabel("bla location [m]")
#plt.show()

print("hihhh")