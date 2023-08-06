# First import the Package
import py_dss_interface

# Creates an OpenDSS object
dss = py_dss_interface.DSSDLL("C:/Program Files/OpenDSS")

# Select the DSS model
dss_file = r"C:\MeuTCC\Paulo_Example\DSSFiles\MASTER_RedeTeste13Barras.dss"

# Compile
dss.text("compile {}".format(dss_file))

# Solve
dss.solution_solve()

dss.text("? Line.684652.phases")

dss.pvsystems_count()
