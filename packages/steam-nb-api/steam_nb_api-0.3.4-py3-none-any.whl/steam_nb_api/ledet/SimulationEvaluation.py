import os
import numpy as np
import pandas as pd
import re
from scipy.interpolate import interp1d
from tqdm import tqdm
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import h5py
from steam_nb_api.ledet.ParameterSweep import *
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
import csv
import nptdms
from nptdms import TdmsFile


@dataclass
class TDMSdata:
    FileName: str = ''
    Tolerance: float = 20.0
    groupHF:  nptdms.GroupObject = nptdms.GroupObject('HF')
    groupMF: nptdms.GroupObject = nptdms.GroupObject('MF')
    VoltageVertices: np.ndarray = np.array([])
    TimeFrame_MF: np.ndarray = np.array([])
    t_steps_MF:  float = 0.0
    t_d_MF: float = 0.0
    trigger_PC: int = 0
    trigger_shoot: int = 0
    I_DCCT_MF: np.ndarray = np.array([])
    I_DCCT_HF: np.ndarray = np.array([])
    I_CLIQ: np.ndarray = np.array([])
    U_CLIQ: np.ndarray = np.array([])
    I_QH: np.ndarray = np.array([])
    U_QH: np.ndarray = np.array([])
    QL1: float = 0.0
    QL2: float = 0.0

@dataclass
class SIMdata:
    FileName: str = ''
    TimeFrame: np.ndarray = np.array([])
    trigger_PC: int = 0
    XY_mag_ave: np.ndarray = np.array([])
    I_CoilSections: np.ndarray = np.array([])
    I_CLIQ: np.ndarray = np.array([])
    directionsCLIQ: np.ndarray = np.array([])
    U_CLIQ: np.ndarray = np.array([])
    I_QH: np.ndarray = np.array([])
    U_QH: np.ndarray = np.array([])
    QL1: float = 0.0
    QL2: float = 0.0

def EvaluateSimulations(MatFolder, MagnetName, MeasFile, SweepObject, Mat = True, Plots = True, SkipAlign = False, SetdITol = 200, showBestFit = 10):
    print("Reading Data and evaluate")
    #Collect Simulated Data
    flag_BasePoints = 0
    BasePoints = 0
    SimData = np.array([])
    RData = np.array([])
    items = os.listdir(MatFolder)
    with tqdm(total=len(items)/2) as pbar:
        for item in items:
            try:
                if Mat:
                    if item.endswith('.mat'):
                        if ".sys" not in item:
                            num = item.replace('SimulationResults_LEDET_', '')
                            num = num.replace(".mat", '')
                            f = h5py.File(MatFolder+"//" + item, 'r')
                            T = np.array(f.get("time_vector"))
                            if not flag_BasePoints:
                                BasePoints = T.shape[0]
                                SimData = np.zeros((1, BasePoints + 1))
                                SimData[0, :] = np.append([0], T.astype(float))
                                flag_BasePoints = 1
                            data = f.get("I_CoilSections")
                            ILedet = np.append([num], np.array(data[0]))
                            try:
                                data = f.get("R_CoilSections")
                                RLedet = np.append([num], np.array(data))
                                RData = np.vstack((RData, RLedet.astype(float)))
                            except:
                                pass
                            SimData = np.vstack((SimData, ILedet.astype(float)))

                if not Mat:
                    if item.endswith('.txt') and 'VariableHistory' in item:
                        if ".sys" not in item:
                            num = item.replace(MagnetName + '_VariableHistory_', '')
                            num = num.replace(".txt", '')
                            try:
                                x = int(num)
                            except:
                                print("Magnetname does not fit to file names. Please check!")
                                return
                            with open(MatFolder+"//" + item, 'r') as file:
                                k = file.readline().split(',')[:-1]
                                try:
                                    idxT = k.index('time_vector')
                                except:
                                    idxT = k.index(' time_vector')
                                idxI = k.index(' I_CoilSections_1')
                                rows = [[float(x) for x in line.split(',')[:-1]] for line in file]
                                cols = [list(col) for col in zip(*rows)]
                                try:
                                    idxR = k.index(' R_CoilSections_1')
                                    R = np.array(cols[idxR])
                                    T  = np.array(cols[idxT])
                                    RLedet = np.append([num], np.array(R))
                                    if RData.size == 0:
                                        RData = RLedet.astype(float)
                                    elif not T.size == SimData[0, :].size:
                                        RL = interp1d(T, np.array(RLedet[1:]), kind='cubic')
                                        RLedet = RL(SimData[0, :])
                                        RData = np.vstack((RData, RLedet.astype(float)))
                                except:
                                    print("Error reading R, no abort")
                                    pass
                                T = np.array(cols[idxT])
                                ISim = np.array(cols[idxI])
                            if not flag_BasePoints:
                                BasePoints = T.shape[0]
                                SimData = np.append([0], T)
                            #Check if size is the same
                            if flag_BasePoints:
                                if not T.size == SimData[0,:].size:
                                    IL = interp1d(T, np.array(ISim), kind='cubic')
                                    ISim = IL(SimData[0,1:])
                            ILedet = np.append([num], np.array(ISim))
                            SimData = np.vstack((SimData, ILedet.astype(float)))
                            flag_BasePoints = 1
            except:
                 print("Reading of " + item + " was not successful")
                 continue
            pbar.update(1)
    if SimData.size != 0:
        print("Reading Data was successful")
    else:
        print("Error while reading. Please check files")
        return

    Time_Zone = [float(T[0]), float(T[-1])]

    #Prepare Measured Data
    mat = pd.read_csv(MeasFile)
    Tmeas = np.array(mat.iloc[:, 0])
    try:
        Imeas = mat["IAB.I_A"].values
    except:
        try:
            Imeas = mat["STATUS.I_MEAS"].values
        except:
            try:
                Imeas = mat["IABI_A"].values
            except:
                print("Measured Data is unknown. Neither I_A nor I_MEAS")
                return

    if not SkipAlign:
        #Find Start-IDX
        idx_up = np.argmin(abs(Tmeas - (Time_Zone[1]-Time_Zone[0])))
        dImeas1 = np.gradient(Imeas, Tmeas)
        dImeas1[abs(dImeas1) < SetdITol] = 0
        tshift = Tmeas[np.nonzero(dImeas1)[0][0]]
        dImeas = np.gradient(SimData[1, 1:], SimData[0, 1:])
        dImeas[abs(dImeas) < SetdITol] = 0
        tshift_Sim = SimData[0, 1:][np.nonzero(dImeas)[0][0]]
        tshift = tshift - tshift_Sim
        idx_low = np.argmin(abs(Tmeas - tshift - Time_Zone[0]))
    else:
        idx_low = 0
        idx_up = -1

    #Start Evaluation
    SimData[0, 1:] = SimData[0, 1:] - Time_Zone[0]
    MSESims = np.ones((SimData.shape[0] - 1, 2)) * 9999
    LDSims = np.ones((SimData.shape[0] - 1, 2)) * 9999
    FImeas = interp1d(Tmeas[idx_low:idx_up]+abs(Tmeas[idx_low]), Imeas[idx_low:idx_up], kind='cubic')
    Tmeas2 = SimData[0, 1:]
    try:
        Imeas2 = FImeas(Tmeas2)
    except:
        print("Interpolating Data was not sucessful.")
        print("Start-Point of Tmeas", Tmeas[idx_low]+abs(Tmeas[idx_low]), ", Start-Point of Tsim:", SimData[0, 1])
        print("End-Point of Tmeas", Tmeas[idx_up] + abs(Tmeas[idx_low]), ", End-Point of Tsim:", SimData[0, -1])
        return

    SweepMatrix = SweepObject.SweepMatrix
    #Calculate MSE
    for i in range(1, SimData.shape[0]):
        MSESims[i-1, 0] = SimData[i, 0]
        MSESims[i-1, 1] = (np.square(SimData[i, 1:] - Imeas2[:])).mean(axis=0)

    # Calculate largest Deviation
    for i in range(1, SimData.shape[0]):
         LDSims[i - 1, 0] = SimData[i, 0]
         LDSims[i - 1, 1] = np.amax(abs(SimData[i, 1:].astype(float) - Imeas2[:]))

    print("Best Fit for Meas-StartIDX: ", idx_low)
    BestFit = np.argsort(MSESims[:, 1])
    print("Best fitting simulations for MSE: ")
    print(MSESims[BestFit[:showBestFit], 0])
    print(MSESims[BestFit[:showBestFit], 1])
    BestFit = np.argsort(LDSims[:, 1])
    print("Best fitting simulations based on smallest, largest Deviation: ")
    print(LDSims[BestFit[:showBestFit], 0])
    print(LDSims[BestFit[:showBestFit], 1])

    SweepMatrix = SweepObject.SweepMatrix
    ParametersToSweep = SweepObject.ParametersToSweep

    #Parameter Importance Study -- Ablation Analysis
    # 1. Extract best 10% of the Simulations
    NumberBest = int(np.floor(SimData.shape[0]/1))
    if SimData.shape[0]<10: NumberBest = SimData.shape[0]-3
    BestFit = np.argsort(MSESims[:, 1])[0:NumberBest]
    SweepedParameters = SweepMatrix.shape[1]
    AbMatrix = np.zeros((SweepedParameters, NumberBest))
    MaxVar = np.zeros((SweepedParameters,))
    Var = np.zeros((SweepedParameters,))
    print(NumberBest)
    print(BestFit.shape)
    for i in range(SweepedParameters):
        for j in range(len(BestFit)):
            AbMatrix[i, j] = SweepMatrix[BestFit[j],i]
        MaxVar[i] = np.var(SweepMatrix[:, i])
        Var[i] = np.var(AbMatrix[i, :])/MaxVar[i]

    print("Ordered Importance of Parameters: ")
    Order = np.argsort(Var)
    for i in range(SweepedParameters):
        print(ParametersToSweep[Order[i]]+", ", end = '')
    print("\n Corresponding Variances: ")
    for i in range(SweepedParameters):
        print(Var[Order[i]])
    print("\n")

    #Make fancy plot
    if Plots:
        ##Plot1
        fig = plt.figure()
        ax = fig.add_subplot(111)
        opacity = 0.5
        dec = 0.4/NumberBest
        colors = cm.spring
        TotLength = int(len(SimData[0,:])/2)
        LengthStep = int(TotLength/len(BestFit))
        ax.plot(SimData[0, 1:].astype(float), SimData[BestFit[0]+1, 1:].astype(float), color=colors(2*opacity),
                alpha=opacity, label='_nolegend_')
        # ax.text(SimData[0, TotLength].astype(float),SimData[BestFit[0]+1, TotLength].astype(float), str(0), alpha = opacity)
        for i in range(1,len(BestFit)):
            opacity = (opacity - dec)
            ax.plot(SimData[0, 1:].astype(float), SimData[BestFit[i]+1, 1:].astype(float), color=colors(2*opacity),
                    alpha=opacity, label='_nolegend_')
            # ax.text(SimData[0, TotLength+i*LengthStep].astype(float), SimData[BestFit[i]+1, TotLength+i*LengthStep].astype(float), str(i),
            #         alpha=opacity)
        sm = plt.cm.ScalarMappable(cmap=colors)
        cbar = plt.colorbar(sm)
        cbar.set_ticks([1])
        cbar.set_ticklabels(["Best Fit"])
        meas = ax.plot(Tmeas2, Imeas2, color='black', label='Measurement')
        ax.set_xlabel('t [s]', fontsize =20)
        ax.set_ylabel('I [A]', fontsize =20)
        ax.legend(fontsize =20)
        ax.grid(True)

        flag_No3Dplots = 0
        try:
            #Plot two most important parameters together on MSE
            Vals1 = SweepObject.ParameterMatrix[Order[0], :][SweepObject.ParameterMatrix[Order[0], :] != 0]
            Vals2 = SweepObject.ParameterMatrix[Order[1], :][SweepObject.ParameterMatrix[Order[1], :] != 0]
            Vals3 = SweepObject.ParameterMatrix[Order[2], :][SweepObject.ParameterMatrix[Order[2], :] != 0]
        except:
            print("No 3D Data Found. Following Plots are not plottable.")
            flag_No3Dplots = 1
        InitVals = SweepMatrix[0, :]
        D1 = np.zeros((Vals1.shape[0]))
        try:
            D2 = np.zeros((Vals2.shape[0]))
            D3 = np.zeros((Vals3.shape[0]))
        except:
            pass
        for i in range(Vals1.shape[0]):
            for j in range(SweepMatrix.shape[0]):
                if SweepMatrix[j, Order[0]] == Vals1[i]:
                    Cp = np.delete(SweepMatrix[j, :], Order[0])
                    Cp2 = np.delete(InitVals[:], Order[0])
                    if np.allclose(Cp, Cp2):
                        Idx = MSESims[:, 0]
                        Idx = Idx[Idx == j]
                        D1[i] = int(Idx[0])
        try:
            for i in range(Vals2.shape[0]):
                for j in range(SweepMatrix.shape[0]):
                    if SweepMatrix[j, Order[1]] == Vals2[i]:
                        Cp = np.delete(SweepMatrix[j, :], Order[1])
                        Cp2 = np.delete(InitVals[:], Order[1])
                        if np.allclose(Cp, Cp2):
                            Idx = MSESims[:, 0]
                            Idx = Idx[Idx == j]
                            D2[i] = int(Idx[0])
            for i in range(Vals3.shape[0]):
                for j in range(SweepMatrix.shape[0]):
                    if SweepMatrix[j, Order[2]] == Vals3[i]:
                        Cp = np.delete(SweepMatrix[j, :], Order[2])
                        Cp2 = np.delete(InitVals[:], Order[2])
                        if np.allclose(Cp, Cp2):
                            Idx = MSESims[:, 0]
                            Idx = Idx[Idx == j]
                            D3[i] = int(Idx[0])
        except:
            pass

        x = SweepMatrix[D1.astype(int), Order[0]]
        try:
            y = SweepMatrix[D2.astype(int), Order[1]]
            k = SweepMatrix[D3.astype(int), Order[2]]
        except:
            pass

        if flag_No3Dplots==1: return
        ##Plot 2
        verts = []
        zs = [1.0, 2.0, 3.0]
        xs = (np.concatenate([[x[0]], x[:], [x[-1]]])-x[0])/(x[-1]-x[0])
        xb = SweepMatrix[BestFit[0]+1,0]
        ys = (np.concatenate([[y[0]], y[:], [y[-1]]])-y[0])/(y[-1]-y[0])
        yb = SweepMatrix[BestFit[0]+1,1]
        ks = (np.concatenate([[k[0]], k[:], [k[-1]]])-k[0])/(k[-1]-k[0])
        kb = SweepMatrix[BestFit[0]+1,2]
        xMS = np.concatenate([[0], 1/MSESims[D1.astype(int), 1], [0]])
        yMS = np.concatenate([[0], 1/MSESims[D2.astype(int), 1], [0]])
        kMS = np.concatenate([[0], 1/MSESims[D3.astype(int), 1], [0]])
        verts.append(list(zip(xs, xMS)))
        verts.append(list(zip(ys, yMS)))
        verts.append(list(zip(ks, kMS)))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        poly = PolyCollection(verts, facecolors=['r', 'g', 'y'])
        poly.set_alpha(0.7)
        zs = [1.0, 2.0, 3.0]
        ax.add_collection3d(poly, zs=zs, zdir='y')
        ax.set_xlabel('Values [0=Min, 1=Max Value]', fontsize =14, labelpad=10)
        ax.set_xlim3d(0, 1)
        ax.set_ylabel('Parameters', fontsize = 14,labelpad=20)
        ax.set_ylim3d(0, 4)
        ax.set_zlabel('Inverse MSE', fontsize = 14,labelpad=10)
        ax.set_zlim3d(0, 1/MSESims[BestFit[0], 1])
        plt.yticks(zs, ParametersToSweep, fontsize =14)
        plt.plot([xb/np.max(SweepMatrix[:,0])],[1.], 1/MSESims[BestFit[0], 1], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=4, alpha=0.6, label="Best fit")
        plt.plot([yb/np.max(SweepMatrix[:,1])], [2.], 1/MSESims[BestFit[0], 1], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=4,
                 alpha=0.6)
        plt.plot([kb/np.max(SweepMatrix[:,2])], [3.], 1/MSESims[BestFit[0], 1], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=4,
                 alpha=0.6)
        plt.plot([xb/np.max(SweepMatrix[:,0]),yb/np.max(SweepMatrix[:,1]),kb/np.max(SweepMatrix[:,2])],[1.,2.,3.],[1/MSESims[BestFit[0], 1],
                                            1/MSESims[BestFit[0], 1],1/MSESims[BestFit[0], 1]],'--',color='black')
        plt.plot([xb / np.max(SweepMatrix[:, 0]),xb / np.max(SweepMatrix[:, 0])], [1.,1.], [0.,1/MSESims[BestFit[0], 1]],'--',color='r')
        plt.plot([yb / np.max(SweepMatrix[:, 1]),yb / np.max(SweepMatrix[:, 1])], [2.,2.], [0.,1/MSESims[BestFit[0], 1]],'--',color='g')
        plt.plot([kb / np.max(SweepMatrix[:, 2]),kb / np.max(SweepMatrix[:, 2])], [3.,3.], [0.,1/MSESims[BestFit[0], 1]],'--',color='y')
        plt.legend(fontsize =14)
        plt.show()

        ##Plot 3
        LastSim = SweepMatrix.shape[0]-D2.shape[0]*Order[1]-1
        D = np.ceil(np.linspace(0, LastSim, D1.shape[0]*D2.shape[0]))
        D_mesh = D.reshape(D1.shape[0], D2.shape[0])
        X, Y = np.meshgrid(x, y)
        Z = 1./MSESims[D_mesh.astype(int), 1]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, np.transpose(Z), color='white', edgecolors='grey', alpha=0.5)
        ax.scatter(X.flatten(), Y.flatten(), np.transpose(Z).flatten(), c='red')
        ax.set_xlabel(ParametersToSweep[Order[0]], fontsize =11)
        ax.set_ylabel(ParametersToSweep[Order[1]], fontsize =11)
        ax.set_zlabel('Inverse MSE', fontsize =16)
        plt.show()

        # # Plot4
        RData = np.max(RData, axis=1)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, RData[D_mesh.astype(int)], color='white', edgecolors='grey', alpha=0.5)
        ax.scatter(X.flatten(), Y.flatten(), RData[D_mesh.astype(int)].flatten(), c='red')
        ax.set_xlabel(ParametersToSweep[Order[0]], fontsize =11)
        ax.set_ylabel(ParametersToSweep[Order[1]], fontsize =11)
        ax.set_zlabel('R_CoilSections', fontsize =16)
        plt.show()

        ##Plot 5
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(SweepMatrix[BestFit, Order[0]], SweepMatrix[BestFit, Order[1]], SweepMatrix[BestFit, Order[2]],
                    c='red', marker='^', label = 'Low Error')
        ax.scatter(np.delete(SweepMatrix[:, Order[0]], BestFit),
                   np.delete(SweepMatrix[:, Order[1]], BestFit),
                   np.delete(SweepMatrix[:, Order[2]], BestFit),
                   c='blue', marker='o', label='High error')
        ax.legend(fontsize =11)
        ax.set_xlabel(ParametersToSweep[Order[0]], fontsize =11)
        ax.set_ylabel(ParametersToSweep[Order[1]], fontsize =11)
        ax.set_zlabel(ParametersToSweep[Order[2]], fontsize =11)
        plt.show()

class QuenchPlanAnalysis():
    def __init__(self,FileNameTDMS, FileNameSIMData):
        self.beforePC = 0.1
        self.Colors = self.__generateColors()

        self.MergedVoltages = {}

        self.SIMdata = SIMdata()
        self.SIMdata.FileName = FileNameSIMData
        self.__CreateSIMDataObject()

        self.TDMSdata = TDMSdata()
        self.TDMSdata.FileName = FileNameTDMS
        self.__CreateTDMSDataObject()

        self.__calculateAllQuenchIntegrals()

    def __generateColors(self):
        # setting colors for plotting
        col = mcolors.TABLEAU_COLORS.keys()
        col2 = mcolors.BASE_COLORS.keys()
        col3 = mcolors.CSS4_COLORS.keys()
        colors = []
        for c in col:
            colors = colors + [c]
        for c in col2:
            if c == 'w': continue
            colors = colors + [c]
        for c in col3:
            if c == 'white': continue
            if c == 'snow': continue
            colors = colors + [c]
        return colors

    def __FillHeaterArrays(self, Heaters, trigger_shoot):
        Heat_len = len(self.TDMSdata.groupMF[Heaters[0]].data[trigger_shoot:])
        if Heaters[0].startswith('I'): self.TDMSdata.I_QH = np.zeros((len(Heaters), Heat_len))
        elif Heaters[0].startswith('U'): self.TDMSdata.U_QH = np.zeros((len(Heaters), Heat_len))
        for k in Heaters:
            order = int(k[-1])
            if Heaters[0].startswith('I'): self.TDMSdata.I_QH[order-1] = self.TDMSdata.groupMF[k].data[trigger_shoot:]
            elif Heaters[0].startswith('U'): self.TDMSdata.U_QH[order-1] = self.TDMSdata.groupMF[k].data[trigger_shoot:]

    def __CreateVoltageVertices(self):
        ## 1. Extract all channels that are relevant
        temp_Sections = re.compile("([a-zA-Z]+)([0-9]+)([a-zA-Z]+)([0-9]+)([a-zA-Z]+)([0-9]+)")
        temp_Coils = re.compile("([0-9]+)([a-zA-Z]+)")
        CSections = []
        Coils = []
        Coils_Diff = []

        for channel in self.TDMSdata.groupMF.channels():
            if channel.properties['TransducerType'] == 'vtaps':
                chName = channel.name.replace("_"," ")
                chName = chName.replace("-"," ")
                chName = chName.replace(" ", "")
                try:
                    res = temp_Sections.match(chName).groups()
                    ChN = res + (str(res[0]+res[1]+'_'+res[2]+res[3]+"_"+res[4]+res[5]),) + (str(res[0]+res[1]+'_'+res[4]+res[5]+"_"+res[2]+res[3]),)+ (channel.name,)
                    CSections.append(ChN)
                except:
                    pass
                if chName.startswith("Vcoil"):
                    try:
                        res = temp_Coils.match(chName[5:]).groups()
                        ChN = res + (channel.name,)
                        Coils_Diff.append(ChN)
                    except:
                        Coils.append((chName[5:], channel.name))

        ## 2. order them in coils
        def getKey0(item):
            return item[0]
        def getKey1(item):
            return item[1]
        CSections = sorted(CSections, key=getKey1)
        Coils = sorted(Coils, key=getKey0)
        Coils_Diff = sorted(Coils_Diff, key=getKey0)

        self.TDMSdata.VoltageVertices = CSections

        ##TODO: also construct sth. for Diffs and Coils

        return

    def __CreateTDMSDataObject(self):
        tdms_file = TdmsFile.read(self.TDMSdata.FileName)
        ## Save groups
        for group in tdms_file.groups():
            if group.name == 'HF': self.TDMSdata.groupHF = tdms_file['HF']
            elif group.name == 'MF': self.TDMSdata.groupMF = tdms_file['MF']
            else: print("Don't understand group: ", group)

        ## Pick channels and store conveniently
        I_Heaters = []
        U_Heaters = []
        for channel in self.TDMSdata.groupHF.channels():
            if channel.name == 'IDCCT_HF': self.TDMSdata.I_DCCT_HF = channel.data
        for channel in self.TDMSdata.groupMF.channels():
            if channel.name == 'IDCCT_HF':
                self.TDMSdata.I_DCCT_MF = channel.data*1000
                self.TDMSdata.t_steps_MF = channel.properties['wf_samples']
                self.TDMSdata.t_d_MF = channel.properties['wf_increment']
            if channel.name == 'Trigger_PC':
                trigger_data = channel.data
            if channel.name == 'I Cliq':self.TDMSdata.I_CLIQ = channel.data
            if channel.name == 'V Cliq': self.TDMSdata.U_CLIQ = channel.data
            if channel.name.startswith("I_Heater"): I_Heaters.append(channel.name)
            if channel.name.startswith("U_Heater"): U_Heaters.append(channel.name)
        ## Set up Timeframe
        self.TDMSdata.TimeFrame_MF = np.linspace(0,self.TDMSdata.t_steps_MF*self.TDMSdata.t_d_MF, int(self.TDMSdata.t_steps_MF))
        #self.TDMSdata.goupHF['IDCCT_HF'].time_track()
        trigger_shoot = np.gradient(trigger_data, self.TDMSdata.t_d_MF)
        trigger_shoot = np.where(abs(trigger_shoot)>self.TDMSdata.Tolerance)[0][0]-int(self.beforePC/self.TDMSdata.t_d_MF)
        self.TDMSdata.trigger_PC = int(self.beforePC/self.TDMSdata.t_d_MF)
        self.TDMSdata.trigger_shoot = trigger_shoot
        self.TDMSdata.TimeFrame_MF = self.TDMSdata.TimeFrame_MF[trigger_shoot:]-self.TDMSdata.TimeFrame_MF[trigger_shoot]
        self.TDMSdata.I_DCCT_MF = self.TDMSdata.I_DCCT_MF[trigger_shoot:]
        self.TDMSdata.I_CLIQ = self.TDMSdata.I_CLIQ[trigger_shoot:]
        self.TDMSdata.U_CLIQ = self.TDMSdata.U_CLIQ[trigger_shoot:]
        self.__FillHeaterArrays(I_Heaters, trigger_shoot)
        self.__FillHeaterArrays(U_Heaters, trigger_shoot)
        self.__CreateVoltageVertices()
        return

    def __CreateSIMDataObject(self):
        if self.SIMdata.FileName.endswith('.mat'):
            file = self.SIMdata.FileName
            f = h5py.File(file, 'r')
            self.SIMdata.TimeFrame = np.array(f.get("time_vector"))
            self.SIMdata.I_CoilSections = np.array(f.get("I_CoilSections")).transpose()
            self.SIMdata.I_CLIQ = np.array(f.get("Ic")).transpose()
            trigger = np.array(f.get("t_PC"))[0][0]-self.beforePC
            if trigger < float(self.SIMdata.TimeFrame[0]):
                self.beforePC = -1* self.SIMdata.TimeFrame[0]
                trigger = np.array(f.get("t_PC"))[0][0] - self.beforePC
                print("Switch aligning to tStart of Simulation!")
            trigger_shoot = np.where(abs(self.SIMdata.TimeFrame-trigger)<1E-4)[0][0]
            self.SIMdata.trigger_PC = np.where(abs(self.SIMdata.TimeFrame-np.array(f.get("t_PC"))[0][0])<1E-4)[0][0]
            self.SIMdata.TimeFrame = self.SIMdata.TimeFrame[trigger_shoot:]-self.SIMdata.TimeFrame[trigger_shoot]
            self.SIMdata.I_CoilSections = self.SIMdata.I_CoilSections[:, trigger_shoot:]
            self.SIMdata.I_CLIQ = self.SIMdata.I_CLIQ[trigger_shoot:]
            self.SIMdata.directionsCLIQ = np.array(f.get("directionCurrentCLIQ"))
            U_CLIQ = np.array(f.get("Uc"))
            self.SIMdata.U_CLIQ = U_CLIQ[:][trigger_shoot:]
            I_QH = np.array(f.get("I_QH"))
            self.SIMdata.I_QH = I_QH[:][trigger_shoot:]
            U_QH = np.array(f.get("U_QH"))
            self.SIMdata.U_QH = U_QH[:][trigger_shoot:]
            self.SIMdata.XY_mag_ave = np.array(f.get("XY_MAG_ave"))
        else:
            print("Please provide .mat file for Simulation.")

    def __calculateQuenchIntegral(self, time, current):
        dt = np.gradient(time)
        QL  = np.sum(np.multiply(dt, np.power(current,2)))/1E6
        return QL

    def __calculateAllQuenchIntegrals(self):
        ## QL Integral 1 - from Quench
        ## Find quench
        ## Cut parts and

        ## QL Integral 2  - full transient
        ## QL Measured Data
        self.TDMSdata.QL2 = self.__calculateQuenchIntegral(self.TDMSdata.TimeFrame_MF[self.TDMSdata.trigger_PC:],
                                                           self.TDMSdata.I_DCCT_MF[self.TDMSdata.trigger_PC:])
        ## QL Sim Data
        if abs(sum(self.SIMdata.I_CLIQ)) > 0:
            idxC = np.where(self.SIMdata.directionsCLIQ > 0)[0][0]
            self.SIMdata.QL2 = self.__calculateQuenchIntegral(self.SIMdata.TimeFrame[self.SIMdata.trigger_PC:, 0],
                                                              self.SIMdata.I_CoilSections[self.SIMdata.trigger_PC:,
                                                              idxC])
        else:
            self.SIMdata.QL2 = self.__calculateQuenchIntegral(self.SIMdata.TimeFrame[self.SIMdata.trigger_PC:, 0],
                                                              self.SIMdata.I_CoilSections[self.SIMdata.trigger_PC:, 0])

    def _GetTDMSCoilStructure(self):
        CoilCount = 0
        for i in range(len(self.TDMSdata.VoltageVertices)):
            temp = self.TDMSdata.VoltageVertices[i][1]
            if CoilCount != temp:
                CoilCount = temp
                print("*** Coil: ", CoilCount)
            print("-->",self.TDMSdata.VoltageVertices[i][2]+self.TDMSdata.VoltageVertices[i][3],
                  " to ", self.TDMSdata.VoltageVertices[i][4]+self.TDMSdata.VoltageVertices[i][5])
        return

    def FindQuenchTDMS(self, Vthreshold, ValidationTime, Plot=1):
        tSteps = int(ValidationTime/self.TDMSdata.t_d_MF)
        found = 0

        if not self.MergedVoltages:
            print("Please first provide Coil-Structure. ")
            print("Obj.ProvideTurnsToCoilStructure(self, TurnsToVtaps: Dict)")
            return

        for key in self.MergedVoltages.keys():
            Udata = self.TDMSdata.groupMF[key].data
            if self.TDMSdata.trigger_shoot > 10000:
                Udata = Udata - np.sum(Udata[:10000]) / 10000
            else:
                print("Failed to calculate SNR for Voltage channel.")
                return
            Qidx = np.where(abs(Udata[:self.TDMSdata.trigger_shoot+self.TDMSdata.trigger_PC]) > Vthreshold)[0]
            if len(Qidx)> 0:
                for i in range(len(Qidx)):
                    QQidx = np.where(Udata[Qidx[i]:Qidx[i]+tSteps]>Vthreshold)[0]
                    if len(QQidx) >= (0.95*tSteps) and (Qidx[i]+tSteps)<(self.TDMSdata.trigger_shoot+self.TDMSdata.trigger_PC):
                        tQuench = Qidx[i]-self.TDMSdata.trigger_shoot
                        if tQuench < 0:
                            print("Detected Quench in {} at {}".format(key, (Qidx[i] - self.TDMSdata.trigger_shoot)*self.TDMSdata.t_d_MF))
                        else:
                            print("Detected Quench in {} at {}".format(key, self.TDMSdata.TimeFrame_MF[Qidx[i] - self.TDMSdata.trigger_shoot]))
                        found = 1
                        if Plot:
                            try:
                                fig = plt.figure()
                                ax = fig.add_subplot(111)
                                ax.grid(True)
                                ax.set_title("Detected quench in - "+key)
                                ax.set_ylim([-3*Vthreshold,3*Vthreshold])
                                ax.plot(self.TDMSdata.TimeFrame_MF[tQuench-tSteps:tQuench+int(3*tSteps)],Udata[Qidx[i]-tSteps:Qidx[i]+int(3*tSteps)],'--')
                                ax.axvline(self.TDMSdata.TimeFrame_MF[Qidx[i] - self.TDMSdata.trigger_shoot],c='r')
                                ax.legend(["$U_{Res,"+key+"}$","$t_{Quench}$"])
                            except:
                                pass
                        break

            # fig = plt.figure()
            # ax = fig.add_subplot(111)
            # ax.set_title(key)
            # ax.plot(np.linspace(0, len(Udata), len(Udata)), Udata, '--')
        if not found:
            print("No quench detected.")

    def GetCoilStructure(self, Print = 0, Plot = 1):
        if Print:
            for key in self.MergedVoltages.keys():
                print(key, " --> ", self.MergedVoltages[key])
        if Plot:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            count = 0
            legend =[]
            for key in self.MergedVoltages.keys():
                idxTap = self.MergedVoltages[key]
                legend.append(key)
                ax.scatter(self.SIMdata.XY_mag_ave[0,idxTap.astype(int)-1], self.SIMdata.XY_mag_ave[1,idxTap.astype(int)-1], s = 10, c = self.Colors[count])
                count = count + 1
            ax.axis('equal')
            ax.grid('minor')
            ax.set_xlabel("x [mm]")
            ax.set_ylabel("y [mm]")
            ax.set_title("Turns to V-Taps")
            ax.legend(legend)
        return

    def ProvideTurnsToCoilStructure(self, Coil):
        if not self.MergedVoltages:
            for i in range(len(Coil)):
                self.MergedVoltages = {**self.MergedVoltages, **Coil[i]}
            MVcopy = self.MergedVoltages.copy()
            for old_key in MVcopy.keys():
                if len(self.MergedVoltages[old_key]) == 0:
                    self.MergedVoltages.pop(old_key)
                else:
                    found = 0
                    for i in range(len(self.TDMSdata.VoltageVertices)):
                        if old_key == self.TDMSdata.VoltageVertices[i][6] or  old_key == self.TDMSdata.VoltageVertices[i][7]:
                            new_key = self.TDMSdata.VoltageVertices[i][8]
                            self.MergedVoltages[new_key] = self.MergedVoltages.pop(old_key)
                            found = 1
                            break
                    if not found:
                        print("Couldn't find voltage-tap: {} in TDMS.".format(old_key))
                        self.MergedVoltages.pop(old_key)
            return
        else:
            self.__CreateTDMSDataObject()
            self.ProvideTurnsToCoilStructure(Coil)
            return

    def QuenchPlanAnalysis(self, Plot = 0):
        # Plot current together
        if Plot:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            legend = []
            for i in range(self.SIMdata.I_CoilSections.shape[1]):
                legend.append("$I_{Sim, CoilSection " + str(i+1) + "}$")
                ax.plot(self.SIMdata.TimeFrame, self.SIMdata.I_CoilSections[:,i], color= self.Colors[i])
            if sum(self.SIMdata.I_CLIQ) != 0:
                ax.plot(self.SIMdata.TimeFrame, self.SIMdata.I_CLIQ, color= self.Colors[self.SIMdata.I_CoilSections.shape[1]+1])
                legend.append("$I_{Sim,CLIQ}$")
                ax.plot(self.TDMSdata.TimeFrame_MF, self.TDMSdata.I_CLIQ, color=self.Colors[self.SIMdata.I_CoilSections.shape[1]+2])
                legend.append("$I_{Meas,CLIQ}$")
            ax.plot(self.TDMSdata.TimeFrame_MF, self.TDMSdata.I_DCCT_MF, color= self.Colors[self.SIMdata.I_CoilSections.shape[1]+3])
            legend.append("$I_{Meas}$")
            ax.grid(True)
            ax.set_ylabel("Current [A]", fontsize=20)
            ax.set_xlabel("Time [s]", fontsize=20)
            ax.set_ylim([np.amin([np.amin(self.SIMdata.I_CoilSections),np.amin(self.SIMdata.I_CLIQ), np.amin(self.TDMSdata.I_DCCT_MF)])*1.1,
                         np.amax([np.amax(self.SIMdata.I_CoilSections),np.amax(self.SIMdata.I_CLIQ), np.amax(self.TDMSdata.I_DCCT_MF)])*1.1])
            ax.set_xlim([0, np.amax([np.amax(self.TDMSdata.TimeFrame_MF), np.amax(self.SIMdata.TimeFrame)])])
            ax.legend(legend,fontsize=20)
            ax.set_title(self.TDMSdata.FileName[-13:])
        return [self.TDMSdata, self.SIMdata]