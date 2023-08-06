# First import the Package
import py_dss_interface

# Creates an OpenDSS object
dss = py_dss_interface.DSSDLL("C:/Program Files/OpenDSS")

# Select the DSS model
dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"

# Compile
dss.text("compile [{}]".format(dss_file))
dss.text("New EnergyMeter.Feeder Line.L115 1")

# Solve
dss.text("set mode=daily")
dss.text("set number=24")
dss.text("set stepsize=1h")

dss.text("Buscoords Buscoords.dat")

energy_base = 100000.0
energy_factor = 0


for j in range(10):
    dss.loads_first()
    for i in range(dss.loads_count()):
        dss.loads_write_kw(dss.loads_read_kw() * (1 + energy_factor))
        dss.loads_write_kvar(dss.loads_read_kvar() * (1 + energy_factor))
        dss.loads_next()

    dss.solution_solve()

    dss.meters_write_name("Feeder")
    energy_cal = dss.meters_registervalues()[0]
    losses = dss.meters_registervalues()[12]
    dss.meters_reset()

    delta_energy = energy_base - energy_cal

    energy_factor = delta_energy / energy_base

    if abs(delta_energy) < 50.0:
        break

print("Losses kW {}\nEnergy Cal kWh {}\nEnergy Base kWh {}\nNumber iterations {}".format(losses, energy_cal,
                                                                                         energy_base, j))



