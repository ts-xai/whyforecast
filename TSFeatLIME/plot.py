import matplotlib.pyplot as plt

# Example data
# data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#
# # Rolling window visualization
# window_size = 5
# rolling_windows = [data[i:i+window_size] for i in range(len(data)-window_size+1)]
#
# plt.figure(figsize=(10, 6))
# for i, window in enumerate(rolling_windows):
#     plt.plot(range(i, i+window_size), window, label=f"Window starting at {i}")
# plt.title('Rolling Window Visualization')
# plt.legend()
# plt.show()

# # Extending window visualization
# extending_windows = [data[:i+1] for i in range(len(data))]
#
# plt.figure(figsize=(10, 6))
# for i, window in enumerate(extending_windows):
#     plt.plot(window, label=f"Window size {i+1}")
# plt.title('Extending Window Visualization')
# plt.legend()
# plt.show()

# import matplotlib.pyplot as plt
#
# # Rolling window mean values
rolling_window_means = [-3.41182412e+11, -7.07880715e+11, 9.63804407e+11, -5.64542188e+11,
                        1.04634699e+12, -6.50936910e+10, 2.66356010e+11, -4.07380950e+10,
                        -4.06045976e+11, 7.98550461e+10]
#
# # Labels for the x-axis. Starting from lag(12,11,10) for the first value and then one lag for each subsequent value
# lags = ['lag(12,11,10)', 'lag(11,10,9)', 'lag(10,9,8)', 'lag(9,8,7)', 'lag(8,7,6)', 'lag(7,6,5)',
#         'lag(6,5,4)', 'lag(5,4,3)', 'lag(4,3,2)', 'lag(3,2,1)']
#
# plt.figure(figsize=(12,6))
# plt.plot(lags, rolling_window_means, marker='o', color='b', linestyle='-')
# plt.title('Rolling Window Mean Values')
# plt.xlabel('Lags')
# plt.ylabel('Mean Value')
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)
# plt.xticks(rotation=45)
# plt.tight_layout()
#
# plt.show()

import matplotlib.pyplot as plt

# Assuming you have your rolling_window_means values defined somewhere above
lags = ['lag(12,11,10)', 'lag(11,10,9)', 'lag(10,9,8)', 'lag(9,8,7)', 'lag(8,7,6)', 'lag(7,6,5)',
        'lag(6,5,4)', 'lag(5,4,3)', 'lag(4,3,2)', 'lag(3,2,1)']

# Create a 2x1 subplot layout
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 12))

# Plot for the first subplot
axes[0].plot(lags, rolling_window_means, marker='o', color='b', linestyle='-')
axes[0].set_title('Rolling Window Mean Values')
axes[0].set_xlabel('Lags')
axes[0].set_ylabel('Mean Value')
axes[0].grid(True, which='both', linestyle='--', linewidth=0.5)
axes[0].tick_params(axis='x', rotation=45)

# Plot for the second subplot - you can modify or duplicate the content as per your needs
axes[1].plot(lags, rolling_window_means, marker='o', color='r', linestyle='-.')
axes[1].set_title('Rolling Window Mean Values')
axes[1].set_xlabel('Lags')
axes[1].set_ylabel('Mean Value')
axes[1].grid(True, which='both', linestyle='--', linewidth=0.5)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()



