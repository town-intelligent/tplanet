/**
 * TenantContext - React Context for tenant information
 *
 * Provides tenant data throughout the application.
 */

import { createContext, useContext } from "react";

/**
 * @typedef {Object} TenantConfig
 * @property {string} tenantId - Unique tenant identifier
 * @property {string} name - Display name
 * @property {string[]} domains - Associated domains
 * @property {Object} features - Feature flags
 * @property {Object} theme - Theme configuration
 */

/**
 * @typedef {Object} TenantContextValue
 * @property {TenantConfig|null} tenant - Current tenant configuration
 * @property {boolean} loading - Whether tenant is being loaded
 * @property {Error|null} error - Error if tenant loading failed
 * @property {function(string): boolean} hasFeature - Check if feature is enabled
 * @property {function(string, *): *} getThemeValue - Get theme value with fallback
 */

/** @type {TenantContextValue} */
const defaultContextValue = {
  tenant: null,
  loading: true,
  error: null,
  hasFeature: () => false,
  getThemeValue: (key, fallback) => fallback,
};

export const TenantContext = createContext(defaultContextValue);

/**
 * Hook to access tenant context
 *
 * @returns {TenantContextValue}
 *
 * @example
 * const { tenant, hasFeature } = useTenant();
 * if (hasFeature('ai_secretary')) {
 *   // Show AI secretary feature
 * }
 */
export function useTenant() {
  const context = useContext(TenantContext);

  if (context === undefined) {
    throw new Error("useTenant must be used within a TenantProvider");
  }

  return context;
}
