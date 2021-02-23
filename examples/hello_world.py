"""
Simple example script showing a few basic uses of asf_search
"""

import json
import asf_search as asf

print('='*80)
print(f'asf.DATASET.AVNIR: {asf.DATASET.SENTINEL1}')
print(f'asf.BEAMMODE.IW: {asf.BEAMMODE.IW}')
print(f'asf.POLARIZATION.HH_HV: {asf.POLARIZATION.HH_HV}')
print(f'asf.PLATFORM.SENTINEL1: {asf.PLATFORM.SENTINEL1}')

print('='*80)
print(f'Health check: {json.dumps(asf.health(), indent=2)}')

print('='*80)
results = asf.search(platform='S1', maxresults=2)
print(f'Basic search check: {json.dumps(results, indent=2)}')

print('='*80)
results = asf.granule_search(['ALPSRS279162400','ALPSRS279162200'])
print(f'Granule search check: {json.dumps(results, indent=2)}')

print('='*80)
results = asf.product_search(['ALAV2A279102730','ALAV2A279133150'])
print(f'Product search check: {json.dumps(results, indent=2)}')
