import random
import time

class Battery:
    def __init__(self, capacity_mwh=50):
        self.capacity_mwh = capacity_mwh
        self.current_charge_mwh = capacity_mwh * 0.8 # Start at 80%
        self.health_percentage = 100.0
        self.cycles = 0
        self.degradation_rate = 0.0005 # Small degradation per cycle

    def charge(self, amount_mwh):
        if self.current_charge_mwh < self.capacity_mwh:
            self.current_charge_mwh = min(self.capacity_mwh, self.current_charge_mwh + amount_mwh)
            # Simulate minor health impact on charging
            self.health_percentage = max(0, self.health_percentage - 0.01)
            return True
        return False

    def discharge(self, amount_mwh):
        if self.current_charge_mwh >= amount_mwh:
            self.current_charge_mwh -= amount_mwh
            self.cycles += 1
            self.degrade_health()
            return True
        return False

    def degrade_health(self):
        # Simulate health degradation over time and cycles
        self.health_percentage -= self.degradation_rate * 100
        self.health_percentage = max(0, self.health_percentage)

    def get_status(self):
        return {
            "current_charge_mwh": round(self.current_charge_mwh, 2),
            "capacity_mwh": self.capacity_mwh,
            "health_percentage": round(self.health_percentage, 2),
            "cycles": self.cycles
        }

class BatteryIQ:
    def __init__(self, battery):
        self.battery = battery

    def predict_remaining_life(self, usage_pattern_mwh_per_day=5):
        # Simple prediction: estimate cycles based on current health and average daily usage
        # In a real system, this would use ML models trained on historical data.
        remaining_capacity_mwh = self.battery.capacity_mwh * (self.battery.health_percentage / 100.0)
        
        # Estimate how many more full cycles can be performed with remaining capacity
        # This is a simplification; actual usage varies.
        estimated_cycles_left = remaining_capacity_mwh / (self.battery.capacity_mwh * 0.5) # Assuming 50% discharge per cycle on average
        
        # Estimate days left based on average daily usage
        estimated_days_left = estimated_cycles_left * (self.battery.capacity_mwh / usage_pattern_mwh_per_day) # Very rough estimate
        
        return {
            "estimated_cycles_left": int(estimated_cycles_left),
            "estimated_days_left": int(estimated_days_left)
        }

    def analyze_performance(self):
        status = self.battery.get_status()
        prediction = self.predict_remaining_life()
        
        print("--- BatteryIQ Analysis ---")
        print(f"Current Charge: {status['current_charge_mwh']} MWh")
        print(f"Total Capacity: {status['capacity_mwh']} MWh")
        print(f"Health: {status['health_percentage']:.2f}%")
        print(f"Cycles: {status['cycles']}")
        print("\n--- Predictions ---")
        print(f"Estimated Cycles Left: {prediction['estimated_cycles_left']} (approx.)")
        print(f"Estimated Days Left: {prediction['estimated_days_left']} (approx. based on daily usage)")
        
        if status['health_percentage'] < 70:
            print("\nALERT: Battery health is significantly degraded. Consider replacement.")
        elif status['health_percentage'] < 85:
            print("\nNOTICE: Battery health is declining. Monitor closely.")

# --- Simulation --- 
if __name__ == "__main__":
    my_battery = Battery(capacity_mwh=100)
    battery_iq_system = BatteryIQ(my_battery)

    print("Initial Battery Status:")
    battery_iq_system.analyze_performance()
    print("\nSimulating usage for 30 days...")

    for day in range(30):
        # Simulate daily usage: discharge and recharge
        discharge_amount = random.uniform(2, 8) # Random discharge between 2-8 MWh
        if my_battery.discharge(discharge_amount):
            recharge_amount = random.uniform(1, 7) # Random recharge
            my_battery.charge(recharge_amount)
        
        # Simulate health degradation and update status periodically
        if (day + 1) % 5 == 0:
            my_battery.degrade_health() # Explicitly call degrade for simulation clarity
            print(f"\n--- Day {day + 1} --- ")
            battery_iq_system.analyze_performance()
        
        time.sleep(0.1) # Small delay for readability

    print("\n--- Final Analysis After Simulation ---")
    battery_iq_system.analyze_performance()
