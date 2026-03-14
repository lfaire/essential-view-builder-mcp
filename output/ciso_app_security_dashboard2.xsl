<?xml version="1.0" encoding="UTF-8"?>
<!--
    CISO Application Security Dashboard
    Built around the Application_Provider_Security_Profile class.

    Primary model:
      Application_Provider_Security_Profile
        - sec_profile_of_element
        - sec_profile_* CIA ratings and risk impacts
        - sec_profile_rbac_usage
        - sec_profile_mfa_usage
        - sec_profile_sso_usage
        - sec_profile_user_access_review_frequency
        - sec_profile_is_internal_facing
        - sec_profile_is_external_facing
        - sec_profile_is_data_encrypted_at_rest

    Enrichment API:
      busCapAppMartApps
        - applications[]
        - lifecycles[]

    Note:
      This file is staged in output/. The relative include paths assume the view
      will ultimately be deployed under the Essential Viewer application folder.
-->
<xsl:stylesheet version="2.0"
    xpath-default-namespace="http://protege.stanford.edu/xml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xalan="http://xml.apache.org/xslt"
    xmlns:pro="http://protege.stanford.edu/xml"
    xmlns:eas="http://www.enterprise-architecture.org/essential"
    xmlns:functx="http://www.functx.com"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:ess="http://www.enterprise-architecture.org/essential/errorview">

    <xsl:import href="../common/core_js_functions.xsl"/>

    <xsl:include href="../common/core_doctype.xsl"/>
    <xsl:include href="../common/core_common_head_content.xsl"/>
    <xsl:include href="../common/core_header.xsl"/>
    <xsl:include href="../common/core_footer.xsl"/>
    <xsl:include href="../common/core_external_doc_ref.xsl"/>
    <xsl:include href="../common/core_api_fetcher.xsl"/>

    <xsl:output method="html" omit-xml-declaration="yes" indent="yes"/>

    <xsl:param name="viewScopeTermIds"/>
    <xsl:variable name="viewScopeTerms" select="eas:get_scoping_terms_from_string($viewScopeTermIds)"/>
    <xsl:variable name="linkClasses" select="('Composite_Application_Provider', 'Application_Provider')"/>

    <xsl:key name="appSecurityProfilesByType" match="/node()/simple_instance[type='Application_Provider_Security_Profile']" use="type"/>
    <xsl:key name="securityEnumsByName" match="/node()/simple_instance[supertype=('Enumeration')]" use="name"/>
    <xsl:key name="stylesByName" match="/node()/simple_instance[type='Element_Style']" use="name"/>

    <xsl:variable name="securityProfiles" select="key('appSecurityProfilesByType', 'Application_Provider_Security_Profile')"/>
    <xsl:variable name="isAuthzForSecurityClasses" select="eas:isUserAuthZClasses(('Security_Profile','Application_Provider_Security_Profile'))"/>
    <xsl:variable name="isAuthzForSecurityInstances" select="eas:isUserAuthZInstances($securityProfiles)"/>

    <xsl:template match="knowledge_base">
        <xsl:call-template name="docType"/>
        <html lang="es">
            <head>
                <xsl:call-template name="commonHeadContent"/>
                <xsl:call-template name="RenderModalReportContent">
                    <xsl:with-param name="essModalClassNames" select="$linkClasses"/>
                </xsl:call-template>
                <title>Panel de Seguridad de Aplicaciones para CISO</title>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <meta charset="UTF-8"/>
                <script src="js/chartjs/Chart.min.js"/>

                <style>
                    .ciso-wrap { padding: 20px; margin-top: 70px; }
                    .ciso-summary-cards {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 16px;
                        margin-bottom: 24px;
                    }
                    .ciso-card {
                        flex: 1;
                        min-width: 180px;
                        background: #ffffff;
                        border-radius: 8px;
                        padding: 18px 22px;
                        box-shadow: 0 1px 4px rgba(0,0,0,0.10);
                        border-left: 5px solid #2c7be5;
                    }
                    .ciso-card--danger  { border-left-color: #e63757; }
                    .ciso-card--warning { border-left-color: #f6c343; }
                    .ciso-card--success { border-left-color: #00d97e; }
                    .ciso-card--info    { border-left-color: #39afd1; }
                    .ciso-card__title {
                        font-size: 11px;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                        color: #6e84a3;
                        font-weight: 700;
                        margin-bottom: 6px;
                    }
                    .ciso-card__value {
                        font-size: 34px;
                        font-weight: 700;
                        color: #12263f;
                        line-height: 1;
                    }
                    .ciso-card__sub {
                        font-size: 11px;
                        color: #95aac9;
                        margin-top: 5px;
                    }
                    .ciso-charts-row {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 20px;
                        margin-bottom: 24px;
                    }
                    .ciso-chart-panel {
                        flex: 1;
                        min-width: 260px;
                        background: #ffffff;
                        border-radius: 8px;
                        padding: 20px 20px 16px;
                        box-shadow: 0 1px 4px rgba(0,0,0,0.10);
                    }
                    .ciso-chart-panel canvas { max-height: 260px; }
                    .ciso-table-panel {
                        background: #ffffff;
                        border-radius: 8px;
                        padding: 20px;
                        box-shadow: 0 1px 4px rgba(0,0,0,0.10);
                        margin-bottom: 24px;
                    }
                    .panel-title {
                        font-size: 13px;
                        font-weight: 700;
                        color: #12263f;
                        margin-bottom: 14px;
                        padding-bottom: 10px;
                        border-bottom: 1px solid #edf2f9;
                    }
                    .ciso-table { font-size: 13px; }
                    .ciso-table thead th {
                        font-size: 11px;
                        text-transform: uppercase;
                        color: #6e84a3;
                        border-top: none;
                        font-weight: 700;
                    }
                    .ciso-badge {
                        display: inline-block;
                        padding: 3px 9px;
                        border-radius: 12px;
                        font-size: 11px;
                        font-weight: 600;
                        white-space: nowrap;
                    }
                    .ciso-badge--neutral {
                        background: #edf2f9;
                        color: #486581;
                    }
                    .ciso-flag-yes {
                        background: #d9f6e5;
                        color: #0f7b47;
                    }
                    .ciso-flag-no {
                        background: #fde2e7;
                        color: #b42318;
                    }
                    .ciso-loading {
                        text-align: center;
                        padding: 50px 20px;
                        color: #95aac9;
                    }
                    #cisoAlertMsg { display: none; }
                </style>
            </head>

            <body role="document" aria-labelledby="main-heading">
                <xsl:call-template name="Heading"/>

                <div class="ciso-wrap container-fluid">
                    <div class="row">
                        <div class="col-xs-12">
                            <div class="page-header">
                                <h1 id="main-heading">
                                    <span class="text-primary">Vista: </span>
                                    <span class="text-darkgrey">Panel de Seguridad de Aplicaciones para CISO</span>
                                </h1>
                                <p class="text-muted">
                                    Postura de seguridad de aplicaciones basada en la clase Perfil de Seguridad del Proveedor de Aplicaciones,
                                    con contexto de ciclo de vida y regulación obtenido del mart de aplicaciones.
                                </p>
                            </div>
                        </div>
                    </div>

                    <div id="cisoAlertMsg" class="alert alert-danger" role="alert"></div>
                    <div id="mainContent">
                        <div class="ciso-loading">
                            <i class="fa fa-spinner fa-spin fa-2x"></i>
                            <p>Cargando perfiles de seguridad de proveedores de aplicaciones&#8230;</p>
                        </div>
                    </div>
                </div>

                <xsl:call-template name="Footer"/>

                <script type="text/javascript">
                    <xsl:call-template name="RenderViewerAPIJSFunction"/>

                    let busCapAppMartApps;
                    let securityProfiles = [
                        <xsl:if test="$isAuthzForSecurityClasses and $isAuthzForSecurityInstances">
                            <xsl:apply-templates select="$securityProfiles" mode="securityProfileJSON"/>
                        </xsl:if>
                    ];

                    function displayError(error) {
                        console.error('Error del Panel de Perfil de Seguridad CISO:', error);
                        var alertEl = document.getElementById('cisoAlertMsg');
                        alertEl.style.display = 'block';
                        alertEl.textContent = 'Error al cargar el panel: ' + (error.message || String(error));
                        document.getElementById('mainContent').innerHTML = '';
                    }

                    $(document).ready(function() {
                        const apiList = ['busCapAppMartApps'];

                        async function executeFetchAndRender() {
                            try {
                                let responses = await fetchAndRenderData(apiList);
                                ({ busCapAppMartApps } = responses);

                                console.log('[CISO] Perfiles de seguridad:', securityProfiles.length);
                                console.log('[CISO] Perfil de seguridad de ejemplo:', securityProfiles[0]);
                                console.log('[CISO] Ejemplo de application mart:', busCapAppMartApps.applications &amp;&amp; busCapAppMartApps.applications[0]);

                                renderDashboard(securityProfiles, busCapAppMartApps);
                            } catch (error) {
                                if (typeof displayError === 'function') displayError(error);
                            }
                        }

                        executeFetchAndRender();
                    });

                    function renderDashboard(profileData, appData) {
                        var apps = appData.applications || [];
                        var lifecycles = appData.lifecycles || [];

                        var appById = {};
                        apps.forEach(function(app) {
                            appById[app.id] = app;
                        });

                        var lifecycleById = {};
                        lifecycles.forEach(function(lifecycle) {
                            lifecycleById[lifecycle.id] = {
                                name: lifecycle.shortname || lifecycle.id,
                                colour: lifecycle.colour || '#95aac9',
                                textColour: lifecycle.colourText || '#ffffff'
                            };
                        });

                        var profileRows = profileData.map(function(profile) {
                            var app = appById[profile.appId] || null;
                            var lifecycleId = app &amp;&amp; app.lifecycle_status_application_provider &amp;&amp; app.lifecycle_status_application_provider.length &gt; 0
                                ? app.lifecycle_status_application_provider[0]
                                : '';
                            var lifecycle = lifecycleById[lifecycleId] || {
                                name: 'Sin definir',
                                colour: '#dfe3eb',
                                textColour: '#4a5568'
                            };

                            return {
                                profile: profile,
                                app: app,
                                appName: app ? app.name : profile.profileName,
                                regulations: app &amp;&amp; app.regulations ? app.regulations : [],
                                lifecycle: lifecycle,
                                maxImpactScore: getMaxImpactScore(profile),
                                isExternalFacing: isPositive(profile.externalFacing),
                                isEncryptedAtRest: isPositive(profile.encryptedAtRest),
                                hasMfa: isPositive(profile.mfaUsage),
                                hasSso: isPositive(profile.ssoUsage),
                                hasRbac: isPositive(profile.rbacUsage)
                            };
                        });

                        profileRows.sort(function(a, b) {
                            if (b.isExternalFacing !== a.isExternalFacing) {
                                return Number(b.isExternalFacing) - Number(a.isExternalFacing);
                            }
                            return b.maxImpactScore - a.maxImpactScore;
                        });

                        var totalApps = apps.length;
                        var profiledApps = profileRows.length;
                        var appsWithoutProfiles = Math.max(totalApps - profiledApps, 0);
                        var mfaEnabled = countWhere(profileRows, function(row) { return row.hasMfa; });
                        var ssoEnabled = countWhere(profileRows, function(row) { return row.hasSso; });
                        var rbacEnabled = countWhere(profileRows, function(row) { return row.hasRbac; });
                        var externalFacing = countWhere(profileRows, function(row) { return row.isExternalFacing; });

                        var confidentialityBreakdown = groupStyledCounts(profileRows, function(row) {
                            return {
                                label: row.profile.confidentialityRating || 'Sin definir',
                                colour: getStyleColour(row.profile.confidentialityRatingStyle, '#95aac9')
                            };
                        });

                        var integrityBreakdown = groupStyledCounts(profileRows, function(row) {
                            return {
                                label: row.profile.integrityRating || 'Sin definir',
                                colour: getStyleColour(row.profile.integrityRatingStyle, '#95aac9')
                            };
                        });

                        var availabilityBreakdown = groupStyledCounts(profileRows, function(row) {
                            return {
                                label: row.profile.availabilityRating || 'Sin definir',
                                colour: getStyleColour(row.profile.availabilityRatingStyle, '#95aac9')
                            };
                        });

                        var confidentialityImpactBreakdown = groupStyledCounts(profileRows, function(row) {
                            return {
                                label: row.profile.confidentialityImpact || 'Sin definir',
                                colour: getStyleColour(row.profile.confidentialityImpactStyle, severityColour(row.profile.confidentialityImpact))
                            };
                        });

                        var integrityImpactBreakdown = groupStyledCounts(profileRows, function(row) {
                            return {
                                label: row.profile.integrityImpact || 'Sin definir',
                                colour: getStyleColour(row.profile.integrityImpactStyle, severityColour(row.profile.integrityImpact))
                            };
                        });

                        var availabilityImpactBreakdown = groupStyledCounts(profileRows, function(row) {
                            return {
                                label: row.profile.availabilityImpact || 'Sin definir',
                                colour: getStyleColour(row.profile.availabilityImpactStyle, severityColour(row.profile.availabilityImpact))
                            };
                        });

                        var lifecycleBreakdown = groupStyledCounts(profileRows, function(row) {
                            return {
                                label: row.lifecycle.name || 'Sin definir',
                                colour: row.lifecycle.colour || '#95aac9'
                            };
                        });

                        var html = '';
                        html += '&lt;div class="ciso-summary-cards"&gt;';
                        html += makeSummaryCard('Aplicaciones', totalApps, 'Total de proveedores de aplicaciones en alcance', '');
                        html += makeSummaryCard('Perfiles de Seguridad', profiledApps, 'Perfiles de seguridad vinculados a aplicaciones', 'info');
                        html += makeSummaryCard('Sin Perfil', appsWithoutProfiles, 'Aplicaciones sin perfil de seguridad vinculado', 'danger');
                        html += makeSummaryCard('MFA Habilitado', mfaEnabled, 'Perfiles que indican uso de MFA', 'success');
                        html += makeSummaryCard('SSO Habilitado', ssoEnabled, 'Perfiles que indican uso de SSO', 'success');
                        html += makeSummaryCard('RBAC Habilitado', rbacEnabled, 'Perfiles que indican uso de RBAC', 'warning');
                        html += makeSummaryCard('Exposición Externa', externalFacing, 'Perfiles marcados como expuestos externamente', 'danger');
                        html += '&lt;/div&gt;';

                        html += '&lt;div class="ciso-charts-row"&gt;';
                        html += '&lt;div class="ciso-chart-panel"&gt;&lt;h5 class="panel-title"&gt;Valoración de Confidencialidad&lt;/h5&gt;&lt;canvas id="confidentialityChart"&gt;&lt;/canvas&gt;&lt;/div&gt;';
                        html += '&lt;div class="ciso-chart-panel"&gt;&lt;h5 class="panel-title"&gt;Valoración de Integridad&lt;/h5&gt;&lt;canvas id="integrityChart"&gt;&lt;/canvas&gt;&lt;/div&gt;';
                        html += '&lt;div class="ciso-chart-panel"&gt;&lt;h5 class="panel-title"&gt;Valoración de Disponibilidad&lt;/h5&gt;&lt;canvas id="availabilityChart"&gt;&lt;/canvas&gt;&lt;/div&gt;';
                        html += '&lt;/div&gt;';

                        html += '&lt;div class="ciso-charts-row"&gt;';
                        html += '&lt;div class="ciso-chart-panel"&gt;&lt;h5 class="panel-title"&gt;Impacto de Riesgo de Confidencialidad&lt;/h5&gt;&lt;canvas id="confidentialityImpactChart"&gt;&lt;/canvas&gt;&lt;/div&gt;';
                        html += '&lt;div class="ciso-chart-panel"&gt;&lt;h5 class="panel-title"&gt;Impacto de Riesgo de Integridad&lt;/h5&gt;&lt;canvas id="integrityImpactChart"&gt;&lt;/canvas&gt;&lt;/div&gt;';
                        html += '&lt;div class="ciso-chart-panel"&gt;&lt;h5 class="panel-title"&gt;Impacto de Riesgo de Disponibilidad&lt;/h5&gt;&lt;canvas id="availabilityImpactChart"&gt;&lt;/canvas&gt;&lt;/div&gt;';
                        html += '&lt;/div&gt;';

                        html += '&lt;div class="ciso-charts-row"&gt;';
                        html += '&lt;div class="ciso-chart-panel"&gt;&lt;h5 class="panel-title"&gt;Estado de Ciclo de Vida de Aplicaciones Perfiladas&lt;/h5&gt;&lt;canvas id="lifecycleChart"&gt;&lt;/canvas&gt;&lt;/div&gt;';
                        html += '&lt;div class="ciso-table-panel" style="flex:1.8;min-width:640px;"&gt;';
                        html += '&lt;h5 class="panel-title"&gt;Aplicaciones con Mayor Exposición&lt;/h5&gt;';

                        if (profileRows.length &gt; 0) {
                            html += '&lt;div class="table-responsive"&gt;';
                            html += '&lt;table class="table table-hover ciso-table"&gt;';
                            html += '&lt;thead&gt;&lt;tr&gt;';
                            html += '&lt;th&gt;Aplicación&lt;/th&gt;';
                            html += '&lt;th&gt;Ciclo de Vida&lt;/th&gt;';
                            html += '&lt;th&gt;Valoración C&lt;/th&gt;';
                            html += '&lt;th&gt;Impacto C&lt;/th&gt;';
                            html += '&lt;th&gt;Valoración I&lt;/th&gt;';
                            html += '&lt;th&gt;Impacto I&lt;/th&gt;';
                            html += '&lt;th&gt;Valoración A&lt;/th&gt;';
                            html += '&lt;th&gt;Impacto A&lt;/th&gt;';
                            html += '&lt;th&gt;Externa&lt;/th&gt;';
                            html += '&lt;th&gt;Cifrada&lt;/th&gt;';
                            html += '&lt;th&gt;MFA&lt;/th&gt;';
                            html += '&lt;th&gt;SSO&lt;/th&gt;';
                            html += '&lt;th&gt;RBAC&lt;/th&gt;';
                            html += '&lt;th&gt;Revisión de Acceso&lt;/th&gt;';
                            html += '&lt;th&gt;Regulaciones&lt;/th&gt;';
                            html += '&lt;/tr&gt;&lt;/thead&gt;&lt;tbody&gt;';

                            profileRows.slice(0, 20).forEach(function(row) {
                                html += '&lt;tr&gt;';
                                html += '&lt;td&gt;&lt;strong&gt;' + escHtml(row.appName || 'Desconocida') + '&lt;/strong&gt;&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeStyledBadge(row.lifecycle.name, { backgroundColour: row.lifecycle.colour, colour: row.lifecycle.textColour }) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeStyledBadge(row.profile.confidentialityRating || 'Sin definir', row.profile.confidentialityRatingStyle) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeStyledBadge(row.profile.confidentialityImpact || 'Sin definir', row.profile.confidentialityImpactStyle) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeStyledBadge(row.profile.integrityRating || 'Sin definir', row.profile.integrityRatingStyle) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeStyledBadge(row.profile.integrityImpact || 'Sin definir', row.profile.integrityImpactStyle) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeStyledBadge(row.profile.availabilityRating || 'Sin definir', row.profile.availabilityRatingStyle) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeStyledBadge(row.profile.availabilityImpact || 'Sin definir', row.profile.availabilityImpactStyle) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeFlagBadge(row.isExternalFacing) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeFlagBadge(row.isEncryptedAtRest) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeFlagBadge(row.hasMfa) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeFlagBadge(row.hasSso) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeFlagBadge(row.hasRbac) + '&lt;/td&gt;';
                                html += '&lt;td&gt;' + makeStyledBadge(row.profile.accessReviewFrequency || 'Sin definir', row.profile.accessReviewFrequencyStyle) + '&lt;/td&gt;';
                                html += '&lt;td&gt;&lt;span class="ciso-badge ciso-badge--neutral"&gt;' + row.regulations.length + '&lt;/span&gt;&lt;/td&gt;';
                                html += '&lt;/tr&gt;';
                            });

                            html += '&lt;/tbody&gt;&lt;/table&gt;&lt;/div&gt;';
                        } else {
                            html += '&lt;p class="text-muted"&gt;No se encontraron instancias de Perfil de Seguridad del Proveedor de Aplicaciones o el usuario actual no tiene autorización para verlas.&lt;/p&gt;';
                        }

                        html += '&lt;/div&gt;';
                        html += '&lt;/div&gt;';

                        document.getElementById('mainContent').innerHTML = html;

                        renderDoughnutChart('confidentialityChart', confidentialityBreakdown);
                        renderDoughnutChart('integrityChart', integrityBreakdown);
                        renderDoughnutChart('availabilityChart', availabilityBreakdown);
                        renderDoughnutChart('confidentialityImpactChart', confidentialityImpactBreakdown);
                        renderDoughnutChart('integrityImpactChart', integrityImpactBreakdown);
                        renderDoughnutChart('availabilityImpactChart', availabilityImpactBreakdown);
                        renderDoughnutChart('lifecycleChart', lifecycleBreakdown);
                    }

                    function countWhere(items, predicate) {
                        var count = 0;
                        items.forEach(function(item) {
                            if (predicate(item)) count++;
                        });
                        return count;
                    }

                    function groupStyledCounts(items, extractor) {
                        var counts = {};
                        var colours = {};
                        items.forEach(function(item) {
                            var result = extractor(item);
                            var label = result.label || 'Sin definir';
                            counts[label] = (counts[label] || 0) + 1;
                            if (!colours[label]) colours[label] = result.colour || '#95aac9';
                        });
                        return { counts: counts, colours: colours };
                    }

                    function renderDoughnutChart(canvasId, grouped) {
                        var labels = Object.keys(grouped.counts || {});
                        var values = labels.map(function(label) { return grouped.counts[label]; });
                        var colours = labels.map(function(label) { return grouped.colours[label] || '#95aac9'; });
                        if (labels.length === 0) {
                            labels = ['Sin datos'];
                            values = [1];
                            colours = ['#dfe3eb'];
                        }

                        new Chart(document.getElementById(canvasId), {
                            type: 'doughnut',
                            data: {
                                labels: labels,
                                datasets: [{
                                    data: values,
                                    backgroundColor: colours,
                                    borderColor: '#ffffff',
                                    borderWidth: 2
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: true,
                                cutout: '55%',
                                plugins: {
                                    legend: {
                                        position: 'bottom',
                                        labels: { boxWidth: 12, font: { size: 11 }, padding: 10 }
                                    },
                                    tooltip: {
                                        callbacks: {
                                            label: function(context) {
                                                return ' ' + context.label + ': ' + context.raw + ' aplicaciones';
                                            }
                                        }
                                    }
                                }
                            }
                        });
                    }

                    function makeSummaryCard(title, value, sub, type) {
                        var cls = type ? 'ciso-card ciso-card--' + type : 'ciso-card';
                        return '&lt;div class="' + cls + '"&gt;' +
                            '&lt;div class="ciso-card__title"&gt;' + escHtml(title) + '&lt;/div&gt;' +
                            '&lt;div class="ciso-card__value"&gt;' + value + '&lt;/div&gt;' +
                            '&lt;div class="ciso-card__sub"&gt;' + escHtml(sub) + '&lt;/div&gt;' +
                            '&lt;/div&gt;';
                    }

                    function makeStyledBadge(label, styleObj) {
                        var background = (styleObj &amp;&amp; styleObj.backgroundColour) ? styleObj.backgroundColour : '#edf2f9';
                        var colour = (styleObj &amp;&amp; styleObj.colour) ? styleObj.colour : '#486581';
                        return '&lt;span class="ciso-badge" style="background:' + escHtml(background) + ';color:' + escHtml(colour) + '"&gt;' + escHtml(label || 'Sin definir') + '&lt;/span&gt;';
                    }

                    function makeFlagBadge(value) {
                        var label = value ? 'Sí' : 'No';
                        var cls = value ? 'ciso-badge ciso-flag-yes' : 'ciso-badge ciso-flag-no';
                        return '&lt;span class="' + cls + '"&gt;' + label + '&lt;/span&gt;';
                    }

                    function getStyleColour(styleObj, fallback) {
                        return (styleObj &amp;&amp; styleObj.backgroundColour) ? styleObj.backgroundColour : fallback;
                    }

                    function getMaxImpactScore(profile) {
                        return Math.max(
                            severityScore(profile.confidentialityImpact),
                            severityScore(profile.integrityImpact),
                            severityScore(profile.availabilityImpact)
                        );
                    }

                    function severityScore(label) {
                        var key = (label || '').toUpperCase();
                        if (key.indexOf('CRITICAL') &gt; -1 || key.indexOf('CRITICO') &gt; -1 || key.indexOf('CRÍTICO') &gt; -1) return 4;
                        if (key.indexOf('HIGH') &gt; -1 || key.indexOf('ALTO') &gt; -1) return 3;
                        if (key.indexOf('MEDIUM') &gt; -1 || key.indexOf('MEDIO') &gt; -1) return 2;
                        if (key.indexOf('LOW') &gt; -1 || key.indexOf('BAJO') &gt; -1) return 1;
                        return 0;
                    }

                    function severityColour(label) {
                        var score = severityScore(label);
                        if (score === 4) return '#b42318';
                        if (score === 3) return '#e63757';
                        if (score === 2) return '#f6c343';
                        if (score === 1) return '#48bb78';
                        return '#95aac9';
                    }

                    function isPositive(value) {
                        var normalized = String(value || '').toLowerCase();
                        return normalized === 'true' ||
                            normalized === 'yes' ||
                            normalized === 'y' ||
                            normalized === 'si' ||
                            normalized === 'sí' ||
                            normalized === 's' ||
                            normalized.indexOf('enabled') &gt; -1 ||
                            normalized.indexOf('in use') &gt; -1 ||
                            normalized.indexOf('used') &gt; -1 ||
                            normalized.indexOf('required') &gt; -1 ||
                            normalized.indexOf('enforced') &gt; -1 ||
                            normalized.indexOf('habilitado') &gt; -1 ||
                            normalized.indexOf('en uso') &gt; -1 ||
                            normalized.indexOf('usado') &gt; -1 ||
                            normalized.indexOf('requerido') &gt; -1 ||
                            normalized.indexOf('obligatorio') &gt; -1;
                    }

                    function escHtml(str) {
                        if (str === null || typeof str === 'undefined') return '';
                        var div = document.createElement('div');
                        div.appendChild(document.createTextNode(String(str)));
                        return div.innerHTML;
                    }
                </script>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="node()" mode="securityProfileJSON">
        <xsl:variable name="availabilityEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_availability_rating']/value)"/>
        <xsl:variable name="confidentialityEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_confidentiality_rating']/value)"/>
        <xsl:variable name="integrityEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_integrity_rating']/value)"/>
        <xsl:variable name="availabilityImpactEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_availability_risk_impact']/value)"/>
        <xsl:variable name="confidentialityImpactEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_confidentiality_risk_impact']/value)"/>
        <xsl:variable name="integrityImpactEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_integrity_risk_impact']/value)"/>
        <xsl:variable name="rbacEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_rbac_usage']/value)"/>
        <xsl:variable name="mfaEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_mfa_usage']/value)"/>
        <xsl:variable name="ssoEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_sso_usage']/value)"/>
        <xsl:variable name="accessReviewEnum" select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_user_access_review_frequency']/value)"/>

        <xsl:variable name="availabilityStyle" select="key('stylesByName', $availabilityEnum/own_slot_value[slot_reference = 'element_styling_classes']/value)[1]"/>
        <xsl:variable name="confidentialityStyle" select="key('stylesByName', $confidentialityEnum/own_slot_value[slot_reference = 'element_styling_classes']/value)[1]"/>
        <xsl:variable name="integrityStyle" select="key('stylesByName', $integrityEnum/own_slot_value[slot_reference = 'element_styling_classes']/value)[1]"/>
        <xsl:variable name="availabilityImpactStyle" select="key('stylesByName', $availabilityImpactEnum/own_slot_value[slot_reference = 'element_styling_classes']/value)[1]"/>
        <xsl:variable name="confidentialityImpactStyle" select="key('stylesByName', $confidentialityImpactEnum/own_slot_value[slot_reference = 'element_styling_classes']/value)[1]"/>
        <xsl:variable name="integrityImpactStyle" select="key('stylesByName', $integrityImpactEnum/own_slot_value[slot_reference = 'element_styling_classes']/value)[1]"/>
        <xsl:variable name="accessReviewStyle" select="key('stylesByName', $accessReviewEnum/own_slot_value[slot_reference = 'element_styling_classes']/value)[1]"/>

        {
            "id": "<xsl:value-of select="eas:validJSONString(current()/name)"/>",
            "profileName": "<xsl:value-of select="eas:validJSONString(current()/own_slot_value[slot_reference = 'name']/value)"/>",
            "appId": "<xsl:value-of select="eas:validJSONString(current()/own_slot_value[slot_reference = 'sec_profile_of_element']/value)"/>",
            "availabilityRating": "<xsl:value-of select="eas:validJSONString($availabilityEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "confidentialityRating": "<xsl:value-of select="eas:validJSONString($confidentialityEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "integrityRating": "<xsl:value-of select="eas:validJSONString($integrityEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "availabilityImpact": "<xsl:value-of select="eas:validJSONString($availabilityImpactEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "confidentialityImpact": "<xsl:value-of select="eas:validJSONString($confidentialityImpactEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "integrityImpact": "<xsl:value-of select="eas:validJSONString($integrityImpactEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "rbacUsage": "<xsl:value-of select="eas:validJSONString($rbacEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "mfaUsage": "<xsl:value-of select="eas:validJSONString($mfaEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "ssoUsage": "<xsl:value-of select="eas:validJSONString($ssoEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "accessReviewFrequency": "<xsl:value-of select="eas:validJSONString($accessReviewEnum/own_slot_value[slot_reference = 'name']/value)"/>",
            "internalFacing": "<xsl:value-of select="eas:validJSONString(current()/own_slot_value[slot_reference = 'sec_profile_is_internal_facing']/value)"/>",
            "externalFacing": "<xsl:value-of select="eas:validJSONString(current()/own_slot_value[slot_reference = 'sec_profile_is_external_facing']/value)"/>",
            "encryptedAtRest": "<xsl:value-of select="eas:validJSONString(current()/own_slot_value[slot_reference = 'sec_profile_is_data_encrypted_at_rest']/value)"/>",
            "authenticationMethods": [
                <xsl:for-each select="key('securityEnumsByName', current()/own_slot_value[slot_reference = 'sec_profile_authentication_methods']/value)">
                    "<xsl:value-of select="eas:validJSONString(current()/own_slot_value[slot_reference = 'name']/value)"/>"<xsl:if test="position() != last()">,</xsl:if>
                </xsl:for-each>
            ],
            "availabilityRatingStyle": {
                "backgroundColour": "<xsl:value-of select="eas:validJSONString($availabilityStyle/own_slot_value[slot_reference = 'element_style_colour']/value)"/>",
                "colour": "<xsl:value-of select="eas:validJSONString($availabilityStyle/own_slot_value[slot_reference = 'element_style_text_colour']/value)"/>"
            },
            "confidentialityRatingStyle": {
                "backgroundColour": "<xsl:value-of select="eas:validJSONString($confidentialityStyle/own_slot_value[slot_reference = 'element_style_colour']/value)"/>",
                "colour": "<xsl:value-of select="eas:validJSONString($confidentialityStyle/own_slot_value[slot_reference = 'element_style_text_colour']/value)"/>"
            },
            "integrityRatingStyle": {
                "backgroundColour": "<xsl:value-of select="eas:validJSONString($integrityStyle/own_slot_value[slot_reference = 'element_style_colour']/value)"/>",
                "colour": "<xsl:value-of select="eas:validJSONString($integrityStyle/own_slot_value[slot_reference = 'element_style_text_colour']/value)"/>"
            },
            "availabilityImpactStyle": {
                "backgroundColour": "<xsl:value-of select="eas:validJSONString($availabilityImpactStyle/own_slot_value[slot_reference = 'element_style_colour']/value)"/>",
                "colour": "<xsl:value-of select="eas:validJSONString($availabilityImpactStyle/own_slot_value[slot_reference = 'element_style_text_colour']/value)"/>"
            },
            "confidentialityImpactStyle": {
                "backgroundColour": "<xsl:value-of select="eas:validJSONString($confidentialityImpactStyle/own_slot_value[slot_reference = 'element_style_colour']/value)"/>",
                "colour": "<xsl:value-of select="eas:validJSONString($confidentialityImpactStyle/own_slot_value[slot_reference = 'element_style_text_colour']/value)"/>"
            },
            "integrityImpactStyle": {
                "backgroundColour": "<xsl:value-of select="eas:validJSONString($integrityImpactStyle/own_slot_value[slot_reference = 'element_style_colour']/value)"/>",
                "colour": "<xsl:value-of select="eas:validJSONString($integrityImpactStyle/own_slot_value[slot_reference = 'element_style_text_colour']/value)"/>"
            },
            "accessReviewFrequencyStyle": {
                "backgroundColour": "<xsl:value-of select="eas:validJSONString($accessReviewStyle/own_slot_value[slot_reference = 'element_style_colour']/value)"/>",
                "colour": "<xsl:value-of select="eas:validJSONString($accessReviewStyle/own_slot_value[slot_reference = 'element_style_text_colour']/value)"/>"
            }
        }<xsl:if test="position() != last()">,</xsl:if>
    </xsl:template>

</xsl:stylesheet>
