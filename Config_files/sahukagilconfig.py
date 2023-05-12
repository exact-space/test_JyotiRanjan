import requests,json
import pandas as pd
import app_config as cfg
config = cfg.getconfig()

#sahu kagal-60
# body= {
	# "input": {
		# "BOILERS":[["Boiler Details","SCSSSKL_60",60,"TG","","AVG"],["Boiler Details","SCSSSKL_60",60,"TG","","MAX"],["Boiler Details","SCSSSKL_60",60,"TG","","MIN"]],
		# "KEY OPERATION PARAMETERS": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["PHK_FT_101"]
			# },
			# {
				# "description": "Main Steam Pressure Avg",
				# "unit": "kg/cm2",
				# "tagList": ["PHK_AO_PT_101"]
			# },
			# {
				# "description": "Main Steam temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["PHK_AO_TT_105"]
			# },
			# {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["PHK_TE_TT_109"]
			# },
			# {
				# "description": "FD air flow Avg",
				# "unit": "Kg/Hr",
				# "tagList": ["PHK_FT_104A"]
			# },
            # {
				# "description": "SA air flow Avg",
				# "unit": "Kg/Hr",
				# "tagList": ["PHK_FT_105"]
			# },
			# {
				# "description": "O2 Avg",
				# "unit": "%",
				# "tagList": ["PHK_AE_AT_101"]
			# },
			# {
				# "description": "ESP inlet temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["PHK_TE_TT_119"]
			# },
            # {
				# "description": "Furnace pressure",
				# "unit": "mmWC",
				# "tagList": ["PHK_PT_112"]
			# },
			# {
				# "description": "Efficiency Avg",
				# "unit": "Deg.c",
				# "tagList": ["PHK_c8fb_1_Boiler_Efficiency"]
			# },
			# {
				# "description": "Steam to fuel ratioAvg",
				# "unit": "%",
				# "tagList": []
			# },
			# {
				# "description": "Fuel consumed Avg",
				# "unit": "TPH",
				# "tagList": ["PHK_c8fb_1_coalFlow"]
			# },
			# {
				# "description": "Aux power consumption Avg",
				# "unit": "Kw/hr",
				# "tagList": []
			# },
			# {
				# "description": "Cost/ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["PHK_c8fb_1_costPerUnitSteam"]
			# },
			# {
				# "description": "Total steam generated/Day",
				# "unit": "TPD",
				# "tagList": ["Applications.Application_1.FT_101.IOValue"]
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
				# "tagList": []
			# }
		# ]
	# },
	# "type": "tbwesDlyRpt",
	# "unitsId": "62e9106d75c9b4657aebc8fb",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{},
# }

# url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

#sahu kagal-70

body= {
	"input": {
		"BOILERS":[["Boiler Details","SCSSSKL_70",70,"TG","","AVG"],["Boiler Details","SCSSSKL_70",70,"TG","","MAX"],["Boiler Details","SCSSSKL_70",70,"TG","","MIN"]],
		"KEY OPERATION PARAMETERS": [{
				"description": "Steam Generated Avg",
				"unit": "TPH",
				"tagList": []
			},
			{
				"description": "Main Steam Pressure Avg",
				"unit": "kg/cm2",
				"tagList": []
			},
			{
				"description": "Main Steam temperature Avg",
				"unit": "Deg.c",
				"tagList": []
			},
			{
				"description": "Feed water temperature Avg",
				"unit": "Deg.c",
				"tagList": []
			},
			{
				"description": "FD air flow Avg",
				"unit": "Kg/Hr",
				"tagList": []
			},
            {
				"description": "SA air flow Avg",
				"unit": "Kg/Hr",
				"tagList": []
			},
			{
				"description": "O2 Avg",
				"unit": "%",
				"tagList": []
			},
			{
				"description": "ESP inlet temperature Avg",
				"unit": "Deg.c",
				"tagList": []
			},
            {
				"description": "Furnace pressure",
				"unit": "mmWC",
				"tagList": []
			},
			{
				"description": "Efficiency Avg",
				"unit": "Deg.c",
				"tagList": []
			},
			{
				"description": "Steam to fuel ratioAvg",
				"unit": "%",
				"tagList": []
			},
			{
				"description": "Fuel consumed Avg",
				"unit": "TPH",
				"tagList": []
			},
			{
				"description": "Aux power consumption Avg",
				"unit": "Kw/hr",
				"tagList": []
			},
			{
				"description": "Cost/ton of steam generation",
				"unit": "Rs/Ton",
				"tagList": []
			},
			{
				"description": "Total steam generated/Day",
				"unit": "TPD",
				"tagList": []
			},
			{
				"description": "Total fuel consumed /Day",
				"unit": "TPD",
				"tagList": []
			},
			{
				"description": "Total Aux power consumption day avg",
				"unit": "Kw/day",
				"tagList": []
			},
			{
				"description": "Availability",
				"unit": "%",
				"tagList": []
			}
		]
	},
	"type": "tbwesDlyRpt",
	"unitsId": "6304549251476a14db49c3e4",
    "equipment":{},
    "equipmentId":{},
    "output":{},
}

url=config['api']['meta']+'/units/6304549251476a14db49c3e4/boilerStressProfiles'
body_req = requests.post(url, json=body)
print(body_req.status_code)
print(body_req.content)




# body = {
	# "input": {
		# "BOILERS":[["Boiler Details","LB-74",90,"AFBC","","AVG"],["Boiler Details","LB-74",90,"AFBC","","MAX"],["Boiler Details","LB-74",90,"AFBC","","MIN"]],
		# "KEY OPERATION PARAMETERS": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_74FT21_03_DACA_PV"]
			# },
			# {
				# "description": "Main Steam Pressure Avg",
				# "unit": "kg/cm2",
				# "tagList": ["GHCL_74PT22_09_DACA_PV"]
			# },
            # {
				# "description": "Main Steam temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_74TI26_18L_DACA_PV"]
			# },
            # {
				# "description": "Feed water temperature Avg",
				# "unit": "Deg.c",
				# "tagList": ["GHCL_74TE101_DACA_PV"]
			# },
            # {
				# "description": "FD air flow Avg",
				# "unit": "Kg/Hr",
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
				# "description": "Efficiency Avg",
				# "unit": "Deg.c",
				# "tagList": ["LB-74_f59a_1_Boiler_Efficiency"]
			# },
            # {
				# "description": "Steam to fuel ratioAvg",
				# "unit": "%",
				# "tagList": ["LB-74_f59a_1_coalFlow_GHCL_74FT21_03_DACA_PV_ratio"]
			# },
            # {
				# "description": "Fuel consumed Avg",
				# "unit": "TPH",
				# "tagList": ["LB-74_f59a_1_coalFlow"]
			# },
            # {
				# "description": "Aux power consumption Avg",
				# "unit": "Kw/hr",
				# "tagList": ["GHCL_74_apc_sum"]
			# },
            # {
				# "description": "Cost/ton of steam generation",
				# "unit": "Rs/Ton",
				# "tagList": ["LB-74_f59a_1_costPerUnitSteam"]
			# },
            # {
				# "description": "Total steam generated/Day",
				# "unit": "TPD",
				# "tagList": ["GHCL_74FT21_03_DACA_PV"]
			# },
            # {
				# "description": "Total fuel consumed /Day",
				# "unit": "TPD",
				# "tagList": ["LB-74_f59a_1_coalFlow"]
			# },
            # {
				# "description": "Total Aux power consumption day avg",
				# "unit": "Kw/day",
				# "tagList": ["GHCL_74_apc_sum"]
			# },
            # {
				# "description": "Availability",
				# "unit": "%",
				# "tagList": ["GHCL_74FT21_03_DACA_PV_PLF_prc_RHRS_AVL"]
			# }            
		# ]
	# },
	# "type": "tbwesDlyRpt",
	# "unitsId": "61caeda654bf6a5bf94bf59a",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{},
# }


# url=config['api']['meta']+'/units/61caeda654bf6a5bf94bf59a/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)





