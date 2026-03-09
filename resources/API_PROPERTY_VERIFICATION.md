# API Property Verification Guide

## CRITICAL: Never Assume Property Names

**Before using ANY property from an API response, you MUST:**

1. **Consult the API Documentation** (`api_documentation.md`)
2. **Verify the exact property path** in the documentation
3. **Never guess or assume** property names based on logical naming

## Common Mistakes to Avoid

### ❌ WRONG: Assuming Properties Exist

```javascript
// DON'T DO THIS - app.capability doesn't exist!
capability: app.capability || 'General'

// DON'T DO THIS - Hardcoding data
labels: ['Sales', 'Finance', 'HR', 'IT', 'Ops']
data: [12, 19, 3, 5, 2]
```

### ✅ CORRECT: Verify Then Use

```javascript
// 1. Check API docs: busCapAppMartApps.applications[].services exists
// 2. Use the actual property:
capability: (app.services && app.services.length > 0) ? app.services[0].name : 'General'

// 3. Build data from actual API responses:
const capLabels = Object.keys(viewModel.mappings.capabilities);
const capData = capLabels.map(label => viewModel.mappings.capabilities[label]);
```

## Property Lookup Workflow

### Step 0: The Console Reveal (Live Debugging)
Before looking at docs, **inspect the live data**. This catches naming variations immediately:
```javascript
async function executeFetchAndRender() {
    let responses = await fetchAndRenderData(apiList);
    // CRITICAL: Log keys to verify actual API structure
    console.log('API Keys:', Object.keys(responses.appMartAPI.applications[0]));
    console.log('Sample Data:', responses.appMartAPI.applications[0]);
}
```

### Step 1: Identify the API
```javascript
// You're using: busCapAppMartApps
const apiList = ['busCapAppMartApps'];
```

### Step 2: Find the API in Documentation
Search `api_documentation.md` for:
```
### core_api_el_bus_cap_to_app_mart_apps.xsl
- **DSA Data Label**: `busCapAppMartApps`
```

### Step 3: Check Available Properties
Look for the exact property path:
```
| `applications[].services` | Array | `[{"id": "store_55_Class910", "name": "Benchmarking", ...}]` |
```

### Step 4: Use the Verified Property
```javascript
// Now you know: app.services is an array of objects with .name
const serviceName = (app.services && app.services.length > 0) ? app.services[0].name : 'General';
```

## Real-World Examples

### Example 1: Application Capabilities

**❌ WRONG** (assuming):
```javascript
// Assumption: applications have a "capability" property
viewModel.applications.map(app => ({
    capability: app.capability || 'General'
}));
```

**✅ CORRECT** (verified):
```javascript
// Verified in docs: applications[].services exists
// Each service has .id and .name
viewModel.applications.map(app => ({
    capability: (app.services && app.services.length > 0) 
        ? app.services[0].name 
        : 'General'
}));
```

### Example 2: Organization Data

**❌ WRONG** (hardcoded):
```javascript
// Hardcoded fake data
const orgChart = {
    labels: ['Sales', 'Finance', 'HR'],
    data: [12, 19, 3]
};
```

**✅ CORRECT** (from API):
```javascript
// Build from actual data
const orgCounts = {};
viewModel.applications.forEach(app => {
    const orgIds = app.orgUserIds || [];
    orgIds.forEach(orgId => {
        orgCounts[orgId] = (orgCounts[orgId] || 0) + 1;
    });
});

// Then look up org names from filters or separate API
const orgChart = {
    labels: Object.keys(orgCounts),
    data: Object.values(orgCounts)
};
```

## Property Verification Checklist

Before using a property, verify:

- [ ] The API documentation lists this exact property path
- [ ] The property type matches your usage (Array, String, Object)
- [ ] You handle the case where the property might be empty/null
- [ ] You're not hardcoding any data that should come from the API

## Common API Property Patterns

### Common Mismatches (Verified)

| API | Documentation Says | Actually Is |
|-----|-------------------|-------------|
| `appLifecycle` | `.lifecycles` | `.application_lifecycles` |
| `appCostApi` | `.application_costs` | `.applicationCost` |
| `orgSummary` | `.organisations` | `.applicationOrgUsers` |
| `busKpiAPI` | `.kpis` | `.applications` |

### busCapAppMartApps
```javascript
applications[]
  .id              // String
  .name            // String
  .services        // Array of {id, name}
  .lifecycle       // String (ID reference)
  .criticality     // String
  .orgUserIds      // Array of String IDs
  .costs           // Array of cost objects
```

### appMartAPI
```javascript
applications[]
  .id              // String
  .name            // String
  .costs           // Array of {cost, name, currency}
  .supplier        // Object {id, name}
  .maxUsers        // String
```

### filters (in busCapAppMartApps)
```javascript
filters[]
  .id              // String (e.g., "Lifecycle_Status")
  .name            // String (display name)
  .values          // Array of {id, name, color}
```

## Red Flags That Indicate Assumptions

🚩 **Using a property without checking docs first**
🚩 **Hardcoded arrays of strings/numbers for chart data**
🚩 **Property names that "sound right" but aren't verified**
🚩 **Fallback values that hide missing data (use console.warn instead)**

## Diagnostic Pattern (The "Console Reveal")

If data isn't showing, add this to your `executeFetchAndRender` function:

```javascript
// 1. Log the entire API response
console.log('Full API response:', responses.appMartAPI);

// 2. Log available properties
console.log('Available properties:', Object.keys(responses.appMartAPI));

// 3. Log first item structure (CRITICAL for nested structures)
if (responses.appMartAPI.applications) {
    console.log('First item keys:', Object.keys(responses.appMartAPI.applications[0]));
    console.log('Sample item:', responses.appMartAPI.applications[0]);
}

// 4. Test specific paths
console.log('Path test:', responses.appMartAPI.applications?.[0]?.costs);
```

## Summary

**Golden Rule**: If you didn't find it in `api_documentation.md`, it doesn't exist. Never assume.
