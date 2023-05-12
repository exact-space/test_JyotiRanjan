import requests,json
import pandas as pd
import app_config as cfg
config = cfg.getconfig()

#GHCL-LB-74
# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_74FT21_03_DACA_PV"]
			# },
			# {
				# "description": "ID Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_74ID1_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "FD Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "PA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_74PA1_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "SA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "ID Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_74ID2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "FD Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_74FD2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "PA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_74PA2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "SA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# }            
		# ]
	# },
	# "type": "AuxpconsRpt",
	# "unitsId": "61caeda654bf6a5bf94bf59a",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }


# url=config['api']['meta']+'/units/61caeda654bf6a5bf94bf59a/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

#GHCL-LB_75
# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["GHCL_75FT11_03_DACA_PV"]
			# },
			# {
				# "description": "ID Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_75ID1_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "FD Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_75FD1_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "PA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_75PA1_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "SA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "ID Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_75ID2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "FD Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_75FD2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "PA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_75PA2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "SA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# }            
		# ]
	# },
	# "type": "AuxpconsRpt",
	# "unitsId": "61caee0154bf6a5bf94bf59f",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }


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
				# "description": "ID Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_76ID1_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "FD Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_76FD1_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "PA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_76PA1_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "SA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "ID Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_76ID2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "FD Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_76FD2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "PA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": ["GHCL_76PA2_AMP_DACA_PV_apc"]
			# },
            # {
				# "description": "SA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# }            
		# ]
	# },
	# "type": "AuxpconsRpt",
	# "unitsId": "61cae1d254bf6a5bf94bf3d3",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

# url=config['api']['meta']+'/units/61cae1d254bf6a5bf94bf3d3/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

#Naini-Tissues
# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["NNI_FCS0101!11-FI-607.PV"]
			# },
			# {
				# "description": "ID Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["NNI_FCS0101!11-M-100-XI.PV_3e-7_plunicstm_NNI_FCS0101!11-M-100-XI.PV_1e-7_plunicstm_avg_1_plunicstm"]
			# },
            # {
				# "description": "FD Fan 1 power",
				# "unit": "kwHr",
				# "tagList": ["NNI_FCS0101!11-M-200-XI.PV_0.5326_pluni_0_pluni_NNI_FCS0101!11-M-200-XI.PV_0.5326_pluni_ratio_1_plunicstm"]
			# },
            # {
				# "description": "PA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "SA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "ID Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "FD Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "PA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "SA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# }            
		# ]
	# },
	# "type": "AuxpconsRpt",
	# "unitsId": "61c4a9a9515e2f6d59bff021",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }


# url=config['api']['meta']+'/units/61c4a9a9515e2f6d59bff021/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

#Sahu_Kagal-70
# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["Applications.App_Compensated_Steam_Flow"]
			# },
			# {
				# "description": "ID Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "FD Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "PA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "SA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "ID Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "FD Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "PA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "SA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# }            
		# ]
	# },
	# "type": "AuxpconsRpt",
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


#Sahu_Kagal-60
# body = {
	# "input": {
		# "table": [{
				# "description": "Steam Generated Avg",
				# "unit": "TPH",
				# "tagList": ["Applications.Application_1.FT_101_COMP.Value_Applications.Application_1.FT_101A_COMP.Value_avg"]
			# },
			# {
				# "description": "ID Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "FD Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "PA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "SA Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 1 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "ID Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "FD Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "PA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "SA Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# },
            # {
				# "description": "BFP Fan 2 power",
				# "unit": "kwHr",
				# "tagList": []
			# }            
		# ]
	# },
	# "type": "AuxpconsRpt",
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

##Nestle Vietnam-TBWES
# body = {
	# "input": {
		# "table": [{
				# "description": "FD Fan power",
				# "unit": "kwHr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.FDFanPower"]
			# },
            # {
				# "description": "ID Fan power",
				# "unit": "kwHr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.IDFanPower"]
			# },
            # {
				# "description": "FGR Fan power",
				# "unit": "kwHr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.FGRFanPower"]
			# },
            # {
				# "description": "BFP 1 power",
				# "unit": "kwHr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.FeedPump1Power"]
			# },
            # {
				# "description": "BFP 2 power",
				# "unit": "kwHr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.FeedPump2Power"]
			# },
            # {
				# "description": "BFP 3 power",
				# "unit": "kwHr",
				# "tagList": ["ICD_AOA.Vietnam.TriAn.UTI01.BH01.BMB01.THX01.FeedPump3Power"]
			# }        
		# ]
	# },
	# "type": "AuxpconsRpt",
	# "unitsId": "630c916f8c19444ca8aed6fb",
    # "equipment":{},
    # "equipmentId":{},
    # "output":{}
# }

# url=config['api']['meta']+'/units/630c916f8c19444ca8aed6fb/boilerStressProfiles'
# body_req = requests.post(url, json=body)
# print(body_req.status_code)
# print(body_req.content)

#Nestle-Abidjan
body = {
	"input": {
		"table": [{
				"description": "FD Fan power",
				"unit": "kwHr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.FDFanPower"]
			},
            {
				"description": "ID Fan power",
				"unit": "kwHr",
				"tagList": []
			},
            {
				"description": "FGR Fan power",
				"unit": "kwHr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.FGRFanPower"]
			},
            {
				"description": "BFP 1 power",
				"unit": "kwHr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.FeedPump1Current"]
			},
            {
				"description": "BFP 2 power",
				"unit": "kwHr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.FeedPump2Power"]
			},
            {
				"description": "BFP 3 power",
				"unit": "kwHr",
				"tagList": ["GLX_AOA.CI.Abidjan.UTI01.BH01.BMB01.THX01.FeedPump3Power"]
			}        
		]
	},
	"type": "AuxpconsRpt",
	"unitsId": "638dc62f6049ba000768c7d2",
    "equipment":{},
    "equipmentId":{},
    "output":{}
}


url=config['api']['meta']+'/units/638dc62f6049ba000768c7d2/boilerStressProfiles'
body_req = requests.post(url, json=body)
print(body_req.status_code)
print(body_req.content)