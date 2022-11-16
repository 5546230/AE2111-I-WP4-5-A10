import numpy as np
import scipy as sp
from scipy import integrate
from interpolation import get_mspan
from matplotlib import pyplot as plt

# find the values of the torque
y_axis = np.linspace(0,11.98,100)
m_span = []
for y in (y_axis):
    m_span_val, error = sp.integrate.quad(get_mspan, y, 11.98)
    m_span.append(m_span_val)

    
#Plot the values
plt.plot(y_axis, m_span)
plt.title("Torque distribution")
plt.ylabel("Torque [Nm]")
plt.xlabel("Spanwise location [m]")
plt.show()