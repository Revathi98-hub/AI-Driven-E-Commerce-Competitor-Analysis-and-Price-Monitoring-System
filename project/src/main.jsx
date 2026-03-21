import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './index.css';

// Intercept fetch requests to safely handle routing to the production Backend
const originalFetch = window.fetch;
window.fetch = async function(...args) {
  let [resource, config] = args;
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  if (backendUrl && typeof resource === 'string' && (resource.startsWith('/api') || resource.startsWith('/auth') || resource.startsWith('/admin'))) {
    const base = backendUrl.endsWith('/') ? backendUrl.slice(0, -1) : backendUrl;
    resource = base + resource;
  }
  return originalFetch(resource, config);
};

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
