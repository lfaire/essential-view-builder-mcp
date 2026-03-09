# MCP Server Resource Updates - Lessons Learned

## Critical Updates Needed for view_build_documentation.md

### 1. JavaScript Script Block Pattern (MOST IMPORTANT)

**Add this section to replace/update the script structure guidance:**

```markdown
### 1.4 JavaScript Section Pattern (CRITICAL)

**CORRECT Pattern** (from working views):

```xml
<script type="text/javascript">
    <xsl:call-template name="RenderViewerAPIJSFunction"/>
    
    <!-- Declare variables for destructuring -->
    let appMartAPI, infoMartAPI, ImpBusCapApi;
    
    var viewModel = {
        applications: [],
        costs: []
    };
    
    $(document).ready(function() {
        const apiList = ['appMartAPI', 'infoMartAPI', 'ImpBusCapApi'];
        
        async function executeFetchAndRender() {
            try {
                let responses = await fetchAndRenderData(apiList);
                ({ appMartAPI, infoMartAPI, ImpBusCapApi } = responses);
                
                // Process data
                buildViewModel(responses);
                renderView();
                
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        executeFetchAndRender();
    });
    
    function buildViewModel(responses) {
        // Your code here
    }
</script>
```

**Key Rules:**
1. **Single `<script type="text/javascript">` tag** - not multiple script blocks
2. **NO CDATA section** - XSL template calls and JavaScript go directly in the script tag
3. **Template call at top** - `<xsl:call-template name="RenderViewerAPIJSFunction"/>` first
4. **Declare variables** - before $(document).ready for destructuring to work
5. **Wrap in $(document).ready()** - for proper initialization
6. **async/await with destructuring** - `({ apiName1, apiName2 } = responses);`

**WRONG Patterns:**
```xml
<!-- DON'T DO THIS - Multiple script blocks -->
<script><xsl:call-template name="RenderViewerAPIJSFunction"/></script>
<script><xsl:call-template name="RenderHandlebarsUtilityFunctions"/></script>
<script><![CDATA[ /* code */ ]]></script>

<!-- DON'T DO THIS - CDATA section -->
<script><![CDATA[
    const apiList = ['appMartAPI'];
]]></script>

<!-- DON'T DO THIS - Callback pattern -->
fetchAndRenderData(apiList, callback);

<!-- DON'T DO THIS - Window object access -->
if (window.appMartAPI) { }
```
```

### 2. Ampersand Encoding Rules (CRITICAL)

**Update the ampersand section with this:**

```markdown
### 1.5 Ampersand Encoding (NO CDATA Context)

Since we don't use CDATA, all JavaScript operators must be XML-encoded:

**CRITICAL RULE**: `&amp;&amp;` must have **NO SPACE** after it

**CORRECT:**
```javascript
if (responses.appMartAPI &amp;&amp;responses.appMartAPI.applications) {
    // Note: NO SPACE between &amp;&amp; and "responses"
}

const value = (busCapData &amp;&amp;busCapData.capabilities) ? busCapData.capabilities : [];
```

**WRONG:**
```javascript
if (responses.appMartAPI &amp;&amp; responses.appMartAPI.applications) {
    // SPACE after &amp;&amp; breaks the condition!
}
```

**Other operators:**
- Comparison: `&lt;`, `&gt;`, `&lt;=`, `&gt;=`
- Logical: `||` (no encoding needed)
- NOT: `!` (no encoding needed)
```

### 3. API Property Name Verification

**Add this new section:**

```markdown
## 6. API Property Name Verification (CRITICAL)

**NEVER ASSUME** property names from documentation alone. The API catalogue may not reflect the actual JSON structure.

**Required Process:**
1. When using an API, ALWAYS verify the actual property names by testing
2. Check the first element of arrays to see actual structure
3. Update your code to match the ACTUAL structure, not the documented one

**Common Mismatches:**

| API | Documentation Says | Actually Is |
|-----|-------------------|-------------|
| `appLifecycle` | `.lifecycles` | `.application_lifecycles` |
| `appCostApi` | `.application_costs` | `.applicationCost` |
| `appOrgId` | `.organisations` | `.applicationOrgUsers` |
| `appKpiAPI` | `.kpis` | `.applications` |

**How to Verify:**
```javascript
// Test code to add during development:
fetchAndRenderData(['appMartAPI']).then(responses => {
    console.log('Keys:', Object.keys(responses.appMartAPI));
    console.log('First item:', responses.appMartAPI.applications?.[0]);
});
```

**Template for buildViewModel:**
```javascript
function buildViewModel(responses) {
    // ALWAYS use actual property names from API, not assumed names
    if (responses.appMartAPI &amp;&amp;responses.appMartAPI.applications) {
        viewModel.applications = responses.appMartAPI.applications;
    }
    
    // Check property names match actual API structure
    if (responses.appLifecycle &amp;&amp;responses.appLifecycle.application_lifecycles) {
        viewModel.lifecycle = responses.appLifecycle.application_lifecycles;
    }
}
```
```

### 4. Cost Data Structure

**Add this important note:**

```markdown
## 7. Common Data Location Patterns

### Cost Data
**IMPORTANT**: Application cost data is typically EMBEDDED in each application object, not in a separate API.

**appMartAPI structure:**
```javascript
{
    applications: [
        {
            id: "...",
            name: "...",
            costs: [
                { cost: "1500", name: "Hosting Cost", ... }
            ]
        }
    ]
}
```

**To calculate total costs:**
```javascript
const totalCost = viewModel.applications.reduce((sum, app) => {
    const appCosts = app.costs || [];
    const appTotal = appCosts.reduce((appSum, cost) => {
        return appSum + parseFloat(cost.cost || 0);
    }, 0);
    return sum + appTotal;
}, 0);
```

**Note**: `appCostApi` may return empty arrays. Use embedded costs in applications instead.
```

### 5. Import/Include Requirements

**Clarify the import section:**

```markdown
### 1.1 Required XSL Structure

**CRITICAL**: All views MUST have these imports/includes:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xpath-default-namespace="http://protege.stanford.edu/xml" ...>
    
    <!-- IMPORT MUST COME FIRST -->
    <xsl:import href="../common/core_js_functions.xsl"/>
    
    <!-- THEN INCLUDES (some may be optional depending on your Essential version) -->
    <xsl:include href="../common/core_doctype.xsl"/>
    <xsl:include href="../common/core_common_head_content.xsl"/>
    <xsl:include href="../common/core_header.xsl"/>
    <xsl:include href="../common/core_footer.xsl"/>
    <xsl:include href="../common/core_external_doc_ref.xsl"/>
    <xsl:include href="../common/core_api_fetcher.xsl"/>
    
    <xsl:output method="html" omit-xml-declaration="yes" indent="yes"/>
    <xsl:param name="param1"/>
    <xsl:param name="viewScopeTermIds"/>
    
    <xsl:variable name="viewScopeTerms" select="eas:get_scoping_terms_from_string($viewScopeTermIds)"/>
    <xsl:variable name="linkClasses" select="('Composite_Application_Provider', 'Application_Provider')"/>
```

**Note**: Some includes like `core_el_ref_model_include.xsl`, `core_roadmap_functions.xsl`, and `core_handlebars_functions.xsl` are OPTIONAL depending on your needs.
```

## Updates for MCP Server Code (Python/JavaScript)

### 1. Template Generation Function

Update your scaffold generator to use this pattern:

```python
def generate_script_section(api_list):
    """Generate the JavaScript section with correct pattern"""
    
    # Declare variables for destructuring
    var_declarations = ', '.join(api_list)
    
    # Generate destructuring
    destructuring = '({ ' + ', '.join(api_list) + ' } = responses);'
    
    script = f'''<script type="text/javascript">
    <xsl:call-template name="RenderViewerAPIJSFunction"/>
    
    let {var_declarations};
    
    var viewModel = {{
        applications: [],
        lifecycle: [],
        costs: []
    }};
    
    $(document).ready(function() {{
        const apiList = {api_list};
        
        async function executeFetchAndRender() {{
            try {{
                let responses = await fetchAndRenderData(apiList);
                {destructuring}
                
                console.log('Responses loaded:', responses);
                
                buildViewModel(responses);
                renderView();
                
            }} catch (error) {{
                console.error('Error loading data:', error);
            }}
        }}
        
        executeFetchAndRender();
    }});
    
    function buildViewModel(responses) {{
        // TODO: Add data processing here
    }}
    
    function renderView() {{
        // TODO: Add rendering logic here
    }}
</script>'''
    
    return script
```

### 2. Ampersand Encoding Function

```python
def encode_for_xsl(javascript_code):
    """
    Encode JavaScript for XSL context (no CDATA)
    CRITICAL: Preserve no-space pattern for &&
    """
    # Replace && with &amp;&amp; but preserve adjacent characters
    # Pattern: identifier&&identifier should become identifier&amp;&amp;identifier
    code = javascript_code.replace('&&', '&amp;&amp;')
    
    # Replace comparison operators
    code = code.replace('<=', '&lt;=')
    code = code.replace('>=', '&gt;=')
    code = code.replace('<', '&lt;')
    code = code.replace('>', '&gt;')
    
    return code
```

### 3. Property Name Validator

```python
def verify_api_property(api_label, property_path):
    """
    Verify actual API property names against documentation
    Returns tuple: (is_valid, actual_property_name, suggestion)
    """
    
    # Known mismatches
    property_corrections = {
        'appLifecycle': {
            'lifecycles': 'application_lifecycles',
        },
        'appCostApi': {
            'application_costs': 'applicationCost',
        },
        'appOrgId': {
            'organisations': 'applicationOrgUsers',
        },
        'appKpiAPI': {
            'kpis': 'applications',
        }
    }
    
    if api_label in property_corrections:
        if property_path in property_corrections[api_label]:
            correct_name = property_corrections[api_label][property_path]
            return (False, correct_name, f"Use '{correct_name}' instead of '{property_path}'")
    
    return (True, property_path, None)
```

## Documentation Updates Summary

### High Priority ⚠️
1. **Script block pattern** - Single script, no CDATA, specific structure
2. **Ampersand spacing** - `&amp;&amp;` with NO SPACE after
3. **Property name verification** - Don't trust documentation, verify actual structure
4. **async/await with destructuring** - Specific pattern required

### Medium Priority
5. **Cost data location** - Embedded in applications, not separate API
6. **Import/include order** - Import first, then includes
7. **Error patterns** - Common mistakes and how to fix them

### Low Priority
8. **Optional includes** - Clarify which are required vs optional
9. **Testing templates** - Add code snippets for verifying API structure
10. **Example working view** - Reference to johan_view.xsl pattern

### 6. Roadmap Timeline Robustness
When implementing Gantt or Timeline charts (e.g., using Chart.js):

**CRITICAL: Explicit Date Scaling**
Avoid the 1970 Unix epoch fallback by explicitly calculating the min/max dates from your data.
```javascript
const allDates = timelineData.flatMap(d => [new Date(d.start), new Date(d.end)]);
const minDate = new Date(Math.min(...allDates));
const maxDate = new Date(Math.max(...allDates));
minDate.setMonth(minDate.getMonth() - 1); // Add buffer
maxDate.setMonth(maxDate.getMonth() + 1);

// In Chart.js options:
scales: {
    x: {
        type: 'time',
        min: minDate,
        max: maxDate,
        // ...
    }
}
```

**Data Access Patterns**
The `planDataAPi` structure can vary between `allProject` and `allProjects`. Always handle both:
```javascript
const projects = responses.planDataAPi.allProjects || responses.planDataAPi.allProject || [];
```

### 7. View Layout & CSS Isolation
To prevent custom dashboard styles from breaking standard Essential Viewer navigation:

1. **Isolation Wrapper**: Move all dashboard-specific backgrounds and global text colors to a dedicated wrapper class (e.g., `.cio-dashboard-wrapper`).
2. **Standard Headers**: Do NOT wrap `<xsl:call-template name="Heading"/>` or `ViewUserScopingUI` inside your custom theme wrapper. They should be siblings.
3. **Fixed Bar Margins**: Add `margin-top: 40px` (or 80px if scoping is enabled) to your main content container to prevent it from being hidden under the fixed viewpoint bar.

```xml
<body>
    <xsl:call-template name="Heading"/>
    <xsl:call-template name="ViewUserScopingUI"/>
    <div class="custom-view-wrapper">
        <div class="main-content-container">
            <!-- Dashboard content here -->
        </div>
    </div>
</body>
```

### 8. Design Philosophy: Visual Compactness
For executive dashboards:
- Avoid forced `min-height: 350px` for metric cards.
- Use flexible padding and flexbox to keep KPIs compact.
- Ensure critical charts are visible without excessive scrolling by using constrained container heights (e.g., `height: 250px` for small charts, `400px` for roadmaps).

## Files to Update

1. **view_build_documentation.md** - Add all sections above
2. **MCP server scaffold generator** - Update to use correct script pattern
3. **MCP server validation** - Add property name verification
4. **Example template** - Create `working_view_template.xsl` with correct pattern

## Testing Checklist

After updates, generate a test view and verify:
- [ ] Single `<script type="text/javascript">` tag
- [ ] No CDATA sections
- [ ] `&amp;&amp;` has no space after it
- [ ] Template call at top of script
- [ ] Variables declared before $(document).ready
- [ ] async/await with destructuring pattern
- [ ] Property names verified against actual API
- [ ] Import comes before includes

### 9. XSLT API Cache Management (Tomcat)
When developing or modifying XSLT APIs in a Tomcat environment, the results may be cached even after file updates.
- **Symptom**: You update the XSL API file, but the JSON response remains the same or shows old data.
- **Manual Fix**: Clear the cache directory at `platform/tmp/reportApiCache/`.
- **Development Best Practice**: When an API is acting "stubborn," version the filename (e.g., append `_v2.xsl`, `_v3.xsl`) and update the calling View. This forces Tomcat to compile and cache a fresh instance.

### 10. Resilient XPath Selection for APIs
Relying on `xpath-default-namespace` or relative paths (like `node()/simple_instance`) can be fragile if the XML structure varies or the namespace context shifts.
- **Rule**: Use explicit namespace prefixes for all element selections (e.g., `xmlns:pro="http://protege.stanford.edu/xml"`).
- **Pattern**: Use `//pro:simple_instance` instead of `/node()/simple_instance` to ensure you find instances regardless of their depth in the `reportXML.xml`.

### 11. ID Normalization at the Source
Data in Essential often contains leading/trailing whitespace or carriage returns that are invisible in the source XML but break string matching in JavaScript.
- **XSL Rule**: Always use `normalize-space(string(.))` when extracting instance names or IDs in your API.
- **JS Rule**: Always apply `.trim()` to IDs retrieved from the API before performing `.includes()` or `===` comparisons.

### 12. API Diagnostic Metadata
To debug "invisible data" issues (where instances exist in the XML but are filtered out by the API), include a debug/metadata block in the JSON response during development.
- **Pattern**:
```json
{
    "_metadata": {
        "evaluationDate": "2026-01-28",
        "totalInstancesEvaluated": 21638,
        "matchingInstancesFound": 275,
        "validItemsReturned": 14
    },
    "items": [ ... ]
}
```

### 13. API Discovery Procedure
Before creating a new API, agents MUST:
1.  **Search Existing APIs**: Use `grep` or `find` to look for existing XSL files in the `api` directories that handle the required classes.
2.  **Consult the User**: If a similar API exists, ask the user if it should be extended or if a new one is truly necessary. Avoid creating redundant "custom" APIs that duplicate existing logic.

### 14. Building HTML Dynamically in JavaScript (XSL Context)

**CRITICAL**: Never use string-based HTML construction inside `<script>` blocks within XSL.

**Problem**: The `<` and `>` characters in HTML strings like `'<tr><td>'` are invalid XML and will break the XSL processor at compile time, not at runtime.

**Broken approaches** (all fail):
```javascript
// ✗ Raw HTML strings - XML parser rejects < >
var html = '<tr><td>' + value + '</td></tr>';

// ✗ CDATA sections - v2.0 pattern forbids CDATA
var html = '<![CDATA[<tr>]]>';

// ✗ xsl:text disable-output-escaping - fragile, hard to maintain
```

**Correct approaches**:
```javascript
// ✓ DOM API (PREFERRED - zero escaping issues)
var tr = document.createElement('tr');
var td = document.createElement('td');
td.textContent = value;  // Auto-escapes content
tr.appendChild(td);
container.appendChild(tr);

// ✓ jQuery element creation (using &lt; &gt; entities)
var tr = $('&lt;tr&gt;');
tr.append($('&lt;td&gt;').text(value));
container.append(tr);
```

**Rule**: Use `document.createElement()` for all dynamic HTML. It avoids every XML/XSL escaping problem.

### 15. Excel Export Views

Views that export data to Excel are **standard HTML views** (same imports, same API fetcher, same `method="html"` output). The Excel file is generated **client-side** using ExcelJS.

**Do NOT** try to output SpreadsheetML XML directly from XSL. The Essential Viewer report engine requires all views to be HTML views with the standard import/include chain.

**Available library**: `js/exceljs/exceljs.min.js`

**Pattern**:
1. Standard HTML view loads data via `fetchAndRenderData()`
2. Renders a preview table using DOM API
3. "Download Excel" button generates `.xlsx` using ExcelJS
4. Uses `Blob` + `URL.createObjectURL` for download

**Include in head**:
```xml
<script src="js/exceljs/exceljs.min.js" type="text/javascript"/>
```

**Reference implementation**: `application/core_al_app_cost_excel_export.xsl`

### 16. Complete Import/Include List (MANDATORY)

Every view MUST include ALL of these. Omitting any one will cause failures:

```xml
<!-- IMPORT MUST COME FIRST -->
<xsl:import href="../common/core_js_functions.xsl"/>

<!-- ALL REQUIRED INCLUDES (order matters) -->
<xsl:include href="../common/core_doctype.xsl"/>
<xsl:include href="../common/core_common_head_content.xsl"/>
<xsl:include href="../common/core_header.xsl"/>
<xsl:include href="../common/core_footer.xsl"/>
<xsl:include href="../common/core_external_doc_ref.xsl"/>
<xsl:include href="../common/core_api_fetcher.xsl"/>
```

**Optional includes** (only when needed):
```xml
<xsl:include href="../common/core_handlebars_functions.xsl"/>  <!-- Handlebars templates -->
<xsl:include href="../common/core_roadmap_functions.xsl"/>     <!-- Roadmap variables (rarely needed) -->
<xsl:include href="../common/datatables_includes.xsl"/>        <!-- DataTables library -->
```

### 17. Cost Object Field Reference

Each entry in `app.costs[]` (from `appMartAPI.applications[n].costs`):

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `name` | string | "Hosting Cost" | Cost component type name |
| `cost` | string | "1500" | Amount - MUST `parseFloat()` |
| `ccy_code` | string | "GBP" | ISO currency code (preferred) |
| `currency` | string | "£" | Currency symbol (fallback) |
| `fromDate` | string | "2024-01-01" | ISO 8601 start date |
| `toDate` | string | "2024-12-31" | ISO 8601 end date |
| `description` | string | "" | Free-text description |
| `costType` | string | "Annual_Cost_Component" | Essential class type |
| `id` | string | "essential_baseline..." | Instance ID |

**Note**: `appCostApi.applicationCost` is typically EMPTY. Always use embedded costs from `appMartAPI.applications[].costs[]`.
