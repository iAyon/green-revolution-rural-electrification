import pandas as pd
import json

epw_articles = [
    {
        "citation": "Barnes, Douglas F., and Hans P. Binswanger. (1986). 'Impact of Rural Electrification and Infrastructure on Agricultural Changes, 1966–1980.' Economic and Political Weekly, 21(1), 26–34.",
        "year": 1986,
        "themes": "Rural electrification, agricultural investment, infrastructure complementarity, pumpsets",
        "data_sources_used": "Secondary district panel data (USAID/NCAER project AID/DSAN-CA-0179); Binswanger-Evenson district agricultural data; REC village electrification statistics (1966-1980).",
        "key_findings": "Demonstrates that rural electrification directly stimulated private agricultural investments in electric pumpsets, but found that broader socio-economic and transformational impacts lagged significantly. Stresses that electrification works in tandem with roads, credit, and markets.",
        "relevance_to_dsi": "Direct precedent for our study! Proves that during 1966-1980, the primary economic return was through irrigation pumpsets, exactly supporting the 'From Pumps to Plugs' first stage."
    },
    {
        "citation": "Pant, Niranjan. (1984). 'Community Tube Wells: An Organisational Alternative to Small Farmers' Irrigation.' Economic and Political Weekly, 19(26), A59–A66.",
        "year": 1984,
        "themes": "Tubewells, minor irrigation, smallholder access, institutional alternatives",
        "data_sources_used": "Field surveys in Vaishali (Bihar) and Deoria (Eastern UP); state minor irrigation census reports; tubewell energization records.",
        "key_findings": "Analyzes the high fixed cost of electric tubewells. While large farmers in early HYV areas could afford individual electric connections, smallholders in eastern India faced severe capital and institutional barriers.",
        "relevance_to_dsi": "Points to state-level and district-level minor irrigation census figures and tubewell records in UP and Bihar for the 1970s and 1980s."
    },
    {
        "citation": "Dhawan, B. D. (1975). 'Economics of Groundwater Irrigation in Hard Rock Areas.' Economic and Political Weekly, 10(25/26), A76–A84.",
        "year": 1975,
        "themes": "Groundwater, diesel vs electric pumps, hard-rock hydrogeology, power tariffs",
        "data_sources_used": "Central Water Commission data; State Groundwater Boards; Ministry of Irrigation Minor Irrigation statistics.",
        "key_findings": "Compares operating costs of diesel pumpsets vs electric pumpsets. Shows that electric pumpsets reduced per-acre water extraction costs by 50-70% compared to diesel, creating intense farm-level lobbying for grid lines.",
        "relevance_to_dsi": "Provides the microeconomic driver for why farmers demanded rural grid connections: massive cost advantage of electric over diesel pumping during the 1970s oil shocks."
    },
    {
        "citation": "John, V. (1971). 'Dilemma of State Tube Wells.' Economic and Political Weekly, 6(13), A27–A32.",
        "year": 1971,
        "themes": "State tubewells, grid power reliability, operational efficiency, UP & Bihar",
        "data_sources_used": "UP State Electricity Board (UPSEB) and Bihar State Electricity Board administrative logs; Irrigation Department operating records.",
        "key_findings": "Documents how State tubewells were plagued by mechanical breakdowns and irregular power supplies, which triggered the private tubewell revolution in the early 1970s as farmers installed their own electric tubewells.",
        "relevance_to_dsi": "Highlights SEB administrative logs as rich sources of feeder-line energization dates and private vs state tubewell connection counts."
    },
    {
        "citation": "Satyanarayana, T. (1979). 'Rural Electrification: Perspective and Problems.' Economic and Political Weekly, 14(34), 1473–1476.",
        "year": 1979,
        "themes": "REC financing, village electrification definitions, household vs agricultural demand",
        "data_sources_used": "Rural Electrification Corporation (REC) annual data; Planning Commission Sixth Plan Working Group on Power; CEA All-India Statistics.",
        "key_findings": "Critiques the official definition of 'electrified village' (which required only a single point of consumption, often a tubewell on the village periphery). Shows that while village electrification was rising fast, household domestic connections remained below 15% nationally.",
        "relevance_to_dsi": "Directly explains our conceptual puzzle: a village was officially classified as electrified as soon as an agricultural tubewell got power, but household 'plugs' lagged by 10 to 20 years!"
    },
    {
        "citation": "Desai, Ashok V. (1980). 'India's Energy Economy: Facts and Their Interpretation.' Economic and Political Weekly, 15(44), 1877–1882.",
        "year": 1980,
        "themes": "National energy balance, electricity consumption structure, commercial vs non-commercial energy",
        "data_sources_used": "NSS 28th and 32nd rounds (fuel and light consumption); Working Group on Energy Policy (1979) reports; CEA statistics.",
        "key_findings": "Shows that domestic lighting in rural India was overwhelmingly kerosene-dependent (~90%), while agricultural power consumption was the fastest-growing component of total electricity generation in India between 1965 and 1980.",
        "relevance_to_dsi": "Points directly to the NSS 28th (1973-74) and 32nd (1977-78) rounds for fuel/light consumption shares and rural energy transitions."
    },
    {
        "citation": "Vashishtha, Prem S. (1989). 'Changes in Structure of Investment of Rural Households: 1970-71 to 1981-82.' Journal of Income and Wealth, 10(2), 21–45.",
        "year": 1989,
        "themes": "ARIS-REDS panel, household investment, farm capital vs consumer durables",
        "data_sources_used": "NCAER ARIS 1970-71 and REDS 1981-82 panel data.",
        "key_findings": "Shows that between 1971 and 1982, rural households in high-adoption Green Revolution areas initially directed capital into irrigation assets (pumps, tubewells, tractors), followed in the second period by residential upgrades and consumer durables.",
        "relevance_to_dsi": "Provides empirical proof within the very ARIS-REDS dataset we have that farm productivity shocks precede domestic consumer investments."
    }
]

df = pd.DataFrame(epw_articles)
csv_out = 'DSI Research/data/epw_literature_annotated_bibliography.csv'
json_out = 'DSI Research/data/epw_literature_annotated_bibliography.json'

df.to_csv(csv_out, index=False)
with open(json_out, 'w') as f:
    json.dump(epw_articles, f, indent=2)

print(f"EPW Annotated Bibliography generated: {len(df)} key studies catalogued.")
print(f"Saved to {csv_out} and {json_out}")
