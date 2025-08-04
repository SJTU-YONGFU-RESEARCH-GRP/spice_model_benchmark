#!/bin/tcsh

## 5/07/2020 Compiled Snapshots with PVS 19.12-s008 

## All DRC
ipvsGenSnapshot -name DRC_GPDK_v1p0 -dir ./Snapshots -log ipvsGenSnapshot.log -preset ./DRC_GPDK_v1p0.vipvs_preset

## FEOL
ipvsGenSnapshot -name FEOL_GPDK_v1p0 -dir ./Snapshots -log ipvsGenSnapshot.log -preset ./FEOL_GPDK_v1p0.vipvs_preset

## BEOL
ipvsGenSnapshot -name BEOL_GPDK_v1p0 -dir ./Snapshots -log ipvsGenSnapshot.log -preset ./BEOL_GPDK_v1p0.vipvs_preset

## CutMx
ipvsGenSnapshot -name CutMx_GPDK_v1p0 -dir ./Snapshots -log ipvsGenSnapshot.log -preset ./CutMx_GPDK_v1p0.vipvs_preset

## ViaColorConflict
ipvsGenSnapshot -name ViaColorConflict_GPDK_v1p0 -dir ./Snapshots -log ipvsGenSnapshot.log -preset ./ViaColorConflict_GPDK_v1p0.vipvs_preset


