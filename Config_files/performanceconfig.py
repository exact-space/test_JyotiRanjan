import requests,json
import pandas as pd
import app_config as cfg
config = cfg.getconfig()


# NAINI TISSUES


# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["NNI_FCS0101!11-FI-607.PV"]
			# },
			# {
				# "description": "Boiler Indirect efficiency",
				# "unit": "%",
				# "tagList": ["NNI_Boiler_Efficiency_prc"]
			# },
            # {
				# "description": "Steam to fuel ratio",
				# "unit": "%",
				# "tagList": ["NNI_FCS0101!11-M-407B-AI.PV_NNI_FCS0101!11-M-407A-XI.PV_sum_3.955696_pluni_NNI_FCS0101!11-M-405A-XI.PV_NNI_FCS0101!11-M-405D-XI.PV_NNI_FCS0101!11-M-405C-XI.PV_NNI_FCS0101!11-M-405B-XI.PV_sum_2.85_pluni_sum_0.001_pluni_NNI_FCS0101!11-FI-607.PV_ratio_filter"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["NNI_FCS0101!11-TI-502.PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "TPH",
				# "tagList": ["NNI_FCS0101!11-FI-201.PV"]
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["NNI_FCS0101!11-AI-101.PV"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["NNI_FCS0101!11-AI-101.PV"]
			# },
            # {
				# "description": "Fly ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["NNI_LossFlyAshUBC"]
			# },
            # {
				# "description": "Bed ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["NNI_LossBedAshUBC"]
			# },
            # {
				# "description": "Sensible heat in fly ash loss",
				# "unit": "%",
				# "tagList": ["NNI_LossSensibleFlyAsh"]
			# },
            # {
				# "description": "Sensible heat in bed ash loss",
				# "unit": "%",
				# "tagList": ["NNI_LossSensibleBedAsh"]
			# },
            # {
				# "description": "Hydrogen in fuel loss",
				# "unit": "%",
				# "tagList": ["NNI_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in fuel loss",
				# "unit": "%",
				# "tagList": ["NNI_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in air loss",
				# "unit": "%",
				# "tagList": ["NNI_LossDueToH2OInAir"]
			# },
            # {
				# "description": "Radiation loss",
				# "unit": "%",
				# "tagList": ["NNI_LossDueToRadiation"]
			# },
            # {
				# "description": "Unaccounted loss",
				# "unit": "%",
				# "tagList": ["NNI_LossUnaccounted"]
			# },
            # {
				# "description": "Total losses",
				# "unit": "%",
				# "tagList": ["NNI_LossTotal"]
			# },
            # {
				# "description": "Total fuel consumed for the period",
				# "unit": "Tonnes",
				# "tagList": ["NNI_1_coalFlow"]
			# },
            # {
				# "description": "Cost /Ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["NNI_1_costPerUnitSteam"]
			# }            
		# ]
	# },
	# "type": "prfmancsumRpt",
	# "unitsId": "61c4a9a9515e2f6d59bff021",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

# url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
# url=config['api']['meta']+'/units/61c4a9a9515e2f6d59bff021/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)






#GHCL-LB-74

# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_74FT21_03_DACA_PV"]
			# },
			# {
				# "description": "Boiler Indirect efficiency",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratio",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_coalFlow_GHCL_74FT21_03_DACA_PV_ratio"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_74TE101_DACA_PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_74FT22_03_DACA_PV"]
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["GHCL_74O2_DACA_PV"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_74TE23_14_DACA_PV"]
			# },
            # {
				# "description": "Fly ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossFlyAshUBC"]
			# },
            # {
				# "description": "Bed ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossBedAshUBC"]
			# },
            # {
				# "description": "Sensible heat in fly ash loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossSensibleFlyAsh"]
			# },
            # {
				# "description": "Sensible heat in bed ash loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossSensibleBedAsh"]
			# },
            # {
				# "description": "Hydrogen in fuel loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossDueToH2InFuel"]
			# },
            # {
				# "description": "Moisture in fuel loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in air loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossDueToH2OInAir"]
			# },
            # {
				# "description": "Radiation loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossDueToRadiation"]
			# },
            # {
				# "description": "Unaccounted loss",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossUnaccounted"]
			# },
            # {
				# "description": "Total losses",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_LossTotal"]
			# },
            # {
				# "description": "Total fuel consumed for the period",
				# "unit": "Tonnes",
				# "tagList": ["LB-74_f59a_1_coalFlow"]
			# },
            # {
				# "description": "Cost /Ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["LB-74_f59a_1_costPerUnitSteam"]
			# }            
		# ]
	# },
	# "type": "prfmancsumRpt",
	# "unitsId": "61caeda654bf6a5bf94bf59a",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

#url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
# url=config['api']['meta']+'/units/61caeda654bf6a5bf94bf59a/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

#GHCL-LB-75

# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_75FT11_03_DACA_PV"]
			# },
			# {
				# "description": "Boiler Indirect efficiency",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratio",
				# "unit": "%",
				# "tagList": []
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_75TE101_DACA_PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_75FT12_03_DACA_PV"]
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["GHCL_75O2_DACA_PV"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_75TE16_18I_DACA_PV"]
			# },
            # {
				# "description": "Fly ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossFlyAshUBC"]
			# },
            # {
				# "description": "Bed ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossBedAshUBC"]
			# },
            # {
				# "description": "Sensible heat in fly ash loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossSensibleFlyAsh"]
			# },
            # {
				# "description": "Sensible heat in bed ash loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossSensibleBedAsh"]
			# },
            # {
				# "description": "Hydrogen in fuel loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossDueToH2InFuel"]
			# },
            # {
				# "description": "Moisture in fuel loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in air loss",
				# "unit": "%",
				# "tagList": ["75_f59f_1_LossDueToH2OInAir"]
			# },
            # {
				# "description": "Radiation loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossDueToRadiation"]
			# },
            # {
				# "description": "Unaccounted loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossUnaccounted"]
			# },
            # {
				# "description": "Total losses",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossTotal"]
			# },
            # {
				# "description": "Total fuel consumed for the period",
				# "unit": "Tonnes",
				# "tagList": ["LB-75_f59f_1_coalFlow"]
			# },
            # {
				# "description": "Cost /Ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["LB-75_f59f_1_costPerUnitSteam"]
			# }            
		# ]
	# },
	# "type": "prfmancsumRpt",
	# "unitsId": "61caee0154bf6a5bf94bf59f",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

#url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
# url=config['api']['meta']+'/units/61caee0154bf6a5bf94bf59f/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

#GHCL-LB-76

# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_76FT31_03_DACA_PV"]
			# },
			# {
				# "description": "Boiler Indirect efficiency",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratio",
				# "unit": "%",
				# "tagList": []
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_76TI35_DACA_PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_76FT32_03_DACA_PV"]
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["GHCL_76O2_DACA_PV"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_76TI33_14_DACA_PV"]
			# },
            # {
				# "description": "Fly ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossFlyAshUBC"]
			# },
            # {
				# "description": "Bed ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossBedAshUBC"]
			# },
            # {
				# "description": "Sensible heat in fly ash loss",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossSensibleFlyAsh"]
			# },
            # {
				# "description": "Sensible heat in bed ash loss",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossSensibleBedAsh"]
			# },
            # {
				# "description": "Hydrogen in fuel loss",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossDueToH2InFuel"]
			# },
            # {
				# "description": "Moisture in fuel loss",
				# "unit": "%",
				# "tagList": ["LB-75_f59f_1_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in air loss",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Radiation loss",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossDueToRadiation"]
			# },
            # {
				# "description": "Unaccounted loss",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossUnaccounted"]
			# },
            # {
				# "description": "Total losses",
				# "unit": "%",
				# "tagList": ["LB-76_f3d3_1_LossTotal"]
			# },
            # {
				# "description": "Total fuel consumed for the period",
				# "unit": "Tonnes",
				# "tagList": ["LB-76_f3d3_1_coalFlow"]
			# },
            # {
				# "description": "Cost /Ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["LB-76_f3d3_1_costPerUnitSteam"]
			# }            
		# ]
	# },
	# "type": "prfmancsumRpt",
	# "unitsId": "61cae1d254bf6a5bf94bf3d3",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

#url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
# url=config['api']['meta']+'/units/61cae1d254bf6a5bf94bf3d3/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)


#Shahu_kagal-60
# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["Applications.Application_1.FT_101_COMP.Value_Applications.Application_1.FT_101A_COMP.Value_avg"]
			# },
			# {
				# "description": "Boiler Indirect efficiency",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratio",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_coalFlow_Applications.Application_1.FT_101_COMP.Value_Applications.Application_1.FT_101A_COMP.Value_avg_ratio"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["Applications.Application_1.TE_TT_109.IOValue"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "TPH",
				# "tagList": ["Applications.Application_1.FT_104A.IOValue"]
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["Applications.Application_1.AE_AT_101.IOValue"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["Applications.Application_1.TE_TT_121.IOValue"]
			# },
            # {
				# "description": "Fly ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossFlyAshUBC"]
			# },
            # {
				# "description": "Bed ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossBedAshUBC"]
			# },
            # {
				# "description": "Sensible heat in fly ash loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossSensibleFlyAsh"]
			# },
            # {
				# "description": "Sensible heat in bed ash loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossSensibleBedAsh"]
			# },
            # {
				# "description": "Hydrogen in fuel loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossDueToH2InFuel"]
			# },
            # {
				# "description": "Moisture in fuel loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in air loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossDueToH2OInAir"]
			# },
            # {
				# "description": "Radiation loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossDueToRadiation"]
			# },
            # {
				# "description": "Unaccounted loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1__LossUnaccounted"]
			# },
            # {
				# "description": "Total losses",
				# "unit": "%",
				# "tagList": ["SCSSSKL_60_c8fb_1_LossTotal"]
			# },
            # {
				# "description": "Total fuel consumed for the period",
				# "unit": "Tonnes",
				# "tagList": ["SCSSSKL_60_c8fb_1_coalFlow"]
			# },
            # {
				# "description": "Cost /Ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["SCSSSKL_60_c8fb_1_costPerUnitSteam"]
			# }            
		# ]
	# },
	# "type": "prfmancsumRpt",
	# "unitsId": "62e9106d75c9b4657aebc8fb",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

#url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
# url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

#shahu_kagal-70
# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["Applications.App_Compensated_Steam_Flow"]
			# },
			# {
				# "description": "Boiler Indirect efficiency",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratio",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_coalFlow_Applications.App_Compensated_Steam_Flow_ratio"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["Applications.App_Feed_water_tank_temperatureTI001"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "TPH",
				# "tagList": ["Applications.App_FD_air_flow_transmitterFT13_Applications.App_FD_air_flow_transmitterFT_14_Applications.App_FD_air_flow_transmitter_FT_06_avg"]
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["Applications.App_Oxygen_analyser_AE_02"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["Applications.App_Flue_gas_at_ESP_inlet_temperature_TE_23"]
			# },
            # {
				# "description": "Fly ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossFlyAshUBC"]
			# },
            # {
				# "description": "Bed ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossBedAshUBC"]
			# },
            # {
				# "description": "Sensible heat in fly ash loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossSensibleFlyAsh"]
			# },
            # {
				# "description": "Sensible heat in bed ash loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossSensibleBedAsh"]
			# },
            # {
				# "description": "Hydrogen in fuel loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossDueToH2InFuel"]
			# },
            # {
				# "description": "Moisture in fuel loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in air loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossDueToH2OInAir"]
			# },
            # {
				# "description": "Radiation loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossDueToRadiation"]
			# },
            # {
				# "description": "Unaccounted loss",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1__LossUnaccounted"]
			# },
            # {
				# "description": "Total losses",
				# "unit": "%",
				# "tagList": ["SCSSSKL_70_c3e4b_1_LossTotal"]
			# },
            # {
				# "description": "Total fuel consumed for the period",
				# "unit": "Tonnes",
				# "tagList": ["SCSSSKL_70_c3e4b_1_coalFlow"]
			# },
            # {
				# "description": "Cost /Ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["SCSSSKL_70_c3e4b_1_costPerUnitSteam"]
			# }            
		# ]
	# },
	# "type": "prfmancsumRpt",
	# "unitsId": "6304549251476a14db49c3e4",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

#url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
# url=config['api']['meta']+'/units/6304549251476a14db49c3e4/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)


##Nestle-Vietnam

# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.SteamFlow"]
			# },
			# {
				# "description": "Boiler Indirect efficiency",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratio",
				# "unit": "%",
				# "tagList": []
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.FeedWaterTemperatureAtEconomizerInlet"]
			# },
            # {
				# "description": "FD air flow to bed",
				# "unit": "Kg/hr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.BedAirFlow"]
			# },
            # {
				# "description": "FD air flow to OFA",
				# "unit": "Kg/hr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.AirFlowToOFANozzels"]
			# },
            # {
				# "description": "FD air flow to burner",
				# "unit": "Kg/hr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.AirFlowToBurner"]
			# },
            # {
				# "description": "FGR Air flow",
				# "unit": "Kg/hr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.FlueGasRecirculationAirFlow"]
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.OxygenAtEconomizerOutlet"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.FlueGasTemperatureIntoESP"]
			# },
            # {
				# "description": "Fly ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossFlyAshUBC"]
			# },
            # {
				# "description": "Bed ash unburnt carbon loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossBedAshUBC"]
			# },
            # {
				# "description": "Sensible heat in fly ash loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossSensibleFlyAsh"]
			# },
            # {
				# "description": "Sensible heat in bed ash loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossSensibleBedAsh"]
			# },
            # {
				# "description": "Dry flue gas loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossDueToDryFlueGas"]
			# },
            # {
				# "description": "Hydrogen in fuel loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in fuel loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossDueToH2OInFuel"]
			# },
            # {
				# "description": "Moisture in air loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossDueToH2OInAir"]
			# },
            # {
				# "description": "Radiation loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossDueToRadiation"]
			# },
            # {
				# "description": "Unaccounted loss",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossUnaccounted"]
			# },
            # {
				# "description": "Total losses",
				# "unit": "%",
				# "tagList": ["Nestle_Vietnam_d6fb_1_LossTotal"]
			# },
            # {
				# "description": "Total fuel consumed for the period",
				# "unit": "Tonnes",
				# "tagList": ["Nestle_Vietnam_d6fb_1_coalFlow"]
			# },
            # {
				# "description": "Cost /Ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["Nestle_Vietnam_d6fb_1_costPerUnitSteam"]
			# }            
		# ]
	# },
	# "type": "prfmancsumRpt",
	# "unitsId": "630c916f8c19444ca8aed6fb",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }


# url=config['api']['meta']+'/units/630c916f8c19444ca8aed6fb/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

##Nestle-Abidjan
body = {
	"input": {
		"table": [{
				"description": "Steam Generated Avg",
				"unit": "TPH",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.SteamFlow"]
			},
			{
				"description": "Boiler Indirect efficiency",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_Boiler_Efficiency"]
			},
            {
				"description": "Steam to fuel ratio",
				"unit": "%",
				"tagList": []
			},
            {
				"description": "Feed water temperature Avg",
				"unit": "Deg.c",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.FeedWaterTemperatureAfterEconomizer"]
			},
            {
				"description": "FD air flow to bed",
				"unit": "Kg/hr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.BedAirFlow"]
			},
            {
				"description": "FD air flow to OFA",
				"unit": "Kg/hr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.AirFlowToOFANozzels"]
			},
            {
				"description": "FD air flow to burner",
				"unit": "Kg/hr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.AirFlowToBurner"]
			},
            {
				"description": "FGR Air flow",
				"unit": "Kg/hr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.FlueGasRecirculationAirFlow"]
			},
            {
				"description": "O2 Avg",
				"unit": "%",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.OxygenInExhaust"]
			},
            {
				"description": "ESP inlet temperature Avg",
				"unit": "Deg.c",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.FlueGasTemperatureIntoESP"]
			},
            {
				"description": "Fly ash unburnt carbon loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossFlyAshUBC"]
			},
            {
				"description": "Bed ash unburnt carbon loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossBedAshUBC"]
			},
            {
				"description": "Sensible heat in fly ash loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossSensibleFlyAsh"]
			},
            {
				"description": "Sensible heat in bed ash loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossSensibleBedAsh"]
			},
            {
				"description": "Dry flue gas loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossDueToDryFlueGas"]
			},
            {
				"description": "Hydrogen in fuel loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossDueToH2InFuel"]
			},
            {
				"description": "Moisture in fuel loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossDueToH2OInFuel"]
			},
            {
				"description": "Moisture in air loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossDueToH2OInAir"]
			},
            {
				"description": "Radiation loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossDueToRadiation"]
			},
            {
				"description": "Unaccounted loss",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossUnaccounted"]
			},
            {
				"description": "Total losses",
				"unit": "%",
				"tagList": ["Abidjan_c7d2_1_LossTotal"]
			},
            {
				"description": "Total fuel consumed for the period",
				"unit": "Tonnes",
				"tagList": ["Abidjan_c7d2_1_coalFlow"]
			},
            {
				"description": "Cost /Ton of steam generation",
				"unit": "Rs/Ton",
				"tagList": ["Abidjan_c7d2_1_costPerUnitSteam"]
			}            
		]
	},
	"type": "prfmancsumRpt",
	"unitsId": "638dc62f6049ba000768c7d2",
    "equipment":{},
    "equipmentId":{},
    "output":{}
}


url=config['api']['meta']+'/units/638dc62f6049ba000768c7d2/boilerStressProfiles'
body_req = requests.post(url, json=body)
print(body_req.status_code)
print(body_req.content)