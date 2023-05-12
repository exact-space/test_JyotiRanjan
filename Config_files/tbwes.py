import requests,json
import pandas as pd
import app_config as cfg
config = cfg.getconfig()

# body={
	# "input": {
		# "BOILERS":[["Boiler Details","SCSSSKL_60",50,"AFBC","","AVG"],["Boiler Details","SCSSSKL_60",50,"AFBC","","MAX"],["Boiler Details","SCSSSKL_60",50,"AFBC","","MIN"]],
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
				# "description": "Efficiency Avg",
				# "unit": "Deg.c",
				# "tagList": ["PHK_Boiler_Efficiency_prc"]
			# },
			# {
				# "description": "Steam to fuel ratioAvg",
				# "unit": "%",
				# "tagList": ["PHK_1_coalFlow_PHK_FCS0101!11-FI-607.PV_ratio"]
			# },
			# {
				# "description": "Fuel consumed Avg",
				# "unit": "TPH",
				# "tagList": ["PHK_1_coalFlow"]
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
				# "tagList": []
			# },
			# {
				# "description": "Total fuel cosumed /Day",
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
    # "output":{}
# }


# NAINI TISSUES

body = {
	"input": {
		"BOILERS":[["Boiler Details","Naini Tissues",60,"AFBC","","AVG"],["Boiler Details","Naini Tissues",60,"AFBC","","MAX"],["Boiler Details","Naini Tissues",60,"AFBC","","MIN"]],
		"KEY OPERATION PARAMETERS": [{
				"description": "Steam Generated Avg",
				"unit": "TPH",
				"tagList": ["NNI_FCS0101!11-FI-607.PV"]
			},
			{
				"description": "Main Steam Pressure Avg",
				"unit": "kg/cm2",
				"tagList": ["NNI_FCS0101!11-PI-605.PV"]
			},
            {
				"description": "Main Steam temperature Avg",
				"unit": "Deg.c",
				"tagList": ["NNI_FCS0101!11-TI-605.PV"]
			},
            {
				"description": "Feed water temperature Avg",
				"unit": "Deg.c",
				"tagList": ["NNI_FCS0101!11-TI-501.PV"]
			},
            {
				"description": "FD air flow Avg",
				"unit": "Kg/Hr",
				"tagList": ["NNI_FCS0101!11-FI-201.PV"]
			},
            {
				"description": "O2 Avg",
				"unit": "%",
				"tagList": ["NNI_FCS0101!11-AI-101.PV"]
			},
            {
				"description": "ESP inlet temperature Avg",
				"unit": "Deg.c",
				"tagList": ["NNI_FCS0101!11-TI-108.PV"]
			},
            {
				"description": "Efficiency Avg",
				"unit": "Deg.c",
				"tagList": ["NNI_Boiler_Efficiency_prc"]
			},
            {
				"description": "Steam to fuel ratioAvg",
				"unit": "%",
				"tagList": ["NNI_FCS0101!11-M-407B-AI.PV_NNI_FCS0101!11-M-407A-XI.PV_sum_3.955696_pluni_NNI_FCS0101!11-M-405A-XI.PV_NNI_FCS0101!11-M-405D-XI.PV_NNI_FCS0101!11-M-405C-XI.PV_NNI_FCS0101!11-M-405B-XI.PV_sum_2.85_pluni_sum_0.001_pluni_NNI_FCS0101!11-FI-607.PV_ratio_filter"]
			},
            {
				"description": "Fuel consumed Avg",
				"unit": "TPH",
				"tagList": ["NNI_1_coalFlow"]
			},
            {
				"description": "Aux power consumption Avg",
				"unit": "Kw/hr",
				"tagList": ["NNI_FCS0101!11-M-200-XI.PV_0.5326_pluni_0_pluni_NNI_FCS0101!11-M-200-XI.PV_0.5326_pluni_ratio_1_plunicstm_NNI_FCS0101!11-M-002-XI.PV_2.89_plunicstm_NNI_FCS0101!11-M-001-XI.PV_2.89_plunicstm_NNI_FCS0101!11-M-100-XI.PV_3e-7_plunicstm_NNI_FCS0101!11-M-100-XI.PV_1e-7_plunicstm_avg_1_plunicstm_sum"]
			},
            {
				"description": "Cost/ton of steam generation",
				"unit": "Rs/Ton",
				"tagList": ["NNI_1_costPerUnitSteam"]
			},
            {
				"description": "Total steam generated/Day",
				"unit": "TPD",
				"tagList": []
			},
            {
				"description": "Total fuel cosumed /Day",
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
				"tagList": ["NNI_FCS0101!11-FI-607.PV_PLF_prc_RHRS_AVL_hrly"]
			}            
		]
	},
	"type": "tbwesDlyRpt",
	"unitsId": "61c4a9a9515e2f6d59bff021",
    "equipment":{},
    "equipmentId":{},
    "output":{}
}

# url=config['api']['meta']+'/units/62e9106d75c9b4657aebc8fb/boilerStressProfiles'
url=config['api']['meta']+'/units/61c4a9a9515e2f6d59bff021/boilerStressProfiles'
body_req = requests.post(url, json=body)
print(body_req.status_code)
print(body_req.content)

