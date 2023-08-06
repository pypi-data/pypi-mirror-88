# just to make sure the local simfempy is found first
from os import path
import sys
simfempypath = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.insert(0,simfempypath)
# just to make sure the local simfempy is found first


import pygmsh
import numpy as np
import simfempy
import matplotlib.pyplot as plt


# ------------------------------------- #
def pygmshexample():
    with pygmsh.geo.Geometry() as geom:
        poly = geom.add_polygon(
            [
                [+0.0, +0.5],
                [-0.1, +0.1],
                [-0.5, +0.0],
                [-0.1, -0.1],
                [+0.0, -0.5],
                [+0.1, -0.1],
                [+0.5, +0.0],
                [+0.1, +0.1],
            ],
            mesh_size=0.05,
        )
        geom.add_physical(poly.surface, label="100")
        top, vol, ext = geom.twist(
            poly,
            translation_axis=[0, 0, 1],
            rotation_axis=[0, 0, 1],
            point_on_axis=[0, 0, 0],
            angle=np.pi / 3,
        )
        geom.add_physical(top, label=f"{101+len(ext)}")
        for i in range(len(ext)): geom.add_physical(ext[i], label=f"{101+i}")
        geom.add_physical(vol, label="10")
        mesh = geom.generate_mesh()
    return mesh


def createData(bdrylabels):
    data = simfempy.applications.problemdata.ProblemData()
    bdrylabels = list(bdrylabels)
    labels_lat = bdrylabels[1:-1]
    firstlabel = bdrylabels[0]
    lastlabel = bdrylabels[-1]
    labels_td = [firstlabel,lastlabel]
    bdrycond =  data.bdrycond
    bdrycond.set("Neumann", labels_lat)
    bdrycond.set("Dirichlet", labels_td)
    bdrycond.fct[firstlabel] = lambda x,y,z: 200
    bdrycond.fct[lastlabel] = lambda x,y,z: 100
    postproc = data.postproc
    postproc.set(name="lateral mean", type='bdry_mean', colors=labels_lat)
    postproc.set(name="normal fux", type='bdry_nflux', colors=labels_td)
    # postproc.type['bdry_mean'] = "bdry_mean"
    # postproc.color['bdry_mean'] = labels_lat
    # postproc.type['bdry_nflux'] = "bdry_nflux"
    # postproc.color['bdry_nflux'] = labels_td
    data.params.scal_glob["kheat"] = 0.0001
    return data

# ------------------------------------- #
mesh = pygmshexample()
mesh = simfempy.meshes.simplexmesh.SimplexMesh(mesh=mesh)
# simfempy.meshes.plotmesh.meshWithBoundaries(mesh)

data = createData(mesh.bdrylabels.keys())
print("data", data)
data.check(mesh)

heat = simfempy.applications.heat.Heat(problemdata=data, mesh=mesh)
result = heat.static()
print(f"{result.info['timer']}")
print(f"{result.info['iter']}")
print(f"postproc: {result.data['global']['postproc']}")
simfempy.meshes.plotmesh.meshWithData(mesh, data=result.data)
plt.show()
