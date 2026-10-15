import pandas as pd
import json

datasets = [
    {
        "id": "CENSUS_1981_HH6",
        "title": "Census of India 1981 - Household Tables (HH-Series, Part VIII-A & B)",
        "source_agency": "Registrar General and Census Commissioner of India",
        "years_covered": "1981",
        "spatial_resolution": "District, Tehsil/Taluk, Town, Rural/Urban",
        "key_variables": "Table HH-6 Part B: Number of rural households and population by availability of electricity (Domestic electricity connection) and tenure status. Separate tables for Total, SC, and ST households.",
        "digitization_status": "Scanned PDF books available at Census Digital Library & Internet Archive. High priority candidate for OCR pipeline.",
        "link": "https://censusindia.gov.in/census.website/data/census-tables",
        "strengths_for_did": "Universal district-level rural household electricity coverage in 1981, providing the exact mid-point of Green Revolution rollout.",
        "limitations": "Need to OCR/extract tables from state-wise Part VIII-B volumes."
    },
    {
        "id": "CENSUS_1971_1981_DCHB_VD",
        "title": "Census 1971 & 1981 Village Directory (District Census Handbooks - DCHB Part X-A / XIII-A)",
        "source_agency": "Directorate of Census Operations (State series)",
        "years_covered": "1971, 1981",
        "spatial_resolution": "Village (all ~600,000 villages in India) aggregated to District/Tehsil",
        "key_variables": "Power Supply availability by specific purpose: ED (Electricity for Domestic use), EAg (Electricity for Agricultural use/pumpsets), EA (Electricity for All purposes), EO (Electricity for Other/Commercial).",
        "digitization_status": "Printed District Handbooks in national and university libraries / Census archives. Sample districts can be targeted for OCR.",
        "link": "https://censusindia.gov.in/census.website/data/census-tables",
        "strengths_for_did": "Crucial distinction between agricultural (EAg) and domestic (ED) village grid access! Directly tests 'Pumps to Plugs' mechanism.",
        "limitations": "Handbooks must be digitized/extracted district by district; large OCR effort if scanning all 350+ districts."
    },
    {
        "id": "CENSUS_1991_HH4",
        "title": "Census of India 1991 - Housing and Amenities Tables (Table H-4 / SHRUG)",
        "source_agency": "Registrar General of India / DevDataLab (SHRUG)",
        "years_covered": "1991",
        "spatial_resolution": "Village, Town, Subdistrict, District",
        "key_variables": "Source of lighting (Electricity, Kerosene, Solar, Other, No lighting), latrine availability, drinking water source.",
        "digitization_status": "Fully digitized and harmonized in SHRUG v1 and v2.",
        "link": "https://www.devdatalab.org/shrug",
        "strengths_for_did": "Already in electronic format; easy to merge with agricultural panel.",
        "limitations": "Post-1990; cannot serve as pre-trend or intermediate Green Revolution check without earlier rounds."
    },
    {
        "id": "NSS_31_1976_77",
        "title": "NSS 31st Round: Survey on Rural Electrification and Use of Power (Schedule 22.1 / 22.2)",
        "source_agency": "National Sample Survey Organisation (NSSO), MoSPI",
        "years_covered": "July 1976 - June 1977",
        "spatial_resolution": "State, NSS Region, Village, Household",
        "key_variables": "Village electrification status and stage; domestic connections; agricultural pump electrification; motive power in rural enterprises; irrigation performance.",
        "digitization_status": "Tabulated in Sarvekshana journal issues (late 1970s / early 1980s). Microdata catalogued at microdata.gov.in.",
        "link": "https://microdata.gov.in/",
        "strengths_for_did": "Sole dedicated national survey on rural electrification during peak Green Revolution (1976-77).",
        "limitations": "NSS representative at NSS Region and State levels; district identifiers in early NSS microdata require masking crosswalks."
    },
    {
        "id": "NSS_CES_ROUNDS",
        "title": "NSS Quinquennial Consumer Expenditure Surveys (Rounds 28, 32, 38, 43)",
        "source_agency": "NSSO / MoSPI",
        "years_covered": "1973-74 (R28), 1977-78 (R32), 1983 (R38), 1987-88 (R43)",
        "spatial_resolution": "Household microdata, NSS Region, State",
        "key_variables": "Schedule 1.0: Household monthly expenditure on fuel and light, specifically itemizing Electricity charges and Kerosene; primary energy source for lighting.",
        "digitization_status": "Rounds 38 and 43 available as microdata (.raw/.dta); Round 32 available in Sarvekshana and MoSPI archives.",
        "link": "https://microdata.gov.in/",
        "strengths_for_did": "Continuous micro-level household panel-like cross-sections measuring actual electricity spending before 1991.",
        "limitations": "Repeated cross-sections rather than true household panel; representative at state/region."
    },
    {
        "id": "ARIS_REDS_PANEL",
        "title": "ARIS-REDS Panel (NCAER / Brown University)",
        "source_agency": "National Council of Applied Economic Research (NCAER) & Foster-Rosenzweig",
        "years_covered": "1968-71 (ARIS), 1982 (REDS), 1999 (REDS), 2006",
        "spatial_resolution": "Household, Village (250 villages, 98-102 districts across 16 states)",
        "key_variables": "Deck 75 (1999): Year village was electrified (elecy), number of domestic electricity connections (hhelec), electric pumpsets (pmpelec), TVs. Household schedules: connection status, electrical asset ownership, electricity charges.",
        "digitization_status": "Available online in public release at Brown PSTC repository.",
        "link": "https://adfdell.pstc.brown.edu/arisreds_data/",
        "strengths_for_did": "Directly stratified by Green Revolution status (IADP vs IAAP vs Control)! Contains retrospective village electrification year.",
        "limitations": "Sample is thin within districts (2-4 villages per district); village names coded."
    },
    {
        "id": "CEA_PUBLIC_ELECTRICITY",
        "title": "Public Electricity Supply, All India Statistics - General Review (Annual)",
        "source_agency": "Central Electricity Authority (CEA) / Ministry of Energy",
        "years_covered": "Annual series, 1960-1995",
        "spatial_resolution": "State, Utility / State Electricity Board (SEB)",
        "key_variables": "Annual electricity sales (GWh) disaggregated by sector: Domestic, Agriculture/Irrigation Pumping, Industrial, Commercial; number of energized pumpsets; number of electrified villages.",
        "digitization_status": "Published annually as government reports; physical copies in Gokhale Institute, Central Secretariat Library, and Google Books.",
        "link": "https://cea.nic.in/",
        "strengths_for_did": "Annual continuous panel of agricultural vs. domestic power consumption by state throughout 1966-1990.",
        "limitations": "State and SEB level rather than district-level."
    },
    {
        "id": "SEB_ADMIN_REPORTS",
        "title": "State Electricity Board (SEB) Annual Administration Reports",
        "source_agency": "Punjab SEB (PSEB), Haryana SEB (HSEB), UPSEB, Tamil Nadu SEB (TNEB)",
        "years_covered": "Annual, 1965-1990",
        "spatial_resolution": "Circle / Division / District",
        "key_variables": "Connected load (kW) by category (Domestic, Tube-wells/Agricultural, Industrial), units sold (kWh), number of consumers by circle/district.",
        "digitization_status": "Historical administrative publications; found in State Archives, SEB libraries, and Nehru Memorial Museum & Library.",
        "link": "State Administrative Archives",
        "strengths_for_did": "Provides sub-state (circle/district) power sales and connection counts for key Green Revolution states.",
        "limitations": "Must be retrieved from state-level archives or university libraries."
    },
    {
        "id": "PEO_PLANNING_COMMISSION",
        "title": "Evaluation of the Rural Electrification Programme (PEO Studies)",
        "source_agency": "Programme Evaluation Organisation (PEO), Planning Commission, GoI",
        "years_covered": "1965, 1972, 1980, 1986",
        "spatial_resolution": "Sample electrified villages and beneficiary households across 15+ states",
        "key_variables": "Time lag between village grid extension and household connection; motive of electrification (pumpsets vs domestic); costs of connection; tariff structures.",
        "digitization_status": "Published evaluation volumes in Planning Commission / NITI Aayog library archives.",
        "link": "https://dmeo.gov.in/",
        "strengths_for_did": "Rich qualitative and quantitative evidence on the 'pumps first, plugs second' adoption lag.",
        "limitations": "Sample survey of selected scheme areas rather than a nationwide census."
    },
    {
        "id": "ICRISAT_VLS",
        "title": "ICRISAT Village Level Studies (VLS / VDSA)",
        "source_agency": "ICRISAT (International Crops Research Institute for the Semi-Arid Tropics)",
        "years_covered": "Continuous panel 1975-1985 (6-10 villages in AP and Maharashtra)",
        "spatial_resolution": "Household (continuous high-frequency panel)",
        "key_variables": "Investment in dug wells, tubewells, electric vs diesel pumps, domestic electricity access, crop yields, input costs.",
        "digitization_status": "Freely available via ICRISAT microdata portal.",
        "link": "http://vdsa.icrisat.org/",
        "strengths_for_did": "Unmatched high-frequency microdata on farm investment dynamics.",
        "limitations": "Covers only semi-arid tropics (not the prime wheat belt like Punjab/Haryana)."
    }
]

df = pd.DataFrame(datasets)
csv_out = 'DSI Research/data/pre1991_electricity_datasets_catalog.csv'
json_out = 'DSI Research/data/pre1991_electricity_datasets_catalog.json'

df.to_csv(csv_out, index=False)
with open(json_out, 'w') as f:
    json.dump(datasets, f, indent=2)

print(f"Catalog generated successfully: {len(df)} dataset sources documented.")
print(f"Saved to {csv_out} and {json_out}")
