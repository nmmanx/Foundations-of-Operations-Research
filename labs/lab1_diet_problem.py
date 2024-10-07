import mip

# Food
I = {'Bread', 'Milk', 'Eggs', 'Meat', 'Cake'}

# Nutrients
J = {'Calories', 'Proteins', 'Calcium'}

# Cost in Euro per hg of food
c = {'Bread':0.1, 'Milk':0.5, 'Eggs':0.12, 'Meat':0.9, 'Cake':1.3}

# Availability per hg of food
q = {'Bread':4, 'Milk':3, 'Eggs':1, 'Meat':2, 'Cake':2}

# minum nutrients 
b = {'Calories':600, 'Proteins':50, 'Calcium':0.7}

# Nutrients per hf of food
a = {('Bread','Calories'):30,('Milk','Calories'):50,('Eggs','Calories'):150,('Meat','Calories'):180,('Cake','Calories'):400,
('Bread','Proteins'):5,('Milk','Proteins'):15,('Eggs','Proteins'):30,('Meat','Proteins'):90,('Cake','Proteins'):70,
('Bread','Calcium'):0.02,('Milk','Calcium'):0.15,('Eggs','Calcium'):0.05,('Meat','Calcium'):0.08,('Cake','Calcium'):0.01}

# Define a model
model = mip.Model()

# Define variables
x = {i:model.add_var(name = i,lb=0) for i in I}

# Define the objective function
model.objective = mip.minimize(mip.xsum(x[i]*c[i] for i in I))

# CONSTRAINTS

# Availability constraint
for i in I:
  model.add_constr(x[i] <= q[i])

# Minum nutrients
for j in J:
  model.add_constr(mip.xsum(x[i]*a[(i,j)] for i in I) >= b[j])

# Optimizing command
model.optimize()

# Optimal objective function value
model.objective.x

# Printing the variables values
for i in model.vars:
  print(i.name)
  print(i.x)