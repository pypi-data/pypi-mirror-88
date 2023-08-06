A tool to estimate Instantaneous Reproduction Number(Rt)
========================================================

cal\_r() provide real-time estimation of time-varying distribution of Rt
and infected numbers from a range of epidemic observations (e.g., number
of onsets and confirmed cases).

Usage
-----

dart = DARt(GT,D\_s,Filename)

cal\_r()

Arguments
---------

GT: generation time distribution; GT[0] represents the probability that
the secondary infection case occurs 1 day after the primary infection.

D\_s: delay time distribution; D\_s[0] represents the probability that
an individual infected is observed after 1 day.

Filename: input file; this file should contain date and corresponding
observations, the date should be sorted from the oldest to the latest.
See 'Example\_input.csv'.

References:
-----------

This tool is described in the following paper:'Revealing the
Transmission Dynamics of COVID-19: A Bayesian Framework for R\_t
Estimation'

Examples
--------

::

    GT = [0, 0, 0.165720874545241, 0.226350757019051, 0.245007574714227, 0.213515210247327,
          0.149405583474155]  # 1:7; non-zero index 3:7
    D_s = np.array([0, 0, 0, 0, 0, 0, 0.0996906, 0.1130266, 0.1143032, 0.1069238, 0.0937167999999999])
    dart = DARt(GT=GT, D_s=D_s, filename='Example_input.csv')
    dart.cal_r()
