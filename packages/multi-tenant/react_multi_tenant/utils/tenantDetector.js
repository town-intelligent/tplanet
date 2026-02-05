/**
 * Tenant detection utilities
 *
 * Detects tenant from URL subdomain or domain.
 */

/**
 * Known subdomain to tenant ID mappings
 * Can be extended via configuration
 */
const DEFAULT_SUBDOMAIN_MAP = {
  nantou: "nantou-gov",
  demo: "demo",
};

/**
 * Known full domain to tenant ID mappings
 */
const DEFAULT_DOMAIN_MAP = {
  "cms.ntsdgs.tw": "nantou-gov",
};

/**
 * Subdomains that should be ignored (not treated as tenant identifiers)
 */
const IGNORED_SUBDOMAINS = new Set([
  "www",
  "api",
  "admin",
  "app",
  "beta",
  "staging",
  "dev",
  "localhost",
]);

/**
 * Detect tenant ID from current URL
 *
 * Detection order:
 * 1. Full domain match
 * 2. Subdomain match
 * 3. Returns null if no match
 *
 * @param {Object} [options] - Detection options
 * @param {Object} [options.subdomainMap] - Custom subdomain to tenant mappings
 * @param {Object} [options.domainMap] - Custom domain to tenant mappings
 * @param {string} [options.url] - URL to parse (defaults to window.location)
 * @returns {string|null} Tenant ID or null
 *
 * @example
 * // At https://nantou.tplanet.ai
 * detectTenant(); // Returns 'nantou-gov'
 *
 * @example
 * // At https://cms.ntsdgs.tw
 * detectTenant(); // Returns 'nantou-gov'
 *
 * @example
 * // With custom mapping
 * detectTenant({
 *   subdomainMap: { custom: 'custom-tenant' }
 * });
 */
export function detectTenant(options = {}) {
  const {
    subdomainMap = DEFAULT_SUBDOMAIN_MAP,
    domainMap = DEFAULT_DOMAIN_MAP,
    url = typeof window !== "undefined" ? window.location.href : null,
  } = options;

  if (!url) return null;

  try {
    const parsedUrl = new URL(url);
    const hostname = parsedUrl.hostname.toLowerCase();

    // 1. Check full domain match
    if (domainMap[hostname]) {
      return domainMap[hostname];
    }

    // 2. Check subdomain
    const parts = hostname.split(".");
    if (parts.length >= 2) {
      const subdomain = parts[0];

      // Skip ignored subdomains
      if (IGNORED_SUBDOMAINS.has(subdomain)) {
        return null;
      }

      // Check mapping
      if (subdomainMap[subdomain]) {
        return subdomainMap[subdomain];
      }

      // Use subdomain as tenant ID if it looks valid
      if (isValidTenantId(subdomain)) {
        return subdomain;
      }
    }

    return null;
  } catch (error) {
    console.error("Failed to parse URL for tenant detection:", error);
    return null;
  }
}

/**
 * Get tenant ID from a specific URL
 * (Alias for detectTenant with url option)
 *
 * @param {string} url - URL to parse
 * @param {Object} [options] - Additional options
 * @returns {string|null} Tenant ID or null
 */
export function getTenantFromUrl(url, options = {}) {
  return detectTenant({ ...options, url });
}

/**
 * Check if a string is a valid tenant ID format
 *
 * Valid: lowercase letters, numbers, hyphens
 * Length: 2-50 characters
 *
 * @param {string} id - Potential tenant ID
 * @returns {boolean}
 */
export function isValidTenantId(id) {
  if (!id || typeof id !== "string") return false;
  if (id.length < 2 || id.length > 50) return false;
  return /^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]{1,2}$/.test(id);
}

/**
 * Build tenant-specific URL
 *
 * @param {string} tenantId - Tenant identifier
 * @param {string} baseDomain - Base domain (e.g., 'tplanet.ai')
 * @param {string} [path] - Optional path
 * @param {boolean} [https] - Use HTTPS (default: true)
 * @returns {string} Full URL
 *
 * @example
 * buildTenantUrl('nantou-gov', 'tplanet.ai', '/dashboard');
 * // Returns 'https://nantou-gov.tplanet.ai/dashboard'
 */
export function buildTenantUrl(tenantId, baseDomain, path = "", https = true) {
  const protocol = https ? "https" : "http";
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${protocol}://${tenantId}.${baseDomain}${normalizedPath}`;
}
