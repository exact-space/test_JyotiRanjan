import requests,json
import pandas as pd
import app_config as cfg
config = cfg.getconfig()
body = {
	"input": {
		"BOILERS":[["Boiler Details","LB-74",90,"AFBC","","AVG"],["Boiler Details","LB-74",90,"AFBC","","MAX"],["Boiler Details","LB-74",90,"AFBC","","MIN"]],
		"KEY OPERATION PARAMETERS": [{
				"description": "Steam Generated Avg",
				"unit": "TPH",
				"tagList": ["GHCL_74FT21_03_DACA_PV"]
			},
			{
				"description": "Main Steam Pressure Avg",
				"unit": "kg/cm2",
				"tagList": ["GHCL_74PT22_09_DACA_PV"]
			},
            {
				"description": "Main Steam temperature Avg",
				"unit": "Deg.c",
				"tagList": ["GHCL_74TI26_18L_DACA_PV"]
			},
            {
				"description": "Feed water temperature Avg",
				"unit": "Deg.c",
				"tagList": ["GHCL_74TE101_DACA_PV"]
			},
            {
				"description": "FD air flow Avg",
				"unit": "Kg/Hr",
				"tagList": ["GHCL_74FT22_03_DACA_PV"]
			},
            {
				"description": "O2 Avg",
				"unit": "%",
				"tagList": ["GHCL_74O2_DACA_PV"]
			},
            {
				"description": "ESP inlet temperature Avg",
				"unit": "Deg.c",
				"tagList": ["GHCL_74TE23_14_DACA_PV"]
			},
            {
				"description": "Efficiency Avg",
				"unit": "Deg.c",
				"tagList": ["LB-74_f59a_1_Boiler_Efficiency"]
			},
            {
				"description": "Steam to fuel ratioAvg",
				"unit": "%",
				"tagList": ["LB-74_f59a_1_coalFlow_GHCL_74FT21_03_DACA_PV_ratio"]
			},
            {
				"description": "Fuel consumed Avg",
				"unit": "TPH",
				"tagList": ["LB-74_f59a_1_coalFlow"]
			},
            {
				"description": "Aux power consumption Avg",
				"unit": "Kw/hr",
				"tagList": ["GHCL_74_apc_sum"]
			},
            {
				"description": "Cost/ton of steam generation",
				"unit": "Rs/Ton",
				"tagList": ["LB-74_f59a_1_costPerUnitSteam"]
			},
            {
				"description": "Total steam generated/Day",
				"unit": "TPD",
				"tagList": ["GHCL_74FT21_03_DACA_PV"]
			},
            {
				"description": "Total fuel consumed /Day",
				"unit": "TPD",
				"tagList": ["LB-74_f59a_1_coalFlow"]
			},
            {
				"description": "Total Aux power consumption day avg",
				"unit": "Kw/day",
				"tagList": ["GHCL_74_apc_sum"]
			},
            {
				"description": "Availability",
				"unit": "%",
				"tagList": ["GHCL_74FT21_03_DACA_PV_PLF_prc_RHRS_AVL"]
			}            
		]
	},
	"type": "tbwesDlyRpt",
	"unitsId": "61caeda654bf6a5bf94bf59a",
    "equipment":{},
    "equipmentId":{},
    "output":{},
}


url=config['api']['meta']+'/units/61caeda654bf6a5bf94bf59a/boilerStressProfiles'
body_req = requests.post(url, json=body)
print(body_req.status_code)
print(body_req.content)



# body = {
	# "input": {
		# "BOILERS":[["Boiler Details","LB-75",90,"AFBC","","AVG"],["Boiler Details","LB-75",90,"AFBC","","MAX"],["Boiler Details","LB-75",90,"AFBC","","MIN"]],
		# "KEY OPERATION PARAMETERS": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_75FT11_03_DACA_PV"]
			# },
			# {
				# "description": "Main Steam Pressure Avg",
				# "unit": "kg/cm2",
				# "tagList": ["GHCL_75PT12_09_DACA_PV"]
			# },
            # {
				# "description": "Main Steam temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_75TE17_08_DACA_PV"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_75TE101_DACA_PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "Kg/Hr",
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
				# "description": "Efficiency Avg",
				# "unit": "Deg.c",
				# "tagList": ["LB-75_f59f_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratioAvg",
				# "unit": "%",
				# "tagList": []
			# },
            # {
				# "description": "Fuel consumed Avg",
				# "unit": "TPH",
				# "tagList": ["LB-75_f59f_1_coalFlow"]
			# },
            # {
				# "description": "Aux power consumption Avg",
				# "unit": "Kw/hr",
				# "tagList": ["GHCL_75_apc_sum"]
			# },
            # {
				# "description": "Cost/ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["LB-75_f59f_1_costPerUnitSteam"]
			# },
            # {
				# "description": "Total steam generated/Day",
				# "unit": "TPD",
				# "tagList": ["GHCL_75FT11_03_DACA_PV"]
			# },
            # {
				# "description": "Total fuel consumed /Day",
				# "unit": "TPD",
				# "tagList": ["LB-75_f59f_1_coalFlow"]
			# },
            # {
				# "description": "Total Aux power consumption day avg",
				# "unit": "Kw/day",
				# "tagList": ["GHCL_75_apc_sum"]
			# },
            # {
				# "description": "Availability",
				# "unit": "%",
				# "tagList": ["GHCL_75FT11_03_DACA_PV_PLF_prc_RHRS_AVL_hrly"]
			# }            
		# ]
	# },
	# "type": "tbwesDlyRpt",
	# "unitsId": "61caee0154bf6a5bf94bf59f",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

# url=config['api']['meta']+'/units/61caee0154bf6a5bf94bf59f/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)








# body = {
	# "input": {
		# "BOILERS":[["Boiler Details","LB-76",90,"AFBC","","AVG"],["Boiler Details","LB-76",90,"AFBC","","MAX"],["Boiler Details","LB-76",90,"AFBC","","MIN"]],
		# "KEY OPERATION PARAMETERS": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_76FT31_03_DACA_PV"]
			# },
			# {
				# "description": "Main Steam Pressure Avg",
				# "unit": "kg/cm2",
				# "tagList": ["GHCL_76PT32_09_DACA_PV"]
			# },
            # {
				# "description": "Main Steam temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_76TI49_DACA_PV"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_76TI35_DACA_PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "Kg/Hr",
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
				# "description": "Efficiency Avg",
				# "unit": "Deg.c",
				# "tagList": ["LB-76_f3d3_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratioAvg",
				# "unit": "%",
				# "tagList": []
			# },
            # {
				# "description": "Fuel consumed Avg",
				# "unit": "TPH",
				# "tagList": ["LB-76_f3d3_1_coalFlow"]
			# },
            # {
				# "description": "Aux power consumption Avg",
				# "unit": "Kw/hr",
				# "tagList": ["GHCL_76_apc_sum"]
			# },
            # {
				# "description": "Cost/ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["LB-76_f3d3_1_costPerUnitSteam"]
			# },
            # {
				# "description": "Total steam generated/Day",
				# "unit": "TPD",
				# "tagList": ["GHCL_76FT31_03_DACA_PV"]
			# },
            # {
				# "description": "Total fuel consumed /Day",
				# "unit": "TPD",
				# "tagList": ["LB-76_f3d3_1_coalFlow"]
			# },
            # {
				# "description": "Total Aux power consumption day avg",
				# "unit": "Kw/day",
				# "tagList": ["GHCL_76_apc_sum"]
			# },
            # {
				# "description": "Availability",
				# "unit": "%",
				# "tagList": ["GHCL_76FT31_03_DACA_PV_PLF_prc_RHRS_AVL_hrly"]
			# }            
		# ]
	# },
	# "type": "tbwesDlyRpt",
	# "unitsId": "61cae1d254bf6a5bf94bf3d3",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

# url=config['api']['meta']+'/units/61cae1d254bf6a5bf94bf3d3/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)





# body = {
	# "input": {
		# "BOILERS":[["Boiler Details","LB-77",90,"AFBC","","AVG"],["Boiler Details","LB-77",90,"AFBC","","MAX"],["Boiler Details","LB-77",90,"AFBC","","MIN"]],
		# "KEY OPERATION PARAMETERS": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_77FT404_DACA_PV"]
			# },
			# {
				# "description": "Main Steam Pressure Avg",
				# "unit": "kg/cm2",
				# "tagList": ["GHCL_77PT412_DACA_PV"]
			# },
            # {
				# "description": "Main Steam temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_77TE474_DACA_PV"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_77TE473_DACA_PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "Kg/Hr",
				# "tagList": ["GHCL_77FT405_DACA_PV"]
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["GHCL_77_AT423"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_77TE416A_DACA_PV"]
			# },
            # {
				# "description": "Efficiency Avg",
				# "unit": "Deg.c",
				# "tagList": []
			# },
            # {
				# "description": "Steam to fuel ratioAvg",
				# "unit": "%",
				# "tagList": []
			# },
            # {
				# "description": "Fuel consumed Avg",
				# "unit": "TPH",
				# "tagList": []
			# },
            # {
				# "description": "Aux power consumption Avg",
				# "unit": "Kw/hr",
				# "tagList": []
			# },
            # {
				# "description": "Cost/ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": []
			# },
            # {
				# "description": "Total steam generated/Day",
				# "unit": "TPD",
				# "tagList": ["GHCL_77FT404_DACA_PV"]
			# },
            # {
				# "description": "Total fuel consumed /Day",
				# "unit": "TPD",
				# "tagList": []
			# },
            # {
				# "description": "Total Aux power consumption day avg",
				# "unit": "Kw/day",
				# "tagList": []
			# },
            # {
				# "description": "Availability",
				# "unit": "%",
				# "tagList": ["GHCL_77FT404_DACA_PV_PLF_prc_RHRS_AVL_hrly"]
			# }            
		# ]
	# },
	# "type": "tbwesDlyRpt",
	# "unitsId": "61cae1db54bf6a5bf94bf3d4",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

# url=config['api']['meta']+'/units/61cae1db54bf6a5bf94bf3d4/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)





# body = {
	# "input": {
		# "BOILERS":[["Boiler Details","LB-78",125,"CFBC","","AVG"],["Boiler Details","LB-78",125,"CFBC","","MAX"],["Boiler Details","LB-78",125,"CFBC","","MIN"]],
		# "KEY OPERATION PARAMETERS": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_LB78_11_FI_210A_DACA_PV"]
			# },
			# {
				# "description": "Main Steam Pressure Avg",
				# "unit": "kg/cm2",
				# "tagList": ["GHCL_LB78_11_PI_210A_DACA_PV"]
			# },
            # {
				# "description": "Main Steam temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_LB78_11_TI_210C"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_LB78_11_TI_203_DACA_PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "Kg/Hr",
				# "tagList": []
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["GHCL_11_AI_374_DACA_PV"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_11_TI_380_DACA_PV"]
			# },
            # {
				# "description": "Efficiency Avg",
				# "unit": "Deg.c",
				# "tagList": []
			# },
            # {
				# "description": "Steam to fuel ratioAvg",
				# "unit": "%",
				# "tagList": []
			# },
            # {
				# "description": "Fuel consumed Avg",
				# "unit": "TPH",
				# "tagList": []
			# },
            # {
				# "description": "Aux power consumption Avg",
				# "unit": "Kw/hr",
				# "tagList": ["GHCL_78_apc_sum"]
			# },
            # {
				# "description": "Cost/ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": []
			# },
            # {
				# "description": "Total steam generated/Day",
				# "unit": "TPD",
				# "tagList": ["GHCL_LB78_11_FI_210A_DACA_PV"]
			# },
            # {
				# "description": "Total fuel consumed /Day",
				# "unit": "TPD",
				# "tagList": []
			# },
            # {
				# "description": "Total Aux power consumption day avg",
				# "unit": "Kw/day",
				# "tagList": ["GHCL_78_apc_sum"]
			# },
            # {
				# "description": "Availability",
				# "unit": "%",
				# "tagList": ["GHCL_LB78_11_FI_210A_DACA_PV_PLF_prc_RHRS_AVL"]
			# }            
		# ]
	# },
	# "type": "tbwesDlyRpt",
	# "unitsId": "61cae1fb54bf6a5bf94bf3d5",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

# url=config['api']['meta']+'/units/61cae1fb54bf6a5bf94bf3d5/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)





# body = {
	# "input": {
		# "BOILERS":[["Boiler Details","LB-79",200,"CFBC","","AVG"],["Boiler Details","LB-79",200,"CFBC","","MAX"],["Boiler Details","LB-79",200,"CFBC","","MIN"]],
		# "KEY OPERATION PARAMETERS": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_79FT_0401A_DACA_PV"]
			# },
			# {
				# "description": "Main Steam Pressure Avg",
				# "unit": "kg/cm2",
				# "tagList": ["GHCL_79PT_0401A_DACA_PV"]
			# },
            # {
				# "description": "Main Steam temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_79TT_0405A_DACA_PV"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": []
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "Kg/Hr",
				# "tagList": []
			# },
            # {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["GHCL_79AT_0501_DACA_PV"]
			# },
            # {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_79TT_0512A_DACA_PV"]
			# },
            # {
				# "description": "Efficiency Avg",
				# "unit": "Deg.c",
				# "tagList": ["LB-74_f59a_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratioAvg",
				# "unit": "%",
				# "tagList": []
			# },
            # {
				# "description": "Fuel consumed Avg",
				# "unit": "TPH",
				# "tagList": []
			# },
            # {
				# "description": "Aux power consumption Avg",
				# "unit": "Kw/hr",
				# "tagList": []
			# },
            # {
				# "description": "Cost/ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": []
			# },
            # {
				# "description": "Total steam generated/Day",
				# "unit": "TPD",
				# "tagList": ["GHCL_79FT_0401A_DACA_PV"]
			# },
            # {
				# "description": "Total fuel consumed /Day",
				# "unit": "TPD",
				# "tagList": []
			# },
            # {
				# "description": "Total Aux power consumption day avg",
				# "unit": "Kw/day",
				# "tagList": []
			# },
            # {
				# "description": "Availability",
				# "unit": "%",
				# "tagList": ["GHCL_79FT_0401A_DACA_PV_PLF_prc_RHRS_AVL_hrly"]
			# }            
		# ]
	# },
	# "type": "tbwesDlyRpt",
	# "unitsId": "61cae20554bf6a5bf94bf3d6",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }
# url=config['api']['meta']+'/units/61cae20554bf6a5bf94bf3d6/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)