import numpy as np

# Define the grid and rewards
rewards = np.array([
    [-5, -5, 20, 0],
    [-5, -1, -5, 0],
    [ 0, -20, 10, 0],
    [ 0,  0, 0,  0],
])


# Dimensions of the grid
rows, cols = rewards.shape
# Define the discount factor (gamma) and the threshold for convergence
gamma = 1.0
threshold = 1e-4

# Initialize the value function to zero for all states
value_function = np.zeros((rows, cols))

# Define the actions and their corresponding move probabilities
actions = {
    'right': [
        (0, 1, 0.8), # go 0 in y direction and 1 in x direction
        (1, 1, 0.2) # go 1 in x direction and 1 in y direction
    ],
    'up': [
        (-1, 0, 1.0) # go -1 in y direction 
    ]
}

def get_value(row, col):
    if 0 <= row < rows and 0 <= col < cols:
        return value_function[row, col]
    return 0

def value_iteration():
    global value_function
    while True:
        new_value_function = np.copy(value_function)
        delta = 0

        for row in range(rows):
            for col in range(cols):
                # consier columns and rows more that 2 as terminal
                if col == 3 or row == 3:
                    continue
                if (col == 2 and row == 2) or (col ==2 and row == 0):  
                    # Skip terminal states (end cells)
                    continue
                
                action_values = []
                for action, transitions in actions.items():
                    action_value = 0
                    for dr, dc, prob in transitions:
                        new_row, new_col = row + dr, col + dc
                        reward = rewards[new_row, new_col]
                        action_value += prob * (reward + gamma * get_value(new_row, new_col))
                    action_values.append(action_value)
                
                new_value_function[row, col] = max(action_values)
                delta = max(delta, abs(new_value_function[row, col] - value_function[row, col]))

        value_function = new_value_function
        if delta < threshold:
            break

def extract_policy():
    policy = np.full((rows, cols), ' ')
    for row in range(rows):
        for col in range(cols):
            if col == 3 or row == 3:  
                # ignore rows and columns more than 2
                policy[row, col] = 'end'
                continue

            if (col == 2 and row == 2) or (col ==2 and row == 0):  
                # Skip terminal states (end cells)
                policy[row, col] = 'end'
                continue
            
            best_action = None
            best_value = float('-inf')
            for action, transitions in actions.items():
                action_value = 0
                for dr, dc, prob in transitions:
                    new_row, new_col = row + dr, col + dc
                    reward = rewards[new_row, new_col]
                    action_value += prob * (reward + gamma * get_value(new_row, new_col))
                
                if action_value > best_value:
                    best_value = action_value
                    best_action = action
            
            policy[row, col] = best_action
    
    return policy

# Run value iteration
value_iteration()

# Extract and print the policy
policy = extract_policy()
print("Grid:")
print(rewards)
print("Optimal Value Function:")
print(value_function)
print("\nOptimal Policy:")
print(policy)

