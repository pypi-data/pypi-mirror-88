# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 18:14:29 2016

@author: becker
"""

import numpy as np
import scipy.sparse as spsp
import scipy.sparse.linalg as splinalg
# from functools import partial

import simfempy.tools.analyticalfunction
import simfempy.tools.timer
import simfempy.tools.iterationcounter
import simfempy.applications.problemdata

#=================================================================#
class Application(object):
    def __init__(self, **kwargs):
        self.linearsolvers=['umf', 'lgmres', 'bicgstab']
        try:
            import pyamg
            self.linearsolvers.append('pyamg')
        except:
            import warnings
            warnings.warn("*** pyamg not found (umf used instead)***")
        self.linearsolver = 'umf'
        self.timer = simfempy.tools.timer.Timer(verbose=0)
        if 'problemdata' in kwargs:
            # self.problemdata = copy.deepcopy(kwargs.pop('problemdata'))
            self.problemdata = kwargs.pop('problemdata')
            self.ncomp = self.problemdata.ncomp
            assert self.ncomp != -1
        if 'exactsolution' in kwargs:
            self.exactsolution = kwargs.pop('exactsolution')
            self._generatePDforES = True
            if 'random' in kwargs:
                self.random_exactsolution = kwargs.pop('random')
            else:
                self.random_exactsolution = False
        else:
            self._generatePDforES = False
        if 'geom' in kwargs:
            self.geom = kwargs.pop('geom')
            print(f"{self.geom=}")
            mesh = self.geom.generate_mesh()
            self.mesh = simfempy.meshes.simplexmesh.SimplexMesh(mesh=mesh)
        if 'mesh' in kwargs:
            self.mesh = kwargs.pop('mesh')
        self._setMeshCalled = False
    def setParameter(self, paramname, param):
        assert 0
    def dirichletfct(self):
        if self.ncomp > 1:
            def _solexactdir(x, y, z):
                return [self.problemdata.solexact[icomp](x, y, z) for icomp in range(self.ncomp)]
        else:
            def _solexactdir(x, y, z):
                return self.problemdata.solexact(x, y, z)
        return _solexactdir
    def generatePoblemDataForAnalyticalSolution(self):
        bdrycond = self.problemdata.bdrycond
        self.problemdata.solexact = self.defineAnalyticalSolution(exactsolution=self.exactsolution, random=self.random_exactsolution)
        print("self.problemdata.solexact", self.problemdata.solexact)
        self.problemdata.params.fct_glob['rhs'] = self.defineRhsAnalyticalSolution(self.problemdata.solexact)
        for color in self.mesh.bdrylabels:
            if color in bdrycond.type and bdrycond.type[color] in ["Dirichlet","dirichlet"]:
                bdrycond.fct[color] = self.dirichletfct()
            else:
                if color in bdrycond.type:
                    cmd = "self.define{}AnalyticalSolution(self.problemdata,{})".format(bdrycond.type[color], color)
                    # print(f"cmd={cmd}")
                    bdrycond.fct[color] = eval(cmd)
                else:
                    bdrycond.fct[color] = self.defineBdryFctAnalyticalSolution(color)
        # for color in self.mesh.bdrylabels:
        #     if not color in bdrycond.type: raise KeyError(f"{color=} {bdrycond.type=}")
        #     if bdrycond.type[color] in ["Dirichlet"]:
        #     else:
        #         type = bdrycond.type[color]
        #         cmd = "self.define{}AnalyticalFunction(self.problemdata,{})".format(type, color)
        #         # print(f"cmd={cmd}")
        #         bdrycond.fct[color] = eval(cmd)
    def defineAnalyticalSolution(self, exactsolution, random=True):
        dim = self.mesh.dimension
        return simfempy.tools.analyticalfunction.analyticalSolution(exactsolution, dim, self.ncomp, random)
    def setMesh(self, mesh):
        self.mesh = mesh
        self._setMeshCalled = True
        if hasattr(self,'_generatePDforES') and self._generatePDforES:
            self.generatePoblemDataForAnalyticalSolution()
            self._generatePDforES = False
    def compute_cell_vector_from_params(self, name, params):
        if name in params.fct_glob:
            xc, yc, zc = self.mesh.pointsc.T
            fct = np.vectorize(params.fct_glob[name])
            arr = fct(self.mesh.cell_labels, xc, yc, zc)
        elif name in params.scal_glob:
            arr = np.full(self.mesh.ncells, params.scal_glob[name])
        elif name in params.scal_cells:
            arr = np.empty(self.mesh.ncells)
            for color in params.scal_cells[name]:
                arr[self.mesh.cellsoflabel[color]] = params.scal_cells[name][color]
        else:
            msg = f"{name} should be given in 'fct_glob' or 'scal_glob' or 'scal_cells' (problemdata.params)"
            raise ValueError(msg)
        return arr
    def static(self, iter=100, dirname='Run'):
        # print(f"### static")
        if not self._setMeshCalled: self.setMesh(self.mesh)
        # self.timer.reset_all()
        return self.solveLinearProblem()

    # def solve(self, iter=0, dirname="Results"):
    #     return self.solveLinearProblem()

    def solveLinearProblem(self):
        # print(f"### solveLinearProblem")
        if not hasattr(self,'mesh'): raise ValueError("*** no mesh given ***")
        result = simfempy.applications.problemdata.Results()
        self.timer.add('init')
        A = self.computeMatrix()
        self.timer.add('matrix')
        b, u = self.computeRhs()
        self.timer.add('rhs')
        u, niter = self.linearSolver(A, b, u, solver=self.linearsolver)
        # print(f"{u=}")
        self.timer.add('solve')
        result.setData(self.postProcess(u))
        self.timer.add('postp')
        result.info['timer'] = self.timer
        result.info['iter'] = {'lin':niter}
        return result


    # def solveNonlinearProblem(self, u=None, sdata=None, method="newton", checkmaxiter=True):
    #     if not hasattr(self,'mesh'): raise ValueError("*** no mesh given ***")
    #     self.timer.add('init')
    #     A = self.matrix()
    #     self.timer.add('matrix')
    #     self.b,u = self.computeRhs(u)
    #     self.du = np.empty_like(u)
    #     self.timer.add('rhs')
    #     if method == 'newton':
    #         from . import newton
    #         u, nit = newton.newton(x0=u, f=self.residualNewton, computedx=self.solveForNewton, sdata=sdata, verbose=True)
    #     elif method in ['broyden2','krylov', 'df-sane', 'anderson']:
    #         sol = optimize.root(self.residualNewton, u, method=method)
    #         u, nit = sol.x, sol.nit
    #     else:
    #         raise ValueError(f"unknown method {method}")
    #     point_data, cell_data, info = self.postProcess(u)
    #     self.timer.add('postp')
    #     info['timer'] = self.timer
    #     info['iter'] = {'lin':nit}
    #     return point_data, cell_data, info

    # def residualNewton(self, u):
    #     # print(f"self.b={self.b.shape}")
    #     self.A = self.matrix()
    #     return self.A.dot(u) - self.b
    #
    # def solveForNewton(self, r, x):
    #     # print(f"solveForNewton r={np.linalg.norm(r)}")
    #     du, niter = self.linearSolver(self.A, r, x, verbose=0)
    #     # print(f"solveForNewton du={np.linalg.norm(du)}")
    #     return du

    def linearSolver(self, A, b, u=None, solver = None, verbose=1):
        print(f"### linearSolver {solver=}")
        if len(b.shape)!=1 or len(A.shape)!=2 or b.shape[0] != A.shape[0]:
            raise ValueError(f"{A.shape=} {b.shape=}")
        if solver is None: solver = self.linearsolver
        if not hasattr(self, 'info'): self.info={}
        if solver not in self.linearsolvers: solver = "umf"
        if solver == 'umf':
            return splinalg.spsolve(A, b, permc_spec='COLAMD'), 1
        elif solver in ['gmres','lgmres','bicgstab','cg']:
            if solver == 'cg':
                def gaussSeidel(A):
                    dd = A.diagonal()
                    D = spsp.dia_matrix(A.shape)
                    D.setdiag(dd)
                    L = spsp.tril(A, -1)
                    U = spsp.triu(A, 1)
                    return splinalg.factorized(D + L)
                M2 = gaussSeidel(A)
            else:
                # defaults: drop_tol=0.0001, fill_factor=10
                M2 = splinalg.spilu(A.tocsc(), drop_tol=0.1, fill_factor=3)
            M_x = lambda x: M2.solve(x)
            M = splinalg.LinearOperator(A.shape, M_x)
            counter = simfempy.tools.iterationcounter.IterationCounter(name=solver, verbose=verbose)
            args=""
            cmd = "u = splinalg.{}(A, b, M=M, tol=1e-14, callback=counter {})".format(solver,args)
            exec(cmd)
            return u, counter.niter
        elif solver == 'pyamg':
            import pyamg
            res=[]
            # u = pyamg.solve(A=A, b=b, x0=u, tol=1e-14, residuals=res, verb=False)
            B = np.ones((A.shape[0], 1))
            SA_build_args = {
                'max_levels': 10,
                'max_coarse': 25,
                'coarse_solver': 'pinv2',
                'symmetry': 'hermitian'}
            smooth = ('energy', {'krylov': 'cg'})
            strength = [('evolution', {'k': 2, 'epsilon': 4.0})]
            presmoother = ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 1})
            postsmoother = ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 1})
            strength = [('evolution', {'k': 2, 'epsilon': 4.0})]
            presmoother = ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 1})
            postsmoother = ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 1})
            ml = pyamg.smoothed_aggregation_solver(A, B, max_coarse=10)
            # ml = pyamg.smoothed_aggregation_solver(
            #     A,
            #     B=B,
            #     smooth=smooth,
            #     strength=strength,
            #     presmoother=presmoother,
            #     postsmoother=postsmoother,
            #     **SA_build_args)
            # u= ml.solve(b=b, x0=u, tol=1e-12, residuals=res, **SA_solve_args)
            SA_solve_args = {'cycle': 'V', 'maxiter': 50, 'tol': 1e-14}
            u= ml.solve(b=b, x0=u, residuals=res, **SA_solve_args)
            if(verbose): print('niter ({}) {:4d} ({:7.1e})'.format(solver, len(res),res[-1]/res[0]))
            return u, len(res)
        else:
            raise NotImplementedError("unknown solve '{}'".format(solver))



# ------------------------------------- #

if __name__ == '__main__':
    raise ValueError("unit test to be written")