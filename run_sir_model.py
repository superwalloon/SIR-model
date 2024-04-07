import sir_model as sir
import matplotlib.pyplot as plt

number_infected = []

for i in range(20):
    sir_run = sir.main()
    number_infected.append(sir_run)

fig, axs = plt.subplots(5, 4, figsize=(15, 15))
axs = axs.flatten()

for i, run_data in enumerate(number_infected):
    axs[i].plot(run_data)
    axs[i].set_title(f"Run {i+1}", fontsize = 8)
    axs[i].set_xlabel("Time (steps)", fontsize = 8)
    axs[i].set_ylabel("Number infected", fontsize = 8)

plt.tight_layout()
plt.show()

