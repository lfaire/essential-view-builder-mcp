import os
import asyncio
import re
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# Define the server
server = Server("Essential View Builder MCP")

# Base directory for the MCP
MCP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(MCP_DIR, "resources")
VIEWER_DIR = os.environ.get("ESSENTIAL_VIEWER_DIR")

# Cache for parsed API documentation
_api_docs_cache = None

# Global view context (exposed as resources)
view_context = {
    "scoping_definitions": [
        {"id": "orgUserIds", "label": "Group_Actor"},
        {"id": "geoIds", "label": "Geographic_Region"},
        {"id": "visId", "label": "SYS_CONTENT_APPROVAL_STATUS"}
    ],
    "resource_type_info": {
        "className": "Application_Provider",
        "label": "Application",
        "icon": "fa-desktop"
    }
}

def parse_api_documentation():
    """
    Parse api_documentation.md to extract API structures dynamically.
    Returns dict with API information.
    """
    global _api_docs_cache
    
    if _api_docs_cache is not None:
        return _api_docs_cache
    
    docs_path = os.path.join(RESOURCES_DIR, "api_documentation.md")
    
    if not os.path.exists(docs_path):
        return {
            'apis': {},
            'property_names': {},
            'data_structures': {}
        }
    
    with open(docs_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    apis = {}
    current_api = None
    
    # Parse API documentation sections
    # Look for patterns like:
    # **DSA Data Label**: `appMartAPI`
    # Then extract the JSON structure and property names
    
    api_sections = re.split(r'\n##\s+', content)
    
    for section in api_sections:
        # Extract DSA Data Label
        label_match = re.search(r'\*\*DSA Data Label\*\*:\s*`([^`]+)`', section)
        if not label_match:
            continue
        
        api_label = label_match.group(1)
        
        # Extract JSON structure examples
        json_blocks = re.findall(r'```json\s*(.*?)```', section, re.DOTALL)
        
        # Extract property names from the JSON
        properties = set()
        sample_structure = None
        
        for json_block in json_blocks:
            try:
                # Try to parse JSON to extract property names
                data = json.loads(json_block)
                if isinstance(data, dict):
                    properties.update(data.keys())
                    if sample_structure is None:
                        sample_structure = data
            except json.JSONDecodeError:
                # If not valid JSON, try to extract property names from text
                prop_matches = re.findall(r'"([a-zA-Z_][a-zA-Z0-9_]*)":', json_block)
                properties.update(prop_matches)
        
        # Extract description
        desc_match = re.search(r'\*\*Description\*\*:\s*([^\n]+)', section)
        description = desc_match.group(1) if desc_match else ""
        
        apis[api_label] = {
            'label': api_label,
            'description': description,
            'properties': list(properties),
            'sample_structure': sample_structure
        }
    
    _api_docs_cache = {
        'apis': apis,
        'property_names': extract_property_mappings(apis),
        'data_structures': extract_data_structures(apis)
    }
    
    return _api_docs_cache

def extract_property_mappings(apis):
    """
    Extract common property name patterns from API structures.
    This helps identify the main data arrays in each API response.
    """
    mappings = {}
    
    for api_label, api_info in apis.items():
        properties = api_info.get('properties', [])
        
        # Identify likely main data property (usually plural, contains api name parts)
        main_props = []
        api_lower = api_label.lower()
        
        for prop in properties:
            prop_lower = prop.lower()
            # Look for array-like property names (plural, contains relevant keywords)
            if (prop_lower.endswith('s') or 
                prop_lower.endswith('ies') or
                prop_lower.endswith('data') or
                any(keyword in prop_lower for keyword in ['application', 'capability', 'technology', 'lifecycle', 'organization'])):
                main_props.append(prop)
        
        if main_props:
            mappings[api_label] = main_props
    
    return mappings

def extract_data_structures(apis):
    """
    Extract suggested viewModel properties based on API focus.
    """
    structures = {}
    
    for api_label, api_info in apis.items():
        desc = api_info.get('description', '').lower()
        label_lower = api_label.lower()
        
        # Infer viewModel property names from API label and description
        suggested_props = []
        
        if 'application' in label_lower or 'app' in label_lower:
            suggested_props.append('applications')
        if 'capability' in label_lower or 'capability' in desc:
            suggested_props.append('capabilities')
        if 'technology' in label_lower or 'tech' in label_lower:
            suggested_props.append('technologies')
        if 'lifecycle' in label_lower:
            suggested_props.append('lifecycle')
        if 'cost' in label_lower:
            suggested_props.append('costs')
        if 'org' in label_lower or 'organization' in desc:
            suggested_props.append('organizations')
        if 'kpi' in label_lower or 'performance' in desc:
            suggested_props.append('kpis')
        if 'business' in desc:
            suggested_props.append('businessCapabilities')
        
        # Fallback: use a generic name based on API label
        if not suggested_props:
            # Convert camelCase to snake_case and pluralize
            generic_name = re.sub(r'API$', '', api_label)
            generic_name = re.sub(r'([a-z])([A-Z])', r'\1_\2', generic_name).lower()
            suggested_props.append(generic_name + '_data')
        
        structures[api_label] = suggested_props
    
    return structures

def get_api_property_hints(api_label):
    """
    Get hints about property names for a specific API.
    Returns list of likely property names to use.
    """
    api_docs = parse_api_documentation()
    
    api_info = api_docs['apis'].get(api_label, {})
    property_mappings = api_docs['property_names'].get(api_label, [])
    
    return property_mappings

def generate_property_warnings(api_labels):
    """
    Generate comments warning about property structure based on API docs.
    """
    api_docs = parse_api_documentation()
    warnings = []
    
    for api in api_labels:
        property_hints = get_api_property_hints(api)
        if property_hints:
            props_str = "', '".join(property_hints)
            warnings.append(f"// NOTE: {api} likely has properties: ['{props_str}']")
            warnings.append(f"//       Check actual response structure with console.log()")
    
    if warnings:
        return "\n        " + "\n        ".join(warnings)
    return ""

def encode_for_xsl(javascript_code: str) -> str:
    """
    Encode JavaScript for XSL context (no CDATA).
    CRITICAL: Maintains no-space pattern for && operator.
    """
    # Replace && with &amp;&amp; (NO SPACE)
    code = javascript_code.replace('&&', '&amp;&amp;')
    
    # Replace comparison operators  
    code = code.replace('<=', '&lt;=')
    code = code.replace('>=', '&gt;=')
    # Handle < and > but avoid double-encoding
    code = re.sub(r'(?<!&lt;)(?<!&gt;)<(?!=)', '&lt;', code)
    code = re.sub(r'(?<!&lt;=)(?<!&gt;=)>(?!=)', '&gt;', code)
    
    return code

def generate_viewmodel_structure(api_labels: list) -> str:
    """
    Generate suggested viewModel structure based on APIs.
    Uses data from api_documentation.md dynamically.
    """
    api_docs = parse_api_documentation()
    data_structures = api_docs['data_structures']
    
    props = []
    for api in api_labels:
        suggested = data_structures.get(api, [])
        props.extend(suggested)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_props = []
    for prop in props:
        if prop not in seen:
            seen.add(prop)
            unique_props.append(prop)
    
    # Build JavaScript object
    if unique_props:
        props_js = ',\n        '.join([f"{prop}: []" for prop in unique_props])
        return f"""var viewModel = {{
        {props_js}
    }};"""
    else:
        return """var viewModel = {
        data: []
    };"""

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="essential-view://api-docs",
            name="API Documentation",
            description="Catalogue of all Essential Viewer APIs",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri="essential-view://view-template",
            name="API Fetch Template",
            description="The base XSL template for creating new views",
            mimeType="text/xml",
        ),
        types.Resource(
            uri="essential-view://handlebars-functions",
            name="Handlebars Utility Functions",
            description="Common Handlebars helpers and formatting utilities",
            mimeType="text/xml",
        ),
        types.Resource(
            uri="essential-view://common-js-functions",
            name="Common JS Functions",
            description="General purpose JavaScript utilities for Essential Viewer",
            mimeType="text/xml",
        ),
        types.Resource(
            uri="essential-view://reference-view-roadmap",
            name="Reference Roadmap View",
            description="Example view showing roadmap enablement and scoping patterns",
            mimeType="text/xml",
        ),
        types.Resource(
            uri="essential-view://view-build-docs",
            name="View Build Documentation v2.0",
            description="Complete guide for building Essential XSL views with validated patterns",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri="essential-view://quick-reference",
            name="Quick Reference Card",
            description="One-page reference for Essential view patterns and troubleshooting",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri="essential-view://implementation-guide",
            name="MCP Implementation Guide",
            description="Developer guide for implementing view scaffold generation",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri="essential-view://roadmap-guide",
            name="Roadmap Scoping Guide",
            description="Complete guide for integrating roadmap scoping and organization filtering",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri="essential-view://api-property-verification",
            name="API Property Verification Guide",
            description="CRITICAL: How to verify API properties before use - prevents hardcoded data and non-existent property errors",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri="essential-view://deprecated-patterns",
            name="Deprecated Patterns Warning",
            description="⚠️ CRITICAL - READ FIRST: Forbidden patterns that cause XML parsing errors and non-functional views. Prevents common AI generation mistakes.",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri="essential-view://viewer-index",
            name="Essential Viewer File Index",
            description="Index of all XSL view and API files in the Essential Viewer, grouped by domain. Use with read_viewer_file to read any file.",
            mimeType="text/markdown",
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    # Map URIs to file paths
    resource_map = {
        "essential-view://api-docs": "api_documentation.md",
        "essential-view://view-template": "api_fetch_template.xsl",
        "essential-view://handlebars-functions": "core_handlebars_functions.xsl",
        "essential-view://common-js-functions": "core_js_functions.xsl",
        "essential-view://reference-view-roadmap": "core_al_app_provider_list_table.xsl",
        "essential-view://view-build-docs": "view_build_documentation.md",
        "essential-view://quick-reference": "QUICK_REFERENCE.md",
        "essential-view://implementation-guide": "MCP_RESOURCE_UPDATES.md",
        "essential-view://roadmap-guide": "ROADMAP_SCOPING_GUIDE.md",
        "essential-view://api-property-verification": "API_PROPERTY_VERIFICATION.md",
        "essential-view://deprecated-patterns": "DEPRECATED_PATTERNS_WARNING.md"
    }
    
    uri_str = str(uri)

    if uri_str == "essential-view://viewer-index":
        return _build_viewer_index()

    if uri_str not in resource_map:
        raise ValueError(f"Unknown resource: {uri}")
    
    path = os.path.join(RESOURCES_DIR, resource_map[uri_str])
    
    # Fallback to updates guide and other docs as needed
    if uri_str == "essential-view://view-build-docs" and not os.path.exists(path):
        path = os.path.join(RESOURCES_DIR, "MCP_RESOURCE_UPDATES.md")
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _build_viewer_index() -> str:
    if not VIEWER_DIR or not os.path.isdir(VIEWER_DIR):
        return "# Essential Viewer File Index\n\nNot available — ESSENTIAL_VIEWER_DIR is not set or does not exist.\n"

    domains = ["application", "business", "common", "enterprise",
               "information", "integration", "platform", "technology"]
    lines = ["# Essential Viewer File Index\n",
             "Use `read_viewer_file` with the relative path shown to read any file.\n"]

    for domain in domains:
        domain_path = os.path.join(VIEWER_DIR, domain)
        if not os.path.isdir(domain_path):
            continue
        xsl_files = sorted(
            f for f in os.listdir(domain_path) if f.endswith(".xsl")
        )
        api_path = os.path.join(domain_path, "api")
        api_files = []
        if os.path.isdir(api_path):
            api_files = sorted(
                f for f in os.listdir(api_path) if f.endswith(".xsl")
            )
        if not xsl_files and not api_files:
            continue
        lines.append(f"\n## {domain}\n")
        if xsl_files:
            lines.append("**Views:**\n")
            for f in xsl_files:
                lines.append(f"- `{domain}/{f}`")
        if api_files:
            lines.append("\n**APIs:**\n")
            for f in api_files:
                lines.append(f"- `{domain}/api/{f}`")

    return "\n".join(lines)

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="generate_view_scaffold",
            description="Generates an XSL view scaffold following v2.0 validated patterns. Supports 'dashboard' (interactive HTML) and 'excel_export' (data export with ExcelJS) view types. All views use the same required imports/includes chain.",
            inputSchema={
                "type": "object",
                "properties": {
                    "view_name": {
                        "type": "string",
                        "description": "The human-readable name of the view"
                    },
                    "api_labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of DSA Data Labels for the APIs to use (e.g., appMartAPI, ImpBusCapApi). Use Mart APIs as primary anchors."
                    },
                    "view_type": {
                        "type": "string",
                        "enum": ["dashboard", "excel_export"],
                        "default": "dashboard",
                        "description": "Type of view: 'dashboard' for interactive HTML views, 'excel_export' for data export views using ExcelJS. Both use the same standard imports."
                    },
                    "view_model_hint": {
                        "type": "string",
                        "description": "Optional hint describing what data the view needs (e.g., 'applications with costs and lifecycle status'). Helps generate appropriate viewModel structure."
                    },
                    "excel_columns": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "header": {"type": "string"},
                                "key": {"type": "string"},
                                "width": {"type": "integer"}
                            }
                        },
                        "description": "Column definitions for excel_export views. Each with header, key, and width."
                    },
                    "include_handlebars": {
                        "type": "boolean",
                        "default": True,
                        "description": "Whether to include Handlebars utility functions"
                    },
                    "enable_roadmap": {
                        "type": "boolean",
                        "default": True,
                        "description": "Whether to enable roadmap scoping and redraw logic"
                    }
                },
                "required": ["view_name", "api_labels"]
            }
        ),
        types.Tool(
            name="generate_api_scaffold",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_name": {"type": "string", "description": "The name of the API (e.g., informationStoreAPI)"},
                    "target_class": {"type": "string", "description": "The Essential Meta-Class to query (e.g., Information_Store)"},
                    "collection_name": {"type": "string", "description": "The JSON property name for the results (e.g., stores)"},
                    "additional_slots": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of slots to include in the output"
                    }
                },
                "required": ["api_name", "target_class", "collection_name"]
            },
            description="Generates an Essential API (XSLT) following the Golden Pattern for JSON delivery."
        ),
        types.Tool(
            name="suggest_view_architecture",
            description="⚠️ MANDATORY: First use read_view_builder_resource(uri='essential-view://deprecated-patterns') to learn forbidden patterns. Then suggests which APIs and data structures to use for a given view description by analyzing the API documentation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "view_description": {
                        "type": "string", 
                        "description": "Description of what the view should do"
                    }
                },
                "required": ["view_description"]
            }
        ),
        types.Tool(
            name="escape_xsl_content",
            description="Escapes JavaScript for XSL context with correct ampersand encoding (NO SPACE after &amp;&amp;).",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string", 
                        "description": "The JavaScript content to escape"
                    }
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="wrap_in_cdata",
            description="Wraps content in CDATA section. NOTE: v2.0 pattern prefers no CDATA - use only if absolutely necessary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string", 
                        "description": "The content to wrap in CDATA"
                    }
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="adapt_external_view",
            description="Port an external HTML/JS demo with sample JSON into an Essential-ready XSL view.",
            inputSchema={
                "type": "object",
                "properties": {
                    "view_name": {"type": "string", "description": "The name of the new view"},
                    "external_html": {"type": "string", "description": "The standalone HTML content"},
                    "external_js": {"type": "string", "description": "The standalone JavaScript content"},
                    "sample_json": {"type": "string", "description": "The sample JSON data the demo uses"},
                    "api_mappings": {
                        "type": "object",
                        "description": "Optional mapping from external JSON keys to Essential API Labels",
                        "additionalProperties": {"type": "string"}
                    }
                },
                "required": ["view_name", "external_html", "external_js", "sample_json"]
            }
        ),
        types.Tool(
            name="read_viewer_file",
            description="Reads a file from the Essential Viewer source tree by its relative path (e.g. 'application/core_al_app_cost_summary.xsl' or 'application/api/core_api_al_application_provider_cost.xsl'). Use essential-view://viewer-index to browse available files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Relative path to the file within the Essential Viewer (e.g. 'application/core_al_app_cost_summary.xsl')"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "generate_view_scaffold":
        view_name = arguments["view_name"]
        api_labels = arguments["api_labels"]
        view_type = arguments.get("view_type", "dashboard")
        view_model_hint = arguments.get("view_model_hint", "")
        excel_columns = arguments.get("excel_columns", [])
        include_handlebars = arguments.get("include_handlebars", True)
        enable_roadmap = arguments.get("enable_roadmap", True)

        if view_type == "excel_export":
            scaffold = generate_excel_export_scaffold(
                view_name=view_name,
                api_labels=api_labels,
                excel_columns=excel_columns,
                view_model_hint=view_model_hint
            )
        else:
            scaffold = generate_scaffold_v2(
                view_name=view_name,
                api_labels=api_labels,
                view_model_hint=view_model_hint,
                include_handlebars=include_handlebars,
                enable_roadmap=enable_roadmap
            )

        return [types.TextContent(type="text", text=scaffold)]

    if name == "generate_api_scaffold":
        api_name = arguments["api_name"]
        target_class = arguments["target_class"]
        collection_name = arguments["collection_name"]
        additional_slots = arguments.get("additional_slots", [])
        
        scaffold = generate_api_scaffold(api_name, target_class, collection_name, additional_slots)
        
        return [
            types.TextContent(
                type="text",
                text=scaffold
            )
        ]

    if name == "suggest_view_architecture":
        description = arguments["view_description"]
        advice = generate_advice_text(description)
        return [types.TextContent(type="text", text=advice)]

    if name == "escape_xsl_content":
        content = arguments["content"]
        escaped = encode_for_xsl(content)
        return [types.TextContent(type="text", text=escaped)]

    if name == "wrap_in_cdata":
        content = arguments["content"]
        wrapped = f"<![CDATA[\n{content}\n]]>"
        note = "\nNOTE: v2.0 pattern recommends avoiding CDATA. Consider using XML entity encoding instead."
        return [types.TextContent(type="text", text=wrapped + note)]

    if name == "adapt_external_view":
        scaffold = generate_adapted_view_scaffold(
            view_name=arguments["view_name"],
            external_html=arguments["external_html"],
            external_js=arguments["external_js"],
            sample_json=arguments["sample_json"],
            api_mappings=arguments.get("api_mappings", {})
        )
        return [types.TextContent(type="text", text=scaffold)]

    if name == "read_viewer_file":
        if not VIEWER_DIR or not os.path.isdir(VIEWER_DIR):
            return [types.TextContent(type="text", text="Error: Essential Viewer directory is not available.")]
        rel_path = arguments["file_path"].lstrip("/")
        abs_path = os.path.realpath(os.path.join(VIEWER_DIR, rel_path))
        viewer_root = os.path.realpath(VIEWER_DIR)
        if not abs_path.startswith(viewer_root + os.sep):
            return [types.TextContent(type="text", text="Error: Access denied — path is outside the Essential Viewer directory.")]
        if not os.path.isfile(abs_path):
            return [types.TextContent(type="text", text=f"Error: File not found: {rel_path}")]
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        return [types.TextContent(type="text", text=content)]

    raise ValueError(f"Unknown tool: {name}")

def view_name_from_description(description: str) -> str:
    """Extract a reasonable view name from description."""
    # Take first 50 chars, capitalize
    name = description[:50].strip()
    if len(description) > 50:
        name += "..."
    return name.title()

def generate_advice_text(description: str) -> str:
    """
    Generates architectural advice for a view based on its description.
    """
    # Parse API documentation to find relevant APIs
    api_docs = parse_api_documentation()
    apis = api_docs['apis']
    
    relevant_apis = []
    keywords = description.lower().split()
    
    # Score each API based on keyword matches
    api_scores = {}
    for api_label, api_info in apis.items():
        score = 0
        api_text = (api_label + ' ' + api_info.get('description', '')).lower()
        
        for keyword in keywords:
            if keyword in api_text:
                score += 1
        
        if score > 0:
            api_scores[api_label] = score
    
    # Get top scoring APIs
    if api_scores:
        sorted_apis = sorted(api_scores.items(), key=lambda x: x[1], reverse=True)
        relevant_apis = [api for api, score in sorted_apis[:5]]
    
    # Default to appMartAPI if nothing found
    if not relevant_apis:
        relevant_apis = ['appMartAPI']
    
    apis_str = ", ".join([f"'{a}'" for a in relevant_apis])
    
    property_info = []
    missing_classes = []
    
    # Identify missing classes from keywords & known gaps
    gap_concepts = {
        "privacy": "Privacy_Impact_Assessment",
        "gdpr": "Privacy_Impact_Assessment",
        "information store": "Information_Store",
        "data store": "Information_Store",
        "objective": "Business_Objective",
        "goal": "Business_Goal",
        "principle": "Architecture_Principle",
        "standard": "Technology_Standard"
    }
    
    # Check for known gaps first
    desc_lower = description.lower()
    for concept, cls in gap_concepts.items():
        if concept in desc_lower:
            # Check if an API already mentions this class in description
            already_covered = False
            for api_info in apis.values():
                if cls.lower() in api_info.get('description', '').lower():
                    already_covered = True
                    break
            if not already_covered and cls not in missing_classes:
                missing_classes.append(cls)

    # Fallback to keyword scan for other potential gaps
    for keyword in keywords:
        if len(keyword) < 5: continue # Ignore short words
        if keyword in ["dashboard", "capability", "application", "business"]: continue
        
        found = False
        for api_info in apis.values():
            if keyword in api_info.get('description', '').lower():
                found = True
                break
        if not found:
            # Only add if not already caught by gap concepts
            cap_keyword = keyword.capitalize()
            if not any(cap_keyword in mc for mc in missing_classes):
                missing_classes.append(cap_keyword)

    for api in relevant_apis:
        hints = get_api_property_hints(api)
        if hints:
            property_info.append(f"  - {api}: likely properties [{', '.join(hints)}]")
    
    property_section = "\n".join(property_info) if property_info else "  Check API documentation for specific property names"
    
    # Check for roadmapping/scoping needs
    roadmap_keywords = ['roadmap', 'timeline', 'horizon', 'plan', 'scoping', 'filter', 'org', 'geo', 'approval']
    needs_roadmap = any(k in description.lower() for k in roadmap_keywords)
    
    roadmap_advice = ""
    if needs_roadmap:
        roadmap_advice = """
**Roadmapping & Scoping Advice**:
1. **Enable Roadmap**: This view should use roadmap scoping (org/geo filtering).
2. **Parameters**: Set `enable_roadmap: true` in `generate_view_scaffold`.
3. **Primary Data**: Ensure your primary API (e.g. `appMartAPI`) has `filters` and `applications` properties.
4. **Pattern**: The generator will add `essInitViewScoping` and `redrawView` automatically.
5. **Resource**: Read `essential-view://roadmap-guide` for implementation details.
"""
    
    api_gen_advice = ""
    if missing_classes:
        missing_text = ", ".join(missing_classes[:3])
        api_gen_advice = f"""
**Missing Data Detected**:
I couldn't find a standard API that explicitly covers: **{missing_text}**.
- Do you know of an existing API for this?
- If not, I can generate a new API for you using `generate_api_scaffold`.
- **Action**: Ask me to "Create an API for {missing_classes[0]}" if you want to proceed.
"""

    suggestion = f"""Architecture Suggestion for: '{description}'

**⚠️ CRITICAL FIRST STEP - STOP AND READ THIS**:
Before generating ANY code, you MUST:
1. Call: read_view_builder_resource(uri='essential-view://deprecated-patterns')
2. Read the ENTIRE document to understand forbidden patterns
3. Common errors this prevents:
   - ❌ Using $utilitiesAllDataSetAPIs (deprecated 2019-2022 pattern)
   - ❌ "entity name must follow '&'" XML parsing errors
   - ❌ Mixing <xsl:call-template> with CDATA blocks
   - ❌ Ampersands without proper encoding

**Recommended APIs**: {apis_str}

**Property Structure Hints**:
{property_section}

{roadmap_advice}
{api_gen_advice}
**Critical v2.0 Pattern Rules**:
1. **Single Script Block**: ONE <script type="text/javascript"> tag
2. **No CDATA**: JavaScript goes directly in script tag with XML encoding
3. **Ampersand Rule**: Use &amp;&amp; with NO SPACE after it
4. **Template Call First**: <xsl:call-template name="RenderViewerAPIJSFunction"/> at top
5. **Variables Declared**: Declare API variables before $(document).ready
6. **View-Specific ViewModel**: Design viewModel structure for THIS view's needs
7. **Verify Properties**: Always use console.log() to check actual API response structure

**🚨 CRITICAL: Property Verification Required**:
- **NEVER assume property names** - Always check `essential-view://api-docs` first
- **NEVER hardcode data** - Build charts/tables from actual API responses
- **READ** `essential-view://api-property-verification` for detailed verification workflow
- Common mistake: Using `app.capability` (doesn't exist) instead of `app.services[0].name`
- Common mistake: Hardcoding `labels: ['Sales', 'Finance']` instead of building from data

**Next Steps**:
1. **READ** `essential-view://deprecated-patterns` (MANDATORY - prevents common failures)
2. **Read** `essential-view://api-property-verification` to understand property verification
3. **Consult** `essential-view://api-docs` to verify exact property paths
4. Call generate_view_scaffold with:
   - view_name: \"{view_name_from_description(description)}\"
   - api_labels: {relevant_apis}
   - view_model_hint: \"{description}\"

The tool will generate a working scaffold following all v2.0 patterns.
"""
    return suggestion

def view_name_from_description(description: str) -> str:
    """Extract a reasonable view name from description."""
    # Take first 50 chars, capitalize
    name = description[:50].strip()
    if len(description) > 50:
        name += "..."
    return name.title()

def generate_scaffold_v2(
    view_name: str,
    api_labels: list,
    view_model_hint: str = "",
    include_handlebars: bool = True,
    enable_roadmap: bool = True
) -> str:
    """
    Generate XSL scaffold using v2.0 validated patterns.
    All values are extracted dynamically from api_documentation.md.
    
    Key patterns:
    - Single script block
    - No CDATA
    - Correct ampersand encoding (no spaces)
    - Variables declared before $(document).ready
    - View-specific viewModel structure
    """
    
    # Build variable declarations
    var_declarations = ', '.join(api_labels)
    
    # Build destructuring (without outer braces for the f-string)
    destructuring = ', '.join(api_labels)
    
    # Build API list for JavaScript
    api_list_js = "['" + "', '".join(api_labels) + "']"
    
    # Generate viewModel structure (dynamically from API docs)
    viewmodel_structure = generate_viewmodel_structure(api_labels)
    
    # Get property warnings (dynamically from API docs)
    property_warnings = generate_property_warnings(api_labels)
    
    # Build imports/includes
    imports = generate_imports(include_handlebars, enable_roadmap)
    
    # Generate main script section
    script_section = generate_script_section_v2(
        api_labels=api_labels,
        var_declarations=var_declarations,
        destructuring=destructuring,
        api_list_js=api_list_js,
        viewmodel_structure=viewmodel_structure,
        property_warnings=property_warnings,
        enable_roadmap=enable_roadmap
    )
    
    # Build complete scaffold
    scaffold = f'''<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0" xpath-default-namespace="http://protege.stanford.edu/xml" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xalan="http://xml.apache.org/xslt" 
    xmlns:pro="http://protege.stanford.edu/xml" 
    xmlns:eas="http://www.enterprise-architecture.org/essential" 
    xmlns:functx="http://www.functx.com" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:ess="http://www.enterprise-architecture.org/essential/errorview">
    
{imports}
    
    <xsl:output method="html" omit-xml-declaration="yes" indent="yes"/>
    <xsl:param name="param1"/>
    
    <!-- START GENERIC PARAMETERS -->
    <xsl:param name="viewScopeTermIds"/>
    <!-- END GENERIC PARAMETERS -->
    
    <!-- START GENERIC LINK VARIABLES -->
    <xsl:variable name="viewScopeTerms" select="eas:get_scoping_terms_from_string($viewScopeTermIds)"/>
    <xsl:variable name="linkClasses" select="('Composite_Application_Provider', 'Application_Provider')"/>
    <!-- END GENERIC LINK VARIABLES -->
    
    <xsl:template match="knowledge_base">
        <xsl:call-template name="docType"/>
        <html>
            <head>
                <xsl:call-template name="commonHeadContent"/>
                <xsl:call-template name="RenderModalReportContent">
                    <xsl:with-param name="essModalClassNames" select="$linkClasses"/>
                </xsl:call-template>
                
                <title>{view_name}</title>
                
                <!-- Add external libraries as needed -->
                <!-- <script src="js/chartjs/Chart.min.js"/> -->
                
                <style>
                    .view-wrapper {{
                        padding: 20px;
                        max-width: 1400px;
                        margin: {"80px" if enable_roadmap else "40px"} auto 0 auto;
                    }}
                    
                    /* Add your view-specific styles here */
                </style>
                
{script_section}
            </head>
            <body>
                <xsl:call-template name="Heading"/>
                {generate_roadmap_ui(enable_roadmap)}
                
                <div class="view-wrapper">
                    <div id="mainContent">
                        <p>Loading {view_name}...</p>
                    </div>
                </div>
                
                <xsl:call-template name="Footer"/>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>'''
    
    return scaffold

def generate_imports(include_handlebars: bool, enable_roadmap: bool) -> str:
    """Generate import/include statements with correct order."""
    
    imports = '''    <!-- IMPORT MUST COME FIRST -->
    <xsl:import href="../common/core_js_functions.xsl"/>
    
    <!-- REQUIRED INCLUDES -->
    <xsl:include href="../common/core_doctype.xsl"/>
    <xsl:include href="../common/core_common_head_content.xsl"/>
    <xsl:include href="../common/core_header.xsl"/>
    <xsl:include href="../common/core_footer.xsl"/>
    <xsl:include href="../common/core_external_doc_ref.xsl"/>
    <xsl:include href="../common/core_api_fetcher.xsl"/>'''
    
    # Note: core_roadmap_functions.xsl is NOT required for roadmap scoping
    # All scoping functions are available in core_js_functions.xsl
    
    if include_handlebars:
        imports += '''
    <xsl:include href="../common/core_handlebars_functions.xsl"/>'''
    
    return imports

def generate_roadmap_ui(enable_roadmap: bool) -> str:
    """Generate roadmap UI template call if enabled."""
    if enable_roadmap:
        return '\n                <xsl:call-template name="ViewUserScopingUI"></xsl:call-template>'
    return ''

def generate_script_section_v2(
    api_labels: list,
    var_declarations: str,
    destructuring: str,
    api_list_js: str,
    viewmodel_structure: str,
    property_warnings: str,
    enable_roadmap: bool
) -> str:
    """
    Generate JavaScript section using v2.0 golden pattern.
    
    CRITICAL RULES:
    - Single script tag
    - No CDATA
    - Template call first
    - Variables before $(document).ready
    - Correct ampersand encoding (no spaces)
    """
    
    # Initialize variables that will be set in if/else blocks
    execution_logic = ""
    additional_functions = ""

    # Build the main execution function
    if enable_roadmap:
        execution_logic = f'''                
                // Extract filters and data from your primary API
                // Primary API: {api_labels[0] if api_labels else 'unknown'}
                let primaryAPI = {api_labels[0] if api_labels else 'responses'};
                let filters = primaryAPI?.filters || [];
                workingArray = primaryAPI?.applications || primaryAPI?.data || [];
                
                // Build dynamic filter definitions from API
                dynamicFilterDefs = filters?.map(function(filterdef) {{{{
                    return new ScopingProperty(filterdef.slotName, filterdef.valueClass);
                }}}}) || [];
                
                buildViewModel(responses);
                
                // Initialize roadmap scoping
                essInitViewScoping(
                    redrawView,
                    ['Group_Actor', 'Geographic_Region', 'SYS_CONTENT_APPROVAL_STATUS'],
                    filters,
                    true
                );'''
        
        additional_functions = '''
    
    var redrawView = function() {{
        essResetRMChanges();
        
        // Define scoping properties
        let appOrgScopingDef = new ScopingProperty('orgUserIds', 'Group_Actor');
        let geoScopingDef = new ScopingProperty('geoIds', 'Geographic_Region');
        let visibilityDef = new ScopingProperty('visId', 'SYS_CONTENT_APPROVAL_STATUS');
        
        // Define resource type info
        let resourceTypeInfo = {{
            className: 'Application_Provider',
            label: 'Application',
            icon: 'fa-desktop'
        }};
        
        // Apply scoping
        scopedResources = essScopeResources(
            workingArray,
            [appOrgScopingDef, geoScopingDef, visibilityDef].concat(dynamicFilterDefs),
            resourceTypeInfo
        );
        
        // Re-render with scoped data
        renderView(scopedResources.resources);
    }};
    
    function renderView(data) {{
        // TODO: Render your view using the provided data
        console.log('Rendering', data.length, 'scoped items');
        
        const html = '&lt;h2&gt;View Ready&lt;/h2&gt;' +
                     '&lt;p&gt;Found ' + data.length + ' items&lt;/p&gt;' +
                     '&lt;p&gt;Customize renderView() to display your data.&lt;/p&gt;';
        
        document.getElementById('mainContent').innerHTML = html;
    }}'''
    else:
        execution_logic = '''                
                buildViewModel(responses);
                renderView();'''
        
        additional_functions = '''
    
    function renderView() {
        // TODO: Render your view using viewModel data
        console.log('Rendering view with viewModel:', viewModel);
        
        const html = '&lt;h2&gt;View Ready&lt;/h2&gt;' +
                     '&lt;p&gt;Customize renderView() to display your data.&lt;/p&gt;';
        
        document.getElementById('mainContent').innerHTML = html;
    }'''
    
    script = f'''                <script type="text/javascript">
                    <xsl:call-template name="RenderViewerAPIJSFunction"/>
                    
                    // Declare API variables for destructuring
                    let {var_declarations};
                    
                    {'// Global variables for roadmap scoping' if enable_roadmap else ''}
                    {'var workingArray, dynamicFilterDefs, scopedResources;' if enable_roadmap else ''}
                    
                    // Define view-specific data model
                    // Structure suggested based on APIs used - customize as needed
                    {viewmodel_structure}{property_warnings}
                    
                    $(document).ready(function() {{
                        const apiList = {api_list_js};
                        
                        async function executeFetchAndRender() {{
                            try {{
                                let responses = await fetchAndRenderData(apiList);
                                ({{ {destructuring} }} = responses);
                                
                                console.log('Responses loaded:', responses);
                                // IMPORTANT: Check actual property names in console
                                // Property names in documentation may not match reality
                                
                                // ROADMAP TIP: If using Chart.js for timelines, calculate explicit 
                                // min/max dates from your dataset to prevent 1970 fallback.
                                // Handle both .allProjects and .allProject keys.
{execution_logic}
                                
                            }} catch (error) {{
                                console.error('Error loading view data:', error);
                                document.getElementById('mainContent').innerHTML = 
                                    '&lt;div class="alert alert-danger"&gt;Error loading data. Check console for details.&lt;/div&gt;';
                            }}
                        }}
                        
                        executeFetchAndRender();
                    }});
                    
                    function buildViewModel(responses) {{
                        // TODO: Process API responses and populate viewModel
                        // CRITICAL: Use console.log() to verify actual property names
                        // Example:
                        //   console.log('API structure:', Object.keys(responses.apiName));
                        //   console.log('Sample data:', responses.apiName);
                        
                        // Then use the ACTUAL property names:
                        if (responses.appMartAPI &amp;&amp;responses.appMartAPI.applications) {{
                            viewModel.applications = responses.appMartAPI.applications;
                            console.log('Populated applications:', viewModel.applications.length);
                        }}
                        
                        // Example: Aggregate costs if available
                        if (viewModel.applications.length &gt; 0 &amp;&amp;viewModel.applications[0].costs) {{
                            viewModel.costs = viewModel.applications.flatMap(app =&gt; app.costs || []);
                            console.log('Populated costs:', viewModel.costs.length);
                        }}
                        
                        console.log('Building view model from responses');
                    }}{additional_functions}
                </script>'''
    
    return script

def generate_excel_export_scaffold(
    view_name: str,
    api_labels: list,
    excel_columns: list = None,
    view_model_hint: str = ""
) -> str:
    """
    Generate an Excel export view scaffold.

    These are standard HTML views (same imports) that:
    1. Load data via API fetcher
    2. Display a preview table using DOM API (NOT string HTML)
    3. Export to .xlsx using ExcelJS on button click

    CRITICAL: Uses document.createElement() for all dynamic HTML
    to avoid XML escaping issues in XSL context.
    """

    # Build variable declarations
    var_declarations = ', '.join(api_labels)
    # Build destructuring (without outer braces for the f-string)
    destructuring = ', '.join(api_labels)
    api_list_js = "['" + "', '".join(api_labels) + "']"

    # Build imports (no roadmap, no handlebars needed for export)
    imports = generate_imports(include_handlebars=False, enable_roadmap=False)

    # Build column definitions
    if not excel_columns:
        excel_columns = [
            {"header": "Name", "key": "name", "width": 30},
            {"header": "Description", "key": "description", "width": 40}
        ]

    # Generate HTML table headers
    th_elements = '\n\t\t\t\t\t\t\t\t\t\t\t'.join(
        [f'<th>{col["header"]}</th>' for col in excel_columns]
    )

    # Generate ExcelJS column definitions
    excel_col_defs = ',\n\t\t\t\t\t\t\t\t'.join(
        [f"{{ header: '{col['header']}', key: '{col['key']}', width: {col.get('width', 20)} }}" for col in excel_columns]
    )

    # Generate DOM row builder (uses document.createElement - NO string HTML)
    col_keys = [col['key'] for col in excel_columns]
    field_list = ', '.join([f"row.{k}" for k in col_keys])

    # Generate ExcelJS addRow object
    excel_row_props = ',\n\t\t\t\t\t\t\t\t\t'.join(
        [f"{col['key']}: row.{col['key']}" for col in excel_columns]
    )

    # Generate autofilter range
    last_col_letter = chr(ord('A') + len(excel_columns) - 1)

    scaffold = f'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xpath-default-namespace="http://protege.stanford.edu/xml"
\txmlns:xsl="http://www.w3.org/1999/XSL/Transform"
\txmlns:xalan="http://xml.apache.org/xslt"
\txmlns:pro="http://protege.stanford.edu/xml"
\txmlns:eas="http://www.enterprise-architecture.org/essential"
\txmlns:functx="http://www.functx.com"
\txmlns:xs="http://www.w3.org/2001/XMLSchema"
\txmlns:ess="http://www.enterprise-architecture.org/essential/errorview">

{imports}

\t<xsl:output method="html" omit-xml-declaration="yes" indent="yes"/>

\t<xsl:param name="param1"/>
\t<xsl:param name="viewScopeTermIds"/>

\t<xsl:variable name="viewScopeTerms" select="eas:get_scoping_terms_from_string($viewScopeTermIds)"/>
\t<xsl:variable name="linkClasses" select="('Composite_Application_Provider', 'Application_Provider')"/>

\t<xsl:template match="knowledge_base">
\t\t<xsl:call-template name="docType"/>
\t\t<html>
\t\t\t<head>
\t\t\t\t<xsl:call-template name="commonHeadContent"/>
\t\t\t\t<xsl:for-each select="$linkClasses">
\t\t\t\t\t<xsl:call-template name="RenderInstanceLinkJavascript">
\t\t\t\t\t\t<xsl:with-param name="instanceClassName" select="current()"/>
\t\t\t\t\t\t<xsl:with-param name="targetMenu" select="()"/>
\t\t\t\t\t</xsl:call-template>
\t\t\t\t</xsl:for-each>
\t\t\t\t<title>{view_name}</title>
\t\t\t\t<script src="js/exceljs/exceljs.min.js" type="text/javascript"/>
\t\t\t\t<style>
\t\t\t\t\t.export-container {{ padding: 20px; }}
\t\t\t\t\t.btn-export {{
\t\t\t\t\t\tpadding: 10px 24px; background-color: #4472C4; color: white;
\t\t\t\t\t\tborder: none; border-radius: 4px; cursor: pointer; font-size: 14px;
\t\t\t\t\t}}
\t\t\t\t\t.btn-export:hover {{ background-color: #3461b0; }}
\t\t\t\t\t.btn-export:disabled {{ background-color: #ccc; cursor: not-allowed; }}
\t\t\t\t\t.summary-info {{ margin: 15px 0; font-size: 13px; color: #666; }}
\t\t\t\t\t.export-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 12px; }}
\t\t\t\t\t.export-table th {{ background-color: #4472C4; color: white; padding: 8px 10px; text-align: left; position: sticky; top: 0; }}
\t\t\t\t\t.export-table td {{ padding: 6px 10px; border-bottom: 1px solid #e0e0e0; }}
\t\t\t\t\t.export-table tr:nth-child(even) {{ background-color: #f8f9fa; }}
\t\t\t\t\t.table-wrapper {{ max-height: 600px; overflow-y: auto; border: 1px solid #ddd; }}
\t\t\t\t\t#loadingMessage {{ padding: 40px; text-align: center; color: #888; }}
\t\t\t\t</style>
\t\t\t</head>
\t\t\t<body>
\t\t\t\t<xsl:call-template name="Heading"/>
\t\t\t\t<div class="container-fluid export-container">
\t\t\t\t\t<div class="row">
\t\t\t\t\t\t<div class="col-xs-12">
\t\t\t\t\t\t\t<div class="page-header">
\t\t\t\t\t\t\t\t<h1>
\t\t\t\t\t\t\t\t\t<span class="text-primary"><xsl:value-of select="eas:i18n('View')"/>: </span>
\t\t\t\t\t\t\t\t\t<span class="text-darkgrey">{view_name}</span>
\t\t\t\t\t\t\t\t</h1>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<button id="btnExport" class="btn-export" disabled="disabled" onclick="exportToExcel()">Download Excel</button>
\t\t\t\t\t\t\t<div id="summaryInfo" class="summary-info">Loading data...</div>
\t\t\t\t\t\t\t<div class="table-wrapper">
\t\t\t\t\t\t\t\t<div id="loadingMessage">Loading data...</div>
\t\t\t\t\t\t\t\t<table id="dataTable" class="export-table" style="display:none;">
\t\t\t\t\t\t\t\t\t<thead>
\t\t\t\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t\t\t\t{th_elements}
\t\t\t\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t\t\t</thead>
\t\t\t\t\t\t\t\t\t<tbody id="dataTableBody"/>
\t\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<xsl:call-template name="Footer"/>

\t\t\t\t<script type="text/javascript">
\t\t\t\t\t<xsl:call-template name="RenderViewerAPIJSFunction"/>

\t\t\t\t\tlet {var_declarations};
\t\t\t\t\tvar exportRows = [];

\t\t\t\t\t$(document).ready(function() {{
\t\t\t\t\t\tconst apiList = {api_list_js};

\t\t\t\t\t\tasync function executeFetchAndRender() {{
\t\t\t\t\t\t\ttry {{
\t\t\t\t\t\t\t\tlet responses = await fetchAndRenderData(apiList);
\t\t\t\t\t\t\t\t({{ {destructuring} }} = responses);

\t\t\t\t\t\t\t\tconsole.log('Responses loaded:', responses);
\t\t\t\t\t\t\t\tbuildExportRows(responses);
\t\t\t\t\t\t\t\trenderTable();
\t\t\t\t\t\t\t}} catch (error) {{
\t\t\t\t\t\t\t\tconsole.error('Error:', error);
\t\t\t\t\t\t\t\tdocument.getElementById('loadingMessage').textContent = 'Error loading data: ' + error.message;
\t\t\t\t\t\t\t}}
\t\t\t\t\t\t}}

\t\t\t\t\t\texecuteFetchAndRender();
\t\t\t\t\t}});

\t\t\t\t\tfunction buildExportRows(responses) {{
\t\t\t\t\t\texportRows = [];
\t\t\t\t\t\t
\t\t\t\t\t\t// Try common patterns
\t\t\t\t\t\tlet data = [];
\t\t\t\t\t\tfor (const api in responses) {{
\t\t\t\t\t\t\tif (responses[api].applications) data = responses[api].applications;
\t\t\t\t\t\t\telse if (responses[api].capabilities) data = responses[api].capabilities;
\t\t\t\t\t\t\telse if (responses[api].data) data = responses[api].data;
\t\t\t\t\t\t}}

\t\t\t\t\t\tdata.forEach(function(item) {{
\t\t\t\t\t\t\texportRows.push(item);
\t\t\t\t\t\t}});
\t\t\t\t\t\t
\t\t\t\t\t\tconsole.log('Built ' + exportRows.length + ' rows for export');
\t\t\t\t\t}}

\t\t\t\t\tfunction renderTable() {{
\t\t\t\t\t\t// CRITICAL: Use document.createElement() for dynamic HTML in XSL context
\t\t\t\t\t\t// NEVER use string HTML like '&lt;tr&gt;&lt;td&gt;' - breaks XML parsing
\t\t\t\t\t\tvar tbody = document.getElementById('dataTableBody');
\t\t\t\t\t\ttbody.innerHTML = '';

\t\t\t\t\t\texportRows.forEach(function(row) {{
\t\t\t\t\t\t\tvar tr = document.createElement('tr');
\t\t\t\t\t\t\tvar fields = [{field_list}];
\t\t\t\t\t\t\tfields.forEach(function(val) {{
\t\t\t\t\t\t\t\tvar td = document.createElement('td');
\t\t\t\t\t\t\t\ttd.textContent = val || '';
\t\t\t\t\t\t\t\ttr.appendChild(td);
\t\t\t\t\t\t\t}});
\t\t\t\t\t\t\ttbody.appendChild(tr);
\t\t\t\t\t\t}});

\t\t\t\t\t\tdocument.getElementById('loadingMessage').style.display = 'none';
\t\t\t\t\t\tdocument.getElementById('dataTable').style.display = '';
\t\t\t\t\t\tdocument.getElementById('btnExport').disabled = false;
\t\t\t\t\t\tdocument.getElementById('summaryInfo').textContent = 'Total rows: ' + exportRows.length;
\t\t\t\t\t}}

\t\t\t\t\tasync function exportToExcel() {{
\t\t\t\t\t\tdocument.getElementById('btnExport').disabled = true;
\t\t\t\t\t\tdocument.getElementById('btnExport').textContent = 'Generating...';

\t\t\t\t\t\ttry {{
\t\t\t\t\t\t\tvar workbook = new ExcelJS.Workbook();
\t\t\t\t\t\t\tworkbook.creator = 'Essential Architecture Manager';
\t\t\t\t\t\t\tworkbook.created = new Date();

\t\t\t\t\t\t\tvar sheet = workbook.addWorksheet('{view_name}');
\t\t\t\t\t\t\tsheet.columns = [
\t\t\t\t\t\t\t\t{excel_col_defs}
\t\t\t\t\t\t\t];

\t\t\t\t\t\t\tvar headerRow = sheet.getRow(1);
\t\t\t\t\t\t\theaderRow.font = {{ bold: true, color: {{ argb: 'FFFFFFFF' }}, size: 11 }};
\t\t\t\t\t\t\theaderRow.fill = {{ type: 'pattern', pattern: 'solid', fgColor: {{ argb: 'FF4472C4' }} }};
\t\t\t\t\t\t\theaderRow.alignment = {{ vertical: 'middle', wrapText: true }};
\t\t\t\t\t\t\theaderRow.height = 22;

\t\t\t\t\t\t\texportRows.forEach(function(row) {{
\t\t\t\t\t\t\t\tsheet.addRow({{
\t\t\t\t\t\t\t\t\t{excel_row_props}
\t\t\t\t\t\t\t\t}});
\t\t\t\t\t\t\t}});

\t\t\t\t\t\t\tsheet.autoFilter = {{ from: 'A1', to: '{last_col_letter}1' }};
\t\t\t\t\t\t\tsheet.views = [{{ state: 'frozen', ySplit: 1 }}];

\t\t\t\t\t\t\tvar buffer = await workbook.xlsx.writeBuffer();
\t\t\t\t\t\t\tvar blob = new Blob([buffer], {{ type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }});
\t\t\t\t\t\t\tvar url = window.URL.createObjectURL(blob);
\t\t\t\t\t\t\tvar a = document.createElement('a');
\t\t\t\t\t\t\ta.href = url;
\t\t\t\t\t\t\ta.download = '{view_name.replace(" ", "_")}_' + new Date().toISOString().split('T')[0] + '.xlsx';
\t\t\t\t\t\t\ta.click();
\t\t\t\t\t\t\twindow.URL.revokeObjectURL(url);
\t\t\t\t\t\t}} catch (error) {{
\t\t\t\t\t\t\tconsole.error('Export error:', error);
\t\t\t\t\t\t\talert('Error generating Excel: ' + error.message);
\t\t\t\t\t\t}} finally {{
\t\t\t\t\t\t\tdocument.getElementById('btnExport').disabled = false;
\t\t\t\t\t\t\tdocument.getElementById('btnExport').textContent = 'Download Excel';
\t\t\t\t\t\t}}
\t\t\t\t\t}}
\t\t\t\t</script>
\t\t\t</body>
\t\t</html>
\t</xsl:template>
</xsl:stylesheet>'''

    return scaffold
def generate_api_scaffold(
    api_name: str,
    target_class: str,
    collection_name: str,
    additional_slots: list = None
) -> str:
    """
    Generate an Essential API (XSLT) following the Golden Pattern.
    Uses XSLT 3.0 for better JSON serialization via maps.
    """
    if not additional_slots:
        additional_slots = []
        
    # Generate slot outputs
    slot_outputs = []
    for slot in additional_slots:
        # Clean slot name for JSON key
        json_key = slot.replace(":", "_").replace("-", "_")
        
        # Determine if it's likely a list vs single value (heuristic)
        # In Essential, most slots are multi-valued in simple_instance
        output = f'''
                        "{json_key}": [<xsl:for-each select="pro:own_slot_value[pro:slot_reference=\'{slot}\']/pro:value">
                            "<xsl:value-of select="normalize-space(string(.))"/>"<xsl:if test="not(position()=last())">,</xsl:if>
                        </xsl:for-each>]'''
        slot_outputs.append(output)
        
    extra_slots_str = ",".join(slot_outputs) if slot_outputs else ""

    scaffold = f'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="3.0" 
    xpath-default-namespace="http://protege.stanford.edu/xml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:pro="http://protege.stanford.edu/xml" 
    xmlns:eas="http://www.enterprise-architecture.org/essential" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="pro eas xs">
    
    <!-- Pattern: Golden API v3.0 (NGV Compatible) -->
    <!-- This API delivers JSON data for {target_class} instances -->
    
    <xsl:import href="../../common/core_js_functions.xsl"/>
    <xsl:include href="../../common/core_utilities.xsl"/>
    <xsl:output method="text" encoding="UTF-8"/>
    
    <xsl:variable name="allInstances" select="//pro:simple_instance"/>
    <xsl:variable name="targetInstances" select="$allInstances[normalize-space(pro:type)=\'{target_class}\']"/>

    <xsl:template match="knowledge_base">
        {{
            "{collection_name}": [
                <xsl:for-each select="$targetInstances">
                    {{
                        "id": "<xsl:value-of select="pro:name"/>",
                        "name": "<xsl:call-template name="RenderMultiLangInstanceName"><xsl:with-param name="isForJSONAPI" select="true()"/><xsl:with-param name="theSubjectInstance" select="."/></xsl:call-template>",
                        "description": "<xsl:call-template name="RenderMultiLangInstanceDescription"><xsl:with-param name="isForJSONAPI" select="true()"/><xsl:with-param name="theSubjectInstance" select="."/></xsl:call-template>"{extra_slots_str}
                    }}<xsl:if test="not(position()=last())">,</xsl:if>
                </xsl:for-each>
            ]
        }}
    </xsl:template>
</xsl:stylesheet>
'''
    return scaffold




def generate_adapted_view_scaffold(
    view_name: str,
    external_html: str,
    external_js: str,
    sample_json: str,
    api_mappings: dict = None
) -> str:
    """
    Core logic for porting an external view.
    1. Identifies likely APIs from sample_json structure or explicit mappings.
    2. Generates an XSLT wrapper that loads these APIs.
    3. Transforms Essential data into the 'viewModel' format the external code expects.
    """
    if not api_mappings:
        api_mappings = {}
        
    try:
        sample_data = json.loads(sample_json)
    except:
        sample_data = {}

    # Identify which APIs we need
    # Heuristic: Match top-level keys in sample_json to API main properties
    api_docs = parse_api_documentation()
    apis = api_docs['apis']
    property_mappings = api_docs['property_names'] # API -> [Properties]
    
    needed_apis = list(api_mappings.values())
    
    # Auto-detection if not provided
    if not needed_apis:
        for key in sample_data.keys():
            # Find an API that provides a property similar to this key
            for api_label, props in property_mappings.items():
                if any(key.lower() in p.lower() for p in props):
                    if api_label not in needed_apis:
                        needed_apis.append(api_label)
                        break

    if not needed_apis:
        needed_apis = ["appMartAPI"] # Fallback

    # Build the viewModel mapping logic
    # This creates the JS code to copy Essential data into the structure the external code expects
    mapping_logic = []
    for key in sample_data.keys():
        # Check explicit mapping first
        source_api = api_mappings.get(key)
        
        if not source_api:
            # Fallback to heuristic
            for api_label in needed_apis:
                if any(key.lower() in p.lower() for p in property_mappings.get(api_label, [])):
                    source_api = api_label
                    break
        
        if source_api:
            # Simple mapping: assume the primary array matches
            # Use the first property of the API if it's a known API, otherwise assume key exists
            source_prop = property_mappings.get(source_api, [key])[0]
            mapping_logic.append(f"            if (responses.{source_api}) viewModel.{key} = responses.{source_api}.{source_prop} || [];")
    
    mapping_js = "\n".join(mapping_logic)
    
    # Encode content for XSL
    safe_js = encode_for_xsl(external_js)
    safe_html = external_html # HTML in body is generally safer but may need careful handling
    
    # Build scaffold
    var_declarations = ", ".join(needed_apis)
    destructuring = ", ".join(needed_apis)
    api_list_js = "[" + ", ".join([f'"{a}"' for a in needed_apis]) + "]"
    
    imports = generate_imports(include_handlebars=False, enable_roadmap=False)

    scaffold = f'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xpath-default-namespace="http://protege.stanford.edu/xml" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:eas="http://www.enterprise-architecture.org/essential">
    
{imports}
    
    <xsl:output method="html" omit-xml-declaration="yes" indent="yes"/>
    
    <xsl:template match="knowledge_base">
        <html>
            <head>
                <xsl:call-template name="commonHeadContent"/>
                <title>{view_name}</title>
                
                <script type="text/javascript">
                    <xsl:call-template name="RenderViewerAPIJSFunction"/>
                    
                    // Ported external View Model
                    var viewModel = {json.dumps(sample_data, indent=8)};
                    
                    let {var_declarations};
                    
                    $(document).ready(function() {{
                        async function loadAndAdapt() {{
                            try {{
                                let apiList = {api_list_js};
                                let responses = await fetchAndRenderData(apiList);
                                ({{ {destructuring} }} = responses);
                                
                                // Map Essential Data to Ported View Model
{mapping_js}
                                
                                // Execute Ported Logic
                                port_init();
                            }} catch (e) {{
                                console.error("Adaptation Error:", e);
                            }}
                        }}
                        loadAndAdapt();
                    }});
                    
                    function port_init() {{
{safe_js}
                    }}
                </script>
            </head>
            <body>
                <xsl:call-template name="Heading"/>
                <div class="container" style="margin-top:40px;">
                    {safe_html}
                </div>
                <xsl:call-template name="Footer"/>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
'''
    return scaffold

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
