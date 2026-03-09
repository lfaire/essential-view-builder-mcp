# Roadmap Functions Fix

## Issue
Generated views were missing `essInitViewScoping` and `redrawView` functions, causing the roadmap toolbar not to show.

## Root Cause
**Variable Scope Bug** in `server.py` function `generate_script_section_v2`:

```python
def generate_script_section_v2(..., enable_roadmap: bool):
    if enable_roadmap:
        execution_logic = '''...essInitViewScoping...'''
        additional_functions = '''...var redrawView...'''
    else:
        execution_logic = '''...'''
        additional_functions = '''...'''
    
    # BUG: execution_logic and additional_functions are local to if/else blocks
    # but used here in the f-string template:
    script = f'''...{execution_logic}...{additional_functions}...'''
```

The variables were defined **inside** the if/else blocks but used **outside** in the f-string template, causing them to be undefined.

## Fix Applied

Added variable initialization **before** the if/else blocks (lines 892-894):

```python
def generate_script_section_v2(..., enable_roadmap: bool):
    # Initialize variables that will be set in if/else blocks
    execution_logic = ""
    additional_functions = ""
    
    if enable_roadmap:
        execution_logic = '''...essInitViewScoping...'''
        additional_functions = '''...var redrawView...'''
    else:
        execution_logic = '''...'''
        additional_functions = '''...'''
    
    # Now variables are in scope
    script = f'''...{execution_logic}...{additional_functions}...'''
```

## What This Fixes

When `enable_roadmap=True`, generated views now include:

1. **`essInitViewScoping` call** (line ~909):
   ```javascript
   essInitViewScoping(
       redrawView,
       ['Group_Actor', 'Geographic_Region', 'SYS_CONTENT_APPROVAL_STATUS'],
       filters,
       true
   );
   ```

2. **`redrawView` function definition** (line ~918):
   ```javascript
   var redrawView = function() {
       essResetRMChanges();
       // ... scoping logic ...
       renderView(scopedResources.resources);
   };
   ```

3. **Roadmap toolbar** now renders via `<xsl:call-template name="ViewUserScopingUI"/>` (line 869)

## Files Modified

- `/mcp_view_builder/server.py` - Lines 892-894: Added variable initialization

## Testing

To verify the fix works:

```bash
cd /Users/johnmayall/Tomcat/apache-tomcat-9.0.97/webapps/essential_viewer_dev/mcp_view_builder
python3.11 -c "import server; scaffold = server.generate_scaffold_v2('Test', ['appMartAPI'], '', True, True); print('Has essInitViewScoping:', 'essInitViewScoping' in scaffold)"
```

Should output: `Has essInitViewScoping: True`

## Related Issues Fixed

This was part of a larger MCP improvement effort that also addressed:
1. ✅ Non-existent property usage (`app.capability`)
2. ✅ Hardcoded data instead of repository data
3. ✅ Missing roadmap functions (this fix)
