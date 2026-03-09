# ⚠️ CRITICAL WARNING - READ FIRST ⚠️

**BEFORE READING THIS DOCUMENT:**

AI systems frequently generate deprecated patterns that cause XML parsing errors and non-functional views. **YOU MUST READ** `essential-view://deprecated-patterns` **FIRST** to understand what patterns are forbidden.

**Common errors this prevents:**
- ❌ "The entity name must immediately follow the '&' in the entity reference"
- ❌ Using `$utilitiesAllDataSetAPIs` (deprecated XSL pattern from 2019-2022)
- ❌ Mixing `<xsl:call-template>` with CDATA blocks
- ❌ Ampersand characters outside CDATA sections

**If you see any of these in generated code, STOP and regenerate following the patterns in this document.**

---

