import Sofa


class SceneElectroMechanical(Sofa.PythonScriptController):
    def __init__(self, node):
        self._total_simu_time = 0
        self.createGraph(node)

    def createGraph(self, root):
        # root
        {}

    # def onBeginAnimationStep(self, dt):
    #     print("Simulation time: " + str(self._total_simu_time))
    #     self._total_simu_time += dt

def createScene(root_node):
    SceneElectroMechanical(root_node)
