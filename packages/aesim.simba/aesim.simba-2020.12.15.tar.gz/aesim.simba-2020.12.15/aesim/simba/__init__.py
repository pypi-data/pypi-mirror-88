#%% Load modules...
import clr, sys, os

foldername = os.path.dirname(os.path.abspath(__file__)) + r'\Resources'
sys.path.append(foldername)
clr.AddReference(foldername+'\\Simba.Data.dll')
from Simba.Data.Repository import ProjectRepository
from Simba.Data import License, Design, Circuit, DesignExamples
import Simba.Data
Simba.Data.FunctionsAssemblyResolver.RedirectAssembly()
Simba.Data.DoubleArrayPythonEncoder.Register()
Simba.Data.ParameterToPythonEncoder.Register()
Simba.Data.PythonToParameterDecoder.Register()
if os.environ.get('SIMBA_DEPLOYMENT_KEY') is not None:
    License.Activate(os.environ.get('SIMBA_DEPLOYMENT_KEY'))