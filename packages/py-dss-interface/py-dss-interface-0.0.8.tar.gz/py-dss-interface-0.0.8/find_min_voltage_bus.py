# First import the Package
import py_dss_interface

# Creates an OpenDSS object
dss = py_dss_interface.DSSDLL("C:/Program Files/OpenDSS")

# Select the DSS model
dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"

# Compile
dss.text("compile [{}]".format(dss_file))

# Solve
dss.solution_solve()


dss.text("Buscoords Buscoords.dat")

vmagpu = dss.circuit_allbusvmagpu()
node_names = dss.circuit_allnodenames()

vmin = min(vmagpu)
vmin_index = vmagpu.index(vmin)

node_min_voltage = node_names[vmin_index]
bus = node_min_voltage.split(".")[0]


color = "Green"
size_marker = 8
code = 15

dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus, color, size_marker, code))
dss.text("plot circuit Power max=2000 n n C1=$00FF0000")
print("here")
