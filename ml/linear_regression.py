import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# generate N random points
N = 25
X = np.reshape(np.linspace(0, 0.9, N), (N, 1)) #array
Y = np.cos(10*X**2) + 0.1 * np.sin(100*X)

def poly_phi(x,n):
    res = x**0
    for i in range(1,(n+1)):
        res = np.concatenate((res,x**i),axis = 1)
    return res

def poly_reg(order):
    Phi = poly_phi(X,order)
    model=LinearRegression()
    model.fit(Phi,Y) # Fit the model -> parameters
    return model

N_ = 200
X_ = np.reshape(np.linspace(-0.3, 1.3, N_), (N_, 1)) #array
Y_ = np.cos(10*X_**2) + 0.1 * np.sin(100*X_)

# Plot
X_test = np.reshape(np.linspace(-0.3,1.3,200), (200,1))
plt.plot(X_,Y_,'ro')

model = poly_reg(0)
plt.plot(X_test,model.predict(poly_phi(X_test,0)),'y')

model = poly_reg(1)
plt.plot(X_test,model.predict(poly_phi(X_test,1)),'g')

model = poly_reg(2)
plt.plot(X_test,model.predict(poly_phi(X_test,2)),'b')

model = poly_reg(3)
plt.plot(X_test,model.predict(poly_phi(X_test,3)),'c')

model = poly_reg(11)
plt.plot(X_test,model.predict(poly_phi(X_test,11)),'k')

plt.xlabel('$x$',fontsize=20)
plt.ylabel('$y$',fontsize=20)

plt.ylim((-2,2))
plt.title('Polynomial Regression',fontsize=20)
plt.legend(['Training data','Order 0','Order 1','Order 2','Order 3','Order 11'], prop={'size':20} ,loc=0)

plt.show()

