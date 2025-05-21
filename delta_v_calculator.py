import numpy as np
import matplotlib.pyplot as plt

# Constants
g0 = 9.81  # Standard gravity (m/s²)
dry_mass = 20000  # kg
max_propellant = 180000  # kg

engine = {
    "isp": 1067,  # seconds
    "thrust": 10463  # kN
}

propellant_masses = np.linspace(0, max_propellant, 100)
initial_mass = dry_mass + propellant_masses
final_mass = dry_mass
delta_v = engine["isp"] * g0 * np.log(initial_mass / final_mass)

plt.figure(figsize=(10, 6))
plt.plot(propellant_masses, delta_v / 1000, label='Theoretical NTP')
plt.xlabel('Propellant Mass (kg)')
plt.ylabel('Delta-V (km/s)')
plt.title('Delta-V vs Propellant Mass for Theoretical NTP Engine')
plt.grid(True)
plt.legend()

max_dv = delta_v[-1] / 1000         
plt.text(max_propellant, max_dv, f'{max_dv:.1f} km/s', 
         verticalalignment='bottom', horizontalalignment='right')

plt.tight_layout()
plt.savefig('delta_v_plot.png')
plt.close()

print("\nMaximum Delta-V value:")
print(f"Theoretical NTP: {max_dv:.1f} km/s") 