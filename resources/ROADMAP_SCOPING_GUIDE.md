# Roadmap Scoping Integration Guide

## Overview
Roadmap scoping allows users to filter view data by organization, geography, approval status, and custom filter definitions. This guide shows how to add optional roadmap scoping to any view.

**IMPORTANT**: The `core_roadmap_functions.xsl` include is **NOT required**. All necessary functions are available through `core_js_functions.xsl` which is already imported.

---

## When to Use Roadmap Scoping

Add roadmap scoping when your view needs to:
- Filter by organization/department (Group_Actor)
- Filter by geography (Geographic_Region)
- Filter by approval status (SYS_CONTENT_APPROVAL_STATUS)
- Use custom filter definitions from Mart APIs
- Allow users to dynamically change data scope

---

## Implementation Pattern

### 1. Variable Declarations (Outside document.ready)

```javascript
// Declare outside $(document).ready for global scope
var workingArray, dynamicFilterDefs;
```

**Why outside?**
- `redrawView()` function needs access to these
- Allows dynamic re-filtering without re-fetching data

### 2. Initialize Scoping (Inside executeFetchAndRender)

```javascript
async function executeFetchAndRender() {
    try {
        let responses = await fetchAndRenderData(apiList);
        ({ appMartAPI, otherAPI } = responses);
        
        // Extract filters from Mart API response
        // Filters are typically in Mart APIs (e.g., appMartAPI, busCapMart)
        let filters = responses[0].filters;
        
        // Store your main data array
        workingArray = responses[0].applications; // or whatever your main data is
        
        // Build dynamic filter definitions from API filters
        dynamicFilterDefs = filters?.map(function(filterdef) {
            return new ScopingProperty(filterdef.slotName, filterdef.valueClass);
        });
        
        // Build view model
        buildViewModel(responses);
        
        // Initialize scoping with standard filter classes
        essInitViewScoping(
            redrawView,
            ['Group_Actor', 'Geographic_Region', 'SYS_CONTENT_APPROVAL_STATUS'],
            filters,
            true
        );
        
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### 3. Implement redrawView Function

```javascript
var redrawView = function() {
    // Reset any roadmap change tracking
    essResetRMChanges();
    
    // Define your scoping properties
    let appOrgScopingDef = new ScopingProperty('orgUserIds', 'Group_Actor');
    let geoScopingDef = new ScopingProperty('geoIds', 'Geographic_Region');
    let visibilityDef = new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS');
    
    // Add any custom scoping properties specific to your data
    // let prodConceptDef = new ScopingProperty('prodConIds', 'Product_Concept');
    // let busDomainDef = new ScopingProperty('domainIds', 'Business_Domain');
    
    // Define the type of resource being scoped
    let resourceTypeInfo = {
        className: 'Application_Provider',  // Adjust to your resource type
        label: 'Application',                // Human-readable label
        icon: 'fa-desktop'                   // Font Awesome icon class
    };
    
    // Scope the resources
    let scopedResources = essScopeResources(
        workingArray,
        [appOrgScopingDef, geoScopingDef, visibilityDef].concat(dynamicFilterDefs),
        resourceTypeInfo
    );
    
    // scopedResources contains:
    //   .resources - filtered array of data items
    //   .resourceIds - array of IDs in scope
    
    // Re-render your view with scoped data
    renderView(scopedResources.resources);
};
```

### 4. Filter Logic in renderView

```javascript
function renderView(data) {
    // data parameter is already filtered by redrawView
    // OR if you need to filter manually:
    
    // Option A: Use scoped data directly
    console.log('Rendering', data.length, 'items');
    
    // Option B: Filter against scopedResources.resourceIds
    let inScopeItems = viewModel.allItems.filter(function(item) {
        return scopedResources.resourceIds.includes(item.id);
    });
    
    // Render your view
    $('#mainContent').html(generateHTML(data));
}
```

### 5. Add UI Template Call

In your XSL template body:

```xml
<body>
    <xsl:call-template name="Heading"/>
    
    <!-- Add scoping UI -->
    <xsl:call-template name="ViewUserScopingUI"></xsl:call-template>
    
    <div class="container">
        <!-- Your content -->
    </div>
    
    <xsl:call-template name="Footer"/>
</body>
```

---

## Complete Example

### Full Script Section with Roadmap Scoping

```xml
<script type="text/javascript">
    <xsl:call-template name="RenderViewerAPIJSFunction"/>
    
    let appMartAPI, appLifecycle;
    
    // Global variables for scoping
    var workingArray, dynamicFilterDefs, scopedResources;
    
    var viewModel = {
        applications: [],
        lifecycle: []
    };
    
    $(document).ready(function() {
        const apiList = ['appMartAPI', 'appLifecycle'];
        
        async function executeFetchAndRender() {
            try {
                let responses = await fetchAndRenderData(apiList);
                ({ appMartAPI, appLifecycle } = responses);
                
                console.log('Responses loaded:', responses);
                
                // Extract filters and data from Mart API
                let filters = appMartAPI.filters;
                workingArray = appMartAPI.applications;
                
                // Build dynamic filter definitions
                dynamicFilterDefs = filters?.map(function(filterdef) {
                    return new ScopingProperty(filterdef.slotName, filterdef.valueClass);
                }) || [];
                
                // Build view model
                buildViewModel(responses);
                
                // Initialize roadmap scoping
                essInitViewScoping(
                    redrawView,
                    ['Group_Actor', 'Geographic_Region', 'SYS_CONTENT_APPROVAL_STATUS'],
                    filters,
                    true
                );
                
            } catch (error) {
                console.error('Error loading view:', error);
            }
        }
        
        executeFetchAndRender();
    });
    
    function buildViewModel(responses) {
        if (responses.appMartAPI &amp;&amp;responses.appMartAPI.applications) {
            viewModel.applications = responses.appMartAPI.applications;
        }
        
        if (responses.appLifecycle &amp;&amp;responses.appLifecycle.application_lifecycles) {
            viewModel.lifecycle = responses.appLifecycle.application_lifecycles;
        }
    }
    
    var redrawView = function() {
        essResetRMChanges();
        
        // Define scoping properties
        let appOrgScopingDef = new ScopingProperty('orgUserIds', 'Group_Actor');
        let geoScopingDef = new ScopingProperty('geoIds', 'Geographic_Region');
        let visibilityDef = new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS');
        
        // Resource type info
        let resourceTypeInfo = {
            className: 'Application_Provider',
            label: 'Application',
            icon: 'fa-desktop'
        };
        
        // Apply scoping
        scopedResources = essScopeResources(
            workingArray,
            [appOrgScopingDef, geoScopingDef, visibilityDef].concat(dynamicFilterDefs),
            resourceTypeInfo
        );
        
        // Re-render with scoped data
        renderView(scopedResources.resources);
    };
    
    function renderView(data) {
        console.log('Rendering', data.length, 'scoped items');
        
        // Generate HTML for your view
        let html = '&lt;h2&gt;Applications (' + data.length + ')&lt;/h2&gt;';
        html += '&lt;table class="table"&gt;';
        
        data.forEach(function(app) {
            html += '&lt;tr&gt;&lt;td&gt;' + app.name + '&lt;/td&gt;&lt;/tr&gt;';
        });
        
        html += '&lt;/table&gt;';
        
        $('#mainContent').html(html);
    }
</script>
```

---

## Key Concepts

### ScopingProperty

Defines how to filter data:

```javascript
new ScopingProperty(propertyName, filterClass)
```

**Parameters:**
- `propertyName`: Property in your data objects containing IDs to filter by
- `filterClass`: Essential meta-class for the filter (e.g., 'Group_Actor')

**Common Examples:**
```javascript
new ScopingProperty('orgUserIds', 'Group_Actor')        // Organization filter
new ScopingProperty('geoIds', 'Geographic_Region')      // Geography filter
new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS')  // Approval status
new ScopingProperty('prodConIds', 'Product_Concept')    // Product filter
new ScopingProperty('domainIds', 'Business_Domain')     // Domain filter
```

### essInitViewScoping

Initializes the scoping UI and handlers:

```javascript
essInitViewScoping(redrawCallback, filterClasses, filters, enableFlag)
```

**Parameters:**
- `redrawCallback`: Function to call when filters change (your `redrawView`)
- `filterClasses`: Array of standard filter class names to enable
- `filters`: Filter definitions from API (contains dynamic filters)
- `enableFlag`: Boolean to enable/disable scoping (typically `true`)

### essScopeResources

Filters data based on current scope selections:

```javascript
let result = essScopeResources(dataArray, scopingProperties, typeInfo)
```

**Parameters:**
- `dataArray`: Your full dataset to filter
- `scopingProperties`: Array of `ScopingProperty` objects
- `typeInfo`: Object describing the resource type

**Returns:**
```javascript
{
    resources: [...],      // Filtered data array
    resourceIds: [...],    // Array of IDs that passed filter
    inScopeIds: {...}      // Map of in-scope IDs by filter class
}
```

### essResetRMChanges

Resets roadmap change tracking. Call at start of `redrawView()`.

```javascript
essResetRMChanges();
```

---

## Data Structure Requirements

Your data objects need filter-related properties:

```javascript
{
    id: "APP_001",
    name: "My Application",
    orgUserIds: ["ORG_1", "ORG_2"],           // Organization IDs
    geoIds: ["GEO_UK", "GEO_US"],            // Geography IDs
    visId: ["STATUS_APPROVED"],               // Approval status
    prodConIds: ["PROD_1"],                   // Product concepts (optional)
    domainIds: ["DOMAIN_SALES"]               // Domains (optional)
}
```

These properties are populated by Essential when exporting API data.

---

## Filter Response Structure

Mart APIs include a `filters` array:

```javascript
{
    applications: [...],
    filters: [
        {
            slotName: "prodConIds",
            valueClass: "Product_Concept",
            label: "Products"
        },
        {
            slotName: "domainIds",
            valueClass: "Business_Domain",
            label: "Domains"
        }
    ]
}
```

The `dynamicFilterDefs` converts these to `ScopingProperty` objects automatically.

---

## Without Roadmap Scoping

If you don't need scoping, simply omit all roadmap-related code:

```javascript
$(document).ready(function() {
    const apiList = ['appMartAPI'];
    
    async function executeFetchAndRender() {
        try {
            let responses = await fetchAndRenderData(apiList);
            ({ appMartAPI } = responses);
            
            buildViewModel(responses);
            renderView();  // Just render directly
            
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    executeFetchAndRender();
});

function renderView() {
    // Use viewModel.applications directly - no filtering
    console.log('Rendering', viewModel.applications.length, 'items');
}
```

**And remove the UI template call:**
```xml
<body>
    <xsl:call-template name="Heading"/>
    <!-- NO ViewUserScopingUI call -->
    <div class="container">...</div>
    <xsl:call-template name="Footer"/>
</body>
```

---

## Common Patterns

### Pattern 1: Application Scoping

```javascript
var appsArray, dynamicAppFilterDefs, scopedApps;

// In executeFetchAndRender:
appsArray = appMartAPI.applications;
let filters = appMartAPI.filters;

dynamicAppFilterDefs = filters?.map(function(filterdef) {
    return new ScopingProperty(filterdef.slotName, filterdef.valueClass);
}) || [];

essInitViewScoping(redrawView, 
    ['Group_Actor', 'Geographic_Region', 'SYS_CONTENT_APPROVAL_STATUS'], 
    filters, true);

// In redrawView:
var redrawView = function() {
    essResetRMChanges();
    
    let appTypeInfo = {
        className: 'Application_Provider',
        label: 'Application',
        icon: 'fa-desktop'
    };
    
    scopedApps = essScopeResources(
        appsArray,
        [
            new ScopingProperty('orgUserIds', 'Group_Actor'),
            new ScopingProperty('geoIds', 'Geographic_Region'),
            new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS')
        ].concat(dynamicAppFilterDefs),
        appTypeInfo
    );
    
    renderView(scopedApps.resources);
};
```

### Pattern 2: Capability Scoping

```javascript
var capsArray, dynamicCapFilterDefs, scopedCaps;

// In executeFetchAndRender:
capsArray = ImpBusCapApi.businessCapabilities;
let filters = ImpBusCapApi.filters;

dynamicCapFilterDefs = filters?.map(function(filterdef) {
    return new ScopingProperty(filterdef.slotName, filterdef.valueClass);
}) || [];

essInitViewScoping(redrawView, 
    ['Business_Domain', 'Group_Actor'], 
    filters, true);

// In redrawView:
var redrawView = function() {
    essResetRMChanges();
    
    let capTypeInfo = {
        className: 'Business_Capability',
        label: 'Capability',
        icon: 'fa-puzzle-piece'
    };
    
    scopedCaps = essScopeResources(
        capsArray,
        [
            new ScopingProperty('domainIds', 'Business_Domain'),
            new ScopingProperty('orgUserIds', 'Group_Actor')
        ].concat(dynamicCapFilterDefs),
        capTypeInfo
    );
    
    renderCapabilityHeatmap(scopedCaps.resources);
};
```

### Pattern 3: Technology Scoping

```javascript
var techArray, dynamicTechFilterDefs, scopedTech;

// In executeFetchAndRender:
techArray = techMartAPI.technologyProducts;
let filters = techMartAPI.filters;

dynamicTechFilterDefs = filters?.map(function(filterdef) {
    return new ScopingProperty(filterdef.slotName, filterdef.valueClass);
}) || [];

essInitViewScoping(redrawView, 
    ['Technology_Product_Family', 'Codebase_Status'], 
    filters, true);

// In redrawView:
var redrawView = function() {
    essResetRMChanges();
    
    let techTypeInfo = {
        className: 'Technology_Product',
        label: 'Technology',
        icon: 'fa-cogs'
    };
    
    scopedTech = essScopeResources(
        techArray,
        [
            new ScopingProperty('familyIds', 'Technology_Product_Family'),
            new ScopingProperty('statusIds', 'Codebase_Status')
        ].concat(dynamicTechFilterDefs),
        techTypeInfo
    );
    
    renderTechRoadmap(scopedTech.resources);
};
```
---

## Additional Patterns

---

### Pattern 4: Information Representation Scoping (infoMartAPI)

`infoMartAPI` does not expose a `filters` array like the Mart APIs do. Scope using `visId` and
`sA2R` only. The primary scopeable array is `information_representation`.

```javascript
let infoMartAPI;
var infoRepArray, scopedInfoReps;

$(document).ready(function() {
    const apiList = ['infoMartAPI'];

    async function executeFetchAndRender() {
        try {
            let responses = await fetchAndRenderData(apiList);
            ({ infoMartAPI } = responses);

            console.log('infoMartAPI keys:', Object.keys(infoMartAPI));

            // infoMartAPI has NO filters array - use visId scoping only
            infoRepArray = infoMartAPI.information_representation || [];

            // No dynamic filter defs - infoMartAPI has no filters property
            // Initialize scoping with visibility only (no custom filters)
            essInitViewScoping(
                redrawView,
                ['SYS_CONTENT_APPROVAL_STATUS'],
                [],    // empty filters - no dynamic filter UI
                true
            );

            buildViewModel();

        } catch (error) {
            console.error('Error:', error);
        }
    }

    executeFetchAndRender();
});

var redrawView = function() {
    essResetRMChanges();

    let visibilityDef = new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS');

    let typeInfo = {
        className: 'Information_Representation',
        label: 'Information Store',
        icon: 'fa-database'
    };

    scopedInfoReps = essScopeResources(
        infoRepArray,
        [visibilityDef],
        typeInfo
    );

    renderView(scopedInfoReps.resources);
};
```

**infoMartAPI scopeable properties by array:**

| Array | orgUserIds | geoIds | visId | Notes |
|-------|-----------|--------|-------|-------|
| `information_representation` | ✗ | ✗ | ✓ `visId` | Scope by visibility only |
| `data_objects` | ✗ | ✗ | ✗ | No scoping properties |
| `data_subjects` | ✗ | ✗ | ✗ | No scoping properties |

If you need org or geo scoping on information stores, join against `busCapAppMartApps.applications`
via `app_infoRep_Pairs` to get the app's `orgUserIds` and `geoIds`.

---

### Pattern 5: busCapAppMartApps / busCapAppMartCaps Scoping

These are the richest Mart APIs and both expose a `filters` array. Use `busCapAppMartApps` as the
primary anchor for application-centric views; use `busCapAppMartCaps` for capability heatmaps.

```javascript
let busCapAppMartApps, busCapAppMartCaps;
var appsArray, capsArray, dynamicAppFilterDefs, dynamicCapFilterDefs;
var scopedApps, scopedCaps;

$(document).ready(function() {
    const apiList = ['busCapAppMartApps', 'busCapAppMartCaps'];

    async function executeFetchAndRender() {
        try {
            let responses = await fetchAndRenderData(apiList);
            ({ busCapAppMartApps, busCapAppMartCaps } = responses);

            // busCapAppMartApps: primary data array is .applications
            appsArray = busCapAppMartApps.applications || [];
            let appFilters = busCapAppMartApps.filters || [];

            dynamicAppFilterDefs = appFilters.map(function(f) {
                return new ScopingProperty(f.slotName, f.valueClass);
            });

            // busCapAppMartCaps: primary data arrays are .busCaptoAppDetails and .busCapHierarchy
            capsArray = busCapAppMartCaps.busCaptoAppDetails || [];
            let capFilters = busCapAppMartCaps.filters || [];

            dynamicCapFilterDefs = capFilters.map(function(f) {
                return new ScopingProperty(f.slotName, f.valueClass);
            });

            buildViewModel();

            // Use app filters to drive the scoping UI
            // (cap filters from busCapAppMartCaps can be merged if needed)
            essInitViewScoping(
                redrawView,
                ['Group_Actor', 'Geographic_Region', 'SYS_CONTENT_APPROVAL_STATUS'],
                appFilters,
                true
            );

        } catch (error) {
            console.error('Error:', error);
        }
    }

    executeFetchAndRender();
});

var redrawView = function() {
    essResetRMChanges();

    // Scope applications
    scopedApps = essScopeResources(
        appsArray,
        [
            new ScopingProperty('orgUserIds', 'Group_Actor'),
            new ScopingProperty('geoIds', 'Geographic_Region'),
            new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS')
        ].concat(dynamicAppFilterDefs),
        { className: 'Composite_Application_Provider', label: 'Application', icon: 'fa-desktop' }
    );

    // Scope capabilities - busCaptoAppDetails uses domainIds and orgUserIds
    scopedCaps = essScopeResources(
        capsArray,
        [
            new ScopingProperty('orgUserIds', 'Group_Actor'),
            new ScopingProperty('domainIds', 'Business_Domain'),
            new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS')
        ].concat(dynamicCapFilterDefs),
        { className: 'Business_Capability', label: 'Capability', icon: 'fa-puzzle-piece' }
    );

    renderView(scopedApps.resources, scopedCaps.resources);
};
```

**busCapAppMartApps filter slot names (from API `filters` array):**

The filters array is dynamic and driven by enumeration slots on `Application_Provider`. Common ones
include:

| slotName | valueClass | Description |
|----------|-----------|-------------|
| `lifecycle_status_application_provider` | `Lifecycle_Status` | Under Planning, Production, Retired, etc. |
| `ap_delivery_model` | `AP_Delivery_Model` | SaaS, On-premise, Private Cloud, etc. |
| `ap_codebase_status` | `AP_Codebase_Status` | Bespoke, Packaged, etc. |
| `application_provider_purpose` | `Application_Provider_Purpose` | Business Application, etc. |
| `ap_disposition_lifecycle_status` | `AP_Disposition_Lifecycle_Status` | Retain, Replace, Retire, etc. |

Always read the `filters` array at runtime rather than hardcoding these — the set varies per
repository configuration.

---

### Pattern 6: Scoping Two Arrays Simultaneously

When a view needs both applications AND capabilities scoped together (e.g. a capability heatmap
that only shows apps in scope), scope each array independently then cross-reference by ID.

```javascript
var appsArray, capsArray;
var dynamicAppFilterDefs = [];
var scopedApps, scopedCaps;

// After fetching...
var redrawView = function() {
    essResetRMChanges();

    // Step 1: Scope the applications
    scopedApps = essScopeResources(
        appsArray,
        [
            new ScopingProperty('orgUserIds', 'Group_Actor'),
            new ScopingProperty('geoIds', 'Geographic_Region'),
            new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS')
        ].concat(dynamicAppFilterDefs),
        { className: 'Composite_Application_Provider', label: 'Application', icon: 'fa-desktop' }
    );

    // Build a Set of in-scope app IDs for fast lookup
    var inScopeAppIds = new Set(scopedApps.resources.map(function(a) { return a.id; }));

    // Step 2: Scope capabilities by filtering to those that have at least one in-scope app
    // busCaptoAppDetails[].apps is an array of app ID strings
    var filteredCaps = capsArray.filter(function(cap) {
        var capApps = cap.apps || cap.thisapps || [];
        return capApps.some(function(appId) { return inScopeAppIds.has(appId); });
    });

    // Step 3: For each scoped cap, filter its apps list to in-scope only
    var enrichedCaps = filteredCaps.map(function(cap) {
        var capApps = cap.apps || cap.thisapps || [];
        return Object.assign({}, cap, {
            scopedApps: capApps.filter(function(appId) { return inScopeAppIds.has(appId); })
        });
    });

    renderCapabilityHeatmap(enrichedCaps, scopedApps.resources);
};
```

**Key principle**: `essScopeResources` is called once per array. Never try to pass two arrays to a
single call. Cross-reference afterward using the returned `.resources` or `.resourceIds`.

---

### Pattern 7: Scaffold Filter Extraction Bug — Correct Pattern

The `generate_view_scaffold` tool emits a broken filter extraction line:

```javascript
// BROKEN - generated by scaffold, do NOT use:
let primaryAPI = {api_labels[0]};
```

This is invalid JavaScript. Always replace it with explicit extraction:

```javascript
// CORRECT - explicit extraction from named API response:
let filters = busCapAppMartApps.filters || [];
workingArray = busCapAppMartApps.applications || [];

dynamicFilterDefs = filters.map(function(filterdef) {
    return new ScopingProperty(filterdef.slotName, filterdef.valueClass);
});
```

The pattern to follow is always:
1. Name the API explicitly (e.g. `busCapAppMartApps.filters`)
2. Provide a `|| []` fallback so it doesn't throw if the property is absent
3. Map to `ScopingProperty` objects before passing to `essInitViewScoping`

---

## Scoping Property Reference by API

Quick lookup: which scoping properties are available on each API's primary data array.

| API Label | Primary Array | orgUserIds | geoIds | visId | domainIds | filters |
|-----------|--------------|:---------:|:------:|:-----:|:---------:|:-------:|
| `busCapAppMartApps` | `.applications` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `busCapAppMartCaps` | `.busCaptoAppDetails` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `appMartAPI` | `.applications` | ✗ | ✗ | ✓ | ✗ | ✗ |
| `ImpBusCapApi` | `.businessCapabilities` | ✗ | ✓ | ✓ | ✓ | ✗ |
| `ImpAppsApi` | `.applications` | ✗ | ✗ | ✓ | ✗ | ✗ |
| `ImpTechProdApi` | `.technology_products` | ✓ | ✗ | ✓ | ✗ | ✓ |
| `techProdSvc` | `.technology_products` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `infoMartAPI` | `.information_representation` | ✗ | ✗ | ✓ | ✗ | ✗ |
| `planDataAPi` | `.allProject` | ✓ | ✗ | ✓ | ✗ | ✗ |
| `orgSummary` | `.orgData` | ✗ | ✗ | ✗ | ✗ | ✗ |

**Rule of thumb**: If the API name contains "Mart" or ends in "Svc", it almost certainly has a
`filters` array. Import APIs (`Imp*`) rarely do.

---

## Troubleshooting

### Issue: Scoping UI doesn't appear
**Check:**
- `<xsl:call-template name="ViewUserScopingUI"/>` is in body
- `essInitViewScoping()` is called
- Filters are being passed from API

### Issue: No data after scoping
**Check:**
- Data objects have required properties (orgUserIds, geoIds, etc.)
- Property names in `ScopingProperty` match data structure
- `console.log(scopedResources)` to see what was filtered

### Issue: redrawView not called
**Check:**
- Function is defined as `var redrawView = function() {...}`
- Passed to `essInitViewScoping()` correctly
- Not wrapped in $(document).ready

### Issue: Dynamic filters not working
**Check:**
- Filters exist in API response: `console.log(filters)`
- `dynamicFilterDefs` is defined and populated
- Concatenated properly: `.concat(dynamicFilterDefs)`

---

## Best Practices

1. **Always check for filters**
   ```javascript
   let filters = responses[0].filters || [];
   ```

2. **Use optional chaining**
   ```javascript
   dynamicFilterDefs = filters?.map(...) || [];
   ```

3. **Log scoped results**
   ```javascript
   console.log('Scoped to', scopedResources.resources.length, 'items');
   ```

4. **Define resource type info**
   ```javascript
   let typeInfo = {
       className: 'Application_Provider',  // Essential meta-class
       label: 'Application',                // Display name
       icon: 'fa-desktop'                   // Icon class
   };
   ```

5. **Reset changes on redraw**
   ```javascript
   var redrawView = function() {
       essResetRMChanges();  // Always first
       // ... rest of function
   };
   ```

6. **Store original data**
   ```javascript
   workingArray = responses[0].applications;  // Keep original
   // Never modify workingArray, always use scopedResources.resources
   ```

---

### 7. Layout Isolation & Top Margins (CRITICAL)
When using the roadmap/scoping UI, the bars are fixed to the top of the viewport. To prevent your content from being hidden:
- Wrap your custom dashboard in a dedicated `div` (e.g. `.view-wrapper`).
- Use `margin-top: 80px` (or calculate dynamically) to clear the standard navigation and scoping bars.
- Keep `<xsl:call-template name="Heading"/>` and `<xsl:call-template name="ViewUserScopingUI"/>` as siblings to your wrapper, not children.

### 8. Timeline/Gantt Date Resilience
When rendering timelines:
- Always calculate `min`/`max` dates explicitly from your dataset to prevent the chart from defaulting to 1970.
- Handle both `allProjects` and `allProject` keys in the roadmap API response.
- Add a 1-month buffer to the calculated date range for better visual spacing.

---

## Summary

**To Add Roadmap Scoping:**
1. Declare global variables outside document.ready
2. Extract filters from Mart API response
3. Build dynamic filter definitions
4. Call `essInitViewScoping()` with filters
5. Implement `redrawView()` function
6. Use `essScopeResources()` to filter data
7. Add `<xsl:call-template name="ViewUserScopingUI"/>` to body

**No Additional Includes Required:**
- All functions available through `core_js_functions.xsl`
- No need for `core_roadmap_functions.xsl`

**When Not to Use:**
- Simple views without filtering needs
- Static data presentations
- Reports that show complete datasets
- Views where user filtering isn't required
---

## Additional Patterns

---

### Pattern 4: Information Representation Scoping (infoMartAPI)

`infoMartAPI` does not expose a `filters` array like the Mart APIs do. Scope using `visId` and
`sA2R` only. The primary scopeable array is `information_representation`.

```javascript
let infoMartAPI;
var infoRepArray, scopedInfoReps;

$(document).ready(function() {
    const apiList = ['infoMartAPI'];

    async function executeFetchAndRender() {
        try {
            let responses = await fetchAndRenderData(apiList);
            ({ infoMartAPI } = responses);

            console.log('infoMartAPI keys:', Object.keys(infoMartAPI));

            // infoMartAPI has NO filters array - use visId scoping only
            infoRepArray = infoMartAPI.information_representation || [];

            // No dynamic filter defs - infoMartAPI has no filters property
            // Initialize scoping with visibility only (no custom filters)
            essInitViewScoping(
                redrawView,
                ['SYS_CONTENT_APPROVAL_STATUS'],
                [],    // empty filters - no dynamic filter UI
                true
            );

            buildViewModel();

        } catch (error) {
            console.error('Error:', error);
        }
    }

    executeFetchAndRender();
});

var redrawView = function() {
    essResetRMChanges();

    let visibilityDef = new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS');

    let typeInfo = {
        className: 'Information_Representation',
        label: 'Information Store',
        icon: 'fa-database'
    };

    scopedInfoReps = essScopeResources(
        infoRepArray,
        [visibilityDef],
        typeInfo
    );

    renderView(scopedInfoReps.resources);
};
```

**infoMartAPI scopeable properties by array:**

| Array | orgUserIds | geoIds | visId | Notes |
|-------|-----------|--------|-------|-------|
| `information_representation` | ✗ | ✗ | ✓ `visId` | Scope by visibility only |
| `data_objects` | ✗ | ✗ | ✗ | No scoping properties |
| `data_subjects` | ✗ | ✗ | ✗ | No scoping properties |

If you need org or geo scoping on information stores, join against `busCapAppMartApps.applications`
via `app_infoRep_Pairs` to get the app's `orgUserIds` and `geoIds`.

---

### Pattern 5: busCapAppMartApps / busCapAppMartCaps Scoping

These are the richest Mart APIs and both expose a `filters` array. Use `busCapAppMartApps` as the
primary anchor for application-centric views; use `busCapAppMartCaps` for capability heatmaps.

```javascript
let busCapAppMartApps, busCapAppMartCaps;
var appsArray, capsArray, dynamicAppFilterDefs, dynamicCapFilterDefs;
var scopedApps, scopedCaps;

$(document).ready(function() {
    const apiList = ['busCapAppMartApps', 'busCapAppMartCaps'];

    async function executeFetchAndRender() {
        try {
            let responses = await fetchAndRenderData(apiList);
            ({ busCapAppMartApps, busCapAppMartCaps } = responses);

            // busCapAppMartApps: primary data array is .applications
            appsArray = busCapAppMartApps.applications || [];
            let appFilters = busCapAppMartApps.filters || [];

            dynamicAppFilterDefs = appFilters.map(function(f) {
                return new ScopingProperty(f.slotName, f.valueClass);
            });

            // busCapAppMartCaps: primary data arrays are .busCaptoAppDetails and .busCapHierarchy
            capsArray = busCapAppMartCaps.busCaptoAppDetails || [];
            let capFilters = busCapAppMartCaps.filters || [];

            dynamicCapFilterDefs = capFilters.map(function(f) {
                return new ScopingProperty(f.slotName, f.valueClass);
            });

            buildViewModel();

            // Use app filters to drive the scoping UI
            // (cap filters from busCapAppMartCaps can be merged if needed)
            essInitViewScoping(
                redrawView,
                ['Group_Actor', 'Geographic_Region', 'SYS_CONTENT_APPROVAL_STATUS'],
                appFilters,
                true
            );

        } catch (error) {
            console.error('Error:', error);
        }
    }

    executeFetchAndRender();
});

var redrawView = function() {
    essResetRMChanges();

    // Scope applications
    scopedApps = essScopeResources(
        appsArray,
        [
            new ScopingProperty('orgUserIds', 'Group_Actor'),
            new ScopingProperty('geoIds', 'Geographic_Region'),
            new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS')
        ].concat(dynamicAppFilterDefs),
        { className: 'Composite_Application_Provider', label: 'Application', icon: 'fa-desktop' }
    );

    // Scope capabilities - busCaptoAppDetails uses domainIds and orgUserIds
    scopedCaps = essScopeResources(
        capsArray,
        [
            new ScopingProperty('orgUserIds', 'Group_Actor'),
            new ScopingProperty('domainIds', 'Business_Domain'),
            new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS')
        ].concat(dynamicCapFilterDefs),
        { className: 'Business_Capability', label: 'Capability', icon: 'fa-puzzle-piece' }
    );

    renderView(scopedApps.resources, scopedCaps.resources);
};
```

**busCapAppMartApps filter slot names (from API `filters` array):**

The filters array is dynamic and driven by enumeration slots on `Application_Provider`. Common ones
include:

| slotName | valueClass | Description |
|----------|-----------|-------------|
| `lifecycle_status_application_provider` | `Lifecycle_Status` | Under Planning, Production, Retired, etc. |
| `ap_delivery_model` | `AP_Delivery_Model` | SaaS, On-premise, Private Cloud, etc. |
| `ap_codebase_status` | `AP_Codebase_Status` | Bespoke, Packaged, etc. |
| `application_provider_purpose` | `Application_Provider_Purpose` | Business Application, etc. |
| `ap_disposition_lifecycle_status` | `AP_Disposition_Lifecycle_Status` | Retain, Replace, Retire, etc. |

Always read the `filters` array at runtime rather than hardcoding these — the set varies per
repository configuration.

---

### Pattern 6: Scoping Two Arrays Simultaneously

When a view needs both applications AND capabilities scoped together (e.g. a capability heatmap
that only shows apps in scope), scope each array independently then cross-reference by ID.

```javascript
var appsArray, capsArray;
var dynamicAppFilterDefs = [];
var scopedApps, scopedCaps;

// After fetching...
var redrawView = function() {
    essResetRMChanges();

    // Step 1: Scope the applications
    scopedApps = essScopeResources(
        appsArray,
        [
            new ScopingProperty('orgUserIds', 'Group_Actor'),
            new ScopingProperty('geoIds', 'Geographic_Region'),
            new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS')
        ].concat(dynamicAppFilterDefs),
        { className: 'Composite_Application_Provider', label: 'Application', icon: 'fa-desktop' }
    );

    // Build a Set of in-scope app IDs for fast lookup
    var inScopeAppIds = new Set(scopedApps.resources.map(function(a) { return a.id; }));

    // Step 2: Scope capabilities by filtering to those that have at least one in-scope app
    // busCaptoAppDetails[].apps is an array of app ID strings
    var filteredCaps = capsArray.filter(function(cap) {
        var capApps = cap.apps || cap.thisapps || [];
        return capApps.some(function(appId) { return inScopeAppIds.has(appId); });
    });

    // Step 3: For each scoped cap, filter its apps list to in-scope only
    var enrichedCaps = filteredCaps.map(function(cap) {
        var capApps = cap.apps || cap.thisapps || [];
        return Object.assign({}, cap, {
            scopedApps: capApps.filter(function(appId) { return inScopeAppIds.has(appId); })
        });
    });

    renderCapabilityHeatmap(enrichedCaps, scopedApps.resources);
};
```

**Key principle**: `essScopeResources` is called once per array. Never try to pass two arrays to a
single call. Cross-reference afterward using the returned `.resources` or `.resourceIds`.

---

### Pattern 7: Scaffold Filter Extraction Bug — Correct Pattern

The `generate_view_scaffold` tool emits a broken filter extraction line:

```javascript
// BROKEN - generated by scaffold, do NOT use:
let primaryAPI = {api_labels[0]};
```

This is invalid JavaScript. Always replace it with explicit extraction:

```javascript
// CORRECT - explicit extraction from named API response:
let filters = busCapAppMartApps.filters || [];
workingArray = busCapAppMartApps.applications || [];

dynamicFilterDefs = filters.map(function(filterdef) {
    return new ScopingProperty(filterdef.slotName, filterdef.valueClass);
});
```

The pattern to follow is always:
1. Name the API explicitly (e.g. `busCapAppMartApps.filters`)
2. Provide a `|| []` fallback so it doesn't throw if the property is absent
3. Map to `ScopingProperty` objects before passing to `essInitViewScoping`

---

## Scoping Property Reference by API

Quick lookup: which scoping properties are available on each API's primary data array.

| API Label | Primary Array | orgUserIds | geoIds | visId | domainIds | filters |
|-----------|--------------|:---------:|:------:|:-----:|:---------:|:-------:|
| `busCapAppMartApps` | `.applications` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `busCapAppMartCaps` | `.busCaptoAppDetails` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `appMartAPI` | `.applications` | ✗ | ✗ | ✓ | ✗ | ✗ |
| `ImpBusCapApi` | `.businessCapabilities` | ✗ | ✓ | ✓ | ✓ | ✗ |
| `ImpAppsApi` | `.applications` | ✗ | ✗ | ✓ | ✗ | ✗ |
| `ImpTechProdApi` | `.technology_products` | ✓ | ✗ | ✓ | ✗ | ✓ |
| `techProdSvc` | `.technology_products` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `infoMartAPI` | `.information_representation` | ✗ | ✗ | ✓ | ✗ | ✗ |
| `planDataAPi` | `.allProject` | ✓ | ✗ | ✓ | ✗ | ✗ |
| `orgSummary` | `.orgData` | ✗ | ✗ | ✗ | ✗ | ✗ |

**Rule of thumb**: If the API name contains "Mart" or ends in "Svc", it almost certainly has a
`filters` array. Import APIs (`Imp*`) rarely do.
