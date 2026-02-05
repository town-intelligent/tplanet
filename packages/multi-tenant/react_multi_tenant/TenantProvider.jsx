/**
 * TenantProvider - Loads and provides tenant configuration
 *
 * Fetches tenant config from API or detects from URL.
 */

import { useState, useEffect, useCallback, useMemo } from "react";
import { TenantContext } from "./TenantContext.jsx";
import { detectTenant } from "./utils/tenantDetector.js";

/**
 * Provider component that loads tenant configuration
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Child components
 * @param {string} [props.configUrl] - API endpoint for tenant config
 * @param {Object} [props.staticConfig] - Static tenant configuration (bypasses API)
 * @param {string} [props.defaultTenant] - Default tenant ID if detection fails
 * @param {function} [props.onTenantLoad] - Callback when tenant is loaded
 * @param {function} [props.onError] - Callback on error
 *
 * @example
 * <TenantProvider configUrl="/api/tenant/config">
 *   <App />
 * </TenantProvider>
 *
 * @example
 * // With static config (for testing or SSR)
 * <TenantProvider staticConfig={{ tenantId: 'test', name: 'Test' }}>
 *   <App />
 * </TenantProvider>
 */
export function TenantProvider({
  children,
  configUrl = "/api/tenant/config",
  staticConfig = null,
  defaultTenant = null,
  onTenantLoad = null,
  onError = null,
}) {
  const [tenant, setTenant] = useState(staticConfig);
  const [loading, setLoading] = useState(!staticConfig);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Skip if static config is provided
    if (staticConfig) {
      setLoading(false);
      onTenantLoad?.(staticConfig);
      return;
    }

    const loadTenant = async () => {
      try {
        setLoading(true);
        setError(null);

        // First, detect tenant from URL
        const detectedTenantId = detectTenant() || defaultTenant;

        // Build API URL with tenant hint
        const url = new URL(configUrl, window.location.origin);
        if (detectedTenantId) {
          url.searchParams.set("tenant_id", detectedTenantId);
        }

        const response = await fetch(url.toString(), {
          headers: {
            Accept: "application/json",
            ...(detectedTenantId && { "X-Tenant-ID": detectedTenantId }),
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to load tenant config: ${response.status}`);
        }

        const config = await response.json();
        setTenant(config);
        onTenantLoad?.(config);
      } catch (err) {
        console.error("Failed to load tenant configuration:", err);
        setError(err);
        onError?.(err);
      } finally {
        setLoading(false);
      }
    };

    loadTenant();
  }, [configUrl, staticConfig, defaultTenant, onTenantLoad, onError]);

  /**
   * Check if a feature is enabled for the current tenant
   */
  const hasFeature = useCallback(
    (featureName) => {
      if (!tenant?.features) return false;
      return Boolean(tenant.features[featureName]);
    },
    [tenant]
  );

  /**
   * Get a theme value with optional fallback
   */
  const getThemeValue = useCallback(
    (key, fallback = null) => {
      if (!tenant?.theme) return fallback;
      return tenant.theme[key] ?? fallback;
    },
    [tenant]
  );

  const contextValue = useMemo(
    () => ({
      tenant,
      loading,
      error,
      hasFeature,
      getThemeValue,
    }),
    [tenant, loading, error, hasFeature, getThemeValue]
  );

  return (
    <TenantContext.Provider value={contextValue}>
      {children}
    </TenantContext.Provider>
  );
}
