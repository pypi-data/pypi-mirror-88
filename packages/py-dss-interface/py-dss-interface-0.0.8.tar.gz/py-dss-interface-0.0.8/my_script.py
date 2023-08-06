# First import the Package
import py_dss_interface

# Creates an OpenDSS object
dss = py_dss_interface.DSSDLL()

# Select the DSS model
dss_file = r"C:\MeuTCC\Paulo_Example\DSSFiles\MASTER_RedeTeste13Barras.dss"

# Compile
dss.text("compile {}".format(dss_file))

# Solve
dss.solution_solve()

dss.loadshapes_first()
dss.loadshapes_read_pmult()

new = list(dss.loadshapes_read_pmult())
new[2] = 0

dss.loadshapes_write_pmult(new)
# Show Voltage Report

print("worked here")
print(dss.loadshapes_read_pmult())
dss.text("show voltages")

# Get all buses voltages
allbusvolts = dss.circuit_allbusvolts()

print(dss.circuit_allbusvolts())

