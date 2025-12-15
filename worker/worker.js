/**
 * edu-guide Worker - Serves content from KV storage
 * KV Binding: env.KV (EDU_GUIDE_DATA namespace)
 * Binary files (images, fonts) are proxied from Pages deployment
 */

// Pages site URL for binary assets
const PAGES_ORIGIN = 'https://3842efa4.edu-guide.pages.dev';

// Binary file extensions (not stored in KV) - proxied from Pages
const BINARY_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.svg'];

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // URL 디코딩 (한글 경로 지원)
    let path = decodeURIComponent(url.pathname);

    // Handle trailing slashes
    if (path !== '/' && path.endsWith('/')) {
      path = path.slice(0, -1);
    }

    // Default to index for root
    if (path === '' || path === '/') {
      path = '/index';
    }

    try {
      // Check if this is a binary file request
      const isBinaryFile = BINARY_EXTENSIONS.some(ext => path.toLowerCase().endsWith(ext));

      if (isBinaryFile) {
        // Proxy binary files from Pages deployment
        const pagesUrl = PAGES_ORIGIN + url.pathname;
        const response = await fetch(pagesUrl, {
          headers: request.headers
        });

        // Return with caching headers
        const newHeaders = new Headers(response.headers);
        newHeaders.set('Cache-Control', 'public, max-age=86400'); // 24 hours
        newHeaders.set('X-Content-Source', 'Pages-Proxy');

        return new Response(response.body, {
          status: response.status,
          headers: newHeaders
        });
      }

      // Helper function to determine content type
      const getContentType = (p) => {
        if (p.endsWith('.css')) return 'text/css';
        if (p.endsWith('.js')) return 'application/javascript';
        if (p.endsWith('.json')) return 'application/json';
        if (p.endsWith('.xml')) return 'application/xml';
        if (p.endsWith('.svg')) return 'image/svg+xml';
        return 'text/html; charset=utf-8';
      };

      // Check if path has a file extension
      const hasExtension = /\.[a-zA-Z0-9]+$/.test(path);

      // Try to get content from KV
      let content = await env.KV.get(path, 'text');

      // If not found and no file extension, try with /index suffix
      if (!content && !hasExtension) {
        content = await env.KV.get(path + '/index', 'text');
      }

      if (content) {
        return new Response(content, {
          status: 200,
          headers: {
            'Content-Type': getContentType(path),
            'Cache-Control': 'public, max-age=3600',
            'X-Content-Source': 'KV'
          }
        });
      }

      // Not found in KV - return custom 404 page if exists
      const notFoundPage = await env.KV.get('/404', 'text');
      return new Response(notFoundPage || 'Page not found', {
        status: 404,
        headers: { 'Content-Type': 'text/html; charset=utf-8' }
      });

    } catch (error) {
      console.error('Error fetching from KV:', error);
      return new Response('Internal Server Error', {
        status: 500,
        headers: { 'Content-Type': 'text/html; charset=utf-8' }
      });
    }
  }
};
