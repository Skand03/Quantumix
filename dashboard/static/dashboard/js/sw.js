/**
 * Service Worker for Bionic Hand IoT Dashboard PWA
 * Provides offline functionality, caching, and background sync
 */

const CACHE_NAME = 'bionic-hand-dashboard-v1.0.0';
const OFFLINE_URL = '/dashboard/offline/';

// Resources to cache for offline functionality
const CACHE_URLS = [
    '/dashboard/',
    '/dashboard/analytics/',
    '/dashboard/control/',
    '/dashboard/settings/',
    '/dashboard/model-testing/',
    '/static/dashboard/js/notifications.js',
    '/static/dashboard/css/mobile-responsive.css',
    '/static/dashboard/images/bionic-hand-logo.png',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://cdn.jsdelivr.net/npm/chart.js',
    OFFLINE_URL
];

// API endpoints to cache
const API_CACHE_URLS = [
    '/api/sensor-data/',
    '/api/device-status/',
    '/api/battery-status/',
    '/api/system-health/'
];

// Background sync tag names
const SYNC_TAGS = {
    DEVICE_CONTROL: 'device-control-sync',
    NOTIFICATION_LOG: 'notification-log-sync',
    ANALYTICS_DATA: 'analytics-data-sync'
};

// Install event - cache resources
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installing...');

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Service Worker: Caching files');
                return cache.addAll(CACHE_URLS);
            })
            .then(() => {
                console.log('Service Worker: Installation complete');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('Service Worker: Installation failed:', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activating...');

    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== CACHE_NAME) {
                            console.log('Service Worker: Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker: Activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', (event) => {
    // Skip cross-origin requests
    if (!event.request.url.startsWith(self.location.origin)) {
        return;
    }

    // Handle different types of requests
    if (event.request.url.includes('/api/')) {
        event.respondWith(handleApiRequest(event.request));
    } else if (event.request.destination === 'document') {
        event.respondWith(handleDocumentRequest(event.request));
    } else {
        event.respondWith(handleStaticRequest(event.request));
    }
});

// Handle API requests with caching and fallback
async function handleApiRequest(request) {
    const url = new URL(request.url);
    const cacheKey = `api-${url.pathname}`;

    try {
        // Try to fetch from network first
        const networkResponse = await fetch(request.clone());

        if (networkResponse.ok) {
            // Cache successful responses
            const cache = await caches.open(CACHE_NAME);
            cache.put(cacheKey, networkResponse.clone());

            return networkResponse;
        } else {
            throw new Error(`HTTP ${networkResponse.status}`);
        }
    } catch (error) {
        console.log('Service Worker: Network request failed, trying cache:', error);

        // Try to serve from cache
        const cache = await caches.open(CACHE_NAME);
        const cachedResponse = await cache.match(cacheKey);

        if (cachedResponse) {
            console.log('Service Worker: Serving API response from cache');
            return cachedResponse;
        }

        // Return offline fallback data
        return new Response(JSON.stringify(getOfflineApiData(url.pathname)), {
            status: 200,
            headers: {
                'Content-Type': 'application/json',
                'SW-Offline': 'true'
            }
        });
    }
}

// Handle document requests
async function handleDocumentRequest(request) {
    try {
        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            return networkResponse;
        } else {
            throw new Error(`HTTP ${networkResponse.status}`);
        }
    } catch (error) {
        console.log('Service Worker: Document request failed, serving offline page');

        const cache = await caches.open(CACHE_NAME);
        const offlineResponse = await cache.match(OFFLINE_URL);

        return offlineResponse || new Response('Offline', {
            status: 503,
            statusText: 'Service Unavailable'
        });
    }
}

// Handle static resource requests
async function handleStaticRequest(request) {
    try {
        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            // Cache new static resources
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
            return networkResponse;
        } else {
            throw new Error(`HTTP ${networkResponse.status}`);
        }
    } catch (error) {
        // Try to serve from cache
        const cachedResponse = await caches.match(request);

        if (cachedResponse) {
            return cachedResponse;
        }

        // Return fallback for images
        if (request.destination === 'image') {
            return new Response('', {
                status: 200,
                headers: { 'Content-Type': 'image/svg+xml' }
            });
        }

        return new Response('Resource not available offline', {
            status: 503,
            statusText: 'Service Unavailable'
        });
    }
}

// Generate offline fallback data for API endpoints
function getOfflineApiData(pathname) {
    switch (pathname) {
        case '/api/sensor-data/':
            return {
                grip_force: 0,
                emg_signal: 0,
                temperature: 22.5,
                battery_level: 85,
                flex_sensor: [0, 0, 0, 0, 0],
                device_state: {
                    is_running: false,
                    emergency_stop: false,
                    connection_status: 'offline'
                },
                timestamp: new Date().toISOString(),
                offline: true,
                message: 'Device data unavailable - using cached values'
            };

        case '/api/device-status/':
            return {
                status: 'offline',
                last_seen: new Date().toISOString(),
                offline: true,
                message: 'Device status unavailable offline'
            };

        case '/api/battery-status/':
            return {
                level: 85,
                charging: false,
                offline: true,
                message: 'Battery status unavailable offline'
            };

        case '/api/system-health/':
            return {
                overall_status: 'offline',
                offline: true,
                message: 'System health check unavailable offline'
            };

        default:
            return {
                error: 'API endpoint not available offline',
                offline: true
            };
    }
}

// Background sync for device control actions
self.addEventListener('sync', (event) => {
    console.log('Service Worker: Background sync triggered:', event.tag);

    switch (event.tag) {
        case SYNC_TAGS.DEVICE_CONTROL:
            event.waitUntil(syncDeviceControlActions());
            break;

        case SYNC_TAGS.NOTIFICATION_LOG:
            event.waitUntil(syncNotificationLogs());
            break;

        case SYNC_TAGS.ANALYTICS_DATA:
            event.waitUntil(syncAnalyticsData());
            break;
    }
});

// Sync device control actions when back online
async function syncDeviceControlActions() {
    try {
        // Get pending actions from IndexedDB
        const pendingActions = await getPendingActions('device-control');

        for (const action of pendingActions) {
            try {
                const response = await fetch('/api/device-control/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(action.data)
                });

                if (response.ok) {
                    await removePendingAction('device-control', action.id);
                    console.log('Service Worker: Synced device control action:', action.id);
                }
            } catch (error) {
                console.error('Service Worker: Failed to sync device control action:', error);
            }
        }
    } catch (error) {
        console.error('Service Worker: Background sync failed:', error);
    }
}

// Sync notification logs
async function syncNotificationLogs() {
    try {
        const pendingLogs = await getPendingActions('notification-logs');

        for (const log of pendingLogs) {
            try {
                const response = await fetch('/api/notifications/log/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(log.data)
                });

                if (response.ok) {
                    await removePendingAction('notification-logs', log.id);
                }
            } catch (error) {
                console.error('Service Worker: Failed to sync notification log:', error);
            }
        }
    } catch (error) {
        console.error('Service Worker: Notification sync failed:', error);
    }
}

// Sync analytics data
async function syncAnalyticsData() {
    try {
        const pendingData = await getPendingActions('analytics-data');

        for (const data of pendingData) {
            try {
                const response = await fetch('/api/analytics/sync/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data.data)
                });

                if (response.ok) {
                    await removePendingAction('analytics-data', data.id);
                }
            } catch (error) {
                console.error('Service Worker: Failed to sync analytics data:', error);
            }
        }
    } catch (error) {
        console.error('Service Worker: Analytics sync failed:', error);
    }
}

// Push notification handling
self.addEventListener('push', (event) => {
    console.log('Service Worker: Push notification received');

    let notificationData = {
        title: 'Bionic Hand Update',
        body: 'New information available',
        icon: '/static/dashboard/images/notification-icon.png',
        badge: '/static/dashboard/images/badge-icon.png',
        tag: 'bionic-hand-notification'
    };

    if (event.data) {
        try {
            notificationData = { ...notificationData, ...event.data.json() };
        } catch (error) {
            console.error('Service Worker: Failed to parse push data:', error);
        }
    }

    event.waitUntil(
        self.registration.showNotification(notificationData.title, {
            body: notificationData.body,
            icon: notificationData.icon,
            badge: notificationData.badge,
            tag: notificationData.tag,
            requireInteraction: notificationData.requireInteraction || false,
            actions: notificationData.actions || [],
            data: notificationData.data || {}
        })
    );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
    console.log('Service Worker: Notification clicked');

    event.notification.close();

    event.waitUntil(
        clients.matchAll({ type: 'window' }).then((clientList) => {
            // Check if dashboard is already open
            for (const client of clientList) {
                if (client.url.includes('/dashboard/') && 'focus' in client) {
                    return client.focus();
                }
            }

            // Open new dashboard window
            if (clients.openWindow) {
                return clients.openWindow('/dashboard/');
            }
        })
    );
});

// Message handling for communication with main thread
self.addEventListener('message', (event) => {
    console.log('Service Worker: Message received:', event.data);

    if (event.data && event.data.type) {
        switch (event.data.type) {
            case 'SKIP_WAITING':
                self.skipWaiting();
                break;

            case 'QUEUE_ACTION':
                queueAction(event.data.category, event.data.action);
                break;

            case 'GET_CACHE_STATUS':
                event.ports[0].postMessage({
                    cached: true,
                    version: CACHE_NAME
                });
                break;
        }
    }
});

// Queue actions for background sync
async function queueAction(category, actionData) {
    try {
        await storePendingAction(category, {
            id: Date.now().toString(),
            data: actionData,
            timestamp: new Date().toISOString()
        });

        // Register background sync
        await self.registration.sync.register(SYNC_TAGS[category.toUpperCase()] || 'generic-sync');

        console.log('Service Worker: Action queued for sync:', category);
    } catch (error) {
        console.error('Service Worker: Failed to queue action:', error);
    }
}

// IndexedDB helpers for storing pending actions
async function storePendingAction(store, data) {
    // Simple localStorage fallback for demo
    // In production, use IndexedDB for better performance
    const key = `pending-${store}`;
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    existing.push(data);
    localStorage.setItem(key, JSON.stringify(existing));
}

async function getPendingActions(store) {
    const key = `pending-${store}`;
    return JSON.parse(localStorage.getItem(key) || '[]');
}

async function removePendingAction(store, actionId) {
    const key = `pending-${store}`;
    const existing = JSON.parse(localStorage.getItem(key) || '[]');
    const filtered = existing.filter(action => action.id !== actionId);
    localStorage.setItem(key, JSON.stringify(filtered));
}

console.log('Service Worker: Script loaded');