## Import functions
import backend.ETrprocess as ETr
import backend.Kc_process as Kc
# import backend.swd_total as swd_total

# from ETr import get_ETr
# from Kc import get_Kc

import backend.asce as asce
import backend.cwsi as cwsi
import backend.irls as irls
import numpy as np
from pandas import read_excel, concat, DataFrame, Index, MultiIndex, date_range
from numpy import empty, full
import matplotlib.pyplot as plt


def load(file_name, sheet):
    return read_excel(file_name, sheet_name=sheet)

def load_filename(file_name):

    #### Loading the information
    st = load(file_name, 'sites')
    wx = load(file_name, 'weather')
    idx = load(file_name, 'index')

    ### canopy temperature
    tc = load(file_name, 'canopy temperature') \
            .merge(idx, on='plot', how='right') \
            .groupby(['DOY', 'hour', 'treatment'])['Tc'] \
            .mean() \
            .reset_index()
            

    cc = load(file_name, 'canopy cover') \
            .merge(idx, on='plot', how='right') \
            .groupby(['DOY', 'treatment'])['cc'] \
            .mean() \
            .reset_index()

    ### SAP: provides a measurement of the transpiration of the plant
    sa = load(file_name, 'sap flow') \
            .merge(idx, on='plot', how='right') \
            .groupby(['treatment', 'DOY', 'hour'])['sap'] \
            .mean() \
            .reset_index() \
            .rename(columns={'sap': 'Sa'})

    return tc, cc, wx, st, idx

def treatment_selection(tc, cc, wx, treatment = 'SWB_90'):
    
    wx['DOY'] = wx['day']               ### Main file Sc computation has problems without DOY in wx, Linh changed
    
    ### Filter the the calculation in the treatment
    cc_tmp = cc[cc['treatment'] == treatment]
    doy = Index(range(cc_tmp['DOY'].min(), cc_tmp['DOY'].max() + 1), name='DOY')
    cc_tmp = cc_tmp.set_index('DOY').reindex(doy).sort_index().interpolate() \
            .reset_index()
    tc_tmp = tc[tc['treatment'] == treatment]
    tmp = []
    for _, df in tc_tmp.groupby('DOY'):
            if len(df) == 24:
                tmp.append(df)
                
    tc_tmp = concat(tmp).sort_values(['DOY', 'hour'])
    days = set(cc_tmp['DOY']).intersection(tc_tmp['DOY']).intersection(wx['DOY'])
    cc_tmp = cc_tmp[cc_tmp['DOY'].isin(days)]
    tc_tmp = tc_tmp[tc_tmp['DOY'].isin(days)]
    wx_tmp = wx[wx['DOY'].isin(days)]

    ### There is a mask applied as a filter to dataframe wx
    df = tc_tmp.merge(wx_tmp, on=['DOY', 'hour'])
    
    return df


def plots_the_retrieval(idx, tc, cc, wx, st, day_start, day_end, treatment_select, h0, h_end, hour_select, plot_cwsi = True, plot_ab = True):
    df = treatment_selection(tc, cc, wx, treatment_select)

    # num_days = len(df['DOY'].unique())
    # num_hours_points = len(range(h0, h_end))
    # n = int(num_days * num_hours_points)
    
    steps = day_end - day_start + 1
    days = np.linspace(day_start, day_end, steps)
    days = [int(item) for item in days]
    h_end = h_end + 1     ### Due to the range function
    

    # print(days)

    ### Data for the date 196 not available
    if 196 in days:
        days.remove(196)
    else:
        pass
    
    num_days = len(days)
    num_hours_points = len(range(h0, h_end))
    n = int(num_days * num_hours_points)
    
    #### Initialize the values: see Cullen's updated function
    DELTA = empty(n)
    Rnc = empty(n)
    VPD = empty(n)
    # omega = empty(n)
    rho = empty(n)
    
    ### Same thing: fixed for all days
    z = st['elev'][0]
    st['P'] = P = asce.P(st['elev'][0])         ### atmospheric pressure (kPa)
    st['Lm'] = Lm = asce.Lm(st['lon'][0])     ### See function Lm: longitude of measurement site (positive degrees west of Greenwich England)
    st['gamma'] = gamma = asce.gamma(P)         #### psychrometric constant (kPa*C^-1)
    st['phi'] = phi = asce.phi(st['lat'][0])    ### latitude of measurement site (rad)
    Lz = st['Lz'][0]
    fcd = 0.055 # initialize fcd for cloudless night
    
    ## Filter the Tc and Ta
    Tc_range = []
    Ta_range = []
    
    for i, DOY in enumerate(days):
        Sc = asce.Sc(DOY)
        delta = asce.delta(DOY)
        omegas = asce.omegas(delta, phi)
        dr = asce.dr(DOY)
        df_oneday = df[df['DOY']== DOY]
        Rs = df_oneday['Rs'].values
        Ta = df_oneday['Ta'].values
        RH = df_oneday['RH'].values
        Tc = df_oneday['Tc'].values
        for j, h in enumerate(range(h0, h_end)):
            Rsh, Tah, Tch = Rs[h], Ta[h], Tc[h] # store for multiple uses
            omega = asce.omega(Lm, Lz, Sc, h, 60, 1)            # Cullen applied condition on omega but not here since the time constraint in Linh's
            omega2 = asce.omega2(omega, omegas, 1)
            omega1 = asce.omega1(omega, omega2, omegas, 1)
            Ra = asce.Ra(dr, delta, omega1, omega2, phi)
            Rso = asce.Rso(Ra, z)
            beta = asce.beta(delta, omega, phi)
            fcd = asce.fcd(Rsh, Rso, beta, fcd)
            es = asce.es(Ta[h])
            ea = asce.ea(RH[h], es)
            Rnl = asce.Rnl(Tah, ea, fcd)
            Rns = asce.Rns(Rsh)
            Rn = asce.Rn(Rnl, Rns)
            DELTA[i*num_hours_points + j] = asce.DELTA(Tah)
            rho[i*num_hours_points + j] = cwsi.rho(P, Tah)
            Rnc[i*num_hours_points + j] = cwsi.Rnc(Rn)
            VPD[i*num_hours_points + j] = es - ea
            
            Tc_range.append(Tch)
            Ta_range.append(Tah)
            
    Tc_range = np.array(Tc_range)
    Ta_range = np.array(Ta_range)
    
    dif = Tc_range - Ta_range
    DELTA_bar = DELTA.mean()
    Rnc_bar = Rnc.mean()
    rho_bar = rho.mean()
    
    # robust (iteratively reweighted least squares, Tukey edition) regression
    X = irls.design(VPD, 1) # first degree polynomial design matrix
    (a, b), _ = irls.irls(X, dif) # regression coefficeints (ignore weights)
    ra_bar = cwsi.ra(DELTA_bar, Rnc_bar, a, b, rho_bar) # aerodynamic resistance
    rc_bar = cwsi.rc(DELTA_bar, b, gamma, ra_bar) # canopy resistance  
    
    ############################################
    ############################################ After retrieving a, b, ra_bar, rc_bar
    cwsi_e = []
    cwsi_t2 = []

    cwsi_e_dictionary = {}
    cwsi_t2_dictionary = {}

    del DELTA
    del rho
    
    for i, DOY in enumerate(days):
        Sc = asce.Sc(DOY)
        delta = asce.delta(DOY)
        omegas = asce.omegas(delta, phi)
        dr = asce.dr(DOY)
        df_oneday = df[df['DOY']== DOY]
        Rs = df_oneday['Rs'].values
        Ta = df_oneday['Ta'].values
        RH = df_oneday['RH'].values
        Tc = df_oneday['Tc'].values
        for j, h in enumerate(range(h0, h_end)):
            Rsh, Tah, Tch = Rs[h], Ta[h], Tc[h] # store for multiple uses
            omega = asce.omega(Lm, Lz, Sc, h, 60, 1)            # Cullen applied condition on omega but not here since the time constraint in Linh's
            omega2 = asce.omega2(omega, omegas, 1)
            omega1 = asce.omega1(omega, omega2, omegas, 1)
            Ra = asce.Ra(dr, delta, omega1, omega2, phi)
            Rso = asce.Rso(Ra, z)
            beta = asce.beta(delta, omega, phi)
            fcd = asce.fcd(Rsh, Rso, beta, fcd)
            es = asce.es(Tah)
            ea = asce.ea(RH[h], es)
            Rnl = asce.Rnl(Tah, ea, fcd)
            Rns = asce.Rns(Rsh)
            Rn = asce.Rn(Rnl, Rns)
            DELTA = asce.DELTA(Tah)   ## diffrent from DELTA in previous loop
            rho = cwsi.rho(P, Tah)
            Rnc = cwsi.Rnc(Rn)
            ul = cwsi.ul(Rnc, ra_bar, rho)
            ll = cwsi.ll(DELTA, ea, es, gamma, ra_bar, rc_bar, ul)
            if h == hour_select:  
                cwsi_t2.append(cwsi.cwsi(Tah, Tch, ll, ul))
                cwsi_t2_dictionary[DOY] = cwsi.cwsi(Tah, Tch, ll, ul)

            ##### The part of emperical method
            vpd = es - ea
            vpg = es - asce.es(Tah + a)
            ul_e = a + b * vpg
            ll_e = a + b * vpd
            if h == hour_select:
                cwsi_e.append(cwsi.cwsi(Tah, Tch, ll_e, ul_e))
                cwsi_e_dictionary[DOY] = cwsi.cwsi(Tah, Tch, ll_e, ul_e)
                
    ETr_dictionary = ETr.get_ETr(st, wx)

    plt.figure(figsize=(20, 6))
    plt.plot(ETr_dictionary.keys(), ETr_dictionary.values(), marker='.', label="ET reference")
    plt.title(f"Evapotranspiration Reference Values (ETr)    Site: {st["site"].iloc[0]}")
    plt.xlabel('Days')
    plt.ylabel("mm/day")
    plt.tight_layout()    
    plt.legend()
    plt.grid(True,alpha=0.4)
    plt.savefig("./static/ETreference.png")

    Kc_dictionary = Kc.get_Kc(day_start, day_end)

    plt.figure(figsize=(20, 6))  # Width of 12 inches and height of 6 inches
    plt.plot(Kc_dictionary.keys(), Kc_dictionary.values(), marker=".", label="Crop Coefficient")

    plt.title(f"Crop Coefficient Values (Kcr)    Site: {st["site"].iloc[0]}")
    plt.xlabel('Days')
    plt.legend()
    plt.grid(True,alpha=0.4)
    plt.tight_layout()    
    plt.savefig("./static/Kc_values.png")
    
    theoretical_result = []
    theoretical_date = []

    emperical_result = []
    emperical_date = []

    now = day_start
    while (now <= day_end):
        if (now in ETr_dictionary and now in Kc_dictionary and now in cwsi_t2_dictionary):
            theoretical_result.append(float(ETr_dictionary[now] * Kc_dictionary[now] * (1-cwsi_t2_dictionary[now])))
            theoretical_date.append(now)

        if (now in ETr_dictionary and now in Kc_dictionary and now in cwsi_t2_dictionary):
            emperical_result.append(float(ETr_dictionary[now] * Kc_dictionary[now] * (1-cwsi_e_dictionary[now])))
            emperical_date.append(now)
        now=now+1

    #### Plot the results
    plt.figure(figsize=(20, 6))

    # plt.figure()
    plt.plot(theoretical_date, theoretical_result, marker=".", color='blue', label = "Theoretical")
    plt.plot(emperical_date, emperical_result, color='red', marker=".", label = "Emperical")
    plt.xlabel('Days')
    plt.ylabel("mm/day")
    plt.title("Evapotranspiration (ET = ETr * Kcr * Ks) for " + treatment_select)
    plt.legend()
    plt.tight_layout()  
    plt.grid(True,alpha=0.4)
    plt.savefig("./static/merged_result.png")

    plt.figure(figsize=(20, 6))
    plt.plot(days, cwsi_t2, marker=".", color='blue', label = "Theoretical")
    plt.plot(days, cwsi_e, marker=".", color='red', label = "Emperical")
    plt.xlabel('Days')
    plt.title("CWSI for " + treatment_select)
    plt.legend()
    plt.tight_layout()    
    plt.grid(True,alpha=0.4)
    plt.savefig("./static/cwsi_graph.png")


    cwsi_t2_2 = []
    for thing in cwsi_t2:
        cwsi_t2_2.append(1 - thing)

    cwsi_e_2 = []
    for thing in cwsi_e:
        cwsi_e_2.append(1 - thing)

    plt.figure(figsize=(20, 6))
    plt.plot(days, (cwsi_t2_2), marker=".", color='blue', label = "Theoretical")
    plt.plot(days, (cwsi_e_2), marker=".", color='red', label = "Emperical")
    plt.xlabel('Days')
    plt.ylabel('Ks coefficients')
    plt.title("Water Stress Coefficient (Ks = 1 - CWSI)")
    plt.legend()
    plt.tight_layout()    
    plt.grid(True,alpha=0.4)
    plt.savefig("./static/Ks_graph.png")

    # ETt = {}
    # ETe = {}

    # for i,day in enumerate(theoretical_date):
    #     ETt[day] = theoretical_result[i]
    # for i,day in enumerate(emperical_date):
    #     ETe[day] = emperical_result[i]

    # swd_total.get_swd(ETt, ETe)

def plot_the_buttons(file_name, day_start, day_end, treatment, start_hour, end_hour, select_hour): 
    tc, cc, wx, st, idx = load_filename(file_name)
    plots_the_retrieval(idx, tc, cc, wx, st, day_start, day_end, treatment, start_hour -1, end_hour, select_hour-1)