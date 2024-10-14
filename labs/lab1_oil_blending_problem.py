import mip

# Set of oil types
I = {'1', '2', '3', '4'}

# Set of gasoline types
J = {'A', 'B', 'C'}

# Unit cost for oil of type i 
c = {'1':9, '2':7, '3':12, '4':6}

# Availability of oil type i
b = {'1':5000, '2':2400, '3':4000, '4':1500}

# Price of gasoline of type j
r = {'A':12, 'B':18, 'C':10}

# Maximum quantity (percentage) of oil
q_max = {}
for i in I:
  for j in J:
    q_max[(str(i),j)] = 1
q_max[('2','A')] = 0.3
q_max[('1','C')] = 0.5

# Minimum quantity (percentage) of oil
q_min = {}
for i in I:
  for j in J:
    q_min[(str(i),j)] = 0
q_min[('1','A')] = 0.2
q_min[('2','B')] = 0.4

# Define a model
model2 = mip.Model()

# Define variables
y = {j:model2.add_var(name = j, lb=0) for j in J}

x = {}
for j in J:
    x[j] = {i:model2.add_var(name = j+i, lb=0) for i in I}

# Define the objective function
profit = mip.xsum(y[j]*r[j] for j in J)
cost = mip.xsum(c[i]*x[j][i] for j in J for i in I)
model2.objective = mip.maximize(profit - cost)

# CONSTRAINTS
# Availability constraint
for i in I:
  model2.add_constr(mip.xsum(x[j][i] for j in J) <= b[i])

# Conservation constraint
for j in J:
  model2.add_constr(y[j] == mip.xsum(x[j][i] for i in I))

# Maximum quantity
for i in I:
  for j in J:
    model2.add_constr(x[j][i] <= y[j]*q_max[(i,j)])
    
# Minimum quantity
for i in I:
  for j in J:
    model2.add_constr(x[j][i] >= y[j]*q_min[(i,j)])

# Optimizing command
model2.optimize()

# Printing the variables values
for i in model2.vars:
  print("{}:{}".format(i.name, i.x))

# Print the optimal profit
print("Profit: ", model2.objective.x)
