/**
 * @tplanet/multi-tenant
 *
 * Multi-tenant React components for TPlanet AI CMS
 */

export { TenantContext, useTenant } from "./TenantContext.jsx";
export { TenantProvider } from "./TenantProvider.jsx";
export { TenantThemeProvider } from "./TenantThemeProvider.jsx";
export { detectTenant, getTenantFromUrl } from "./utils/tenantDetector.js";
