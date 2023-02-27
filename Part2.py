#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 22:22:39 2023

@author: aglaefrison
"""

import numpy as np

# Data
hi, h0 = 8, 25
ρ, c = 1.2, 1000
e, λ = 0.028, 1.7
ρ, c = 1.2, 1000

# Geometry of the model
L = 2.15
l = 1.80
H = 3

# Surfaces
Stot = L * l
# Volume
V = L * l * H

# Surface of the bay window which is open
a = L * l * 0

# Temperatures [°C]
T0 = 4.8  # Outdoor Temperature
T2 = 18  # Setpoint temperature for room 2

# Conditions of openings
S1 = Stot - a
S2 = Stot - a

# Bay Window 1
ACH1 = 1  # 1 Volume/heure
V_dot1 = ACH1 * V / 3600  # volumetric air flow rate
m_dot1 = V_dot1 * ρ  # mass air flow rate

# Bay Window 2
ACH2 = 1  # 1 Volume/heure
V_dot2 = ACH2 * V / 3600  # volumetric air flow rate
m_dot2 = V_dot2 * ρ  # mass air flow rate

# Solar absorption [W/m2]
E = 342
ϵ_glass = 0.92

# Caractéristiques du système
ng = 6  # Number of flows
nθ = 3  # Number of temperatures

# A : incidence matrix 
A = np.zeros((ng, nθ))
A[0, 0] = 1
A[1, 0], A[1, 1] = -1, 1
A[2, 1] = 1
A[3, 1], A[3, 2] = -1, 1
A[4, 1], A[4, 2] = -1, 1
A[5, 2] = 1

# G : conductance matrix
g = np.zeros(A.shape[0])

Kp = 0

g[0] = h0 * S1
g[1] = 1 / (1 / hi + e / λ) * S1
g[2] = m_dot1 * c
g[3] = 1 / (2 / hi + e / λ) * S2
g[4] = m_dot2 * c
g[5] = Kp

G = np.diag(g)

# b : vector of sources
b = np.zeros((ng, 1))
b[0, 0] = T0
b[2, 0] = T0
b[5, 0] = T2

# f : Heat flow source vector
f = np.zeros((nθ, 1))
ϕ = E * S1 * ϵ_glass
f[0, 0] = ϕ

# Results
θ = np.linalg.inv(A.T @ G @ A) @ (A.T @ G @ b + f)
q = G @ (-A @ θ + b)

print("θ:", θ, "°C")
