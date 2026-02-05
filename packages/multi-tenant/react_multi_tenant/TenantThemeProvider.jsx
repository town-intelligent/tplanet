/**
 * TenantThemeProvider - Applies tenant-specific theme via CSS variables
 *
 * Injects CSS custom properties based on tenant theme configuration.
 */

import { useEffect, useMemo } from "react";
import { useTenant } from "./TenantContext.jsx";

/**
 * Default theme values
 */
const DEFAULT_THEME = {
  primary_color: "#1976d2",
  secondary_color: "#424242",
  background_color: "#ffffff",
  text_color: "#212121",
  error_color: "#d32f2f",
  success_color: "#388e3c",
  warning_color: "#f57c00",
  info_color: "#0288d1",
  border_radius: "8px",
  font_family: "'Noto Sans TC', 'Roboto', sans-serif",
};

/**
 * Maps theme config keys to CSS variable names
 */
const CSS_VAR_MAP = {
  primary_color: "--tenant-primary",
  secondary_color: "--tenant-secondary",
  background_color: "--tenant-background",
  text_color: "--tenant-text",
  error_color: "--tenant-error",
  success_color: "--tenant-success",
  warning_color: "--tenant-warning",
  info_color: "--tenant-info",
  border_radius: "--tenant-border-radius",
  font_family: "--tenant-font-family",
};

/**
 * Provider component that applies tenant theme via CSS variables
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Child components
 * @param {string} [props.targetSelector] - CSS selector for theme target (default: :root)
 * @param {Object} [props.defaultTheme] - Override default theme values
 *
 * @example
 * <TenantProvider configUrl="/api/tenant/config">
 *   <TenantThemeProvider>
 *     <App />
 *   </TenantThemeProvider>
 * </TenantProvider>
 */
export function TenantThemeProvider({
  children,
  targetSelector = ":root",
  defaultTheme = {},
}) {
  const { tenant, loading } = useTenant();

  // Merge default theme with tenant theme
  const mergedTheme = useMemo(() => {
    const base = { ...DEFAULT_THEME, ...defaultTheme };
    if (!tenant?.theme) return base;
    return { ...base, ...tenant.theme };
  }, [tenant, defaultTheme]);

  // Apply CSS variables when theme changes
  useEffect(() => {
    if (loading) return;

    const target =
      targetSelector === ":root"
        ? document.documentElement
        : document.querySelector(targetSelector);

    if (!target) {
      console.warn(`TenantThemeProvider: Target not found: ${targetSelector}`);
      return;
    }

    // Apply each theme value as a CSS variable
    Object.entries(CSS_VAR_MAP).forEach(([themeKey, cssVar]) => {
      const value = mergedTheme[themeKey];
      if (value !== undefined) {
        target.style.setProperty(cssVar, value);
      }
    });

    // Apply any additional custom theme properties
    if (tenant?.theme) {
      Object.entries(tenant.theme).forEach(([key, value]) => {
        if (!CSS_VAR_MAP[key] && typeof value === "string") {
          // Convert snake_case to kebab-case for CSS var name
          const cssVar = `--tenant-${key.replace(/_/g, "-")}`;
          target.style.setProperty(cssVar, value);
        }
      });
    }

    // Cleanup function to remove CSS variables
    return () => {
      Object.values(CSS_VAR_MAP).forEach((cssVar) => {
        target.style.removeProperty(cssVar);
      });
    };
  }, [mergedTheme, loading, targetSelector, tenant]);

  return children;
}

/**
 * Hook to generate inline style object from tenant theme
 *
 * @param {Object} styleMap - Map of style property to theme key
 * @returns {Object} React style object
 *
 * @example
 * const style = useTenantStyle({
 *   backgroundColor: 'primary_color',
 *   color: 'text_color',
 * });
 * return <div style={style}>...</div>;
 */
export function useTenantStyle(styleMap) {
  const { tenant } = useTenant();

  return useMemo(() => {
    const style = {};

    Object.entries(styleMap).forEach(([styleProp, themeKey]) => {
      const value = tenant?.theme?.[themeKey] ?? DEFAULT_THEME[themeKey];
      if (value !== undefined) {
        style[styleProp] = value;
      }
    });

    return style;
  }, [tenant, styleMap]);
}
