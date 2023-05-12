import requests,json
import pandas as pd
import app_config as cfg
config = cfg.getconfig()

body = {
	"input": {
		"table": [{
				"description": "Steam Generated Avg",
				"unit": "TPH",
				"tagList": {"measureProperty":"Main Steam","measureType":"Flow","measureLocation":"Outlet"}
			},
			{
				"description": "Boiler Indirect efficiency",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Coal", "measureType":"Ratio"}
			},
            {
				"description": "Steam to fuel ratio",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Coal", "measureType":"Ratio"}
			},
            {
				"description": "Feed water temperature Avg",
				"unit": "Deg.c",
				"tagList": {"equipment":"Economizer","measureProperty":"Feed Water", "measureType":"Temperature","measureInstance":1, "measureLocation":"Outlet"}
			},
            {
				"description": "FD air flow to bed",
				"unit": "Kg/hr",
				"tagList": {"equipment":"Fd Fan", "measureProperty":"Position", "measureType":"Percentage"}
			},
            {
				"description": "FD air flow to OFA",
				"unit": "Kg/hr",
				"tagList": {"equipment":"Fd Fan", "measureProperty":"Secondary Air", "measureType":"Flow"}
			},
            {
				"description": "FD air flow to burner",
				"unit": "Kg/hr",
				"tagList": {"equipment":"Fd Fan", "measureProperty":"Primary Air", "measureType":"Flow","measureLocation":"Inlet"}
			},
            {
				"description": "FGR Air flow",
				"unit": "Kg/hr",
				"tagList": {"equipment":"Fgr Fan", "measureProperty":"Tertiary Air", "measureType":"Flow"}
			},
            {
				"description": "O2 Avg",
				"unit": "%",
				"tagList": {"equipment":"Economizer", "measureProperty":"Flue Gas", "measureType":"O2"}
			},
            {
				"description": "ESP inlet temperature Avg",
				"unit": "Deg.c",
				"tagList": {"equipment":"Esp", "measureProperty":"Flue Gas", "measureType":"Temperature", "measureLocation":"Inlet"}
			},
            {
				"description": "Fly ash unburnt carbon loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Fly Ash Ubc", "measureType":"Loss"}
			},
            {
				"description": "Bed ash unburnt carbon loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Bed Ash Ubc", "measureType":"Loss"}
			},
            {
				"description": "Sensible heat in fly ash loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Sensible Fly Ash", "measureType":"Loss"}
			},
            {
				"description": "Sensible heat in bed ash loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Sensible Bed Ash", "measureType":"Loss"}
			},
            {
				"description": "Dry flue gas loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Dry Flue Gas", "measureType":"Loss"}
			},
            {
				"description": "Hydrogen in fuel loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"H2 In Fuel", "measureType":"Loss"}
			},
            {
				"description": "Moisture in fuel loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"H2 O In Fuel", "measureType":"Loss"}
			},
            {
				"description": "Moisture in air loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"H2 O In Air", "measureType":"Loss"}
			},
            {
				"description": "Radiation loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Radiation", "measureType":"Loss"}
			},
            {
				"description": "Unaccounted loss",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Unaccounted", "measureType":"Loss"}
			},
            {
				"description": "Total losses",
				"unit": "%",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Total", "measureType":"Loss"}
			},
            {
				"description": "Total fuel consumed for the period",
				"unit": "Tonnes",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"coal", "measureType":"Total Moisture"}
			},
            {
				"description": "Cost /Ton of steam generation",
				"unit": "Rs/Ton",
				"tagList": {"equipment":"Performance Kpi", "measureProperty":"Coal", "measureType":"CostPerUnit"}
			}            
		]
	},
	"type": "prfmancsumRpt",
    "equipment":{},
    "unitsId": "common",
    "equipmentId":{},
    "output":{}
}


url=config['api']['meta']+'/boilerStressProfiles'
body_req = requests.post(url, json=body)
print(body_req.status_code)
print(body_req.content)