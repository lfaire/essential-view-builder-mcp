# API Documentation

This document lists the APIs available in the Business, Application, Integration, Technology, Information, and Enterprise modules.

## How to use with `api_fetch_template.xsl`

To use these APIs in a custom view, you can base your XSLT on `api_fetch_template.xsl`.
You need to configure the `apiList` variable in the JavaScript section of the template with the **DSA Data Label** of the APIs you want to call.
Do not maned any other bots of the XSL file.  Use the xsl template provided for the surrounding code.  make sure to add `<xsl:call-template name="RenderViewerAPIJSFunction"/>` after the first `<script>` tag where the code is generated	

# Essential API catalogue (source of truth)

> ❗ For LLMs / AI tools:
> - **Never invent new API keys or URLs.**
> - **Always search for existing APIs first** using `grep` or `find` in the `api/` directories (application, business, enterprise) before creating a new one.
> - **Consult the User** if you find a similar API but think you need a new one. 
> - **Always use the APIs defined in this document.**
> - When generating XSL/JS that calls APIs, **follow the usage pattern shown for each API**, including the required `<xsl:include>` and JavaScript `fetchAndRenderData` calls.
> - If you are unsure which API to use, **pick the one documented here that best matches the description** instead of making up a new one.
> - **Implement ID Normalization**: Use `normalize-space()` in XSL and `.trim()` in JS to ensure IDs match correctly.


### Example Configuration of `api_fetch_template.xsl`.
If you want to use the `Application Mart` and `Information Mart` APIs, find their DSA Data Labels in the documentation below (e.g., `appMartAPI` and `infoMartAPI`).
Then update the JavaScript in your XSLT:

```javascript
let appMartAPI, infoMartAPI;
$(document).ready(function() {
    // DEFINE APIS - the list of apis to call based on their data label
    const apiList=['appMartAPI','infoMartAPI'];

    async function executeFetchAndRender() {
        try {
            let responses = await fetchAndRenderData(apiList);
            ({ appMartAPI, infoMartAPI } = responses);
            
            console.log('App Mart Data', appMartAPI);
            console.log('Info Mart Data', infoMartAPI);

            // INSERT AI javascript code here to use the data
        }
        catch (error) {
            // Handle errors
        }
    }
    executeFetchAndRender()
});
```

## Application

### core_api_al_app_apr.xsl
- **Path**: `application/api/core_api_al_app_apr.xsl`
- **DSA Data Label**: `aprsAPI`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `apr` | Array | `[ 
  {
    "aprId": "store_1224_Class20014",
    "serviceId": "store_55_Class936",
    "appId": "store_55_Class1161"
  }
]` | mapping of Application Provider Role ids to Application Service and Application ids |
| `apr[].aprId` | String | `"store_283_Class10001"` |Application Provider Role id |
| `apr[].serviceId` | String | `"store_55_Class904"` | Application Service id |
| `apr[].appId` | String | `"store_55_Class1234"` | Application id |


### core_api_al_app_perf_measures.xsl
- **Path**: `application/api/core_api_al_app_perf_measures.xsl`
- **DSA Data Label**: `appKpiAPI`
- **Parameters**: None
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `applications` | Array | `[{"id": "store_174_Class10085", "app": "GenIntell", "name": "GenIntell", "perfMeasures": [{"category...`| array of applications and their performance score for different performance categories, each object provides an application id and list of measures |
| `applications[].id` | String | `"store_174_Class10085"` | Unique identifier for the app |
| `applications[].app` | String | `"GenIntell"` | application name |
| `applications[].name` | String | `"GenIntell"` | Display name, preferred ove .app |
| `applications[].perfMeasures` | Array | `[{"categoryid": "store_736_Class4", "id": "store_736_Class134", "date": "2022-06-30", "createdDate":...` | list of performance measure grouped by performance category |
| `applications[].processPerfMeasures` | Array | `[]` | array of performance measures related to processes the application supports |
| `applications[].securityClassifications` | Array | `[]` | Security classification tags |
| `perfCategory` | Array | `[{"id": "store_188_Class1", "type": "Performance_Measure_Category", "name": "Business Fit", "enumera...` | list of performance categories, you can use these to identify the categories used in the application instance by mapping by performance catoegory id |
| `perfCategory[].id` | String | `"store_188_Class1"` | Unique identifier |
| `perfCategory[].type` | String | `"Performance_Measure_Category"` | a category that groups Service qualities |
| `perfCategory[].name` | String | `"Business Fit"` | Display name for the category|
| `perfCategory[].enumeration_sequence_number` | String | `""` | the order the categeory should appear in lists if required, e.g. select boxes |
| `perfCategory[].enumeration_value` | String | `"Business Fit"` | label name, more user friendly |
| `perfCategory[].description` | String | `""` | Descriptive text |
| `perfCategory[].classes` | Array | `["Application_Provider"]` | the classes that can use this performance category|
| `perfCategory[].enumeration_value_for_classes` | Array | `[]` | the classes that can use this performance category |
| `perfCategory[].qualities` | Array | `["store_283_Class226"]` | array of service qualities that this category covers |
| `serviceQualities` | Array | `[{"id": "store_736_Class8", "name": "ESG Rating", "description": "", "type": "Application_Service_Qu...` | the services qualities that this category covers|
| `serviceQualities[].id` | String | `"store_736_Class8"` | Unique identifier |
| `serviceQualities[].name` | String | `"ESG Rating"` | Display name |
| `serviceQualities[].description` | String | `""` | Descriptive text |
| `serviceQualities[].type` | String | `"Application_Service_Quality"` | the subclass of the service quality |
| `serviceQualities[].shortName` | String | `"ESG Rating"` | a shorter name for the quality|
| `serviceQualities[].maxScore` | String | `""` | if set, the maximum number the service quality can be |
| `serviceQualities[].serviceWeighting` | String | `""` | a weighting that allows the quality to have greater impact on an overall score |
| `serviceQualities[].serviceIndex` | String | `""` | index number of the service quality |
| `serviceQualities[].sqvs` | Array | `[{"id": "store_736_Class108", "type": "Application_Service_Quality_Value", "name": "ESG Rating - Goo...` | the service quality values allowed with this service quality |

### core_api_al_application_capabilities_l1_to_services.xsl
- **Path**: `application/api/core_api_al_application_capabilities_l1_to_services.xsl`
- **DSA Data Label**: `appCapL1ITAData`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `application_capabilities` | Array | `[ 
  {
    "id": "store_55_Class762",
    "application_services": [
      {
  ...
}]}]` | array of application capabilities with their contained application services
| `application_capabilities_all` | Array | `[
  {
    "id": "store_219_Class148"
  }
]` |
| `id` | String | `N/A` | unique identifier for the capability|
| `application_services` | Array | `N/A` | services supporting the capability|
| `name` | String | `N/A` | name of the capability|
| `apps` | Array | `N/A` | applications supporting the capability|





### core_api_al_get_all_application_lifecycles.xsl
- **Path**: `application/api/core_api_al_get_all_application_lifecycles.xsl`
- **DSA Data Label**: `appLifecycle`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `application_lifecycles` | Array | `N/A` | array of application lifecycle by application, match by application id |
| `all_lifecycles` | Array | `N/A` | all lifecycles for deployments|
| `lifecycleJSON` | Array | `N/A` | list of all the lifecycles available with colours, and sequence |
| `name` | String | `N/A` | name of app |
| `id` | String | `N/A` | id of app |
| `supplierId` | String | `N/A` | name of application supplier |
| `allDates` | Array | `N/A` | all lifecycle dates for the application, with lifecycle type so can be grouped |
| `className` | String | `N/A` | class of the instance |
| `dateOf` | String | `N/A` | lifecycle from data |
| `thisid` | String | `N/A` | id of the instance |
| `type` | String | `N/A` | type of the instance |
| `seq` | Unknown | `N/A` | sequence number for the lifecycle |
| `backgroundColour` | String | `N/A` | backgroundColour of the lifecycle |
| `colour` | String | `N/A` | text Colour of the lifecycle |
| `productId` | String | `N/A` | id of the product tied to the lifecycle |
 
  

### core_api_app_orgs.xsl
- **Path**: `application/api/core_api_app_orgs.xsl`
- **DSA Data Label**: `appOrgId`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `applicationOrgUsers` | Array | `[{"id": "store_55_Class1161", "name": "ADEXCell Energy Manager", "organisations": ["store_55_Class67...` | array of applications and organisations using the app|
| `applicationOrgUsers[].id` | String | `"store_55_Class1161"` | Unique identifier for app |
| `applicationOrgUsers[].name` | String | `"ADEXCell Energy Manager"` | Display name for app|
| `applicationOrgUsers[].organisations` | Array | `["store_55_Class679"]` | ids of the orgs, can use to map via id to orgs found in orgData proerty of the core_api_el_org_summary_data_v2.xsl |

### core_api_application_mart.xsl
- **Path**: `application/api/core_api_application_mart.xsl`
- **DSA Data Label**: `appMartAPI`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `capability_hierarchy` | Array | `[{"id": "store_55_Class772", "level": "0", "name": "Business Management", "appCapCategory": "Core", ...` | array of application capabilities as a hierarchy, these are not business capabilities |
| `capability_hierarchy[].id` | String | `"store_55_Class772"` | Unique identifier for the application capability |
| `capability_hierarchy[].level` | String | `"0"` | level of the application capability |
| `capability_hierarchy[].name` | String | `"Business Management"` | Display name for the application capability |
| `capability_hierarchy[].appCapCategory` | String | `"Core"` | Category for the application capability |
| `capability_hierarchy[].visId` | Array | `[""]` | visibility of the application capability |
| `capability_hierarchy[].domainIds` | Array | `[{"id": "store_55_Class11"}]` | domains for the application capability|
| `capability_hierarchy[].sequence_number` | String | `""` | sequence for the application capability in views |
| `capability_hierarchy[].businessDomain` | Array | `[{"id": "store_55_Class11"}]` | business domains for the application capability|
| `capability_hierarchy[].childrenCaps` | Array | `[{"id": "store_55_Class774", "level": "1", "name": "Business Planning", "appCapCategory": "", "visId...` | children application capabilities for an application capability |
| `capability_hierarchy[].supportingServices` | Array | `[]` | Application services supporting the application capability |
| `capability_hierarchy[].securityClassifications` | Array | `[]` | Security classification tags |
| `application_capabilities` | Array | `[{"id": "store_55_Class762", "name": "Account Planning", "appCapCategory": "", "description": "Sales...` | flat list of all the application capabilities |
| `application_capabilities[].id` | String | `"store_55_Class762"` | Unique identifier for the application capability |
| `application_capabilities[].name` | String | `"Account Planning"` | Display name for the application capability |
| `application_capabilities[].appCapCategory` | String | `""` | Category for the application capability |
| `application_capabilities[].description` | String | `"Sales account planning software"` | Descriptive text or the application capability|
| `application_capabilities[].visId` | Array | `[""]` | visibility of the instance based on system lifecycle|
| `application_capabilities[].sequence_number` | String | `""` | sequence for the application capability in views |
| `application_capabilities[].domainIds` | Array | `[{"id": "store_55_Class20"}]` | list of Ids of the Application Domains to which this Application Capability belongs |
| `application_capabilities[].businessDomain` | Array | `[{"id": "store_55_Class20", "name": "Sales and Marketing"}]` | The business domain(s) to which an Application Capability belongs. |
| `application_capabilities[].ParentAppCapability` | Array | `[{"id": "store_55_Class759", "name": "Sales Management", "ReferenceModelLayer": ""}]` | Parent application capability of the current application capability |
| `application_capabilities[].SupportedBusCapability` | Array | `[{"id": "store_55_Class197", "name": "Strategic Relationship Management"}]` | The set of Business Capabilities that the Application Capability supports. |
| `application_capabilities[].securityClassifications` | Array | `[]` | Security classification tags |
| `application_capabilities[].supportingServices` | Array | `["store_55_Class1094"]` | List if Ids of application services supporting the capability |
| `application_capabilities[].documents` | Array | `[]` | URL document links to documents relevant to the appication capability |
| `application_services` | Array | `[{"id": "store_55_Class898", "sequence_number": "", "name": "Architecture Design", "description": "D...` | List of application services (business fucntionality).  A well-defined component of functional behaviour that provides a  logical grouping of related Application Functions. e.g. ExchangeRates Service, CreditCardPayment Service or logical application such as CRM System, ERP System. The specification of the service - in terms of what it does - is defined by the set of Application Functions that it provides. |
| `application_services[].id` | String | `"store_55_Class898"` | Unique identifier |
| `application_services[].sequence_number` | String | `""` | sequence for the application service in views |
| `application_services[].name` | String | `"Architecture Design"` | Display name |
| `application_services[].description` | String | `"Design architectural plans"` | Descriptive text |
| `application_services[].securityClassifications` | Array | `[]` | Security classification tags |
| `application_services[].visId` | Array | `[""]` | visibility of the instance based on system lifecycle|
| `application_services[].APRs` | Array | `[{"visId": ["store_90_Class44"], "id": "store_316_Class40000", "lifecycle": "", "appId": "store_55_C...` | array of application provider roles supporting the application service |
| `application_services[].busProc` | Array | `["store_55_Class221"]` | business processes supporting the application service |
| `application_services[].functions` | Array | `["store_90_Class150002"]` | application functions that realise the application service |
| `application_functions` | Array | `[{"id": "store_219_Class2", "name": "Calculate Comparisons", "description": "", "securityClassificat...` | list of application functions |
| `application_functions[].id` | String | `"store_219_Class2"` | Unique identifier for the application function |
| `application_functions[].name` | String | `"Calculate Comparisons"` | Display name for the application function |
| `application_functions[].description` | String | `""` | Descriptive text for the application function |
| `application_functions[].securityClassifications` | Array | `[]` | Security classification tags |
| `application_technology` | Array | `[{"id": "store_55_Class1161", "name": "ADEXCell Energy Manager", "environments": [{"id": "store_55_C...` | Applications with technology dependencies by environment.  Map by application id |
| `application_technology[].id` | String | `"store_55_Class1161"` | Application ID - **matches IDs in busCaptoAppDetails[].apps** |
| `application_technology[].name` | String | `"ADEXCell Energy Manager"` | Application name |
| `application_technology[].environments` | Array | `[{"id": "store_55_Class2108", "name": "DEXCell Energy Manager - Production", "colour": "", "role": "...` | Deployment environments (Production, DR, Training, etc.) |
| `applications` | Array | `[{"id": "store_55_Class1161", "ea_reference": "CAP001", "name": "ADEXCell Energy Manager", "short_na...` | array of applications |
| `applications[].id` | String | `"store_55_Class1161"` | Unique identifier for application |
| `applications[].ea_reference` | String | `"CAP001"` | unique ea-reference for application |
| `applications[].name` | String | `"ADEXCell Energy Manager"` | Display name for application|
| `applications[].short_name` | String | `""` | shorter name for application |
| `applications[].type` | String | `"Composite_Application_Provider"` | class for application |
| `applications[].afis` | Array | `[{"id": "store_219_Class11", "funcId": "store_219_Class1"}]` | list of application function implementations ids for application |
| `applications[].synonyms` | Array | `[]` | synonyms for application|
| `applications[].documents` | Array | `[]` | documents for application |
| `applications[].supplier` | Object | `{"id": "store_53_Class2", "name": "Dexma"}` | supplier of the application |
| `applications[].costs` | Array | `[{"name": "Hosting Cost", "description": "", "cost": "10000.0", "costType": "Annual_Cost_Component",...` | costs associated with the application |
| `applications[].maxUsers` | String | `"25"` | maximum users for the application |
| `applications[].family` | Array | `[]` | application family for the application |
| `app_function_implementations` | Array | `[{"id": "store_219_Class17", "name": "ADEXCell Energy Manager::Calculate Comparisons", "afiname": "C...` | application function implementations for the applications with names |
| `app_function_implementations[].id` | String | `"store_219_Class17"` | Unique identifier for application function implementation |
| `app_function_implementations[].name` | String | `"ADEXCell Energy Manager::Calculate Comparisons"` | Display name for application function implementation |
| `app_function_implementations[].afiname` | String | `"Calculate Comparisons"` | name for application function implementation |
| `app_function_implementations[].description` | String | `""` | Descriptive text for application function implementation|
| `app_function_implementations[].appId` | String | `"store_55_Class1161"` | this app id |
| `app_function_implementations[].afuncId` | String | `"store_219_Class2"` | application function id for this application function implementation |
| `stdStyles` | Array | `[{"id": "store_55_Class5266", "shortname": "View Styling for Mandatory", "colour": "#1B51A5", "colou...` | list of styles for application standards |
| `stdStyles[].id` | String | `"store_55_Class5266"` | Unique identifier |
| `stdStyles[].shortname` | String | `"View Styling for Mandatory"` | name of style |
| `stdStyles[].colour` | String | `"#1B51A5"` | background colour for style |
| `stdStyles[].colourText` | String | `"#ffffff"` | text colour for style |
| `ccy` | Array | `[{"id": "essential_baseline_v505_Class16", "name": "British Pound", "default": "", "exchangeRate": "...` | array of currencies |
| `ccy[].id` | String | `"essential_baseline_v505_Class16"` | Unique identifier |
| `ccy[].name` | String | `"British Pound"` | Display name |
| `ccy[].default` | String | `""` | default currency |
| `ccy[].exchangeRate` | String | `""` | exchnage rate for currency |
| `ccy[].ccySymbol` | String | `"£"` | symbol for currency |
| `ccy[].ccyCode` | String | `"GBP"` | currency code for currency  |
| `apus` | Array | `[{"id": "store_174_Class10006", "name": "Static Architecture of::DMS: Relation from Creds API::in::S...` | List of application usages, used to work out integrations between applications |
| `apus[].id` | String | `"store_174_Class10006"` | Unique identifier |
| `apus[].name` | String | `"Static Architecture of::DMS: Relation from Creds API::in::Static Architecture of::DMS to Creds::in:...` | Display name |
| `apus[].fromtype` | String | `"Application_Provider_Interface"` | type of the from application |
| `apus[].totype` | String | `"Composite_Application_Provider"` | type of the to application  |
| `apus[].edgeName` | String | `"store_174_Class10000 to store_55_Class1224"` | Name for the edge |
| `apus[].fromAppId` | String | `"store_174_Class10000"` | id of the from application or API |
| `apus[].toAppId` | String | `"store_55_Class1224"` | id of the to application or API|
| `apus[].fromApp` | String | `"Creds API"` | name of the from application or API |
| `apus[].toApp` | String | `"Creds"` |name of the to application or API |
| `apus[].infoData` | Array | `[{"id": "store_174_Class10008", "type": "APP_PRO_TO_INFOREP_EXCHANGE_RELATION", "name": "", "acquisi...` | Information passed on the connection along with mechanism used, etc |
| `apus[].info` | Array | `[{"id": "store_297_Class40009", "type": "Information_Representation", "name": "Energy Trends"}]` | information passed on the connection |


## Business

### core_api_bl_actor_to_roles.xsl
- **Path**: `business/api/core_api_bl_actor_to_roles.xsl`
- **DSA Data Label**: `N/A`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `a2rs` | Array | `N/A` | array of actor to role relations |
| `id` | String | `N/A` | id of the a2r |
| `actorName` | String | `N/A` | name of actor |
| `actorId` | String | `N/A` | id of actor |
| `roleName` | String | `N/A` | role for actor |
| `roleId` | String | `N/A` | id of role |


### core_api_bl_bus_domain.xsl
- **Path**: `business/api/core_api_bl_bus_domain.xsl`
- **DSA Data Label**: `N/A`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `businessDomains` | Array | `N/A` | array of business domains |
| `id` | String | `N/A` | id of the business domain|
| `name` | String | `N/A` | name of the business domain |

### core_api_bl_bus_perf_measures.xsl
- **Path**: `business/api/core_api_bl_bus_perf_measures.xsl`
- **DSA Data Label**: `busKpiAPI`
- **Parameters**: None
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `processes` | Array | `[{"id": "store_113_Class10852", "name": "Track Generation Portfolio Availability", "physical": ["sto...` | list of business processes id and name with array of performance measures |
| `processes[].id` | String | `"store_113_Class10852"` | Unique identifier for process |
| `processes[].name` | String | `"Track Generation Portfolio Availability"` | Display name for process|
| `processes[].physical` | Array | `["store_113_Class10854"]` | array of supporting physical process Ids |
| `processes[].description` | String | `""` | Descriptive text for process |
| `processes[].perfMeasures` | Array | `[{"categoryid": "store_315_Class170", "id": "store_315_Class277", "date": "2025-01-01", "createdDate...` | array of performance measures for the process |
| `processes[].securityClassifications` | Array | `[]` | Security classification tags |
| `businessCapabilities` | Array | `[{"id": "store_219_Class149", "name": "Portfolio Risk", "description": "", "perfMeasures": [{"catego...` | list of business capabilities id and name with array of performance measures |
| `businessCapabilities[].id` | String | `"store_219_Class149"` | Unique identifier for the business capability|
| `businessCapabilities[].name` | String | `"Portfolio Risk"` | Display name for the business capability|
| `businessCapabilities[].description` | String | `""` | Descriptive text for the business capability|
| `businessCapabilities[].perfMeasures` | Array | `[{"categoryid": "store_315_Class69", "id": "store_315_Class171", "date": "2025-01-01", "createdDate"...` | array of performance measures for the business capability |
| `businessCapabilities[].securityClassifications` | Array | `[]` | Security classification tags |
| `perfCategory` | Array | `[{"id": "store_315_Class170", "type": "Performance_Measure_Category", "name": "Process Maturity", "c...` | A performance catagory for specific classes that groups Business Service Qualities |
| `perfCategory[].id` | String | `"store_315_Class170"` | Unique identifier |
| `perfCategory[].type` | String | `"Performance_Measure_Category"` | a category that groups Service qualities  |
| `perfCategory[].name` | String | `"Process Maturity"` | Display name for the category |
| `perfCategory[].classes` | Array | `["Business_Process"]` | the classes that can use this performance category |
| `perfCategory[].qualities` | Array | `["store_315_Class71"]` | array of service qualities that this category covers  |
| `serviceQualities` | Array | `[{"id": "store_315_Class70", "type": "Business_Service_Quality", "name": "Governance and Compliance"...` | the services qualities that this category covers |
| `serviceQualities[].id` | String | `"store_315_Class70"` | Unique identifier |
| `serviceQualities[].type` | String | `"Business_Service_Quality"` | the subclass of the service quality |
| `serviceQualities[].name` | String | `"Governance and Compliance"` | Display name |
| `serviceQualities[].shortName` | String | `""` |  a shorter name for the quality |
| `serviceQualities[].maxScore` | String | `""` | if set, the maximum number the service quality can be  |
| `serviceQualities[].description` | String | `"Measures the policies, frameworks, and governance mechanisms in place to ensure alignment with orga...` | Descriptive text |
| `serviceQualities[].serviceWeighting` | String | `""` | a weighting that allows the quality to have greater impact on an overall score |
| `serviceQualities[].serviceIndex` | String | `""` | an index for the service quality |
| `serviceQualities[].sqvs` | Array | `[{"id": "store_315_Class72", "type": "Business_Service_Quality_Value", "name": "Governance and Compl...` | the service quality values allowed with this service quality |

 

## Enterprise

### core_api_el_bus_cap_to_app_mart_apps.xsl
- **Path**: `enterprise/api/core_api_el_bus_cap_to_app_mart_apps.xsl`
- **DSA Data Label**: `busCapAppMartApps`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `meta` | Array | `[{"classes": ["Group_Actor"], "menuId": "grpActorGenMenu"}]` | array of meta data for menus IGNORE|
| `meta[].classes` | Array | `["Group_Actor"]` | meta data for menus  IGNORE|
| `meta[].menuId` | String | `"grpActorGenMenu"` | id of menus IGNORE|
| `reports` | Array | `[{"name": "appRat", "link": "application/core_al_app_rationalisation_analysis_simple.xsl"}]` | list of relevant reports IGNORE|
| `reports[].name` | String | `"appRat"` | Display name IGNORE|
| `reports[].link` | String | `"application/core_al_app_rationalisation_analysis_simple.xsl"` | path for report IGNORE |
| `applications` | Array | `[{"id": "store_55_Class1161", "name": "ADEXCell Energy Manager", "description": "Real time energy co...` | array of applications, should be seen as the primary applications master data source that is enriched with data from other APIs, match on application id |
| `applications[].id` | String | `"store_55_Class1161"` | Unique identifier for the application |
| `applications[].name` | String | `"ADEXCell Energy Manager"` | Display name for the application |
| `applications[].description` | String | `"Real time energy consumption monitoring of facilities"` | Descriptive text for the application|
| `applications[].class` | String | `"Composite_Application_Provider"` | class type for the application |
| `applications[].className` | String | `"Composite_Application_Provider"` | class Name for the application |
| `applications[].visId` | Array | `[""]` | visibility of the instance based on system lifecycle|
| `applications[].children` | Array | `[]` | ids for any child apps for the application |
| `applications[].family` | Array | `[]` | array of families for the application, id and name |
| `applications[].regulations` | Array | `[{"id": "store_877_Class1", "name": "GDPR", "description": "", "className": "Regulation"}]` | regulations in scope for the application |
| `applications[].issues` | Array | `[]` | issues for the application |
| `applications[].inI` | String | `"4"` | count of application interfaces into the application |
| `applications[].inDataCount` | Array | `["store_174_Class10109"]` | ids of application interfaces into the application |
| `applications[].inIList` | Array | `[{"id": "store_55_Class1168", "name": "Microsoft Project Server"}]` | list of application interfaces into the application |
| `applications[].outI` | String | `"4"` | count of application interfaces from the application |
| `applications[].valueClass` | String | `"Composite_Application_Provider"` | class of the instance |
| `applications[].dispositionId` | String | `"store_183_Class27"` | Id of disposition - map to the enumerations -> values in the filters property of this api|
| `applications[].outIList` | Array | `[{"name": "Entronix EMP", "id": "store_55_Class1158"}]` | list of application interfaces from the application  |
| `applications[].outDataCount` | Array | `["store_174_Class68"]` |  ids of application interfaces from the application |
| `applications[].criticality` | String | `""` | criticality of this application |
| `applications[].type` | String | `"Business Application"` | type of this application  |
| `applications[].typeid` | String | `"essential_prj_CC_v1_4_2_Instance_670003"` | type id of this application |
| `applications[].orgUserIds` | Array | `["store_55_Class679"]` | array of ids for orgs using this application |
| `applications[].geoIds` | Array | `["essential_baseline_v2_0_Class50065"]` | array of ids for geographies using this application |
| `applications[].siteIds` | Array | `["store_55_Class1328"]` | array of ids for sites using this application |
| `applications[].codebaseID` | String | `"essential_prj_AA_v1_4_Instance_119"` | id for codebase status - find the match in filters property of this api enumeration-> values (match here by id)|
| `applications[].deliveryID` | String | `"essential_baseline_v505_Class20"` | id for delivery type - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].sA2R` | Array | `["store_307_Class0"]` | stakeholders for the application |
| `applications[].al_managed_by_services` | Array | `[]` | Manage services mapped to this application|
| `applications[].lifecycle` | String | `"EAS_Meta_Model_v1_3_Instance_189"` | lifecycle for this application (direct not via lifecycle model) - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].physP` | Array | `["store_177_Class0"]` | list of ids of physical processes using this app, match to physcial processes by id  |
| `applications[].allServicesIdOnly` | Array | `[{"id": "store_55_Class2257", "securityClassifications": []}]` | list of application services ids use by this application |
| `applications[].allServices` | Array | `[{"id": "store_55_Class2257", "lifecycleId": "", "serviceId": "store_55_Class910", "className": "App...` |  list of application services used by this application |
| `applications[].ap_business_criticality` | Array | `[]` | array of criticality for this application |
| `applications[].ap_codebase_status` | Array | `["essential_prj_AA_v1_4_Instance_119"]` | id for codebase status - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].ap_delivery_model` | Array | `["essential_baseline_v505_Class20"]` | id for delivery_model - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].ap_disaster_recovery_failover_model` | Array | `[]` | array of  disaster_recovery_failover_model for this application|
| `applications[].ap_disposition_lifecycle_status` | Array | `["store_183_Class27"]` | id for disposition status - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].application_provider_purpose` | Array | `["essential_prj_CC_v1_4_2_Instance_670003"]` | id for application provider purpose - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].apt_customisation_level` | Array | `[]` | id for customisation level - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].apt_pace_of_change_level` | Array | `[]` | id for pace of change level - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].apt_user_interaction_methods` | Array | `[]` | id for user interaction methods - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].ea_recovery_point_objective` | Array | `["store_174_Class20006"]` | id for RPO - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].ea_recovery_time_objective` | Array | `["store_174_Class20001"]` | id for RTO - find the match in filters property of this api enumeration-> values (match here by id) |
| `applications[].lifecycle_status_application_provider` | Array | `["EAS_Meta_Model_v1_3_Instance_189"]` | ?id for lifecycle_status_application_provider - find the match in filters property of this api enumeration-> values (match here by id |
| `applications[].purchase_status` | Array | `[]` | purchase status for the application |
| `applications[].user_count_range` | Array | `[]` | Defines a numerical range for the number of users of an EA element |
| `applications[].vendor_product_lifecycle_status` | Array | `[]` | Vendor-defined product lifecycle status (e.g. General Availability, Extended Support, End of Life) |
| `applications[].ap_supports_multi_language` | Array | `["true"]` | Defines whether this Application Provider provides support for multiple languages |
| `applications[].distribute_costs` | Array | `["true"]` | Defines whether the costs associated with the element should be evenly distributed across the consumers of its capabilities |
| `applications[].services` | Array | `[{"id": "store_55_Class910", "name": "Benchmarking", "securityClassifications": []}]` | Application services provided by this application |
| `applications[].securityClassifications` | Array | `[]` | Security classification tags |
| `compositeServices` | Array | `[{"id": "store_911_Class10017", "name": "ERP System", "containedService": ["store_55_Class1104", "st...` | Composite application services (services made up of other services) |
| `compositeServices[].id` | String | `"store_911_Class10017"` | Unique identifier |
| `compositeServices[].name` | String | `"ERP System"` | Display name |
| `compositeServices[].containedService` | Array | `["store_55_Class1104"]` | Child services contained within this composite service |
| `compositeServices[].securityClassifications` | Array | `[]` | Security classification tags |
| `apis` | Array | `[{"id": "store_174_Class63", "name": "ADEXCell Energy Manager API", "description": "", "class": "App...` | Application provider interfaces (APIs, integrations, middleware) |
| `apis[].id` | String | `"store_174_Class63"` | Unique identifier |
| `apis[].name` | String | `"ADEXCell Energy Manager API"` | Display name |
| `apis[].description` | String | `""` | Descriptive text |
| `apis[].class` | String | `"Application_Provider_Interface"` | Essential metamodel class name |
| `apis[].className` | String | `"Application_Provider_Interface"` | Essential metamodel class name |
| `apis[].visId` | Array | `["store_90_Class44"]` | visibility of the instance based on system lifecycle |
| `apis[].children` | Array | `[]` | Child elements or sub-components |
| `apis[].family` | Array | `[]` | Technology or product family grouping |
| `apis[].regulations` | Array | `[]` | Applicable regulations or compliance requirements |
| `apis[].issues` | Array | `[]` | Known issues or problems |
| `apis[].inI` | String | `"1"` | count of interfaces into the application |
| `apis[].inDataCount` | Array | `["store_174_Class68"]` | list of interface ids into the application |
| `apis[].inIList` | Array | `[{"id": "store_55_Class1161", "name": "ADEXCell Energy Manager"}]` | Inbound integrations or consuming applications |
| `apis[].outI` | String | `"1"` | count of interfaces out of the application |
| `apis[].valueClass` | String | `"Application_Provider_Interface"` | Essential metamodel class for value tracking |
| `apis[].dispositionId` | String | `""` | Disposition lifecycle status identifier |
| `apis[].outIList` | Array | `[{"name": "AMS Fleet Solutions", "id": "store_55_Class1190"}]` | Outbound integrations or target applications |
| `apis[].outDataCount` | Array | `["store_174_Class70"]` | list of interface ids out of the application  |
| `apis[].criticality` | String | `""` | Business criticality rating |
| `apis[].orgUserIds` | Array | `[]` | List of ids of Organizations using this interface |
| `apis[].geoIds` | Array | `[]` | List of ids of Geographic regions or locations where interface is used |
| `apis[].siteIds` | Array | `[]` | List of ids of Physical sites where interface is deployed |
| `apis[].codebaseID` | String | `""` | Codebase status identifier |
| `apis[].deliveryID` | String | `""` | Delivery model identifier |
| `apis[].sA2R` | Array | `[]` | stakeholders for the API |
| `apis[].al_managed_by_services` | Array | `[]` | Services managing this application layer element |
| `apis[].lifecycle` | String | `""` | Lifecycle status |
| `apis[].physP` | Array | `[]` | Physical processes using this interface |
| `apis[].allServicesIdOnly` | Array | `[]` | List of service IDs only |
| `apis[].allServices` | Array | `[]` | All related application services |
| `apis[].ap_business_criticality` | Array | `[]` | Business criticality rating for application provider |
| `apis[].ap_codebase_status` | Array | `[]` | Status of the codebase (e.g. Custom, COTS, SaaS) |
| `apis[].ap_delivery_model` | Array | `[]` | How the application is delivered (e.g. On-premise, Cloud, Hybrid) |
| `apis[].ap_disaster_recovery_failover_model` | Array | `[]` | Disaster recovery and failover approach |
| `apis[].ap_disposition_lifecycle_status` | Array | `[]` | Disposition lifecycle status (retirement/decommissioning status) |
| `apis[].application_provider_purpose` | Array | `[]` | Purpose classification of the application |
| `apis[].apt_customisation_level` | Array | `[]` | Level of customization applied to packaged software |
| `apis[].apt_pace_of_change_level` | Array | `[]` | Expected frequency of changes to the application |
| `apis[].apt_user_interaction_methods` | Array | `[]` | Methods users interact with the application (e.g. Web, Mobile, Desktop) |
| `apis[].ea_recovery_point_objective` | Array | `[]` | Maximum acceptable data loss measured in time |
| `apis[].ea_recovery_time_objective` | Array | `[]` | Maximum acceptable downtime for recovery |
| `apis[].lifecycle_status_application_provider` | Array | `[]` | Deployment lifecycle status (e.g. Production, Pilot, Retired) |
| `apis[].purchase_status` | Array | `[]` | Purchase or procurement status |
| `apis[].user_count_range` | Array | `[]` | Numerical range for the number of users |
| `apis[].vendor_product_lifecycle_status` | Array | `[]` | Vendor-defined product lifecycle status |
| `apis[].ap_supports_multi_language` | Array | `["none"]` | Defines whether this Application Provider provides support for multiple languages |
| `apis[].distribute_costs` | Array | `["true"]` | Defines whether the costs associated with the element should be evenly distributed across the consumers of its capabilities |
| `apis[].services` | Array | `[]` | array of services supporting the API |
| `apis[].securityClassifications` | Array | `[]` | Security classification tags |
| `lifecycles` | Array | `[{"id": "essential_prj_AA_v1_4_Instance_10068", "shortname": "Under Planning", "colour": "#4196D9", ...` | list of lifecycles |
| `lifecycles[].id` | String | `"essential_prj_AA_v1_4_Instance_10068"` | Unique identifier |
| `lifecycles[].shortname` | String | `"Under Planning"` | short name for the lifecycle |
| `lifecycles[].colour` | String | `"#4196D9"` | background colour for style |
| `lifecycles[].colourText` | String | `"#ffffff"` | text colour for style |
| `codebase` | Array | `[{"id": "essential_prj_AA_v1_0_Instance_10002", "shortname": "Packaged", "colour": "#4196D9", "colou...` | list of codebases |
| `codebase[].id` | String | `"essential_prj_AA_v1_0_Instance_10002"` | Unique identifier |
| `codebase[].shortname` | String | `"Packaged"` | short name for the codebase |
| `codebase[].colour` | String | `"#4196D9"` | background colour for style |
| `codebase[].colourText` | String | `"#ffffff"` | text colour for style |
| `delivery` | Array | `[{"id": "essential_baseline_v505_Class23", "shortname": "Desktop", "colour": "#EF3F4A", "colourText"...` | array of delivery models |
| `delivery[].id` | String | `"essential_baseline_v505_Class23"` | Unique identifier |
| `delivery[].shortname` | String | `"Desktop"` | short name for the delivery model |
| `delivery[].colour` | String | `"#EF3F4A"` | background colour for style |
| `delivery[].colourText` | String | `"#ffffff"` | text colour for style |
| `filters` | Array | `[{"id": "Lifecycle_Status", "name": "Lifecycle Status", "valueClass": "Lifecycle_Status", "descripti...` | dynamic list of filters from enumerations tied to the application provider class |
| `filters[].id` | String | `"Lifecycle_Status"` | Unique identifier |
| `filters[].name` | String | `"Lifecycle Status"` | Display name |
| `filters[].valueClass` | String | `"Lifecycle_Status"` | class type |
| `filters[].description` | String | `""` | Descriptive text |
| `filters[].slotName` | String | `"lifecycle_status_application_provider"` | slot name for enumeration|
| `filters[].isGroup` | Boolean | `false` | identifies if it is part of a group |
| `filters[].icon` | String | `"fa-circle"` | icon for the enumeration |
| `filters[].color` | String | `"#93592f"` | colour for the enumeration |
| `filters[].values` | Array | `[{"id": "essential_prj_AA_v1_4_Instance_10068", "sequence": "1", "enum_name": "Under Planning", "nam...` | all values for the filter |
| `version` | String | `"6152"` | DO NOT USE |

### core_api_el_bus_cap_to_app_mart_caps.xsl
- **Path**: `enterprise/api/core_api_el_bus_cap_to_app_mart_caps.xsl`
- **DSA Data Label**: `busCapAppMartCaps`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `meta` | Array | `[{"classes": ["Group_Actor"], "menuId": "grpActorGenMenu"}]` | array of meta data for menus IGNORE |
| `meta[].classes` | Array | `["Group_Actor"]` | array of classes for menus IGNORE |
| `meta[].menuId` | String | `"grpActorGenMenu"` | menu ids for menus IGNORE |
| `busCapHierarchy` | Array | `[{"id": "store_55_Class30", "visId": [""], "name": "Maintenance", "className": "Business_Capability"...` | Top-level business capabilities (level 0) with recursive child structure |
| `busCapHierarchy[].id` | String | `"store_55_Class30"` | Unique identifier for the capability |
| `busCapHierarchy[].visId` | Array | `[""]` | visibility of the instance based on system lifecycle|
| `busCapHierarchy[].name` | String | `"Maintenance"` | Human-readable capability name |
| `busCapHierarchy[].className` | String | `"Business_Capability"` | name of the class used |
| `busCapHierarchy[].description` | String | `"Maintenance of equipment and sites"` | Description of what this capability does |
| `busCapHierarchy[].position` | String | `""` | Position/sequence number within the capability hierarchy level (used for ordering siblings) |
| `busCapHierarchy[].order` | String | `""` | Display order override for custom sorting of capabilities in visualizations |
| `busCapHierarchy[].diffLevelIds` | Array | `[]` | Array of Business Differentiation Level instance IDs that classify how the capability differentiates the business (e.g., competitive advantage, parity, commodity) |
| `busCapHierarchy[].business_capability_purpose` | Array | `[]` | Array of purpose classification instances describing the capability's strategic intent (e.g., core, supporting, enabling) |
| `busCapHierarchy[].business_differentiation_level` | Array | `[]` | Array containing Business Differentiation Level instances with full metadata (name, description, scores) rather than just IDs |
| `busCapHierarchy[].operating_model_geographic_scope` | Array | `[]` | Array of Geographic Scope instances indicating where this capability operates (e.g., global, regional, local markets) |
| `busCapHierarchy[].level` | String | `"0"` | Hierarchy level: "0" (top), "1", "2", etc. |
| `busCapHierarchy[].childrenCaps` | Array | `[{"id": "store_55_Class121", "visId": [""], "name": "Performance Management", "className": "Business...` | **Recursive** - Array of child capability objects at next level |
| `busCapHierarchy[].securityClassifications` | Array | `[]` | Security classification tags |
| `busCaptoAppDetails` | Array | `[{"id": "store_219_Class149", "link": "<a href = \"?XML=reportXML.xml&PMA=store_219_Class149&cl=en-g...` | Array of all business capabilities with their supporting applications |
| `busCaptoAppDetails[].id` | String | `"store_219_Class149"` | Unique identifier - **join with busCapHierarchy by ID** |
| `busCaptoAppDetails[].link` | String | `"<a href = "?XML=reportXML.xml&PMA=store_219_Class149&cl=en-gb" class = " context-menu-busCapGenMenu...` | url - legacy do not use |
| `busCaptoAppDetails[].className` | String | `"Business_Capability"` | name of the class used |
| `busCaptoAppDetails[].index` | String | `""` | index of the business capability for ordering |
| `busCaptoAppDetails[].isRoot` | String | `""` | define if root capability or not |
| `busCaptoAppDetails[].name` | String | `"Portfolio Risk"` | Human-readable capability name |
| `busCaptoAppDetails[].allProcesses` | Array | `[]` | list of all business processes for the business capability inculding children capabilities |
| `busCaptoAppDetails[].infoConcepts` | Array | `[]` | list of all information concepts for the business capability |
| `busCaptoAppDetails[].processes` | Array | `[]` |  list of all business processes directly mapped to the business capability  |
| `busCaptoAppDetails[].physP` | Array | `[]` |  list of all physical business processes for the business capability  |
| `busCaptoAppDetails[].classifications` | Array | `[]` | classification relevant for the business capability |
| `busCaptoAppDetails[].orgUserIds` | Array | `[]` |  List of ids of Organizations using this Business capability |
| `busCaptoAppDetails[].domainIds` | Array | `[]` |  List of ids of business domains mapped to this Business capability |
| `busCaptoAppDetails[].prodConIds` | Array | `[]` | List of ids Prodict Concepts mapped to this Business capability |
| `busCaptoAppDetails[].geoIds` | Array | `[]` | List of ids of geographies using this Business capability |
| `busCaptoAppDetails[].visId` | Array | `["store_90_Class44"]` | visibility of the instance based on system lifecycle |
| `busCaptoAppDetails[].business_capability_purpose` | Array | `[]` | purposes of this business capabilty |
| `busCaptoAppDetails[].business_differentiation_level` | Array | `[]` | differentiation of this business capability |
| `busCaptoAppDetails[].operating_model_geographic_scope` | Array | `[]` | scope of the operating model for this business capability |
| `busCaptoAppDetails[].thisapps` | Array | `[]` | ✓ Array of application ID strings - **join with application_technology by ID** (same as apps) |
| `busCaptoAppDetails[].apps` | Array | `[]` | ✓ Array of application ID strings - **join with application_technology by ID** (same as thisapps) |
| `busCaptoAppDetails[].securityClassifications` | Array | `[]` | Security classification tags |
| `rootCap` | String | `"Energy"` | root capability name |
| `physicalProcessToProcess` | Array | `[{"pPID": "store_113_Class10806", "procID": "store_55_Class381"}]` | pairs of business processes ids to physical processes ids |
| `physicalProcessToProcess[].pPID` | String | `"store_113_Class10806"` | physical processes id |
| `physicalProcessToProcess[].procID` | String | `"store_55_Class381"` | business processes id |
| `filters` | Array | `[{"id": "Business_Capability_Purpose", "name": "Business Capability Purpose", "valueClass": "Busines...` | dynamic list of filters from enumerations tied to the business capability class |
| `filters[].id` | String | `"Business_Capability_Purpose"` | Unique identifier |
| `filters[].name` | String | `"Business Capability Purpose"` | Display name |
| `filters[].valueClass` | String | `"Business_Capability_Purpose"` | class for values |
| `filters[].description` | String | `""` | Descriptive text |
| `filters[].slotName` | String | `"business_capability_purpose"` | slot name for enumeration |
| `filters[].isGroup` | Boolean | `false` | is this filter part of a group |
| `filters[].icon` | String | `"fa-circle"` | icon for enumeration |
| `filters[].color` | String | `"hsla(25, 52%, 38%, 1)"` | colour for enumeration |
| `filters[].values` | Array | `[{"id": "essential_baseline_v2_0_Class60006", "enum_name": "Direct", "name": "Direct", "sequence": "...` | list of value for the enumeration |
| `rootOrgs` | Array | `[]` | List of root organisations where multiple set, based on isRoot slot |
| `bus_model_management` | Object | `{"businessModels": [{"id": "store_911_Class10119", "domain": "", "name": "Gentailer", "description":...` | list of business models |
| `version` | String | `"620"` | IGNORE |


### core_api_el_org_summary_data_v2.xsl
- **Path**: `enterprise/api/core_api_el_org_summary_data_v2.xsl`
- **DSA Data Label**: `orgSummary`
- **Parameters**: None
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `orgData` | Array | `[{"id": "store_55_Class677", "parent": [], "name": "Distribution", "short_name": "", "description": ...` | array of organisations |
| `orgData[].id` | String | `"store_55_Class677"` | Unique identifier |
| `orgData[].parent` | Array | `[]` | parents of this organisation |
| `orgData[].name` | String | `"Distribution"` | Display name |
| `orgData[].short_name` | String | `""` | short name for organisation |
| `orgData[].description` | String | `"Responsible client facing, non-operational services"` | Descriptive text |
| `orgData[].regulations` | Array | `[]` | List if regulations impacting this organisation |
| `orgData[].documents` | Array | `[]` | URL links to documents for this organisation |
| `orgData[].orgEmployees` | Array | `[]` | employees in this organisation |
| `orgData[].site` | Array | `[{"name": "Paris", "id": "store_55_Class749"}]` | sites for this organisation |
| `orgData[].businessProcess` | Array | `[{"name": "Monitor Environmental Trends", "id": "store_55_Class451", "criticality": "High"}]` | processes performed by this organisation |
| `orgData[].applicationsUsedbyProcess` | Array | `[]` | array of applications mapped by the physical process |
| `orgData[].applicationsUsedbyOrgUser` | Array | `[]` | array of applications where the stakleholder is this organisation |
| `orgData[].children` | Array | `["store_55_Class679"]` | children organisations of this organisation |
| `orgRoles` | Array | `[{"id": "store_55_Class677", "name": "Distribution", "actor": "store_283_Class2239 store_55_Class464...` | List of organisation roles |
| `orgRoles[].id` | String | `"store_55_Class677"` | Unique identifier |
| `orgRoles[].name` | String | `"Distribution"` | Display name |
| `orgRoles[].actor` | String | `"store_283_Class2239 store_55_Class4645"` | ids of actors playing this role DO NOT USE|
| `orgRoles[].a2rs` | Array | `["store_283_Class2239"]` | actor to role relation ids |
| `orgRoles[].roles` | Array | `[{"id": "essential_baseline_v62_Class15", "name": "Technology Organisation User"}]` | roles for this organisation |
| `indivData` | Array | `[{"name": "Alan Law", "id": "store_90_Class90000", "roles": [{"id": "store_113_Class102", "roleid": ...` | Individuals and roles held |
| `indivData[].name` | String | `"Alan Law"` | Display name |
| `indivData[].id` | String | `"store_90_Class90000"` | Unique identifier |
| `indivData[].roles` | Array | `[{"id": "store_113_Class102", "roleid": "store_113_Class98", "name": ""}]` | roles for the individual |
| `roleData` | Array | `[{"name": "Data Standard Owning Organisation", "id": "essential_baseline_v3_0_3_Class10001"}]` | role names and ids |
| `roleData[].name` | String | `"Data Standard Owning Organisation"` | Display name |
| `roleData[].id` | String | `"essential_baseline_v3_0_3_Class10001"` | Unique identifier |
| `a2rs` | Array | `[{"id": "store_113_Class100", "actor": "Sales", "actorid": "store_55_Class681", "type": "Group_Actor...` | list of actor to role relations, with actor and roles |
| `a2rs[].id` | String | `"store_113_Class100"` | Unique identifier |
| `a2rs[].actor` | String | `"Sales"` | actor name |
| `a2rs[].actorid` | String | `"store_55_Class681"` | actor id |
| `a2rs[].type` | String | `"Group_Actor"` | type of the class |
| `a2rs[].role` | String | `" Data Subject Organisational Owner "` | role name |
| `version` | String | `"621"` | DO NOT USE |


### core_api_el_planned_elements.xsl
- **Path**: `enterprise/api/core_api_el_planned_elements.xsl`
- **DSA Data Label**: `planActionData`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `applications` | Array | `N/A` | Array of Application instances that are the subject of planned changes |
| `plan_actions` | Array | `N/A` | Array of Planned_Change instances detailing specific transformation actions |
| `id` | String | `N/A` | Unique identifier for the planned element record |
| `strategic_plan` | String | `N/A` | Name/reference of the Strategic_Plan instance governing these changes |
| `strategic_plan_start` | String | `N/A` | ISO 8601 start date for the strategic plan period |
| `strategic_plan_end` | String | `N/A` | ISO 8601 end date for the strategic plan period |
| `change_activity` | String | `N/A` | Name/reference of the Change_Activity (project/initiative) implementing the change |
| `change_activity_start_forecast` | String | `N/A` | ISO 8601 forecasted start date for the change activity |
| `change_activity_start_actual` | String | `N/A` | ISO 8601 actual start date when change activity began |
| `change_activity_end_forecast` | String | `N/A` | ISO 8601 forecasted completion date for the change activity |
| `change_activity_end_actual` | String | `N/A` | ISO 8601 actual completion date when change activity finished |
| `action` | String | `N/A` | Type of planned action (e.g., "Retire", "Replace", "Enhance", "Acquire") |

### core_api_el_plans_prog_proj.xsl
- **Path**: `enterprise/api/core_api_el_plans_prog_proj.xsl`
- **DSA Data Label**: `planDataAPi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `programmes` | Array | `[{"name": "Business Process Rationalisation Programme", "description": "Programme to rationalise the...` | Collection of programmes - coordinated groups of related projects |
| `programmes[].name` | String | `"Business Process Rationalisation Programme"` | Display name |
| `programmes[].description` | String | `"Programme to rationalise the business processes across the business"` | Descriptive text |
| `programmes[].className` | String | `"Programme"` | name of the class used |
| `programmes[].id` | String | `"store_283_Class1932"` | Unique identifier |
| `programmes[].ea_reference` | String | `""` | External reference identifier |
| `programmes[].orgUserIds` | Array | `[]` | Organizations using or sponsoring this programme |
| `programmes[].stakeholders` | Array | `[]` | People and roles involved in the programme |
| `programmes[].milestones` | Array | `[]` | Key milestones or checkpoints in programme delivery |
| `programmes[].proposedStartDate` | String | `"2022-01-01"` | Planned start date for the programme |
| `programmes[].targetEndDate` | String | `"2024-01-01"` | Target completion date for the programme |
| `programmes[].actualStartDate` | String | `"2020-01-01"` | Actual date programme commenced |
| `programmes[].forecastEndDate` | String | `"2020-06-01"` | Current forecast completion date |
| `programmes[].budget` | String | `""` | Allocated budget for the programme |
| `programmes[].approvalStatus` | String | `"Not Set"` | Approval status (e.g., Approved, Pending, Not Set) |
| `programmes[].approvalId` | String | `""` | Identifier of the approval status enumeration |
| `programmes[].plans` | Array | `[]` | Strategic plans supported by this programme |
| `programmes[].projects` | Array | `[{"id": "store_283_Class1902", "priority": "", "ea_reference": "", "name": "Business Process Automat...` | Projects contained within this programme |
| `programmes[].documents` | Array | `[]` | Supporting documents and attachments |
| `programmes[].securityClassifications` | Array | `[]` | Security classification tags |
| `allPlans` | Array | `[{"name": "Application Data Analysis", "description": "", "id": "store_948_Class17", "ea_reference":...` | All strategic plans in the repository |
| `allPlans[].name` | String | `"Application Data Analysis"` | Display name |
| `allPlans[].description` | String | `""` | Descriptive text |
| `allPlans[].id` | String | `"store_948_Class17"` | Unique identifier |
| `allPlans[].ea_reference` | String | `""` | External reference identifier |
| `allPlans[].className` | String | `"Enterprise_Strategic_Plan"` | name of the class used |
| `allPlans[].dependsOn` | Array | `[]` | Dependencies on other plans or elements |
| `allPlans[].validStartDate` | String | `"2023-08-14"` | Date when plan becomes valid/active |
| `allPlans[].validEndDate` | String | `"2023-10-16"` | Date when plan expires or completes |
| `allPlans[].planP2E` | Array | `[]` | Plan-to-Element relationships (impacted EA elements) |
| `allPlans[].objectives` | Array | `[]` | Business objectives this plan supports |
| `allPlans[].drivers` | Array | `[]` | Business drivers motivating this plan |
| `allPlans[].planStatus` | String | `"Future"` | Current status of the plan |
| `allPlans[].projects` | Array | `[]` | Projects delivering this strategic plan |
| `allPlans[].orgUserIds` | Array | `[]` | Organizations impacted by or using this plan |
| `allPlans[].stakeholders` | Array | `[]` | People and roles involved in the plan |
| `allPlans[].documents` | Array | `[]` | Supporting documents and attachments |
| `allPlans[].securityClassifications` | Array | `[]` | Security classification tags |
| `styles` | Array | `[{"id": "essential_prj_CC_v1_4_2_Instance_80015", "colour": "#d3d3d3", "icon": "", "textColour": "#0...` | Visual styling definitions for UI rendering |
| `styles[].id` | String | `"essential_prj_CC_v1_4_2_Instance_80015"` | Unique identifier |
| `styles[].colour` | String | `"#d3d3d3"` | background colour for style |
| `styles[].icon` | String | `""` | Icon identifier or path |
| `styles[].textColour` | String | `"#000000"` | text colour for style |
| `roadmaps` | Array | `[{"name": "Agility and Operational Efficiency", "description": "", "orgUserIds": [], "stakeholders":...` | High-level roadmaps grouping strategic plans by theme |
| `roadmaps[].name` | String | `"Agility and Operational Efficiency"` | Display name |
| `roadmaps[].description` | String | `""` | Descriptive text |
| `roadmaps[].orgUserIds` | Array | `[]` | Organizations impacted by this roadmap |
| `roadmaps[].stakeholders` | Array | `[]` | People and roles involved in the roadmap |
| `roadmaps[].id` | String | `"store_53_Class1231"` | Unique identifier |
| `roadmaps[].ea_reference` | String | `""` | External reference identifier |
| `roadmaps[].strategicPlans` | Array | `["store_53_Class1229"]` | Strategic plans contained in this roadmap |
| `roadmaps[].className` | String | `"Roadmap"` | name of the class used |
| `roadmaps[].securityClassifications` | Array | `[]` | Security classification tags |
| `allProject` | Array | `[{"id": "store_283_Class1902", "priority": "", "ea_reference": "", "name": "Business Process Automat...` | All projects in the repository |
| `allProject[].id` | String | `"store_283_Class1902"` | Unique identifier |
| `allProject[].priority` | String | `""` | Project priority level |
| `allProject[].ea_reference` | String | `""` | External reference identifier |
| `allProject[].name` | String | `"Business Process Automation Project"` | Display name |
| `allProject[].description` | String | `"Look to automate business processes to sace costs"` | Descriptive text |
| `allProject[].orgUserIds` | Array | `[]` | Organizations impacted by or sponsoring this project |
| `allProject[].programme` | String | `"store_283_Class1932"` | Parent programme containing this project |
| `allProject[].visId` | Array | `["store_90_Class44"]` | visibility of the instance based on system lifecycle |
| `allProject[].budget` | Array | `[]` | Budgetary allocations for this project |
| `allProject[].costs` | Array | `[]` | Actual or planned costs for this project |
| `allProject[].strategicPlans` | Array | `[{"id": "store_283_Class1890", "name": "Business Process Automation", "securityClassifications": []}...` | Strategic plans this project delivers |
| `allProject[].stakeholders` | Array | `[{"actorName": "Andy Taylor", "roleName": "Project Sponsor", "type": "ACTOR_TO_ROLE_RELATION", "acto...` | People and their roles in the project |
| `allProject[].milestones` | Array | `[]` | Key milestones or checkpoints in project delivery |
| `allProject[].className` | String | `"Project"` | name of the class used |
| `allProject[].proposedStartDate` | String | `"2020-01-01"` | Planned start date for the project |
| `allProject[].targetEndDate` | String | `"2024-01-01"` | Target completion date for the project |
| `allProject[].actualStartDate` | String | `"2020-03-01"` | Actual date project commenced |
| `allProject[].forecastEndDate` | String | `"2024-06-01"` | Current forecast completion date |
| `allProject[].lifecycleStatus` | String | `"Execution"` | Current project lifecycle phase (e.g., Planning, Execution, Complete) |
| `allProject[].lifecycleStatusID` | String | `"essential_baseline_v2_0_Class30003"` | Identifier of the lifecycle status enumeration |
| `allProject[].lifecycleStatusOrder` | String | `"4"` | Sort order for lifecycle status |
| `allProject[].approvalStatus` | String | `"Approved"` | Project approval status |
| `allProject[].approvalId` | String | `"essential_baseline_v2_0_Class30005"` | Identifier of the approval status enumeration |
| `allProject[].p2e` | Array | `[{"id": "store_283_Class1900", "actionid": "essential_baseline_v3_0_3_Class10000", "impactedElement"...` | Project-to-Element relationships (which EA elements this project changes) |
| `allProject[].documents` | Array | `[]` | Supporting documents and attachments |
| `allProject[].securityClassifications` | Array | `[]` | Security classification tags |
| `currency` | String | `"£"` | Default currency symbol |
| `currencyId` | String | `"essential_baseline_v505_Class16"` | Identifier of the default currency |
| `currencyData` | Array | `[{"id": "essential_baseline_v505_Class15", "exchangeRate": "", "name": "US Dollar", "code": "USD", "...` | All available currencies in the repository |
| `currencyData[].id` | String | `"essential_baseline_v505_Class15"` | Unique identifier |
| `currencyData[].exchangeRate` | String | `""` | Exchange rate to base currency (often unpopulated) |
| `currencyData[].name` | String | `"US Dollar"` | Display name |
| `currencyData[].code` | String | `"USD"` | ISO 4217 currency code |
| `currencyData[].symbol` | String | `"$"` | Currency symbol |
| `currencyData[].default` | String | `""` | Boolean flag indicating if this is the default currency |

### core_api_el_principles.xsl
- **Path**: `enterprise/api/core_api_el_principles.xsl`
- **DSA Data Label**: `N/A`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `principles` | Array | `N/A` | Architecture principles governing EA decisions (Business, Application, Information, Technology, Security) |
| `levels` | Array | `N/A` | Compliance levels or hierarchy levels for assessment |
| `id` | String | `N/A` | Unique identifier |
| `className` | String | `N/A` | Essential metamodel class name (e.g., Business_Principle, Application_Architecture_Principle) |
| `name` | String | `N/A` | Display name of the principle |
| `description` | String | `N/A` | Detailed description of the principle |
| `principle_rationale` | String | `N/A` | Rationale or justification for the principle |
| `information_implications` | String | `N/A` | How this principle impacts information/data architecture |
| `technology_implications` | String | `N/A` | How this principle impacts technology architecture |
| `business_implications` | String | `N/A` | How this principle impacts business operations and capabilities |
| `application_implications` | String | `N/A` | How this principle impacts application architecture |
| `method` | String | `N/A` | Assessment or evaluation method |
| `indent` | Integer | `N/A` | Indentation level for hierarchical display |
| `scores` | Array | `N/A` | Compliance assessment scores or ratings |
| `id2` | String | `N/A` | Secondary or alternate identifier |
| `thislevel` | String | `N/A` | Current level in hierarchy or assessment scale |
| `assessment` | Object | `N/A` | Compliance assessment details for an element against this principle |
| `score` | Number | `N/A` | Numerical compliance score or rating |
| `style` | String | `N/A` | CSS class or style identifier for UI rendering |
| `value` | String/Number | `N/A` | Assessment value or enumeration value |
| `backgroundColour` | String | `N/A` | Background color for visual representation (hex color code) |
| `colour` | String | `N/A` | Foreground/text color for visual representation (hex color code) |

### core_api_el_strat_planner_analysis_data.xsl
- **Path**: `enterprise/api/core_api_el_strat_planner_analysis_data.xsl`
- **DSA Data Label**: `strategy-planner-data`
- **Parameters**: None
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `planningActions` | Array | `[{"id": "essential_prj_CC_v1.4.2_Instance_160169", "name": "Replace", "description": "Strategic plan...` | Planning actions defining intended changes to EA elements (e.g., Replace, Retire, Invest, Rationalize) |
| `planningActions[].id` | String | `"essential_prj_CC_v1.4.2_Instance_160169"` | Unique identifier |
| `planningActions[].name` | String | `"Replace"` | Display name |
| `planningActions[].description` | String | `"Strategic planning actions capturing that an element has been identified as something that will be ...` | Descriptive text |
| `goals` | Array | `[{"id": "store_90_Class130004", "name": "All Employees Briefed on Strategic Goals by 2020", "descrip...` | Business goals (high-level desired outcomes) |
| `goals[].id` | String | `"store_90_Class130004"` | Unique identifier |
| `goals[].name` | String | `"All Employees Briefed on Strategic Goals by 2020"` | Display name |
| `goals[].description` | String | `""` | Descriptive text |
| `goals[].link` | String | `"All Employees Briefed on Strategic Goals by 2020"` | HTML anchor tag for navigation |
| `goals[].objectiveIds` | Array | `[]` | Identifiers of objectives supporting this goal |
| `goals[].objectives` | Array | `[]` | Objectives supporting this goal |
| `goals[].inScope` | Boolean | `false` | Whether this element is included in current view/analysis scope |
| `goals[].isSelected` | Boolean | `false` | Whether this element is currently selected in the UI |
| `objectives` | Array | `[{"id": "store_53_Class90", "name": "Aligning our Employees to our Strategic Goals", "description": ...` | Business objectives (measurable steps toward goals) |
| `objectives[].id` | String | `"store_53_Class90"` | Unique identifier |
| `objectives[].name` | String | `"Aligning our Employees to our Strategic Goals"` | Display name |
| `objectives[].description` | String | `"Ensure employees are clear and working to the strategic goals"` | Descriptive text |
| `objectives[].link` | String | `"<a href = "?XML=reportXML.xml&PMA=store_53_Class90&cl=en-gb" class = " context-menu-busObjGenMenu" ...` | HTML anchor tag for navigation |
| `objectives[].targetDate` | String | `"2020-08-31"` | Target date for achieving this objective |
| `objectives[].goalIds` | Array | `["store_53_Class74"]` | Identifiers of goals this objective supports |
| `objectives[].inScope` | Boolean | `true` | Whether this element is included in current view/analysis scope |
| `valueStreams` | Array | `[{"id": "store_55_Class7101", "name": "Client Advert to Engage", "description": "", "link": "<a href...` | End-to-end collections of activities delivering customer outcomes |
| `valueStreams[].id` | String | `"store_55_Class7101"` | Unique identifier |
| `valueStreams[].name` | String | `"Client Advert to Engage"` | Display name |
| `valueStreams[].description` | String | `""` | Descriptive text |
| `valueStreams[].link` | String | `"<a href = "?XML=reportXML.xml&PMA=store_55_Class7101&cl=en-gb" class = " context-menu-valStreamGenM...` | HTML anchor tag for navigation |
| `valueStreams[].valueStages` | Array | `[{"id": "store_55_Class7121", "name": "Client Advert to Engage: 1. Advert Creation", "index": "1", "...` | Sequential stages within this value stream |
| `valueStreams[].physProcessIds` | Array | `["store_55_Class5360"]` | Physical processes contributing to this value stream |
| `valueStreams[].appProRoleIds` | Array | `["store_55_Class2243"]` | Application provider roles supporting this value stream |
| `valueStreams[].prodTypeIds` | Array | `["store_55_Class7095"]` | Product types delivered by this value stream |
| `valueStreams[].roles` | Array | `[{"id": "store_55_Class7283", "type": "Individual_Business_Role", "name": "Marketer"}]` | Business roles involved in this value stream |
| `valueStreams[].triggerEvents` | Array | `[{"id": "store_316_Class20001", "name": "Business Sales Initiative"}]` | Events that initiate this value stream |
| `valueStreams[].outcomeEvents` | Array | `[{"id": "store_316_Class20003", "name": "Sales Increase"}]` | Events resulting from completion of this value stream |
| `valueStreams[].triggerConditions` | Array | `[{"id": "store_316_Class20000", "name": "Requirement to Increase Brand Recognition & Sales"}]` | Conditions that trigger this value stream |
| `valueStreams[].outcomeConditions` | Array | `[{"id": "store_316_Class20004", "name": "Clients recognise the brand"}]` | Conditions resulting from this value stream |
| `valueStages` | Array | `[{"id": "store_55_Class7121", "name": "Client Advert to Engage: 1. Advert Creation", "index": "1", "...` | Individual activities within value streams contributing to customer outcomes |
| `valueStages[].id` | String | `"store_55_Class7121"` | Unique identifier |
| `valueStages[].name` | String | `"Client Advert to Engage: 1. Advert Creation"` | Display name |
| `valueStages[].index` | String | `"1"` | Sequence order within the value stream |
| `valueStages[].label` | String | `"Advert Creation"` | Short display label |
| `valueStages[].description` | String | `"Creation of the advert and collateral"` | Descriptive text |
| `valueStages[].link` | String | `"Advert Creation"` | HTML anchor tag for navigation |
| `valueStages[].customerJourneyPhaseIds` | Array | `[]` | Customer journey phases aligned with this value stage |
| `valueStages[].customerJourneyPhases` | Array | `[]` | Customer journey phases aligned with this value stage |
| `valueStages[].emotionScore` | Number | `0` | Aggregated customer emotion score for this stage |
| `valueStages[].cxScore` | Number | `0` | Customer experience rating score |
| `valueStages[].kpiScore` | Number | `-1` | Key performance indicator score (-1 indicates no data) |
| `valueStages[].emotionStyleClass` | String | `"mediumHeatmapColour"` | CSS class for emotion heatmap visualization |
| `valueStages[].cxStyleClass` | String | `"mediumHeatmapColour"` | CSS class for customer experience heatmap visualization |
| `valueStages[].kpiStyleClass` | String | `"noHeatmapColour"` | CSS class for KPI heatmap visualization |
| `valueStages[].styleClass` | String | `"mediumHeatmapColour"` | Overall CSS class for heatmap visualization |
| `valueStages[].inScope` | Boolean | `false` | Whether this element is included in current view/analysis scope |
| `valueStages[].valueStream` | Object | `{"name": "Client Advert to Engage", "id": "store_55_Class7101"}` | Parent value stream containing this stage |
| `valueStages[].parentValueStage` | Object | `{"name": "", "id": ""}` | Parent value stage if this is a sub-stage |
| `valueStages[].roles` | Array | `[{"id": "store_55_Class7256", "type": "Business_Role_Type", "name": "Business Division"}]` | Business roles performing this value stage |
| `valueStages[].emotions` | Array | `[{"id": "store_55_Class7149", "relation_description": "", "emotion": "Excited"}]` | Customer emotions experienced during this stage |
| `valueStages[].perfMeasures` | Array | `[{"id": "store_55_Class7187", "uom": "Minutes", "kpiVal": "Time to create - 2000Minutes", "quality":...` | Performance measures for this value stage |
| `valueStages[].entranceEvents` | Array | `[{"id": "store_960_Class1", "type": "Business_Event", "name": "Management Sign-off"}]` | Events triggering entry into this stage |
| `valueStages[].entranceCondition` | Array | `[{"id": "store_316_Class20006", "type": "Business_Condition", "name": "Campaign Budget Approved"}]` | Conditions required to enter this stage |
| `valueStages[].exitCondition` | Array | `[{"id": "store_960_Class2", "type": "Business_Condition", "name": "Advert Produced"}]` | Conditions indicating completion of this stage |
| `valueStages[].exitEvent` | Array | `[{"id": "store_316_Class20007", "type": "Business_Event", "name": "Advert Approved"}]` | Events signaling exit from this stage |
| `customerJourneys` | Array | `[{"id": "store_55_Class7374", "name": "Advert Interaction to Sign-up", "description": "How the clien...` | Customer personas' typical experiences engaging with the enterprise over time |
| `customerJourneys[].id` | String | `"store_55_Class7374"` | Unique identifier |
| `customerJourneys[].name` | String | `"Advert Interaction to Sign-up"` | Display name |
| `customerJourneys[].description` | String | `"How the clients move from an advert to a decision to buy"` | Descriptive text |
| `customerJourneys[].link` | String | `"Advert Interaction to Sign-up"` | HTML anchor tag for navigation |
| `customerJourneyPhases` | Array | `[{"id": "store_55_Class7428", "name": "Advert Interaction to Sign-up: 1. Awareness of Advert", "desc...` | Key touchpoints in customer journeys between customer persona and enterprise |
| `customerJourneyPhases[].id` | String | `"store_55_Class7428"` | Unique identifier |
| `customerJourneyPhases[].name` | String | `"Advert Interaction to Sign-up: 1. Awareness of Advert"` | Display name |
| `customerJourneyPhases[].description` | String | `"Awareness of the products offered"` | Descriptive text |
| `customerJourneyPhases[].link` | String | `"Awareness of Advert"` | HTML anchor tag for navigation |
| `customerJourneyPhases[].customerJourneyId` | String | `"store_55_Class7374"` | Parent customer journey containing this phase |
| `customerJourneyPhases[].cxScore` | Number | `0` | Customer experience rating score |
| `customerJourneyPhases[].emotionScore` | Number | `5.5` | Customer emotion score |
| `customerJourneyPhases[].kpiScore` | Number | `7.5` | Key performance indicator score |
| `busCaps[].ref` | String | `"busCap20"` | Reference code or identifier for this capability |
| `busCaps[].link` | String | `"<a href = "?XML=reportXML.xml&PMA=store_55_Class13&cl=en-gb" class = " context-menu-busCapGenMenu" ...` | HTML anchor tag for navigation |
| `busCaps[].type` | Object | `{"list": "busCaps", "colour": "black", "label": "Business Capability", "defaultButton": "View", "isL...` | Type metadata for UI rendering |
| `busCaps[].goalIds` | Array | `[]` | Business goals supported by this capability |
| `busCaps[].objectiveIds` | Array | `[]` | Business objectives supported by this capability |
| `busCaps[].physProcessIds` | Array | `["store_177_Class3"]` | Physical processes realizing this capability |
| `busCaps[].appProRoleIds` | Array | `["store_53_Class1050"]` | Application provider roles supporting this capability |
| `busCaps[].applicationIds` | Array | `[]` | Applications supporting this capability |
| `busCaps[].customerJourneyIds` | Array | `[]` | Customer journeys using this capability |
| `busCaps[].customerJourneyPhaseIds` | Array | `[]` | Customer journey phases using this capability |
| `busCaps[].valueStreamIds` | Array | `[]` | Value streams using this capability |
| `busCaps[].valueStageIds` | Array | `[]` | Value stages using this capability |
| `busCaps[].overallScores` | Object | `{"cxScore": 0, "cxStyleClass": "noHeatmapColour", "cxStyle": {"label": "Undefined", "icon": "images/...` | Aggregated scores for this element |
| `busCaps[].heatmapScores` | Array | `[{"id": "store_55_Class7099", "cxScore": 0, "cxStyleClass": "noHeatmapColour", "cxStyle": {"label": ...` | Scores for heatmap visualizations by dimension |
| `busCaps[].editorId` | String | `"busCapModal"` | Identifier of the modal editor component for this element type |
| `busCaps[].inScope` | Boolean | `false` | Whether this element is included in current view/analysis scope |
| `bcmData` | Object | `{"l0BusCapName": "Energy", "l0BusCapId": "store_55_Class56", "l0BusCapLink": "<a href = \"?XML=repor...` | Business capability model data structure |
| `busProcesses[].index` | Number | `0` | Array index or sequence order |
| `busProcesses[].type` | Object | `{"list": "busProcesses", "colour": "#5cb85c", "label": "Business Process", "defaultButton": "No Chan...` | Type metadata for UI rendering |
| `busProcesses[].busCapIds` | Array | `["store_55_Class119"]` | Business capabilities realized by this process |
| `busProcesses[].planningActionIds` | Array | `["essential_baseline_v3.0.3_Class10000"]` | Planning actions assigned to this element |
| `busProcesses[].planningActions` | Null | `null` | Populated planning actions (when loaded) |
| `busProcesses[].planningAction` | Null | `null` | Single selected planning action |
| `busProcesses[].planningNotes` | String | `""` | Notes about planned changes |
| `busProcesses[].hasPlan` | Boolean | `false` | Whether this element has assigned planning actions |
| `physProcesses[].busCapId` | String | `"store_55_Class119"` | Business capability this physical process realizes |
| `physProcesses[].busCapLink` | String | `"<a href = "?XML=reportXML.xml&PMA=store_55_Class119&cl=en-gb" class = " context-menu-busCapGenMenu"...` | HTML link to business capability |
| `physProcesses[].busProcessId` | String | `"store_55_Class215"` | Logical business process this physical process implements |
| `physProcesses[].busProcessRef` | String | `"busProc2"` | Reference code for business process |
| `physProcesses[].busProcessDescription` | String | `"Process to "agree" and action the most viable hedging opportunities identified"` | Description of logical business process |
| `physProcesses[].orgName` | String | `"Accounting"` | Organization performing this process |
| `physProcesses[].orgDescription` | String | `"Manage the production of the accounts for the organisation"` | Description of performing organization |
| `physProcesses[].busProcessName` | String | `"Action Hedging"` | Name of logical business process |
| `physProcesses[].busProcessLink` | String | `"<a href = "?XML=reportXML.xml&PMA=store_55_Class215&cl=en-gb" class = " context-menu-busProcessGenM...` | HTML link to business process |
| `physProcesses[].orgId` | String | `"store_55_Class713"` | Organization identifier |
| `physProcesses[].orgRef` | String | `"org15"` | Reference code for organization |
| `physProcesses[].orgLink` | String | `"<a href = "?XML=reportXML.xml&PMA=store_55_Class713&cl=en-gb" class = " context-menu-grpActorGenMen...` | HTML link to organization |
| `physProcesses[].emotionIcon` | String | `"fa-smile-o"` | Font Awesome icon class for emotion visualization |
| `organisations[].type` | Object | `{"list": "organisations", "colour": "#9467bd", "label": "Organisation", "defaultButton": "No Change"...` | Type metadata for UI rendering |
| `appServices[].techHealthScore` | Number | `31` | Technology health assessment score (0-100) |
| `appServices[].techHealthStyle` | String | `"neutralHeatmapColour"` | CSS class for technology health visualization |
| `applications[].objectives` | Null | `null` | Business objectives supported by this application (when loaded) |
| `applications[].appProRoles` | Null | `null` | Application provider roles for this application (when loaded) |
| `applications[].physProcesses` | Null | `null` | Physical processes using this application (when loaded) |
| `applications[].organisations` | Null | `null` | Organizations using this application (when loaded) |
| `applications[].valueStreams` | Null | `null` | Value streams using this application (when loaded) |
| `appProviderRoles[].appId` | String | `"store_55_Class1161"` | Application identifier |
| `appProviderRoles[].appRef` | String | `"app2"` | Application reference code |
| `appProviderRoles[].serviceName` | String | `"Benchmarking"` | Application service name |
| `appProviderRoles[].serviceDescription` | String | `"Benchmarks energy performance against market"` | Application service description |
| `appProviderRoles[].appName` | String | `"ADEXCell Energy Manager"` | Application name |
| `appProviderRoles[].appDescription` | String | `"Real time energy consumption monitoring of facilities"` | Application description |
| `appProviderRoles[].appLink` | String | `"<a href = "?XML=reportXML.xml&PMA=store_55_Class1161&cl=en-gb" class = " context-menu-appProviderGe...` | HTML link to application |
| `appProviderRoles[].serviceId` | String | `"store_55_Class910"` | Application service identifier |
| `appProviderRoles[].serviceRef` | String | `"appService82"` | Application service reference code |
| `appProviderRoles[].serviceLink` | String | `"<a href = "?XML=reportXML.xml&PMA=store_55_Class910&cl=en-gb" class = " context-menu-appSvcGenMenu"...` | HTML link to service |
| `unitsofMeasure[].enumeration_sequence_number` | String | `""` | Sort order in enumeration list |
| `unitsofMeasure[].class` | String | `""` | CSS class for styling |
| `unitsofMeasure[].enumeration_value` | String | `"GBP"` | Standard enumeration value (e.g., currency code) |
| `unitsofMeasure[].enumeration_score` | String | `""` | Numeric score for this enumeration value |
| `customerEmotions[].enumeration_sequence_number` | String | `"1"` | Sort order in enumeration list |
| `customerEmotions[].class` | String | `"boredEmotion"` | CSS class for styling this emotion |
| `customerEmotions[].enumeration_value` | String | `"Bored"` | Standard enumeration value |
| `customerEmotions[].enumeration_score` | String | `"8"` | Numeric score for this emotion (e.g., sentiment polarity) |
| `custEx[].label` | String | `"Average Experience"` | Short display label |
| `custEx[].seqNo` | String | `"3"` | Sequence number for ordering |
| `custEx[].score` | String | `"0"` | Numeric score for this experience rating |
| `custEx[].synonyms` | Array | `[]` | Alternate names or synonyms for this value |
| `custEmotions[].label` | String | `"Excited"` | Short display label |
| `custEmotions[].seqNo` | String | `"6"` | Sequence number for ordering |
| `custEmotions[].score` | String | `"8"` | Numeric score for this emotion |
| `custEmotions[].synonyms` | Array | `[]` | Alternate names or synonyms for this emotion |
| `custServiceQualVal[].score` | String | `"5"` | Numeric score for this service quality value |
| `custServiceQualVal[].value` | String | `"Medium"` | Display value (e.g., Low, Medium, High) |
| `custServiceQualVal[].classStyle` | String | `"backColourOrange"` | CSS class for visualization styling |
| `custJourney[].products` | Array | `[{"id": "store_55_Class7340", "name": "Consumer Solar"}]` | Products associated with this customer journey |
| `custJourneyPhase[].cjp_customer_journey` | String | `"Prospect to Client"` | Parent customer journey name |
| `custJourneyPhase[].cjp_experience_rating` | String | `"Average Experience"` | Customer experience rating for this phase |
| `custJourneyPhase[].emotions` | Array | `[{"id": "store_55_Class7135", "name": "Excited", "description": ""}]` | Customer emotions in this phase |
| `custJourneyPhase[].physProcs` | Array | `[{"id": "store_55_Class5534", "name": "Marketing performing Initiate Advertising"}]` | Physical processes supporting this journey phase |
| `custJourneyPhase[].bsqvs` | Array | `[{"id": "store_55_Class7513", "name": "Customer Service Empathy - Medium"}]` | Business service quality values for this phase |

### core_api_el_strat_trends_and_impls.xsl
- **Path**: `enterprise/api/core_api_el_strat_trends_and_impls.xsl`
- **DSA Data Label**: `N/A`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `strategicTrends` | Array | `N/A` | Array of Strategic_Trend instances representing market/industry trends affecting the enterprise |
| `implCategories` | Array | `N/A` | Array of Strategic_Trend_Implication_Category enumeration instances (e.g., Technology, Market, Regulatory) |
| `implLifecycleStatii` | Array | `N/A` | Array of Strategic_Trend_Implication_Lifecycle_Status enumeration instances (e.g., Emerging, Active, Declining) |
| `id` | String | `N/A` | Unique identifier for the strategic trend or implication instance |
| `name` | String | `N/A` | Display name of the strategic trend |
| `link` | String | `N/A` | Hyperlink to the trend's detail page in Essential viewer |
| `description` | String | `N/A` | Multi-language description of the strategic trend and its potential impacts |
| `confidencePercent` | Number | `N/A` | Percentage (0-100) indicating confidence level in the trend's materialization (from `strategic_trend_confidence_percent` slot) |
| `earliestImpactDate` | String | `N/A` | ISO 8601 date indicating when trend impacts are expected to begin (from `strategic_trend_from_year_iso8601` slot) |
| `implications` | Array | `N/A` | Array of Strategic_Trend_Implication instances detailing specific consequences of the trend |
| `categoryId` | String | `N/A` | Reference ID to the Strategic_Trend_Implication_Category for this implication |
| `categoryScore` | Number | `N/A` | Enumeration score from the implication category (severity/importance weighting) |
| `probability` | Number | `N/A` | Percentage (0-100) likelihood of implication occurring (from `sti_probability_percent` slot) |
| `priority` | Number | `N/A` | Numeric priority score for addressing this implication (from `sti_priority_score` slot) |
| `geoScope` | Array | `N/A` | Array of Geographic_Region identifiers indicating where the implication applies |
| `busEnvFactorImpacts` | Array | `N/A` | Array of impacts to Business_Environment_Factor instances (PESTLE factors) with change percentages |
| `costTypeImpacts` | Array | `N/A` | Array of impacts to Cost_Component_Type instances showing expected cost changes (increase/decrease %) |
| `revTypeImpacts` | Array | `N/A` | Array of impacts to Revenue_Component_Type instances showing expected revenue changes (%) |
| `svcQualityImpacts` | Array | `N/A` | Array of impacts to Service_Quality instances (e.g., Availability, Performance) with change scores |
| `productConceptImpacts` | Array | `N/A` | Array of impacts to Product_Concept instances (product portfolio affected by trend) |
| `externalRoleImpacts` | Array | `N/A` | Array of impacts to Group_Business_Role instances (external stakeholders/customers affected) |
| `busCapImpacts` | Array | `N/A` | Array of impacts to Business_Capability instances indicating which capabilities are affected |
| `appCapImpacts` | Array | `N/A` | Array of impacts to Application_Capability instances requiring application changes |
| `techCapImpacts` | Array | `N/A` | Array of impacts to Technology_Capability instances requiring technology changes |
| `stratPlanImpactIds` | Array | `N/A` | Array of Strategic_Plan instance IDs that address this implication via PLAN_TO_ELEMENT_RELATION |
| `change` | Number | `N/A` | Percentage value indicating magnitude of expected change (from `change_percentage` slot on impact relations) |
| `label` | String | `N/A` | Short label text for implication (from `sti_label` slot) |
| `score` | Number | `N/A` | Enumeration score for lifecycle status or category (from `enumeration_score` slot) |

### core_api_el_strategic_driver_goal_objectives.xsl
- **Path**: `enterprise/api/core_api_el_strategic_driver_goal_objectives.xsl`
- **DSA Data Label**: `strategyData`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `drivers` | Array | `[{"id": "store_90_Class130001", "type": "Business_Driver", "name": "Customer Retention", "descriptio...` | Array of Business_Driver instances representing external forces or internal motivations driving strategic change |
| `drivers[].id` | String | `"store_90_Class130001"` | Unique identifier for the business driver instance |
| `drivers[].type` | String | `"Business_Driver"` | Metamodel class type (always "Business_Driver") |
| `drivers[].name` | String | `"Customer Retention"` | Display name of the business driver |
| `drivers[].description` | String | `""` | Multi-language description explaining the driver's context and importance |
| `drivers[].goals` | Array | `[{"id": "store_53_Class66", "name": "Improve Customer Satisfaction", "description": "", "type": "Bus...` | Array of Business_Goal instances that this driver motivates (from `bd_motivates_bus_goal` slot) |
| `drivers[].motivatingObjectives` | Array | `[]` | Array of Business_Objective instance IDs directly motivated by this driver (from `bd_motivates_bus_objective` slot) |
| `objectives` | Array | `[{"id": "store_53_Class90", "name": "Aligning our Employees to our Strategic Goals", "description": ...` | Array of Business_Objective instances representing measurable targets for achieving strategic goals |
| `objectives[].id` | String | `"store_53_Class90"` | Unique identifier for the business objective instance |
| `objectives[].name` | String | `"Aligning our Employees to our Strategic Goals"` | Display name of the business objective |
| `objectives[].description` | String | `"Ensure employees are clear and working to the strategic goals"` | Detailed description of the objective and success criteria |
| `objectives[].type` | String | `"Business_Objective"` | Metamodel class type (always "Business_Objective") |
| `objectives[].targetDate` | String | `"2020-08-31"` | ISO 8601 target completion date for achieving the objective (from `bo_target_date_iso_8601` slot) |
| `objectives[].boDriverMotivated` | Array | `["store_90_Class130000"]` | Array of Business_Driver instance IDs that motivate this objective (inverse of `bd_motivates_bus_objective`) |
| `objectives[].supportingCapabilities` | Array | `["store_55_Class87"]` | Array of Business_Capability instance IDs required to deliver this objective (from `bo_supported_by_business_capability` slot) |

### core_api_el_supplier_impact.xsl
- **Path**: `enterprise/api/core_api_el_supplier_impact.xsl`
- **DSA Data Label**: `suppImpApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `suppliers` | Array | `[{"id": "essential_prj_AA_v1_1_graphArchTest_Instance_20", "repoId": "essential_prj_AA_v1.1_graphArc...` | Array of Supplier instances providing products/services to the organization |
| `suppliers[].id` | String | `"essential_prj_AA_v1_1_graphArchTest_Instance_20"` | Unique identifier for the supplier instance |
| `suppliers[].repoId` | String | `"essential_prj_AA_v1.1_graphArchTest_Instance_20"` | Repository identifier used for menu links and cross-references |
| `suppliers[].name` | String | `"Oracle Corporation"` | Display name of the supplier organization |
| `suppliers[].supplier_url` | String | `"http://www.oracle.com"` | URL to the supplier's website (from `external_repository_instance_reference` slot) |
| `suppliers[].description` | String | `"Oracle Corporation"` | Multi-language description of the supplier |
| `suppliers[].supplierRelStatus` | String | `""` | Supplier relationship status indicating the current state of the business relationship |
| `suppliers[].technologies` | Array | `[]` | Array of Technology_Product instances provided by this supplier |
| `suppliers[].apps` | Array | `[]` | Array of Application_Provider instances supplied by this vendor |
| `suppliers[].visId` | Array | `[""]` | Visibility array based on system lifecycle status for UI filtering |
| `suppliers[].licences` | Array | `[]` | Array of Software License instances associated with this supplier |
| `suppliers[].contracts` | Array | `[]` | Array of Contract instance IDs for agreements with this supplier |
| `suppliers[].techlicences` | Array | `[]` | Array of Technology_Product_License instances provided by this supplier |
| `suppliers[].className` | String | `"Supplier"` | Metamodel class type (always "Supplier") |
| `suppliers[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `capabilities` | Array | `[{"id": "store_55_Class103", "repoId": "store_55_Class103", "name": "Risk Management", "className": ...` | Array of Business_Capability instances potentially impacted by supplier relationships |
| `capabilities[].id` | String | `"store_55_Class103"` | Unique identifier for the business capability instance |
| `capabilities[].repoId` | String | `"store_55_Class103"` | Repository identifier for cross-references |
| `capabilities[].name` | String | `"Risk Management"` | Display name of the business capability |
| `capabilities[].className` | String | `"Business_Capability"` | Metamodel class type (always "Business_Capability") |
| `capabilities[].subCaps` | Array | `[{"id": "store_55_Class105", "className": "Business_Capability", "repoId": "store_55_Class105", "nam...` | Array of child Business_Capability instances in the capability hierarchy |
| `capabilities[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `contracts` | Array | `[{"id": "store_283_Class2244", "repoId": "store_283_Class2244", "contract_ref": "CTR1 - Checkpoint -...` | Array of Contract instances governing supplier relationships |
| `contracts[].id` | String | `"store_283_Class2244"` | Unique identifier for the contract instance |
| `contracts[].repoId` | String | `"store_283_Class2244"` | Repository identifier for cross-references |
| `contracts[].contract_ref` | String | `"CTR1 - Checkpoint - Statement of Work - 2020-02-28"` | Contract reference number or identifier |
| `contracts[].contract_type` | String | `"Statement of Work"` | Type of contract (e.g., SoW, Master Agreement, Purchase Order) |
| `contracts[].contract_customer` | String | `"Distribution"` | Internal organization or business unit that is the customer for this contract |
| `contracts[].name` | String | `"CTR1 - Checkpoint - Statement of Work - 2020-02-28"` | Display name of the contract |
| `contracts[].owner` | String | `"Distribution"` | Internal owner/responsible party for managing this contract |
| `contracts[].signature_date` | String | `"2020-02-28"` | ISO 8601 date when the contract was signed |
| `contracts[].description` | String | `"Blah"` | Multi-language description of the contract scope and terms |
| `contracts[].supplier_name` | String | `"Checkpoint"` | Name of the supplier party to the contract |
| `contracts[].contract_end_date` | String | `""` | ISO 8601 date when the contract expires or terminates |
| `contracts[].supplierId` | String | `"store_55_Class3001"` | Unique identifier of the Supplier instance for this contract |
| `contracts[].relStatusId` | String | `""` | Identifier for the relationship status enumeration |
| `contracts[].startDate` | String | `"2020-02-28"` | ISO 8601 contract start/effective date |
| `contracts[].renewalDate` | Null | `null` | ISO 8601 date for next contract renewal decision point |
| `contracts[].renewalNoticeDays` | Number | `0` | Number of days advance notice required for renewal/non-renewal |
| `contracts[].renewalReviewDays` | Number | `0` | Number of days before renewal to begin internal review process |
| `contracts[].renewalModel` | String | `"Auto-renew"` | Contract renewal model (e.g., Auto-renew, Opt-in, Fixed term) |
| `contracts[].type` | String | `"Statement of Work"` | Contract type classification |
| `contracts[].docLinks` | Array | `[{"label": "Contract Link for CTR1 - Checkpoint - Statement of Work - 2020-02-28", "url": "www.enter...` | Array of document links to contract files and related documentation |
| `contracts[].contractComps` | Array | `[{"id": "store_283_Class2250", "repoid": "store_283_Class2250", "contractId": "store_283_Class2244",...` | Array of Contract_Component instances detailing specific contract line items |
| `contracts[].contractCompIds` | Array | `["store_283_Class2250"]` | Array of Contract_Component instance IDs for quick reference |
| `contracts[].busProcIds` | Array | `["store_53_Class1062"]` | Array of Business_Process instance IDs covered by this contract |
| `contracts[].appIds` | Array | `["store_53_Class1062"]` | Array of Application_Provider instance IDs covered by this contract |
| `contracts[].techProdIds` | Array | `["store_53_Class1062"]` | Array of Technology_Product instance IDs covered by this contract |
| `contracts[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `contract_components` | Array | `[{"id": "store_283_Class2250", "debug": "essential_baseline_v505_Class16", "ccr_end_date_ISO8601": "...` | Array of Contract_Component instances representing individual line items within contracts |
| `contract_components[].id` | String | `"store_283_Class2250"` | Unique identifier for the contract component instance |
| `contract_components[].debug` | String | `"essential_baseline_v505_Class16"` | Debug/trace identifier for development purposes |
| `contract_components[].ccr_end_date_ISO8601` | String | `"2021-02-28"` | ISO 8601 end date for this contract component (from `ccr_end_date_ISO8601` slot) |
| `contract_components[].ccr_total_annual_cost` | String | `"10000.0"` | Total annual cost for this contract component |
| `contract_components[].ccr_renewal_notice_days` | String | `"60"` | Days of advance notice required for renewal of this component |
| `contract_components[].name` | String | `""` | Display name of the contract component |
| `contract_components[].ccr_contracted_units` | String | `"1"` | Number of units contracted (licenses, seats, instances) |
| `contract_components[].ccr_contract_unit_of_measure` | String | `"Enteprise"` | Unit of measure for contracted quantities (e.g., Enterprise, Per Seat, Per Device) |
| `contract_components[].ccr_renewal_model` | String | `"Auto-renew"` | Renewal model for this specific contract component |
| `contract_components[].contract_component_from_contract` | String | `"CTR1 - Checkpoint - Statement of Work - 2020-02-28"` | Name of the parent Contract instance |
| `contract_components[].ccr_start_date_ISO8601` | String | `""` | ISO 8601 start date for this contract component |
| `contract_components[].ccr_currency` | String | `"British Pound"` | Currency for cost values (e.g., British Pound, USD, EUR) |
| `contract_components[].busElements` | Array | `[]` | Array of business layer elements (Business_Process, Business_Capability) covered by this component |
| `contract_components[].appElements` | Array | `[]` | Array of Application_Provider instances covered by this contract component |
| `contract_components[].techElements` | Array | `[{"id": "store_53_Class1062", "name": "Endpoint Security"}]` | Array of Technology_Product instances covered by this contract component |
| `contract_components[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `enums` | Array | `[{"id": "store_90_Class40030", "type": "Contract_Renewal_Model", "styleClass": "", "name": "Auto-ren...` | Array of enumeration instances for contract-related classifications |
| `enums[].id` | String | `"store_90_Class40030"` | Unique identifier for the enumeration instance |
| `enums[].type` | String | `"Contract_Renewal_Model"` | Metamodel class type of the enumeration (e.g., Contract_Renewal_Model, Contract_Type) |
| `enums[].styleClass` | String | `""` | CSS style class for UI rendering |
| `enums[].name` | String | `"Auto-renew"` | Display name of the enumeration value |
| `enums[].label` | String | `"Auto-renew"` | Display label for the enumeration |
| `enums[].textColour` | String | `""` | Hex color code for text rendering |
| `enums[].backgroundColour` | String | `""` | Hex color code for background rendering |
| `enums[].enumeration_score` | String | `""` | Numeric score for sorting/weighting enumeration values |
| `enums[].description` | String | `""` | Multi-language description of the enumeration value |
| `enums[].sequence_no` | String | `"1"` | Display sequence number for ordering enumeration values |
| `plans` | Array | `[{"id": "store_283_Class1890", "repoId": "store_283_Class1890", "name": "Business Process Automation...` | Array of Strategic_Plan instances that may impact supplier relationships |
| `plans[].id` | String | `"store_283_Class1890"` | Unique identifier for the strategic plan instance |
| `plans[].repoId` | String | `"store_283_Class1890"` | Repository identifier for cross-references |
| `plans[].name` | String | `"Business Process Automation"` | Display name of the strategic plan |
| `plans[].fromDate` | String | `"2022-01-01"` | ISO 8601 start date for the strategic plan period |
| `plans[].endDate` | String | `"2030-06-01"` | ISO 8601 end date for the strategic plan period |
| `plans[].impacts` | Array | `[{"id": "store_283_Class1900", "impacted_element": "store_55_Class239", "repoId": "store_283_Class19...` | Array of plan impact instances showing which elements are affected by this strategic plan |
| `plans[].objectives` | Array | `[{"id": "store_53_Class118", "repoId": "store_53_Class118", "name": "Provide an Efficient Operationa...` | Array of Business_Objective instances supporting this strategic plan |

### core_api_el_support_perf_measures.xsl
- **Path**: `enterprise/api/core_api_el_support_perf_measures.xsl`
- **DSA Data Label**: `support-kpi-data`
- **Parameters**: None
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `projects` | Array | `[]` | Array of Project instances with associated performance measures and KPIs |
| `suppliers` | Array | `[{"id": "essential_prj_AA_v1_4_Instance_98", "name": "Microsoft", "instance": "Microsoft", "security...` | Array of Supplier instances with performance measurement data |
| `suppliers[].id` | String | `"essential_prj_AA_v1_4_Instance_98"` | Unique identifier for the supplier instance |
| `suppliers[].name` | String | `"Microsoft"` | Display name of the supplier |
| `suppliers[].instance` | String | `"Microsoft"` | Instance name/reference for the supplier |
| `suppliers[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `suppliers[].perfMeasures` | Array | `[{"categoryid": "", "id": "store_911_Class10020", "date": "", "createdDate": "2023-12-08T12:46:56.24...` | Array of Performance_Measure instances recording KPI values for this supplier |
| `perfCategory` | Array | `[{"id": "store_911_Class10018", "name": "ESG Ratings", "classes": ["Supplier"], "qualities": ["store...` | Array of Performance_Measure_Category instances grouping related KPIs |
| `perfCategory[].id` | String | `"store_911_Class10018"` | Unique identifier for the performance measure category |
| `perfCategory[].name` | String | `"ESG Ratings"` | Display name of the performance measure category (e.g., ESG Ratings, Financial Performance, Service Quality) |
| `perfCategory[].classes` | Array | `["Supplier"]` | Array of metamodel class names this category applies to (e.g., Supplier, Project, Application_Provider) |
| `perfCategory[].qualities` | Array | `["store_736_Class8"]` | Array of Service_Quality instance IDs defining the measurable qualities in this category |
| `serviceQualities` | Array | `[{"id": "store_736_Class8", "shortName": "ESG Rating", "name": "ESG Rating", "sqvs": [{"id": "store_...` | Array of Service_Quality instances defining measurable attributes and their valid values |
| `serviceQualities[].id` | String | `"store_736_Class8"` | Unique identifier for the service quality instance |
| `serviceQualities[].shortName` | String | `"ESG Rating"` | Short/abbreviated name for the service quality metric |
| `serviceQualities[].name` | String | `"ESG Rating"` | Full display name of the service quality metric |
| `serviceQualities[].sqvs` | Array | `[{"id": "store_736_Class108", "name": "ESG Rating - Good", "score": "1", "value": "Good", "elementCo...` | Array of Service_Quality_Value instances representing valid values/ratings for this quality (e.g., Good, Fair, Poor) |


### core_api_issues.xsl
- **Path**: `enterprise/api/core_api_issues.xsl`
- **DSA Data Label**: `coreIssue`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `issues` | Array | `N/A` | Array of Issue instances representing problems, defects, or requirements |
| `issue_categories` | Array | `N/A` | Array of Issue_Category enumeration instances for classifying issues (e.g., Performance, Security, Availability) |
| `requirement_status_list` | Array | `N/A` | Array of Requirement_Status enumeration instances (e.g., Open, In Progress, Resolved, Closed) |
| `sr_lifecycle_status_list` | Array | `N/A` | Array of Strategic_Requirement_Lifecycle_Status enumeration instances tracking requirement maturity |
| `version` | String | `N/A` | Version identifier for the issue or requirement instance |
| `id` | String | `N/A` | Unique identifier for the issue/requirement instance |
| `name` | String | `N/A` | Display name/title of the issue or requirement |
| `description` | String | `N/A` | Multi-language detailed description of the issue, its context, and impact |
| `enumeration_value` | String | `N/A` | Numeric or text value for enumeration instances (used for sorting/scoring) |
| `method` | String | `N/A` | Resolution method or approach for addressing the issue |
| `indent` | Number | `N/A` | Hierarchy indent level for displaying nested requirements or issues |
| `sequence_number` | String | `N/A` | Display sequence number for ordering issues within a category |
| `synonyms` | Array | `N/A` | Array of alternative names or synonyms for the issue/requirement |
| `sr_required_from_date_ISO8601` | String | `N/A` | ISO 8601 date when the requirement becomes active or issue was first observed |
| `sr_required_by_date_ISO8601` | String | `N/A` | ISO 8601 target date for requirement implementation or issue resolution |
| `sr_root_causes` | Array | `N/A` | Array of root cause analysis elements identifying underlying reasons for the issue |
| `short_name` | String | `N/A` | Abbreviated name or reference code for the issue/requirement |
| `className` | String | `N/A` | Metamodel class type (e.g., "Issue", "Strategic_Requirement") |
| `sr_type` | String | `N/A` | System requirement type classification (e.g., Functional, Non-Functional, Business Rule) |
| `sr_geo_scope` | Array | `N/A` | Array of Geographic_Region instances indicating where the requirement/issue applies |
| `sr_lifecycle_status` | String | `N/A` | Current lifecycle status name for the system requirement |
| `sr_life_id` | Array | `N/A` | Array of Strategic_Requirement_Lifecycle_Status instance IDs |
| `system_last_modified_datetime_iso8601` | String | `N/A` | ISO 8601 timestamp of last modification to this instance |
| `valueClass` | String | `N/A` |  class name|
| `issue_source` | String | `N/A` | Source or origin of the issue (e.g., Incident Report, Audit Finding, User Feedback) |
| `requirement_status_id` | String | `N/A` | Unique identifier of the Requirement_Status enumeration instance |
| `orgScopes` | Array | `N/A` | Array of Group_Actor instances indicating which organizational units are affected |
| `issue_priority` | String | `N/A` | Priority level for addressing the issue (e.g., Critical, High, Medium, Low) |
| `external_reference_links` | Array | `N/A` | Array of external reference objects with labels and URLs to related documentation |
| `external_reference_url` | String | `N/A` | URL to external system (e.g., JIRA, ServiceNow) tracking this issue |
| `issue_impacts` | Array | `N/A` | Array of impact assessment instances describing consequences of the issue on capabilities, services, or applications |
| `visId` | Array | `N/A` | Visibility array based on system lifecycle status for UI filtering |
| `sA2R` | Array | `N/A` | Array of Stakeholder_to_Role instances identifying who is responsible for addressing the issue |
| `shortname` | String | `N/A` | Short reference name for the issue or requirement |
| `colour` | String | `N/A` | Hex color code for background rendering of status/priority indicators |
| `colourText` | String | `N/A` | Hex color code for text rendering on colored backgrounds |

## Information

### core_api_data_object_data.xsl
- **Path**: `information/api/core_api_data_object_data.xsl`
- **DSA Data Label**: `N/A`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `busProcs` | Array | `N/A` | Array of Business_Process instances that create, read, update, or delete data objects |
| `physProcs` | Array | `N/A` | Array of Physical_Process instances (process implementations) that handle data objects |
| `appProToProcess` | Array | `N/A` | Array of APP_PRO_TO_PHYS_BUS_RELATION instances linking applications to physical processes for data flow analysis |
| `regulations` | Array | `N/A` | Array of Regulation instances (e.g., GDPR, HIPAA) governing data object handling and retention |
| `version` | String | `N/A` | Version identifier for API  IGNORE |
| `id` | String | `N/A` | Unique identifier for the data object instance |
| `name` | String | `N/A` | Display name of the data object (e.g., "Customer Record", "Invoice", "Product Catalog") |
| `elements` | Array | `N/A` | Array of Data_Subject (attribute/field) instances composing the data object structure |
| `physProcesses` | Array | `N/A` | Array of Physical_Process instances that implement business processes handling this data object |
| `actor` | String | `N/A` | Name of the Group_Actor (organizational unit or role) responsible for or using this data object |
| `actorid` | String | `N/A` | Unique identifier of the Group_Actor instance |
| `usages` | Array | `N/A` | Array of data usage instances describing CRUD operations (Create, Read, Update, Delete) on this data object |
| `appInfoRep` | String | `N/A` | Name of the Application_Provider that stores/manages information representations of this data object |
| `app_info_rep` | String | `N/A` | Identifier or name for the Information_Representation (database table, file, API) storing this data object |
| `processes` | Array | `N/A` | Array of Business_Process instances that interact with this data object |
| `physicalProcesses` | Array | `N/A` | Array of Physical_Process instances implementing data handling operations for this data object |

### core_api_information_data_mart.xsl
- **Path**: `information/api/core_api_information_data_mart.xsl`
- **DSA Data Label**: `infoMartAPI`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `data_subjects` | Array | `[{"id": "store_113_Class13", "indivOwner": "", "name": "Customer", "description": "Someone who buys ...` | Array of Data_Subject instances representing business entities or concepts (e.g., Customer, Product, Employee) |
| `data_subjects[].id` | String | `"store_113_Class13"` | Unique identifier for the data subject instance |
| `data_subjects[].indivOwner` | String | `""` | Name of Individual_Actor who owns/is accountable for this data subject |
| `data_subjects[].name` | String | `"Customer"` | Display name of the data subject |
| `data_subjects[].description` | String | `"Someone who buys services from the organisation"` | Multi-language business definition of the data subject |
| `data_subjects[].synonyms` | Array | `[]` | Array of alternative names or business terms for this data subject |
| `data_subjects[].dataObjects` | Array | `[{"id": "store_113_Class19", "name": "Customer Address", "securityClassifications": []}]` | Array of Data_Object instances that are subtypes or detailed views of this data subject |
| `data_subjects[].category` | String | `"Master Data"` | Data classification category (e.g., Master Data, Transactional Data, Reference Data) |
| `data_subjects[].orgOwner` | String | `""` | Name of Group_Actor (organizational unit) responsible for managing this data subject |
| `data_subjects[].stakeholders` | Array | `[{"type": "Group_Actor", "actorName": "Sales", "roleName": " Data Subject Organisational Owner ", "a...` | Array of stakeholder relationships showing actors and their roles regarding this data subject |
| `data_subjects[].externalDocs` | Array | `[]` | Array of external document links to glossaries, policies, or data dictionaries |
| `data_subjects[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `data_objects` | Array | `[{"id": "store_113_Class19", "name": "Customer Address", "description": "The address of the customer...` | Array of Data_Object instances representing specific data entities with attributes |
| `data_objects[].id` | String | `"store_113_Class19"` | Unique identifier for the data object instance |
| `data_objects[].name` | String | `"Customer Address"` | Display name of the data object |
| `data_objects[].description` | String | `"The address of the customer"` | Detailed business definition of the data object |
| `data_objects[].debug` | String | `""` | Debug information or internal notes |
| `data_objects[].synonyms` | Array | `[]` | Array of alternative names or business terms for this data object |
| `data_objects[].category` | String | `"Master Data"` | Data classification category |
| `data_objects[].isAbstract` | String | `"false"` | Boolean string indicating if this is an abstract data object (template) or concrete implementation |
| `data_objects[].orgOwner` | String | `""` | Name of Group_Actor responsible for this data object |
| `data_objects[].indivOwner` | String | `""` | Name of Individual_Actor accountable for this data object |
| `data_objects[].dataAttributes` | Array | `[{"name": "Customer Address - Street Number", "description": "", "id": "store_121_Class10000", "type...` | Array of Data_Object_Attribute instances defining the structure/fields of this data object |
| `data_objects[].requiredByApps` | Array | `[]` | Array of Application_Provider instances that require this data object |
| `data_objects[].systemOfRecord` | Array | `[{"id": "store_55_Class1161", "name": "ADEXCell Energy Manager"}]` | Array of Application_Provider instances designated as authoritative source for this data |
| `data_objects[].infoRepsToApps` | Array | `[{"id": "store_174_Class10231", "persisted": "false", "datarepsimplemented": [], "appid": "store_55_...` | Array of APP_PRO_TO_INFOREP_FROM_INFOREP relationships linking applications to information representations |
| `data_objects[].infoReps` | Array | `[{"id": "store_265_Class168", "name": "Entronix Meter Reading Database"}]` | Array of Information_Representation instances (databases, files) storing this data object |
| `data_objects[].infoViews` | Array | `[{"id": "store_113_Class79", "name": "Meter Reading"}]` | Array of Information_View instances grouping related data objects for specific use cases |
| `data_objects[].dataReps` | Array | `[{"id": "store_265_Class166", "name": "Entronix Meter Reading Database - Entronix Meter Reading Cust...` | Array of Data_Representation instances (tables, schemas) physically implementing this data object |
| `data_objects[].stakeholders` | Array | `[{"type": "Individual_Actor", "actorName": "Martin Thompson", "roleName": "Data Steward", "actorId":...` | Array of stakeholder relationships including data stewards, owners, and consumers |
| `data_objects[].classifications` | Array | `[]` | Array of data classification tags (e.g., PII, confidential, public) |
| `data_objects[].tables` | Array | `[{"name": "", "dataRep": "Entronix Meter Reading Database - Entronix Meter Reading Customer Table", ...` | Array of database table implementations for this data object |
| `data_objects[].externalDocs` | Array | `[]` | Array of external document links to specifications, policies, or standards |
| `data_objects[].parents` | Array | `[{"name": "Customer", "securityClassifications": []}]` | Array of parent Data_Subject instances in the data taxonomy hierarchy |
| `data_objects[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `data_representation` | Array | `[{"id": "store_121_Class20000", "name": "Customer Contract Table", "description": "", "synonyms": []...` | Array of Data_Representation instances representing physical database tables or file structures |
| `data_representation[].id` | String | `"store_121_Class20000"` | Unique identifier for the data representation instance |
| `data_representation[].name` | String | `"Customer Contract Table"` | Display name of the data representation (table/file name) |
| `data_representation[].description` | String | `""` | Technical description of the data representation |
| `data_representation[].synonyms` | Array | `[]` | Array of alternative technical names for this data representation |
| `data_representation[].tables` | Array | `[{"name": "", "id": "store_121_Class20003", "create": "Yes", "read": "Unknown", "update": "Unknown",...` | Array of related table instances with CRUD operation indicators |
| `data_representation[].apps` | Array | `[{"name": "", "id": "store_55_Class1161", "create": "Unknown", "read": "Unknown", "update": "Unknown...` | Array of Application_Provider instances that access this data representation with CRUD permissions |
| `data_representation[].technicalName` | String | `"Customer Contract Table"` | Technical/physical name as it appears in the database or file system |
| `information_representation` | Array | `[{"id": "store_121_Class20001", "representation_label": "", "ea_reference": "", "name": "Customer Da...` | Array of Information_Representation instances representing logical data stores (databases, file systems, APIs) |
| `information_representation[].id` | String | `"store_121_Class20001"` | Unique identifier for the information representation instance |
| `information_representation[].representation_label` | String | `""` | Classification label for the information representation type |
| `information_representation[].ea_reference` | String | `""` | External reference identifier for integration with other EA tools |
| `information_representation[].name` | String | `"Customer Database"` | Display name of the information representation |
| `information_representation[].short_name` | String | `""` | Abbreviated name for the information representation |
| `information_representation[].description` | String | `""` | Detailed description of purpose and contents |
| `information_representation[].ea_notes` | String | `""` | Additional notes or implementation details |
| `information_representation[].synonyms` | Array | `[]` | Array of alternative names for this information representation |
| `information_representation[].valueClass` | String | `"Information_Representation"` | Metamodel class type (always "Information_Representation") |
| `information_representation[].inforep_category` | Array | `[]` | Array of Information_Representation_Category instance IDs (e.g., Database, File, API) |
| `information_representation[].il_managed_by_services` | Array | `[]` | Array of Information_Service instances that manage/expose this information representation |
| `information_representation[].visId` | Array | `["store_90_Class44"]` | Visibility array based on system lifecycle status for UI filtering |
| `information_representation[].sA2R` | Array | `[]` | Array of Stakeholder_to_Role relationships for this information representation |
| `information_representation[].infoViews` | Array | `[]` | Array of Information_View instance IDs that reference this representation |
| `information_representation[].dataReps` | Array | `[{"id": "store_121_Class20000"}]` | Array of Data_Representation instance IDs contained within this information representation |
| `information_representation[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `information_views` | Array | `[{"id": "store_113_Class79", "className": "Information_View", "name": "Meter Reading", "owner": [], ...` | Array of Information_View instances grouping data objects for specific business contexts or use cases |
| `information_views[].id` | String | `"store_113_Class79"` | Unique identifier for the information view instance |
| `information_views[].className` | String | `"Information_View"` | Metamodel class type (always "Information_View") |
| `information_views[].name` | String | `"Meter Reading"` | Display name of the information view |
| `information_views[].owner` | Array | `[]` | Array of Group_Actor instances responsible for this information view |
| `information_views[].dataObjects` | Array | `[{"id": "store_113_Class19"}]` | Array of Data_Object instance IDs included in this information view |
| `information_views[].synonyms` | Array | `[]` | Array of alternative names for this information view |
| `information_views[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `information_concepts` | Array | `[{"id": "store_113_Class89", "className": "Information_Concept", "name": "Production Order", "descri...` | Array of Information_Concept instances representing high-level information themes or domains |
| `information_concepts[].id` | String | `"store_113_Class89"` | Unique identifier for the information concept instance |
| `information_concepts[].className` | String | `"Information_Concept"` | Metamodel class type (always "Information_Concept") |
| `information_concepts[].name` | String | `"Production Order"` | Display name of the information concept |
| `information_concepts[].description` | String | `"The request for increased production"` | Business definition of the information concept |
| `information_concepts[].sequence_number` | String | `"4"` | Display sequence number for ordering information concepts in views |
| `information_concepts[].infoViews` | Array | `[{"id": "store_174_Class10360", "className": "Information_View", "name": "Inventory Information", "o...` | Array of Information_View instances associated with this information concept |
| `app_infoRep_Pairs` | Array | `[{"id": "store_121_Class20002", "persisted": "true", "infoRep": {"name": "Customer Database", "id": ...` | Array of APP_PRO_TO_INFOREP_FROM_INFOREP relationship instances linking applications to information representations |
| `app_infoRep_Pairs[].id` | String | `"store_121_Class20002"` | Unique identifier for the application-to-information-representation relationship |
| `app_infoRep_Pairs[].persisted` | String | `"true"` | Boolean string indicating if the application persistently stores data (true) or only reads/caches (false) |
| `app_infoRep_Pairs[].infoRep` | Object | `{"name": "Customer Database", "id": "store_121_Class20001"}` | Information_Representation instance object with name and ID |
| `app_infoRep_Pairs[].appId` | String | `"store_55_Class1161"` | Unique identifier of the Application_Provider instance |
| `info_domains` | Array | `[{"id": "store_858_Class46", "name": "Energy", "description": "", "sequence_number": "", "infoConcep...` | Array of Information_Domain instances organizing information concepts into business domains |
| `info_domains[].id` | String | `"store_858_Class46"` | Unique identifier for the information domain instance |
| `info_domains[].name` | String | `"Energy"` | Display name of the information domain (e.g., Finance, Customer, Product) |
| `info_domains[].description` | String | `""` | Business description of the information domain scope |
| `info_domains[].sequence_number` | String | `""` | Display sequence number for ordering information domains in views |
| `info_domains[].infoConcepts` | Array | `[{"id": "store_90_Class130031"}]` | Array of Information_Concept instance IDs belonging to this domain |
| `info_domains[].synonyms` | Array | `[]` | Array of alternative names for this information domain |
| `info_domains[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `info_rep_categories` | Array | `[{"id": "essential_baseline_v6_Class6", "name": "Database", "enumeration_value": "Database", "descri...` | Array of Information_Representation_Category enumeration instances for classifying data stores |
| `info_rep_categories[].id` | String | `"essential_baseline_v6_Class6"` | Unique identifier for the information representation category |
| `info_rep_categories[].name` | String | `"Database"` | Display name of the category (e.g., Database, File, API, Message Queue) |
| `info_rep_categories[].enumeration_value` | String | `"Database"` | Enumeration value for technical classification |
| `info_rep_categories[].description` | String | `""` | Description of the information representation category |
| `info_rep_categories[].synonyms` | Array | `[]` | Array of alternative names for this category |
| `info_rep_categories[].securityClassifications` | Array | `[]` | Array of security classification tags for access control |
| `version` | String | `"615"` | Version identifier for the API response or data snapshot |

## Integration


### core_api_import_application_capabilities_to_services.xsl
- **Path**: `integration/api/core_api_import_application_capabilities_to_services.xsl`
- **DSA Data Label**: `ImpAppCapSvcApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `application_capabilities_services` | Array | `[{"id": "store_55_Class762", "name": "Account Planning", "services": [{"id": "store_55_Class1094", "...` | Array of Application Capabilities with their associated Application Services |
| `application_capabilities_services[].id` | String | `"store_55_Class762"` | Unique identifier |
| `application_capabilities_services[].name` | String | `"Account Planning"` | Display name |
| `application_capabilities_services[].services` | Array | `[{"id": "store_55_Class1094", "sequence_number": "", "name": "Sales Reporting Services"}]` | Application Services that realize or implement this Application Capability |
| `application_capabilities_services[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"620"` | API version number |

### core_api_import_application_dependency.xsl
- **Path**: `integration/api/core_api_import_application_dependency.xsl`
- **DSA Data Label**: `ImpAppDepApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `application_dependencies` | Array | `[{"target": "", "source": "Creds", "sourceType": "Composite_Application_Provider", "targetType": "",...` | Array of application-to-application dependencies showing data flows and integration relationships |
| `application_dependencies[].target` | String | `""` | Name of the target/consuming application |
| `application_dependencies[].source` | String | `"Creds"` | Name of the source/providing application |
| `application_dependencies[].sourceType` | String | `"Composite_Application_Provider"` | Essential meta-class type of the source application |
| `application_dependencies[].targetType` | String | `""` | Essential meta-class type of the target application |
| `application_dependencies[].info` | Array | `[]` | Information objects exchanged in this dependency relationship |
| `application_dependencies[].frequency` | Array | `[{"name": "Timeliness - daily"}]` | Frequency or timeliness of data exchange |
| `application_dependencies[].acquisition` | String | `"Manual Data Entry"` | Method of data acquisition/integration |
| `application_dependencies[].securityClassifications` | Array | `[]` | Security classification tags |

### core_api_import_application_services.xsl
- **Path**: `integration/api/core_api_import_application_services.xsl`
- **DSA Data Label**: `ImpAppSvcApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `application_services` | Array | `[{"id": "store_55_Class898", "name": "Architecture Design", "description": "Design architectural pla...` | A well-defined component of functional behaviour that provides a  logical grouping of related Application Functions. e.g. ExchangeRates Service, CreditCardPayment Service or logical application such as CRM System, ERP System. The specification of the service - in terms of what it does - is defined by the set of Application Functions that it provides. |
| `application_services[].id` | String | `"store_55_Class898"` | Unique identifier |
| `application_services[].name` | String | `"Architecture Design"` | Display name |
| `application_services[].description` | String | `"Design architectural plans"` | Descriptive text |
| `application_services[].aprs` | Array | `["store_55_Class2489"]` | Array of Application Provider Role IDs that implement/provide this service |
| `application_services[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"620"` | API version number |

### core_api_import_application_to_technology.xsl
- **Path**: `integration/api/core_api_import_application_to_technology.xsl`
- **DSA Data Label**: `ImpApptoTechApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `application_technology_architecture` | Array | `[{"id": "store_55_Class1161", "application": "ADEXCell Energy Manager", "supportingTech": [{"fromTec...` | Array of applications with their supporting technology architecture stack |
| `application_technology_architecture[].id` | String | `"store_55_Class1161"` | Unique identifier |
| `application_technology_architecture[].application` | String | `"ADEXCell Energy Manager"` | Name of the application |
| `application_technology_architecture[].supportingTech` | Array | `[{"fromTechProduct": "Okta Identity Cloud", "fromTechComponent": "Single Sign-On Solution", "toTechP...` | Technology products and components that support this application |
| `application_technology_architecture[].allTechProds` | Array | `[{"tpr": "store_53_Class1165", "productId": "store_53_Class1163", "componentId": "store_55_Class2712...` | Complete list of all technology product relationships with IDs |
| `application_technology_architecture[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"615"` | API version number |

### core_api_import_applications to_services.xsl
- **Path**: `integration/api/core_api_import_applications to_services.xsl`
- **DSA Data Label**: `ImpApp2SvcApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `applications_to_services` | Array | `[{"id": "store_55_Class1161", "name": "ADEXCell Energy Manager", "services": [{"id": "store_55_Class...` | Array of applications with the Application Services they provide |
| `applications_to_services[].id` | String | `"store_55_Class1161"` | Unique identifier |
| `applications_to_services[].name` | String | `"ADEXCell Energy Manager"` | Display name |
| `applications_to_services[].services` | Array | `[{"id": "store_55_Class1046", "name": "Load Control", "securityClassifications": []}]` | Application Services provided by this application |
| `applications_to_services[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"616"` | API version number |

### core_api_import_applications.xsl
- **Path**: `integration/api/core_api_import_applications.xsl`
- **DSA Data Label**: `ImpAppsApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `applications` | Array | `[{"id": "store_55_Class1161", "lifecycle_name": "Prototype", "lifecycle": "Prototype", "name": "ADEX...` | Array of applications with their core properties |
| `applications[].id` | String | `"store_55_Class1161"` | Unique identifier |
| `applications[].lifecycle_name` | String | `"Prototype"` | Display name of the lifecycle status |
| `applications[].lifecycle` | String | `"Prototype"` | Lifecycle status value |
| `applications[].name` | String | `"ADEXCell Energy Manager"` | Display name |
| `applications[].codebase_name` | String | `"Bespoke"` | Display name of the codebase type |
| `applications[].delivery` | String | `"Private Cloud Service"` | Delivery model value |
| `applications[].delivery_name` | String | `"Private Cloud Service"` | Display name of the delivery model |
| `applications[].description` | String | `"Real time energy consumption monitoring of facilities"` | Descriptive text |
| `applications[].codebase` | String | `"Bespoke"` | Codebase type value (e.g., COTS, Bespoke, Open Source) |
| `applications[].class` | String | `"Composite_Application_Provider"` | Essential meta-class type |
| `applications[].dispositionId` | String | `"store_183_Class27"` | ID of the disposition lifecycle status for this application |
| `applications[].visId` | Array | `[""]` | Visibility of the instance based on system lifecycle |
| `applications[].securityClassifications` | Array | `[]` | Security classification tags |


### core_api_import_applications_to_orgs.xsl
- **Path**: `integration/api/core_api_import_applications_to_orgs.xsl`
- **DSA Data Label**: `ImpAppOrgApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `applications_to_orgs` | Array | `[{"id": "store_55_Class1161", "name": "ADEXCell Energy Manager", "owner": [], "actors": [{"id": "sto...` | Array of applications with their organizational relationships (owners and user organizations) |
| `applications_to_orgs[].id` | String | `"store_55_Class1161"` | Unique identifier |
| `applications_to_orgs[].name` | String | `"ADEXCell Energy Manager"` | Display name |
| `applications_to_orgs[].owner` | Array | `[]` | Organization(s) that own or are responsible for the application |
| `applications_to_orgs[].actors` | Array | `[{"id": "store_55_Class679", "name": "Marketing", "securityClassifications": []}]` | Organizations that use or interact with the application |
| `applications_to_orgs[].securityClassifications` | Array | `[]` | Security classification tags |

### core_api_import_applications_to_services.xsl
- **Path**: `integration/api/core_api_import_applications_to_services.xsl`
- **DSA Data Label**: `N/A`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `applications_to_services` | Array | `N/A` | Array of applications with the services they provide  |
| `id` | String | `N/A` | Application identifier |
| `name` | Unknown | `N/A` | Application name |
| `services` | Array | `N/A` | Services provided by the application |
| `apr` | String | `N/A` | Application Provider Role identifier |

### core_api_import_apps_to_servers.xsl
- **Path**: `integration/api/core_api_import_apps_to_servers.xsl`
- **DSA Data Label**: `ImpApp2ServerApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `app2server` | Array | `[{"id": "store_55_Class1168", "server": "ED1UAT", "name": "Microsoft Project Server", "deployment": ...` | Array of applications with their server deployment relationships |
| `app2server[].id` | String | `"store_55_Class1168"` | Unique identifier |
| `app2server[].server` | String | `"ED1UAT"` | Name of the server hosting the application |
| `app2server[].name` | String | `"Microsoft Project Server"` | Display name |
| `app2server[].deployment` | Array | `[{"id": "essential_prj_EE_v0_1_Instance_20013", "name": "Test", "securityClassifications": []}]` | Deployment instance(s) with environment type (e.g., Production, Test, Development) |
| `app2server[].securityClassifications` | Array | `[]` | Security classification tags |

### core_api_import_business_capabilities.xsl
- **Path**: `integration/api/core_api_import_business_capabilities.xsl`
- **DSA Data Label**: `ImpBusCapApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `businessCapabilities` | Array | `[{"id": "store_55_Class13", "businessDomain": "Management Services", "name": "Acquisition Management...` | Array of business capabilities representing what the business does or needs to do |
| `businessCapabilities[].id` | String | `"store_55_Class13"` | Unique identifier for capability|
| `businessCapabilities[].businessDomain` | String | `"Management Services"` | Name of the parent business domain |
| `businessCapabilities[].name` | String | `"Acquisition Management"` | Display name |
| `businessCapabilities[].description` | String | `"Monitoring and assessment of potential acquisitions for the organisation"` | Descriptive text |
| `businessCapabilities[].infoConcepts` | Array | `[]` | Information concepts used by this business capability |
| `businessCapabilities[].link` | String | `"<a href = "?XML=reportXML.xml&PMA=store_55_Class13&cl=en-gb" class = " context-menu-busCapGenMenu" ...` | HTML link for navigation to the capability detail view |
| `businessCapabilities[].domainIds` | Array | `["store_55_Class11"]` | Array of business domain IDs this capability belongs to |
| `businessCapabilities[].geoIds` | Array | `[]` | List of ids of geographies using this Business Capability |
| `businessCapabilities[].visId` | Array | `[""]` | visibility of the instance based on system lifecycle|
| `businessCapabilities[].prodConIds` | Array | `[]` | Product concept IDs associated with this capability |
| `businessCapabilities[].parentBusinessCapability` | Array | `[{"id": "store_55_Class9", "name": "Corporate Support"}]` | Parent business capability in the hierarchy |
| `businessCapabilities[].positioninParent` | String | `""` | Position or order within the parent capability |
| `businessCapabilities[].sequenceNumber` | String | `"2"` | Sequence number for ordering capabilities |
| `businessCapabilities[].rootCapability` | String | `""` | ID of the root/top-level capability in the hierarchy |
| `businessCapabilities[].businessDomains` | Array | `[{"id": "store_55_Class11", "name": "Management Services"}]` | Business domains this capability is associated with |
| `businessCapabilities[].children` | Array | `[]` | Child business capabilities in the hierarchy |
| `businessCapabilities[].documents` | Array | `[]` | Related documents or external references |
| `businessCapabilities[].level` | String | `"0"` | Hierarchical level (0 = top level, 1 = first child level, etc.) |
| `businessCapabilities[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |

### core_api_import_business_domains.xsl
- **Path**: `integration/api/core_api_import_business_domains.xsl`
- **DSA Data Label**: `ImpBusDomApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `businessDomains` | Array | `[{"id": "store_55_Class44", "name": "Digital Services", "description": "Failure Prediction, performa...` | Array of business domains representing high-level groupings of business capabilities |
| `businessDomains[].id` | String | `"store_55_Class44"` | Unique identifier |
| `businessDomains[].name` | String | `"Digital Services"` | Display name |
| `businessDomains[].description` | String | `"Failure Prediction, performance monitoring. xyzzy"` | Descriptive text |
| `businessDomains[].visId` | Array | `[""]` | visibility of the instance based on system lifecycle|
| `businessDomains[].parentDomain` | Array | `[]` | Parent business domain if this is a sub-domain |
| `businessDomains[].subDomain` | Array | `[]` | Child business domains within this domain |
| `businessDomains[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |

### core_api_import_business_families.xsl
- **Path**: `integration/api/core_api_import_business_families.xsl`
- **DSA Data Label**: `ImpBusPrecFamApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `businessProcessFamilies` | Array | `[{"id": "store_219_Class164", "name": "Collect Meter Data", "description": "", "visId": ["store_90_C...` | Array of business process families grouping related business processes across different contexts or geographies |
| `businessProcessFamilies[].id` | String | `"store_219_Class164"` | Unique identifier for family|
| `businessProcessFamilies[].name` | String | `"Collect Meter Data"` | Display name for family|
| `businessProcessFamilies[].description` | String | `""` | Descriptive text |
| `businessProcessFamilies[].visId` | Array | `["store_90_Class44"]` | visibility of the instance based on system lifecycle |
| `businessProcessFamilies[].containedProcesses` | Array | `[{"id": "store_219_Class159", "name": "Collect Meter Data - AsiaPac", "securityClassifications": []}...` | Business processes that are members of this family |
| `businessProcessFamilies[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |

### core_api_import_business_process_to_app_services.xsl
- **Path**: `integration/api/core_api_import_business_process_to_app_services.xsl`
- **DSA Data Label**: `ImpBusProcAppSvcApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `process_to_service` | Array | `[{"id": "store_55_Class215", "name": "Action Hedging", "services": [{"id": "store_55_Class1058", "na...` | Array of business processes with the application services that support them |
| `process_to_service[].id` | String | `"store_55_Class215"` | Unique identifier for process |
| `process_to_service[].name` | String | `"Action Hedging"` | Display name of process |
| `process_to_service[].services` | Array | `[{"id": "store_55_Class1058", "name": "Office Productivity Tools", "criticality": "", "securityClass...` | Application services that support this business process, with optional criticality ratings |
| `process_to_service[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |


### core_api_import_business_processes.xsl
- **Path**: `integration/api/core_api_import_business_processes.xsl`
- **DSA Data Label**: `ImpBusProcApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `meta` | Array | `[{"classes": ["Individual_Actor"], "menuId": "indActorGenMenu"}]` | Metadata for context menu configuration |
| `meta[].classes` | Array | `["Individual_Actor"]` | Essential meta-classes associated with the context menu |
| `meta[].menuId` | String | `"indActorGenMenu"` | Context menu identifier for UI interactions |
| `businessProcesses` | Array | `[{"id": "store_55_Class215", "business_process_id": "", "name": "Action Hedging", "standardisation":...` | Array of business processes representing activities that transform inputs to outputs |
| `businessProcesses[].id` | String | `"store_55_Class215"` | Unique identifier |
| `businessProcesses[].business_process_id` | String | `""` | Alternative or external business process identifier |
| `businessProcesses[].name` | String | `"Action Hedging"` | Display name |
| `businessProcesses[].standardisation` | String | `"Standard"` | Standardization level (e.g., Standard, Custom, Variant) |
| `businessProcesses[].description` | String | `"Process to "agree" and action the most viable hedging opportunities identified"` | Descriptive text |
| `businessProcesses[].bus_process_type_creates_information` | Array | `[]` | Information views created by this process |
| `businessProcesses[].bus_process_type_reads_information` | Array | `[]` | Information views read/consumed by this process |
| `businessProcesses[].bus_process_type_updates_information` | Array | `[]` | Information views updated/modified by this process |
| `businessProcesses[].bus_process_type_deletes_information` | Array | `[]` | Information views deleted by this process |
| `businessProcesses[].busproctype_relation` | Array | `[{"id": "store_90_Class130012", "create": "Unknown", "read": "Yes", "update": "Unknown", "delete": "...` | Detailed CRUD (Create, Read, Update, Delete) relationships with information |
| `businessProcesses[].busproctype_uses_infoviews` | Array | `[{"id": "store_90_Class130013", "name": "Market Spot Prices", "description": "Market prices for ener...` | Information views/reports used by this process |
| `businessProcesses[].performedbyRole` | Array | `[{"id": "store_67_Class346", "name": "Energy Data Analyst"}]` | Business roles that perform/execute this process |
| `businessProcesses[].ownedbyRole` | Array | `[{"id": "store_90_Class130011", "name": "Treasury"}]` | Business roles that own/are accountable for this process |
| `businessProcesses[].bp_sub_business_processes` | Array | `[]` | Sub-processes or child processes within this process |
| `businessProcesses[].realises_business_capability` | Array | `["store_55_Class119"]` | Business capability IDs that this process realizes or implements |
| `businessProcesses[].flow` | String | `"Y"` | Flag indicating if process flow diagram exists (Y/N) |
| `businessProcesses[].flowid` | String | `"store_261_Class80"` | Identifier of the process flow instance |
| `businessProcesses[].flowdetails` | Object | `{"name": "Action Hedging::PROCESS_FLOW", "diagram": "store_153_Class77", "diagramName": "Action Hedg...` | Process flow diagram details and metadata |
| `businessProcesses[].actors` | Array | `[{"id": "store_55_Class695", "name": "Finance", "securityClassifications": []}]` | Organizations that perform or participate in this process |
| `businessProcesses[].parentCaps` | Array | `[{"id": "store_55_Class119", "name": "Hedging Management", "securityClassifications": []}]` | Parent business capabilities that this process supports |
| `businessProcesses[].debug` | String | `""` | Debug information or internal notes |
| `businessProcesses[].costs` | Array | `[]` | Cost information associated with this process |
| `businessProcesses[].orgUserIds` | Array | `["store_55_Class695"]` | Organization IDs that use this process |
| `businessProcesses[].prodConIds` | Array | `[]` | Product concept IDs associated with this process |
| `businessProcesses[].visId` | Array | `[""]` | visibility of the instance based on system lifecycle|
| `businessProcesses[].geoIds` | Array | `["store_265_Class598"]` | List of ids of geographies using this Business process |
| `businessProcesses[].documents` | Array | `[{"id": "store_174_Class30512", "name": "https://university.enterprise-architecture.org/", "document...` | Related documents, links, or reference materials |
| `businessProcesses[].securityClassifications` | Array | `[]` | Security classification tags |
| `businessActivities` | Array | `[{"id": "store_261_Class84", "name": "Check Market Rates", "description": "", "bus_process_type_crea...` | Array of business activities (lower-level tasks within processes) |
| `businessActivities[].id` | String | `"store_261_Class84"` | Unique identifier |
| `businessActivities[].name` | String | `"Check Market Rates"` | Display name |
| `businessActivities[].description` | String | `""` | Descriptive text |
| `businessActivities[].bus_process_type_creates_information` | Array | `[]` | Information views created by this activity |
| `businessActivities[].bus_process_type_reads_information` | Array | `[]` | Information views read by this activity |
| `businessActivities[].bus_process_type_updates_information` | Array | `[]` | Information views updated by this activity |
| `businessActivities[].bus_process_type_deletes_information` | Array | `[]` | Information views deleted by this activity |
| `businessActivities[].securityClassifications` | Array | `[]` | Security classification tags |
| `ccy` | Array | `[{"id": "essential_baseline_v505_Class16", "name": "British Pound", "default": "", "exchangeRate": "...` | Array of currencies used for cost/financial data |
| `ccy[].id` | String | `"essential_baseline_v505_Class16"` | Unique identifier |
| `ccy[].name` | String | `"British Pound"` | Display name |
| `ccy[].default` | String | `""` | default currency |
| `ccy[].exchangeRate` | String | `""` | exchange rate for currency |
| `ccy[].ccySymbol` | String | `"£"` | symbol for currency |
| `ccy[].ccyCode` | String | `"GBP"` | currency code for currency  |
| `version` | String | `"620"` | API version number |

### core_api_import_data_object.xsl
- **Path**: `integration/api/core_api_import_data_object.xsl`
- **DSA Data Label**: `ImpDataObjApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `data_objects` | Array | `[{"id": "store_113_Class19", "indivOwner": "", "name": "Customer Address", "isAbstract": "false", "o...` | Array of data objects representing discrete data entities managed by the organization |
| `data_objects[].id` | String | `"store_113_Class19"` | Unique identifier |
| `data_objects[].indivOwner` | String | `""` | Individual person who owns or is accountable for this data object |
| `data_objects[].name` | String | `"Customer Address"` | Display name |
| `data_objects[].isAbstract` | String | `"false"` | Flag indicating if this is an abstract data object (true) or concrete (false) |
| `data_objects[].orgOwner` | String | `""` | Organization that owns or is accountable for this data object |
| `data_objects[].description` | String | `"The address of the customer"` | Descriptive text |
| `data_objects[].category` | String | `"Master Data"` | Data category (e.g., Master Data, Reference Data, Transactional Data) |
| `data_objects[].synonyms` | Array | `[]` | Alternative names or synonyms for this data object |
| `data_objects[].dataAttributes` | Array | `[{"id": "store_121_Class10000", "name": "Street Number", "type": "Integer", "description": "", "secu...` | Data attributes (fields/properties) that comprise this data object |
| `data_objects[].stakeholders` | Array | `[{"type": "Individual_Actor", "actorName": "Martin Thompson", "roleName": "Data Steward", "actorId":...` | Individuals or groups with roles/responsibilities for this data object |
| `data_objects[].externalDocs` | Array | `[]` | External documentation or reference links |
| `data_objects[].parents` | Array | `[{"name": "Customer", "securityClassifications": []}]` | Parent data objects in inheritance hierarchy |
| `data_objects[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |

### core_api_import_data_object_attributes.xsl
- **Path**: `integration/api/core_api_import_data_object_attributes.xsl`
- **DSA Data Label**: `ImpDataObjAttrApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `data_object_attributes` | Array | `[{"id": "store_113_Class19", "name": "Customer Address", "attributes": [{"id": "store_121_Class10000...` | Array of data objects with their detailed attribute definitions |
| `data_object_attributes[].id` | String | `"store_113_Class19"` | Unique identifier |
| `data_object_attributes[].name` | String | `"Customer Address"` | Display name |
| `data_object_attributes[].attributes` | Array | `[{"id": "store_121_Class10000", "name": "Customer Address - Street Number", "description": "", "syno...` | Detailed attributes/fields with their properties (name, type, description, etc.) |
| `data_object_attributes[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |

### core_api_import_data_object_inherit.xsl
- **Path**: `integration/api/core_api_import_data_object_inherit.xsl`
- **DSA Data Label**: `ImpDataObjInheritApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `data_object_inherit` | Array | `[{"id": "store_113_Class19", "name": "Customer Address", "children": [], "securityClassifications": ...` | Array of data objects with their inheritance relationships (parent-child hierarchy) |
| `data_object_inherit[].id` | String | `"store_113_Class19"` | Unique identifier |
| `data_object_inherit[].name` | String | `"Customer Address"` | Display name |
| `data_object_inherit[].children` | Array | `[]` | Child data objects that inherit from this data object |
| `data_object_inherit[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"620"` | API version number |

### core_api_import_data_subject.xsl
- **Path**: `integration/api/core_api_import_data_subject.xsl`
- **DSA Data Label**: `ImpDataSubjApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `data_subjects` | Array | `[{"id": "store_113_Class13", "name": "Customer", "description": "Someone who buys services from the ...` | Array of data subjects representing real-world entities (people, organizations, things) about which data is collected |
| `data_subjects[].id` | String | `"store_113_Class13"` | Unique identifier |
| `data_subjects[].name` | String | `"Customer"` | Display name |
| `data_subjects[].description` | String | `"Someone who buys services from the organisation"` | Descriptive text |
| `data_subjects[].synonyms` | Array | `[]` | Alternative names or synonyms for this data subject |
| `data_subjects[].dataObjects` | Array | `[{"id": "store_113_Class19", "name": "Customer Address", "securityClassifications": []}]` | Data objects associated with or describing this data subject |
| `data_subjects[].category` | String | `"Master Data"` | Data category classification |
| `data_subjects[].orgOwner` | String | `""` | Organization that owns or is accountable for this data subject |
| `data_subjects[].stakeholders` | Array | `[{"type": "Group_Actor", "actorName": "Sales", "roleName": " Data Subject Organisational Owner ", "a...` | Individuals or groups with roles/responsibilities for this data subject |
| `data_subjects[].externalDocs` | Array | `[]` | External documentation or reference links |
| `data_subjects[].indivOwner` | String | `""` | Individual person who owns or is accountable for this data subject |
| `data_subjects[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |

### core_api_import_framework_data.xsl
- **Path**: `integration/api/core_api_import_framework_data.xsl`
- **DSA Data Label**: `controlsApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `assessment` | Array | `[{"id": "store_174_Class30006", "control_solution_assessor": "Joe Smith", "name": "AC-04 Control Sol...` | Array of control solution assessments evaluating compliance or effectiveness |
| `assessment[].id` | String | `"store_174_Class30006"` | Unique identifier |
| `assessment[].control_solution_assessor` | String | `"Joe Smith"` | Name of the person who performed the assessment |
| `assessment[].name` | String | `"AC-04 Control Solution assessed on 2022-01-01"` | Display name |
| `assessment[].assessment_date` | String | `"2022-01-01"` | Date when the assessment was conducted |
| `assessment[].assessment_finding` | String | `"Pass"` | Result or finding of the assessment (e.g., Pass, Fail, Partial) |
| `assessment[].assessment_comments` | String | `"Successfully Passed"` | Additional comments or notes about the assessment |
| `assessment[].controls` | Array | `[]` | Controls being assessed |
| `assessment[].securityClassifications` | Array | `[]` | Security classification tags |
| `controlSolutions` | Array | `[{"id": "store_174_Class30007", "name": "AC-04 Control Solution", "processes": [{"id": "store_174_Cl...` | Array of control solutions implementing specific controls or requirements |
| `controlSolutions[].id` | String | `"store_174_Class30007"` | Unique identifier |
| `controlSolutions[].name` | String | `"AC-04 Control Solution"` | Display name |
| `controlSolutions[].processes` | Array | `[{"id": "store_174_Class40000", "name": "Manage User Account"}]` | Business processes that implement or support this control solution |
| `controlSolutions[].assessments` | Array | `[{"id": "store_174_Class30006", "name": "AC-04 Control Solution assessed on 2022-01-01", "assessment...` | Assessments conducted on this control solution |
| `controlSolutions[].solutionForControl` | Array | `[{"id": "store_182_Class1", "name": "AC-04", "description": "Perform more frequent reviews of user a...` | Controls that this solution implements or addresses |
| `controlSolutions[].securityClassifications` | Array | `[]` | Security classification tags |
| `control` | Array | `[{"id": "store_90_Class100355", "name": "A.10.1.1", "description": "Documented operating procedures ...` | Array of controls from compliance or security frameworks |
| `control[].id` | String | `"store_90_Class100355"` | Unique identifier |
| `control[].name` | String | `"A.10.1.1"` | Display name |
| `control[].description` | String | `"Documented operating procedures - Operating procedures shall be documented, maintained, and made av...` | Descriptive text |
| `control[].framework` | String | `"ISO27001"` | Framework or standard this control belongs to (e.g., ISO27001, NIST, SOC2) |
| `control[].controlAssessessments` | Array | `[]` | Assessments related to this control |
| `control[].controlSolutions` | Array | `[]` | Solutions that implement this control |
| `framework_controls` | Array | `[{"id": "store_90_Class100541", "name": "ISO27001", "controls": ["store_90_Class100355", "store_90_C...` | Array of compliance frameworks with their associated controls |
| `framework_controls[].id` | String | `"store_90_Class100541"` | Unique identifier |
| `framework_controls[].name` | String | `"ISO27001"` | Display name |
| `framework_controls[].controls` | Array | `["store_90_Class100355"]` | Array of control IDs belonging to this framework |
| `version` | String | `"620"` | API version number |

### core_api_import_information_representations.xsl
- **Path**: `integration/api/core_api_import_information_representations.xsl`
- **DSA Data Label**: `ImpInfoRepApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `infoReps` | Array | `[{"id": "store_174_Class10364", "name": "BlackCurve API Customer Data Flow", "description": ""}]` | Array of information representations (data flows, data exchanges, or information transfers between systems) |
| `infoReps[].id` | String | `"store_174_Class10364"` | Unique identifier |
| `infoReps[].name` | String | `"BlackCurve API Customer Data Flow"` | Display name |
| `infoReps[].description` | String | `""` | Descriptive text |
| `version` | String | `"620"` | API version number |

### core_api_import_nodes.xsl
- **Path**: `integration/api/core_api_import_nodes.xsl`
- **DSA Data Label**: `ImpNodeApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `nodes` | Array | `[{"id": "store_55_Class1962", "className": "Technology_Node", "criticalityId": "", "name": "AWS Dubl...` | Array of technology nodes representing physical or virtual infrastructure components (servers, nodes, devices) |
| `nodes[].id` | String | `"store_55_Class1962"` | Unique identifier |
| `nodes[].className` | String | `"Technology_Node"` | name of the class used |
| `nodes[].criticalityId` | String | `""` | ID of the criticality rating for this node |
| `nodes[].name` | String | `"AWS Dublin"` | Display name |
| `nodes[].hostedIn` | String | `"Dublin"` | Name of the location or site where this node is hosted |
| `nodes[].criticality` | String | `""` | Criticality level or rating (e.g., High, Medium, Low) |
| `nodes[].hostInfo` | Object | `{"id": "store_55_Class1334", "name": "Dublin", "className": "Site"}` | Information about the hosting location including ID, name, and type |
| `nodes[].hostedInid` | String | `"store_55_Class1334"` | ID of the hosting location |
| `nodes[].hostedLocation` | String | `"store_265_Class588"` | Geographic location ID |
| `nodes[].ipAddress` | String | `""` | Primary IP address of the node |
| `nodes[].ipAddresses` | Array | `[]` | Array of all IP addresses associated with this node |
| `nodes[].lon` | String | `"-6.2602732"` | Longitude coordinate for geographic positioning |
| `nodes[].lat` | String | `"53.3497645"` | Latitude coordinate for geographic positioning |
| `nodes[].securityClassifications` | Array | `[]` | Security classification tags |
| `nodes[].inboundConnections` | Array | `[]` | Network connections coming into this node |
| `nodes[].outboundConnections` | Array | `[]` | Network connections going out from this node |
| `nodes[].techStack` | Array | `[]` | Technology stack or components running on this node |
| `nodes[].attributes` | Array | `[]` | Custom attributes or properties |
| `nodes[].technology_node_type` | Object | `{"id": "", "className": "Technology_Node_Type", "name": "", "icon": ""}` | Type classification of the node (e.g., Server, Network Device, Storage) |
| `nodes[].instances` | Array | `[{"id": "store_55_Class2121", "runtime_status_id": "essential_prj_CC_v1.4.2_Instance_10005", "name":...` | Technology component instances deployed on this node |
| `nodes[].stakeholders` | Array | `[]` | Individuals or organizations responsible for this node |
| `nodes[].parentNodes` | Array | `[]` | Parent nodes in a hierarchy (e.g., physical server hosting virtual nodes) |
| `appSoftwareMap` | Array | `[{"id": "store_55_Class1161", "software_usages": []}]` | Mapping of applications to software components |
| `appSoftwareMap[].id` | String | `"store_55_Class1161"` | Unique identifier |
| `appSoftwareMap[].software_usages` | Array | `[]` | Software components used by this application |
| `styles` | Array | `[{"id": "essential_prj_CC_v1.4.2_Instance_40008", "icon": "", "textColour": "", "backgroundColour": ...` | Visual styling information for rendering nodes |
| `styles[].id` | String | `"essential_prj_CC_v1.4.2_Instance_40008"` | Unique identifier |
| `styles[].icon` | String | `""` | Icon identifier or URL for visual representation |
| `styles[].textColour` | String | `""` | Text color for labels (hex or color name) |
| `styles[].backgroundColour` | String | `""` | Background color for node visualization (hex or color name) |
| `version` | String | `"621"` | API version number |

### core_api_import_orgs_sites.xsl
- **Path**: `integration/api/core_api_import_orgs_sites.xsl`
- **DSA Data Label**: `ImpOrgSitesApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `organisations` | Array | `[{"id": "store_90_Class110008", "name": "AMS", "external": "true", "description": ""}]` | ?????? |
| `organisations[].id` | String | `"store_90_Class110008"` | Unique identifier |
| `organisations[].name` | String | `"AMS"` | Display name |
| `organisations[].external` | String | `"true"` | ?????? |
| `organisations[].description` | String | `""` | Descriptive text |
| `version` | String | `"614"` | ?????? |

### core_api_import_physical_process_app_svc.xsl
- **Path**: `integration/api/core_api_import_physical_process_app_svc.xsl`
- **DSA Data Label**: `ImpPhysProcAppApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `process_to_apps` | Array | `[{"id": "store_90_Class40071", "processCriticality": "High", "org": "Accounting", "name": "Accountin...` | Array of physical business processes (organization + process combinations) with supporting applications |
| `process_to_apps[].id` | String | `"store_90_Class40071"` | Unique identifier |
| `process_to_apps[].processCriticality` | String | `"High"` | Criticality rating of the process for this organization (e.g., High, Medium, Low) |
| `process_to_apps[].org` | String | `"Accounting"` | Name of the organization performing the process |
| `process_to_apps[].name` | String | `"Accounting performing Action Hedging"` | Display name |
| `process_to_apps[].processName` | String | `"Action Hedging"` | Name of the business process |
| `process_to_apps[].criticalityStyle` | Object | `{"colour": "", "backgroundColour": ""}` | Visual styling for the criticality rating |
| `process_to_apps[].orgid` | String | `"store_55_Class713"` | ID of the organization |
| `process_to_apps[].orgUserId` | Array | `["store_55_Class713"]` | Array of organization IDs using this process |
| `process_to_apps[].processid` | String | `"store_55_Class215"` | ID of the business process |
| `process_to_apps[].appProcessCriticalities` | Array | `[{"appid": "store_55_Class2471", "appCriticality": "", "criticalityStyle": {"colour": "", "backgroun...` | Applications supporting this process with their individual criticality ratings |
| `process_to_apps[].sites` | Array | `[{"id": "store_55_Class747", "name": "London", "long": "-0.1276474", "lat": "51.5073219"}]` | Sites/locations where this process is performed |
| `process_to_apps[].appsviaservice` | Array | `[{"id": "store_55_Class2471", "svcid": "store_55_Class1124", "name": "WorkMan as Work Order Manageme...` | Applications supporting the process via application services |
| `process_to_apps[].appsdirect` | Array | `[]` | Applications directly supporting the process (without explicit service mapping) |
| `process_to_apps[].securityClassifications` | Array | `[]` | Security classification tags |
| `activity_to_apps` | Array | `[{"id": "store_261_Class101", "org": "Finance", "activityId": "store_261_Class89", "name": "Finance ...` | Array of business activities (sub-process level) with supporting applications |
| `activity_to_apps[].id` | String | `"store_261_Class101"` | Unique identifier |
| `activity_to_apps[].org` | String | `"Finance"` | Name of the organization performing the activity |
| `activity_to_apps[].activityId` | String | `"store_261_Class89"` | ID of the business activity |
| `activity_to_apps[].name` | String | `"Finance as Hedge Management performing Initiate Transaction"` | Display name |
| `activity_to_apps[].appsviaservice` | Array | `[]` | Applications supporting the activity via application services |
| `activity_to_apps[].appsdirect` | Array | `[]` | Applications directly supporting the activity |
| `activity_to_apps[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"621"` | API version number |

### core_api_import_sites.xsl
- **Path**: `integration/api/core_api_import_sites.xsl`
- **DSA Data Label**: `ImpSitesApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `sites` | Array | `[{"id": "store_55_Class1337", "name": "Amsterdam", "long": "4.8979755", "description": "Microsoft Am...` | Array of physical sites/locations used by the organization |
| `sites[].id` | String | `"store_55_Class1337"` | Unique identifier |
| `sites[].name` | String | `"Amsterdam"` | Display name |
| `sites[].long` | String | `"4.8979755"` | Longitude coordinate for geographic positioning |
| `sites[].description` | String | `"Microsoft Amsterdam"` | Descriptive text |
| `sites[].lat` | String | `"52.3745403"` | Latitude coordinate for geographic positioning |
| `sites[].securityClassifications` | Array | `[]` | Security classification tags |
| `countries` | Array | `[{"id": "essential_baseline_v2_0_Class50126", "name": "Afghanistan"}]` | Array of countries for geographic reference |
| `countries[].id` | String | `"essential_baseline_v2_0_Class50126"` | Unique identifier |
| `countries[].name` | String | `"Afghanistan"` | Display name |
| `version` | String | `"614"` | API version number |

### core_api_import_suppliers.xsl
- **Path**: `integration/api/core_api_import_suppliers.xsl`
- **DSA Data Label**: `allSupplier`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `suppliers` | Array | `N/A` | Array of supplier organizations providing products or services |
| `suppliersProcess` | Array | `N/A` | Suppliers mapped to the business processes they support |
| `suppliersApps` | Array | `N/A` | Suppliers mapped to the applications they provide or support |
| `filters` | Array | `N/A` | Filter definitions for supplier categorization |
| `version` | String | `N/A` | API version number |
| `id` | String | `N/A` | Unique identifier |
| `name` | Unknown | `N/A` | Display name |
| `method` | String | `N/A` | Output method (likely XML or text) |
| `indent` | Unknown | `N/A` | Indentation setting for output formatting |
| `className` | String | `N/A` | Essential meta-class name |
| `sites` | Unknown | `N/A` | Sites/locations associated with the supplier |
| `supplierActor` | String | `N/A` | Supplier organization identifier or name |
| `esg_rating` | String | `N/A` | Environmental, Social, and Governance (ESG) rating for the supplier |
| `processes` | Array | `N/A` | Business processes supported by this supplier |
| `busProc` | Object | `N/A` | Business process object details |
| `physname` | Unknown | `N/A` | Physical process name or identifier |
| `apps` | Array | `N/A` | Applications provided or supported by this supplier |
| `valueClass` | String | `N/A` | Value classification or category |
| `description` | String | `N/A` | Descriptive text |
| `slotName` | String | `N/A` | slot name for enumeration |
| `isGroup` | Unknown | `N/A` | Flag indicating if this is a group/parent supplier |
| `icon` | String | `N/A` | Icon identifier for visual representation |
| `color` | String | `N/A` | Color code for visual styling |
| `values` | Array | `N/A` | Enumeration values or options |
| `enum_name` | Unknown | `N/A` | Enumeration name or identifier |
| `sequence` | String | `N/A` | Sequence number for ordering |
| `backgroundColor` | String | `N/A` | Background color for visual styling |
| `colour` | String | `N/A` | Color for visual styling |


### core_api_import_technology_capabilities.xsl
- **Path**: `integration/api/core_api_import_technology_capabilities.xsl`
- **DSA Data Label**: `ImpTechCapApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_capabilities` | Array | `[{"id": "EAS_Meta_Model_Instance_10013", "legacyId": "EAS_Meta_Model_Instance_10013", "type": "Techn...` | Array of technology capabilities representing what the technology infrastructure can or should do |
| `technology_capabilities[].id` | String | `"EAS_Meta_Model_Instance_10013"` | Unique identifier |
| `technology_capabilities[].legacyId` | String | `"EAS_Meta_Model_Instance_10013"` | Unique identifier but based on old version with fullstops in id |
| `technology_capabilities[].type` | String | `"Technology_Capability"` | type of the class |
| `technology_capabilities[].className` | String | `"Technology_Capability"` | name of the class used |
| `technology_capabilities[].domain` | String | `"Client Technology"` | Name of the technology domain this capability belongs to |
| `technology_capabilities[].name` | String | `"User Presentation Services"` | Display name |
| `technology_capabilities[].description` | String | `"Capability for users to interact with a system"` | Descriptive text |
| `technology_capabilities[].domainId` | String | `"essential_baseline_v1_Instance_30016"` | ID of the technology domain |
| `technology_capabilities[].securityClassifications` | Array | `[]` | Security classification tags |
| `technology_capability_hierarchy` | Array | `[{"id": "EAS_Meta_Model_Instance_10013", "type": "Technology_Capability", "className": "Technology_C...` | Hierarchical structure of technology capabilities with parent-child relationships |
| `technology_capability_hierarchy[].id` | String | `"EAS_Meta_Model_Instance_10013"` | Unique identifier |
| `technology_capability_hierarchy[].type` | String | `"Technology_Capability"` | type of the class |
| `technology_capability_hierarchy[].className` | String | `"Technology_Capability"` | name of the class used |
| `technology_capability_hierarchy[].name` | String | `"User Presentation Services"` | Display name |
| `technology_capability_hierarchy[].supportingCapabilities` | Array | `[]` | Child technology capabilities that support or comprise this capability |
| `technology_capability_hierarchy[].components` | Array | `[{"id": "EAS_Meta_Model_v1_0_Instance_10030", "type": "Technology_Component", "className": "Technolo...` | Technology components that realize this capability |
| `technology_capability_hierarchy[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"620"` | API version number |

### core_api_import_technology_components.xsl
- **Path**: `integration/api/core_api_import_technology_components.xsl`
- **DSA Data Label**: `ImpTechCompApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_components` | Array | `[{"id": "EAS_Meta_Model_v1_0_Instance_10018", "legacyId": "EAS_Meta_Model_v1.0_Instance_10018", "nam...` | Array of technology components representing logical technology building blocks (e.g., database, web server, messaging) |
| `technology_components[].id` | String | `"EAS_Meta_Model_v1_0_Instance_10018"` | Unique identifier |
| `technology_components[].legacyId` | String | `"EAS_Meta_Model_v1.0_Instance_10018"` | Legacy identifier from previous version with different format |
| `technology_components[].name` | String | `"J2EE Application Server"` | Display name |
| `technology_components[].description` | String | `"An application runtime environment that supports the full J2EE specification"` | Descriptive text |
| `technology_components[].caps` | Array | `["Application Runtime Services"]` | Technology capabilities that this component realizes or provides |
| `technology_components[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |

### core_api_import_technology_domains.xsl
- **Path**: `integration/api/core_api_import_technology_domains.xsl`
- **DSA Data Label**: `ImpTechDomApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_domains` | Array | `[{"id": "essential_baseline_v1_Instance_30011", "name": "Security Technology", "ReferenceModelLayer"...` | Array of technology domains representing high-level groupings of technology capabilities |
| `technology_domains[].id` | String | `"essential_baseline_v1_Instance_30011"` | Unique identifier |
| `technology_domains[].name` | String | `"Security Technology"` | Display name |
| `technology_domains[].ReferenceModelLayer` | String | `""` | Reference architecture layer this domain belongs to |
| `technology_domains[].description` | String | `"Domain for all technology capabilities related to security"` | Descriptive text |
| `technology_domains[].supportingCapabilities` | Array | `["essential_prj_CC_v1_4_2_Instance_140264"]` | Technology capability IDs within this domain |
| `technology_domains[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"620"` | API version number |

### core_api_import_technology_product_families.xsl
- **Path**: `integration/api/core_api_import_technology_product_families.xsl`
- **DSA Data Label**: `ImpTechProdFmApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_product_family` | Array | `[{"id": "store_55_Class3241", "name": "Acer TravelMate", "description": "", "securityClassifications...` | Array of technology product families grouping related technology products from the same vendor |
| `technology_product_family[].id` | String | `"store_55_Class3241"` | Unique identifier |
| `technology_product_family[].name` | String | `"Acer TravelMate"` | Display name |
| `technology_product_family[].description` | String | `""` | Descriptive text |
| `technology_product_family[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |

### core_api_import_technology_products.xsl
- **Path**: `integration/api/core_api_import_technology_products.xsl`
- **DSA Data Label**: `ImpTechProdApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_products` | Array | `[{"vendor": "EAS", "lifecycle": "", "name": "NW_TEST", "supplier": "EAS", "delivery": "", "id": "sto...` | Array of technology products (specific vendor implementations of technology components) |
| `technology_products[].vendor` | String | `"EAS"` | Vendor/manufacturer of the technology product |
| `technology_products[].lifecycle` | String | `""` | Lifecycle status of the product |
| `technology_products[].name` | String | `"NW_TEST"` | Display name |
| `technology_products[].supplier` | String | `"EAS"` | Supplier providing the technology product |
| `technology_products[].delivery` | String | `""` | Delivery model (e.g., On-Premise, SaaS, PaaS) |
| `technology_products[].id` | String | `"store_121_Class50000"` | Unique identifier |
| `technology_products[].description` | String | `"The Document Storage service is a self contained service that offers storage and retrieval of docum...` | Descriptive text |
| `technology_products[].technology_provider_version` | String | `""` | Version number of the technology product |
| `technology_products[].visId` | Array | `["store_90_Class44"]` | visibility of the instance based on system lifecycle |
| `technology_products[].orgUserIds` | Array | `[]` | Organization IDs using this technology product |
| `technology_products[].costs` | Array | `[]` | Cost information associated with this product |
| `technology_products[].family` | Array | `[]` | Technology product family this product belongs to |
| `technology_products[].functions` | Array | `[]` | Technology components/functions this product implements |
| `technology_products[].instances` | Array | `[]` | Deployed instances of this technology product |
| `technology_products[].usages` | Array | `[]` | Usage contexts or applications using this product |
| `technology_products[].documents` | Array | `[]` | Related documentation or reference materials |
| `technology_products[].stakeholders` | Array | `[]` | Individuals or groups with roles/responsibilities for this product |
| `technology_products[].purchase_status` | Array | `[]` | Procurement or licensing status |
| `technology_products[].technology_product_family` | Array | `[]` | Product family details |
| `technology_products[].technology_provider_delivery_model` | Array | `[]` | Delivery model details |
| `technology_products[].technology_provider_lifecycle_status` | Array | `[]` | Provider's lifecycle status for the product |
| `technology_products[].vendor_product_lifecycle_status` | Array | `[]` | Vendor's lifecycle status for the product |
| `technology_products[].securityClassifications` | Array | `[]` | Security classification tags |
| `tprStandards` | Array | `[{"id": "store_53_Class1063", "compliance2": [], "compliance": "", "adoption": {"id": "essential_bas...` | Technology product standards compliance and adoption status |
| `tprStandards[].id` | String | `"store_53_Class1063"` | Unique identifier |
| `tprStandards[].compliance2` | Array | `[]` | Detailed compliance information |
| `tprStandards[].compliance` | String | `""` | Compliance status or level |
| `tprStandards[].adoption` | Object | `{"id": "essential_baseline_v5_Class15", "name": ""}` | Adoption status (e.g., Strategic, Tactical, Deprecated) |
| `ccy` | Array | `[{"id": "essential_baseline_v505_Class16", "name": "British Pound", "default": "", "exchangeRate": "...` | Array of currencies used for cost/financial data |
| `ccy[].id` | String | `"essential_baseline_v505_Class16"` | Unique identifier |
| `ccy[].name` | String | `"British Pound"` | Display name |
| `ccy[].default` | String | `""` | Flag indicating if this is the default currency |
| `ccy[].exchangeRate` | String | `""` | Exchange rate for currency conversion |
| `filters` | Array | `[{"id": "Lifecycle_Status", "name": "Lifecycle Status", "valueClass": "Lifecycle_Status", "descripti...` | Filter definitions for categorizing and filtering technology products |
| `filters[].id` | String | `"Lifecycle_Status"` | Unique identifier |
| `filters[].name` | String | `"Lifecycle Status"` | Display name |
| `filters[].valueClass` | String | `"Lifecycle_Status"` | Essential meta-class for the filter values |
| `filters[].description` | String | `""` | Descriptive text |
| `filters[].slotName` | String | `"technology_provider_lifecycle_status"` | slot name for enumeration |
| `filters[].isGroup` | Boolean | `false` | Flag indicating if this is a grouping filter |
| `filters[].icon` | String | `"fa-circle"` | Icon identifier for visual representation |
| `filters[].color` | String | `"#93592f"` | Color code for visual styling |
| `filters[].values` | Array | `[{"id": "essential_prj_AA_v1_4_Instance_10068", "sequence": "1", "enum_name": "Under Planning", "nam...` | Enumeration values for this filter |
| `version` | String | `"620"` | API version number |


### core_api_import_technology_products_orgs.xsl
- **Path**: `integration/api/core_api_import_technology_products_orgs.xsl`
- **DSA Data Label**: `ImpTechProdOrgApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_product_orgs` | Array | `[{"id": "store_55_Class3311", "name": ".NET", "org": [{"id": "store_55_Class687", "name": "IT", "sec...` | ?????? |
| `technology_product_orgs[].id` | String | `"store_55_Class3311"` | Unique identifier |
| `technology_product_orgs[].name` | String | `".NET"` | Display name |
| `technology_product_orgs[].org` | Array | `[{"id": "store_55_Class687", "name": "IT", "securityClassifications": []}]` | ?????? |
| `technology_product_orgs[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | ?????? |

### core_api_import_technology_suppliers.xsl
- **Path**: `integration/api/core_api_import_technology_suppliers.xsl`
- **DSA Data Label**: `ImpTechSuppApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_suppliers` | Array | `[{"id": "essential_prj_AA_v1_1_graphArchTest_Instance_20", "name": "Oracle Corporation", "descriptio...` | Array of technology supplier organizations providing technology products |
| `technology_suppliers[].id` | String | `"essential_prj_AA_v1_1_graphArchTest_Instance_20"` | Unique identifier |
| `technology_suppliers[].name` | String | `"Oracle Corporation"` | Display name |
| `technology_suppliers[].description` | String | `"Oracle Corporation"` | Descriptive text |
| `technology_suppliers[].securityClassifications` | Array | `[]` | Security classification tags |
| `version` | String | `"614"` | API version number |


## Technology

### core_api_get_all_tech_nodes_detail.xsl
- **Path**: `technology/api/core_api_get_all_tech_nodes_detail.xsl`
- **DSA Data Label**: `techNoApi`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_nodes` | Array | `N/A` | Array of technology nodes with detailed deployment and infrastructure information |
| `id` | String | `N/A` | Unique identifier |
| `name` | Unknown | `N/A` | Display name |
| `description` | Unknown | `N/A` | Descriptive text |
| `method` | String | `N/A` | Output method (likely XML or text) |
| `indent` | Unknown | `N/A` | Indentation setting for output formatting |
| `ip` | String | `N/A` | IP address of the technology node |
| `apps` | Array | `N/A` | Applications deployed on this node |
| `link` | String | `N/A` | URL link to the node detail view |
| `deployment` | Array | `N/A` | Deployment instances running on this node |
| `country` | String | `N/A` | Country where the node is located |
| `attributes` | Array | `N/A` | Custom attributes or properties of the node |
| `key` | String | `N/A` | Attribute key/name |
| `attribute_value_of` | String | `N/A` | Attribute being measured |
| `attribute_value` | String | `N/A` | Attribute value |
| `attribute_value_unit` | String | `N/A` | Unit of measurement for the attribute |
| `deployment_status` | Object | `N/A` | Status of the deployment (e.g., Production, Test, Development) |
| `className` | String | `N/A` | Essential meta-class name |
| `technology_node_type` | Object | `N/A` | Type classification of the technology node |
| `deployment_of` | Object | `N/A` | Technology component or product being deployed |
| `instances` | Array | `N/A` | Technology component instances on this node |
| `app` | Object | `N/A` | Application object details |
| `tech` | Object | `N/A` | Technology object details |
| `stakeholders` | Array | `N/A` | Individuals or organizations responsible for this node |
| `type` | String | `N/A` | Type of stakeholder relationship |
| `actor` | String | `N/A` | Name of the stakeholder actor |
| `actorId` | String | `N/A` | ID of the stakeholder actor |
| `role` | String | `N/A` | Role name of the stakeholder |
| `roleId` | String | `N/A` | ID of the stakeholder role |
| `parentNodes` | Array | `N/A` | Parent nodes in the infrastructure hierarchy |
| `techType` | String | `N/A` | Technology type classification |

### core_api_tl_get_all_technology_lifecycles.xsl
- **Path**: `technology/api/core_api_tl_get_all_technology_lifecycles.xsl`
- **DSA Data Label**: `techLifecycle`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_lifecycles` | Array | `N/A` | Array of technology products with their lifecycle status information |
| `all_lifecycles` | Array | `N/A` | All lifecycle status records across all technology products |
| `lifecycleJSON` | Array | `N/A` | JSON-formatted lifecycle data |
| `standardsJSON` | Array | `N/A` | JSON-formatted technology standards data |
| `lifecycleType` | Array | `N/A` | Types of lifecycle statuses available |
| `id` | String | `N/A` | Unique identifier |
| `linkid` | Unknown | `N/A` | Link identifier for navigation |
| `name` | Unknown | `N/A` | Display name |
| `description` | Unknown | `N/A` | Descriptive text |
| `supplier` | Unknown | `N/A` | Supplier name |
| `method` | String | `N/A` | Output method (likely XML or text) |
| `indent` | Unknown | `N/A` | Indentation setting for output formatting |
| `supplierId` | String | `N/A` | ID of the technology supplier |
| `allDates` | Array | `N/A` | All lifecycle milestone dates |
| `dates` | Array | `N/A` | Specific lifecycle dates (start, end, retirement, etc.) |
| `applications` | Array | `N/A` | Applications using this technology product |
| `standards` | Array | `N/A` | Technology standards or adoption status |
| `className` | String | `N/A` | Essential meta-class name |
| `componentName` | Unknown | `N/A` | Technology component name |
| `standardStrength` | String | `N/A` | Strength of the technology standard (e.g., Strategic, Tactical, Deprecated) |
| `geoScope` | Array | `N/A` | Geographic scope where the standard applies |
| `orgScope` | Array | `N/A` | Organizational scope where the standard applies |
| `dateOf` | String | `N/A` | Type of date (e.g., start date, end of life, retirement) |
| `thisid` | String | `N/A` | Instance identifier |
| `type` | String | `N/A` | Type classification |
| `seq` | Unknown | `N/A` | Sequence number for ordering |
| `enumeration_value` | String | `N/A` | Enumeration value name |
| `backgroundColour` | String | `N/A` | Background color for visual styling |
| `colour` | String | `N/A` | Color for visual styling |
| `productId` | String | `N/A` | Technology product identifier |


### core_api_tl_get_all_technology_suppliers.xsl
- **Path**: `technology/api/core_api_tl_get_all_technology_suppliers.xsl`
- **DSA Data Label**: `N/A`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_suppliers` | Array | `N/A` | Array of technology supplier organizations |
| `id` | String | `N/A` | Unique identifier |
| `name` | String | `N/A` | Display name |
| `description` | String | `N/A` | Descriptive text |


### core_api_tl_tech_perf_measures.xsl
- **Path**: `technology/api/core_api_tl_tech_perf_measures.xsl`
- **DSA Data Label**: `techKpiAPI`
- **Parameters**: None
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_product` | Array | `[{"id": "store_121_Class50000", "name": "NW_TEST", "perfMeasures": [], "securityClassifications": []...` | Array of technology products with their performance measures/KPIs |
| `technology_product[].id` | String | `"store_121_Class50000"` | Unique identifier |
| `technology_product[].name` | String | `"NW_TEST"` | Display name |
| `technology_product[].perfMeasures` | Array | `[]` | Performance measures/KPIs associated with this technology product |
| `technology_product[].securityClassifications` | Array | `[]` | Security classification tags |
| `technology_product_role` | Array | `[{"id": "store_53_Class1063", "name": "Endpoint Security::as::Firewall", "description": "", "perfMea...` | Array of technology product roles (specific uses/configurations) with performance measures |
| `technology_product_role[].id` | String | `"store_53_Class1063"` | Unique identifier |
| `technology_product_role[].name` | String | `"Endpoint Security::as::Firewall"` | Display name |
| `technology_product_role[].description` | String | `""` | Descriptive text |
| `technology_product_role[].perfMeasures` | Array | `[]` | Performance measures/KPIs for this specific role |
| `technology_product_role[].securityClassifications` | Array | `[]` | Security classification tags |
| `perfCategory` | Array | `[]` | Performance measure categories (e.g., Availability, Performance, Security) |
| `serviceQualities` | Array | `[]` | Service quality metrics and targets |
 
### core_api_tl_technology_capability_list.xsl
- **Path**: `technology/api/core_api_tl_technology_capability_list.xsl`
- **DSA Data Label**: `N/A`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_capabilities` | Array | `N/A` | Array of technology capabilities |
| `tech_components` | Array | `N/A` | Array of technology components that realize the capabilities |
  

### core_api_tl_technology_product_list.xsl
- **Path**: `technology/api/core_api_tl_technology_product_list.xsl`
- **DSA Data Label**: `techProdListData`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `technology_products` | Array | `N/A` | Array of technology products with basic information |
| `link` | String | `N/A` | URL link to the product detail view |
| `supplier` | String | `N/A` | Supplier/vendor name |
| `caps` | Array | `N/A` | Technology capabilities provided by this product |
| `comp` | Array | `N/A` | Technology components implemented by this product |


### core_api_tl_technology_product_list_with_supplier_componentIDs.xsl
- **Path**: `technology/api/core_api_tl_technology_product_list_with_supplier_componentIDs.xsl`
- **DSA Data Label**: `techProdSvc`
- **Parameters**: param1
- **Properties**:
| Property | Type | Example | Description |
| --- | --- | --- | --- |
| `meta` | Array | `N/A` | Metadata for context menu configuration |
| `technology_products` | Array | `N/A` | Array of technology products with comprehensive details including supplier and component relationships |
| `filters` | Array | `N/A` | Filter definitions for categorizing technology products |
| `name` | Unknown | `N/A` | Display name |
| `description` | Unknown | `N/A` | Descriptive text |
| `method` | String | `N/A` | Output method (likely XML or text) |
| `indent` | Unknown | `N/A` | Indentation setting for output formatting |
| `id` | String | `N/A` | Unique identifier |
| `supplierId` | String | `N/A` | ID of the technology supplier |
| `member_of_technology_product_families` | Array | `N/A` | Technology product families this product belongs to |
| `vendor_lifecycle` | Array | `N/A` | Vendor's lifecycle status information |
| `start_date` | String | `N/A` | Start date for lifecycle status |
| `status` | Unknown | `N/A` | Status name or description |
| `statusId` | String | `N/A` | ID of the status |
| `order` | String | `N/A` | Order/sequence number |
| `caps` | Array | `N/A` | Technology capabilities |
| `comp` | Array | `N/A` | Technology components |
| `tprid` | String | `N/A` | Technology Product Role ID |
| `strategic_lifecycle_status` | String | `N/A` | Strategic/enterprise lifecycle status |
| `std` | String | `N/A` | Technology standard or adoption status |
| `stdStyle` | String | `N/A` | CSS style for standard visualization |
| `stdColour` | String | `N/A` | Color for standard status |
| `stdTextColour` | String | `N/A` | Text color for standard status |
| `allStandards` | Array | `N/A` | All technology standards applicable to this product |
| `stdStrength` | Unknown | `N/A` | Strength of the technology standard |
| `orgScope` | Array | `N/A` | Organizational scope where standard applies |
| `type` | Unknown | `N/A` | Type classification |
| `geoScope` | Array | `N/A` | Geographic scope where standard applies |
| `supplier` | Unknown | `N/A` | Supplier/vendor information |
| `lifecycleStatus` | Unknown | `N/A` | Current lifecycle status |
| `statusScore` | Unknown | `N/A` | Numeric score for lifecycle status |
| `ea_reference` | String | `N/A` | Enterprise architecture reference identifier |
| `delivery` | String | `N/A` | Delivery model (e.g., On-Premise, SaaS, PaaS) |
| `techOrgUsers` | Array | `N/A` | Organizations using this technology product |
| `orgUserIds` | Array | `N/A` | Array of organization IDs using this product |
| `visId` | Array | `N/A` | visibility of the instance based on system lifecycle |
| `valueClass` | String | `N/A` | Essential meta-class for filter values |
| `slotName` | String | `N/A` | slot name for enumeration |
| `isGroup` | Unknown | `N/A` | Flag indicating if this is a grouping filter |
| `icon` | String | `N/A` | Icon identifier for visual representation |
| `color` | String | `N/A` | Color code for visual styling |
| `values` | Array | `N/A` | Enumeration values for filters |
| `enum_name` | String | `N/A` | Enumeration value name |
| `sequence` | String | `N/A` | Sequence number for ordering |
| `backgroundColor` | String | `N/A` | Background color for visual styling |
| `colour` | String | `N/A` | Color for visual styling |
| `classes` | Array | `N/A` | Essential meta-classes for context menu |
| `menuId` | String | `N/A` | Context menu identifier |