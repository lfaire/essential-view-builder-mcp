# ⚠️ CRITICAL: DEPRECATED PATTERNS - DO NOT USE

## READ THIS FIRST BEFORE BUILDING ANY VIEW

---

## ❌ NEVER USE: Old XSLT Data Access Pattern

**THIS PATTERN IS COMPLETELY DEPRECATED AND MUST NEVER BE USED:**

```xml
<!-- ❌ WRONG - DEPRECATED - DO NOT USE -->
<xsl:variable name="appMartAPI" select="$utilitiesAllDataSetAPIs[contains(...)]"/>
<xsl:variable name="apiLabel" select="if ($appMartAPI) then translate(...) else ''"/>
```

**Why this appears in some contexts:**
- Old views from 2019-2022 used this pattern
- Some documentation may still reference it
- It appears in legacy XSL files that haven't been migrated

**Why it's wrong:**
- Requires server-side XSLT variable access
- Doesn't work with the current Essential Viewer architecture
- Causes "entity reference" XML parsing errors
- Bypasses the client-side rendering model

---

## ✅ CORRECT PATTERN: Client-Side API Fetching

**ALL new views MUST use this pattern:**

```javascript
<script>
    <xsl:call-template name="RenderViewerAPIJSFunction"/>
</script>

<script>
    <![CDATA[
    
    let appMartAPI, infoMartAPI;
    
    $(document).ready(function() {
        const apiList = ['appMartAPI', 'infoMartAPI'];
        
        async function executeFetchAndRender() {
            try {
                let responses = await fetchAndRenderData(apiList);
                ({ appMartAPI, infoMartAPI } = responses);
                
                console.log('Data loaded:', responses);
                
                // Now use the data in JavaScript
                buildViewModel();
                renderView();
                
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        executeFetchAndRender();
    });
    
    ]]>
</script>
```

---

## ❌ NEVER USE: Ampersand Without Encoding

**THIS CAUSES XML PARSING ERRORS:**

```javascript
// ❌ WRONG - Outside CDATA section
if (data && data.items) { }  // XML parser error: "entity reference"
const url = "?param1=x&param2=y";  // XML parser error
```

**Why it's wrong:**
- XML parsers interpret `&` as the start of an entity reference (like `&amp;`)
- Causes "The entity name must immediately follow the '&'" error
- Breaks the entire XSL file compilation

---

## ✅ CORRECT PATTERN: CDATA or Encoding

**INSIDE CDATA sections (your JavaScript code):**

```javascript
<![CDATA[
// ✓ CORRECT - Inside CDATA, use plain &
if (data && data.items) { }
const url = "?param1=x&param2=y";
]]>
```

**OUTSIDE CDATA (in XML attributes):**

```xml
<!-- ✓ CORRECT - Outside CDATA, use &amp; -->
<xsl:attribute name="href">report?cl=en-gb&amp;XSL=view.xsl</xsl:attribute>
```

---

## ❌ NEVER MIX: Template Calls and CDATA

**THIS BREAKS XSL COMPILATION:**

```xml
<!-- ❌ WRONG - Cannot mix template calls with CDATA -->
<script>
    <xsl:call-template name="RenderViewerAPIJSFunction"/>
    <![CDATA[
    const apiList = ['appMartAPI'];
    ]]>
</script>
```

**Why it's wrong:**
- XSL processors cannot parse mixed content
- Template calls execute at compile time
- CDATA is literal content
- Mixing them causes parser errors

---

## ✅ CORRECT PATTERN: Separate Script Blocks

```xml
<!-- ✓ CORRECT - Separate blocks for each template call -->
<script>
    <xsl:call-template name="RenderViewerAPIJSFunction"/>
</script>

<script>
    <xsl:call-template name="RenderHandlebarsUtilityFunctions"/>
</script>

<!-- ✓ CORRECT - Separate block for your JavaScript -->
<script>
    <![CDATA[
    const apiList = ['appMartAPI'];
    
    $(document).ready(function() {
        // Your code here
    });
    ]]>
</script>
```

---

## How to Detect Wrong Patterns

### Red Flags in Generated Code:

1. **ANY reference to `$utilitiesAllDataSetAPIs`** → STOP, wrong pattern
2. **ANY reference to `translate(translate(...))` in XSL** → STOP, wrong pattern
3. **ANY reference to `own_slot_value[slot_reference = 'dsa_data_label']`** → STOP, wrong pattern
4. **`&` without CDATA or `&amp;` encoding** → STOP, will cause XML error
5. **Template calls inside CDATA blocks** → STOP, will fail
6. **CDATA blocks inside template calls** → STOP, will fail

### Green Flags in Correct Code:

1. ✓ `fetchAndRenderData(apiList)` in JavaScript
2. ✓ `const apiList = ['appMartAPI', 'infoMartAPI']`
3. ✓ `async function executeFetchAndRender()`
4. ✓ Separate `<script>` blocks for template calls and CDATA
5. ✓ Plain `&` inside CDATA sections
6. ✓ `&amp;` in XML attributes outside CDATA

---

## The Golden Pattern (Always Start Here)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
    xpath-default-namespace="http://protege.stanford.edu/xml" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xalan="http://xml.apache.org/xslt" 
    xmlns:pro="http://protege.stanford.edu/xml" 
    xmlns:eas="http://www.enterprise-architecture.org/essential" 
    xmlns:functx="http://www.functx.com" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:ess="http://www.enterprise-architecture.org/essential/errorview">
    
    <!-- IMPORT MUST COME FIRST -->
    <xsl:import href="../common/core_js_functions.xsl"/>
    
    <!-- REQUIRED INCLUDES -->
    <xsl:include href="../common/core_doctype.xsl"/>
    <xsl:include href="../common/core_common_head_content.xsl"/>
    <xsl:include href="../common/core_header.xsl"/>
    <xsl:include href="../common/core_footer.xsl"/>
    <xsl:include href="../common/core_external_doc_ref.xsl"/>
    <xsl:include href="../common/core_api_fetcher.xsl"/>
    <xsl:include href="../common/core_handlebars_functions.xsl"/>
    
    <xsl:output method="html" omit-xml-declaration="yes" indent="yes"/>
    <xsl:param name="param1"/>
    <xsl:param name="viewScopeTermIds"/>
    
    <xsl:variable name="viewScopeTerms" select="eas:get_scoping_terms_from_string($viewScopeTermIds)"/>
    <xsl:variable name="linkClasses" select="('Composite_Application_Provider', 'Application_Provider')"/>
    
    <xsl:template match="knowledge_base">
        <xsl:call-template name="docType"/>
        <html>
            <head>
                <xsl:call-template name="commonHeadContent"/>
                <xsl:call-template name="RenderModalReportContent">
                    <xsl:with-param name="essModalClassNames" select="$linkClasses"/>
                </xsl:call-template>
                
                <title>Your View Title</title>
                
                <style>
                    .view-wrapper {
                        padding: 20px;
                        max-width: 1400px;
                        margin: 80px auto 0 auto;
                    }
                </style>
                
                <!-- Template call in separate script block -->
                <script>
                    <xsl:call-template name="RenderViewerAPIJSFunction"/>
                </script>
                
                <!-- Your JavaScript in separate CDATA block -->
                <script>
                    <![CDATA[
                    
                    let appMartAPI, infoMartAPI;
                    var viewModel = {};
                    
                    $(document).ready(function() {
                        const apiList = ['appMartAPI', 'infoMartAPI'];
                        
                        async function executeFetchAndRender() {
                            try {
                                let responses = await fetchAndRenderData(apiList);
                                ({ appMartAPI, infoMartAPI } = responses);
                                
                                console.log('Responses loaded:', responses);
                                
                                buildViewModel();
                                renderView();
                                
                            } catch (error) {
                                console.error('Error loading data:', error);
                            }
                        }
                        
                        executeFetchAndRender();
                    });
                    
                    function buildViewModel() {
                        // Process API responses here
                        viewModel.applications = appMartAPI.applications || [];
                        console.log('View model built:', viewModel);
                    }
                    
                    function renderView() {
                        // Render your HTML here
                        let html = '<h2>Applications (' + viewModel.applications.length + ')</h2>';
                        $('#mainContent').html(html);
                    }
                    
                    ]]>
                </script>
            </head>
            <body>
                <xsl:call-template name="Heading"/>
                
                <div class="view-wrapper">
                    <div id="mainContent">
                        <p>Loading...</p>
                    </div>
                </div>
                
                <xsl:call-template name="Footer"/>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
```

---

## Why These Errors Happen

**Root causes:**

1. **Training Data Contamination**: AI models trained on old Essential views from 2019-2022
2. **Pattern Recognition**: Old XSL variables look "correct" to pattern-matching systems
3. **Documentation Lag**: Some Essential documentation still shows deprecated patterns
4. **Example Pollution**: Legacy view files in the codebase serve as bad examples

**Prevention:**

1. **Always check the resource docs FIRST** before generating any code
2. **Reject any code containing `$utilitiesAllDataSetAPIs`** immediately
3. **Verify CDATA usage** in every script block
4. **Test for XML errors** by attempting to load the XSL file

---

## Self-Check Questions Before Submitting Code

❓ **Does the code contain `$utilitiesAllDataSetAPIs`?**  
→ If YES: REJECT, use `fetchAndRenderData()` instead

❓ **Does the code contain `own_slot_value[slot_reference = 'dsa_data_label']`?**  
→ If YES: REJECT, use direct API labels in `apiList`

❓ **Are there `&` characters outside CDATA sections?**  
→ If YES: REJECT, wrap in CDATA or use `&amp;`

❓ **Are template calls mixed with CDATA in the same `<script>` block?**  
→ If YES: REJECT, separate into multiple blocks

❓ **Does the JavaScript use `async/await` with `fetchAndRenderData()`?**  
→ If NO: REJECT, must use the async fetch pattern

❓ **Is there a `<xsl:call-template name="RenderViewerAPIJSFunction"/>`?**  
→ If NO: REJECT, this is required for API fetching

---

## Quick Decision Tree

```
START: Need to build a view
    ↓
    ↓── Read essential-view://view-build-docs FIRST
    ↓
    ↓── Use the Golden Pattern above
    ↓
    ↓── Check API labels in essential-view://api-docs
    ↓
    ↓── Does generated code contain "$utilitiesAllDataSetAPIs"?
        ├─ YES → REJECT, regenerate with fetchAndRenderData
        └─ NO  → Continue
    ↓
    ↓── Does generated code have "&" outside CDATA?
        ├─ YES → REJECT, wrap in CDATA or use &amp;
        └─ NO  → Continue
    ↓
    ↓── Are template calls and CDATA mixed?
        ├─ YES → REJECT, separate into blocks
        └─ NO  → Continue
    ↓
    ↓── Does code use fetchAndRenderData(apiList)?
        ├─ YES → PROCEED
        └─ NO  → REJECT, must use async fetch
```

---

## Emergency Fix Guide

**If you encounter a view with the old pattern:**

### Step 1: Remove old XSLT variables

```xml
<!-- DELETE these lines completely -->
<xsl:variable name="appMartAPI" select="$utilitiesAllDataSetAPIs[...]"/>
<xsl:variable name="apiLabel" select="..."/>
```

### Step 2: Add the async fetch pattern

```javascript
<script>
    <xsl:call-template name="RenderViewerAPIJSFunction"/>
</script>

<script>
    <![CDATA[
    
    let appMartAPI;
    
    $(document).ready(function() {
        const apiList = ['appMartAPI'];
        
        async function executeFetchAndRender() {
            try {
                let responses = await fetchAndRenderData(apiList);
                ({ appMartAPI } = responses);
                
                // Continue with the rest of the view logic...
                
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        executeFetchAndRender();
    });
    
    ]]>
</script>
```

### Step 3: Wrap all JavaScript in CDATA

Move ANY code containing `&` characters inside CDATA blocks.

### Step 4: Separate template calls

Move each `<xsl:call-template>` into its own `<script>` block, separate from CDATA.

---

## Summary

**Three Rules to Never Break:**

1. **NEVER use `$utilitiesAllDataSetAPIs`** - always use `fetchAndRenderData(apiList)`
2. **ALWAYS wrap JavaScript in CDATA** - or use `&amp;` for XML attributes
3. **ALWAYS separate template calls from CDATA** - one per `<script>` block

**If in doubt:** Start from the Golden Pattern above and modify it rather than generating from scratch.
