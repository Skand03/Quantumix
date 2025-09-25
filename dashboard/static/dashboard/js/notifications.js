/**
 * Advanced Notification System for Bionic Hand Dashboard
 * Provides toast notifications, real-time alerts, and system status updates
 */

class NotificationManager {
    constructor() {
        this.notifications = new Map();
        this.notificationId = 0;
        this.container = null;
        this.sound = null;
        this.settings = {
            enableSound: true,
            position: 'top-right',
            autoClose: true,
            defaultDuration: 5000,
            maxNotifications: 5,
            enableVibration: true,
            priority: {
                low: 1,
                normal: 2,
                high: 3,
                critical: 4
            }
        };

        this.init();
        this.loadSettings();
        this.setupEventListeners();
    }

    init() {
        // Create notification container
        this.createContainer();

        // Create notification sounds
        this.createSounds();

        // Initialize WebSocket for real-time notifications
        this.initWebSocket();

        // Setup system monitoring
        this.setupSystemMonitoring();

        // Add CSS styles
        this.addStyles();
    }

    createContainer() {
        // Remove existing container if any
        const existing = document.getElementById('notification-container');
        if (existing) existing.remove();

        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.className = `notification-container ${this.settings.position}`;
        document.body.appendChild(this.container);
    }

    addStyles() {
        if (document.getElementById('notification-styles')) return;

        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification-container {
                position: fixed;
                z-index: 10000;
                pointer-events: none;
                max-width: 400px;
            }

            .notification-container.top-right {
                top: 20px;
                right: 20px;
            }

            .notification-container.top-left {
                top: 20px;
                left: 20px;
            }

            .notification-container.bottom-right {
                bottom: 20px;
                right: 20px;
            }

            .notification-container.bottom-left {
                bottom: 20px;
                left: 20px;
            }

            .notification-container.top-center {
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
            }

            .notification {
                pointer-events: auto;
                margin-bottom: 15px;
                min-width: 300px;
                max-width: 450px;
                padding: 16px 20px;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
                transform: translateX(400px);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                opacity: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            .notification.show {
                transform: translateX(0);
                opacity: 1;
            }

            .notification.success {
                background: linear-gradient(135deg, rgba(72, 187, 120, 0.95) 0%, rgba(56, 161, 105, 0.95) 100%);
                color: white;
                border-left: 4px solid #48bb78;
            }

            .notification.error {
                background: linear-gradient(135deg, rgba(229, 62, 62, 0.95) 0%, rgba(197, 48, 48, 0.95) 100%);
                color: white;
                border-left: 4px solid #e53e3e;
            }

            .notification.warning {
                background: linear-gradient(135deg, rgba(237, 137, 54, 0.95) 0%, rgba(221, 107, 32, 0.95) 100%);
                color: white;
                border-left: 4px solid #ed8936;
            }

            .notification.info {
                background: linear-gradient(135deg, rgba(74, 144, 226, 0.95) 0%, rgba(53, 122, 189, 0.95) 100%);
                color: white;
                border-left: 4px solid #4a90e2;
            }

            .notification.system {
                background: linear-gradient(135deg, rgba(128, 90, 213, 0.95) 0%, rgba(102, 68, 187, 0.95) 100%);
                color: white;
                border-left: 4px solid #805ad5;
            }

            .notification-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 8px;
            }

            .notification-icon {
                font-size: 1.2em;
                margin-right: 10px;
                display: flex;
                align-items: center;
            }

            .notification-title {
                font-weight: 600;
                font-size: 1em;
                flex-grow: 1;
                display: flex;
                align-items: center;
            }

            .notification-close {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                font-size: 1.2em;
                opacity: 0.7;
                transition: opacity 0.3s ease;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
            }

            .notification-close:hover {
                opacity: 1;
                background: rgba(255, 255, 255, 0.2);
            }

            .notification-message {
                font-size: 0.9em;
                line-height: 1.4;
                opacity: 0.95;
                margin-bottom: 8px;
            }

            .notification-timestamp {
                font-size: 0.8em;
                opacity: 0.8;
                text-align: right;
            }

            .notification-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: rgba(255, 255, 255, 0.3);
                transition: width linear;
            }

            .notification-actions {
                margin-top: 12px;
                display: flex;
                gap: 10px;
            }

            .notification-action {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.85em;
                transition: all 0.3s ease;
            }

            .notification-action:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-1px);
            }

            .notification-action.primary {
                background: rgba(255, 255, 255, 0.9);
                color: #1a1a1a;
            }

            .notification-action.primary:hover {
                background: white;
            }

            /* Priority indicators */
            .notification.priority-critical {
                animation: shake 0.5s ease-in-out 3;
                box-shadow: 0 0 30px rgba(229, 62, 62, 0.6);
            }

            .notification.priority-high {
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            }

            /* Animations */
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }

            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
            }

            .notification.pulsing {
                animation: pulse 2s ease-in-out infinite;
            }

            /* Mobile responsive */
            @media (max-width: 768px) {
                .notification-container {
                    left: 10px !important;
                    right: 10px !important;
                    max-width: none;
                    transform: none !important;
                }

                .notification {
                    min-width: auto;
                    margin-bottom: 10px;
                    transform: translateY(-100px);
                }

                .notification-container.top-right,
                .notification-container.top-left,
                .notification-container.top-center {
                    top: 10px;
                }

                .notification-container.bottom-right,
                .notification-container.bottom-left {
                    bottom: 10px;
                }
            }

            /* Dark theme adjustments */
            .dark-theme .notification {
                border: 1px solid rgba(192, 192, 192, 0.1);
                backdrop-filter: blur(25px);
            }

            /* System status bar */
            .system-status-bar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: rgba(26, 26, 26, 0.95);
                backdrop-filter: blur(10px);
                border-bottom: 1px solid rgba(192, 192, 192, 0.1);
                padding: 8px 20px;
                z-index: 9999;
                transform: translateY(-100%);
                transition: transform 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: space-between;
                color: white;
                font-size: 0.9em;
            }

            .system-status-bar.show {
                transform: translateY(0);
            }

            .status-item {
                display: flex;
                align-items: center;
                gap: 6px;
            }

            .status-indicator {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #48bb78;
            }

            .status-indicator.warning {
                background: #ed8936;
            }

            .status-indicator.error {
                background: #e53e3e;
            }
        `;
        document.head.appendChild(style);
    }

    createSounds() {
        // Create notification sounds
        this.sounds = {
            success: this.createAudioContext('success'),
            error: this.createAudioContext('error'),
            warning: this.createAudioContext('warning'),
            info: this.createAudioContext('info'),
            system: this.createAudioContext('system')
        };
    }

    createAudioContext(type) {
        // Create simple notification sounds using Web Audio API
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            return {
                play: () => {
                    if (!this.settings.enableSound) return;

                    const oscillator = audioContext.createOscillator();
                    const gainNode = audioContext.createGain();

                    oscillator.connect(gainNode);
                    gainNode.connect(audioContext.destination);

                    // Different frequencies for different notification types
                    const frequencies = {
                        success: [523.25, 659.25], // C5, E5
                        error: [415.30, 311.13], // G#4, D#4
                        warning: [440, 554.37], // A4, C#5
                        info: [261.63, 329.63], // C4, E4
                        system: [196, 246.94] // G3, B3
                    };

                    const freq = frequencies[type] || frequencies.info;

                    oscillator.frequency.setValueAtTime(freq[0], audioContext.currentTime);
                    oscillator.frequency.setValueAtTime(freq[1], audioContext.currentTime + 0.1);

                    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.3);
                }
            };
        } catch (e) {
            return { play: () => { } }; // Fallback for browsers without Web Audio API
        }
    }

    initWebSocket() {
        // Initialize WebSocket connection for real-time notifications
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;

            this.websocket = new WebSocket(wsUrl);

            this.websocket.onopen = () => {
                console.log('Notification WebSocket connected');
                this.showSystemNotification('Connected to notification service', 'info');
            };

            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };

            this.websocket.onclose = () => {
                console.log('Notification WebSocket disconnected');
                // Attempt to reconnect after 5 seconds
                setTimeout(() => this.initWebSocket(), 5000);
            };

            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

        } catch (error) {
            console.warn('WebSocket not available, using polling fallback');
            this.setupPolling();
        }
    }

    handleWebSocketMessage(data) {
        const { type, title, message, priority, actions } = data;

        this.show(title, message, {
            type: type || 'info',
            priority: priority || 'normal',
            actions: actions || []
        });
    }

    setupPolling() {
        // Fallback: Poll for notifications every 30 seconds
        setInterval(() => {
            this.checkForNotifications();
        }, 30000);
    }

    async checkForNotifications() {
        try {
            const response = await fetch('/api/notifications/check/', {
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (response.ok) {
                const notifications = await response.json();
                notifications.forEach(notification => {
                    this.show(notification.title, notification.message, {
                        type: notification.type,
                        priority: notification.priority
                    });
                });
            }
        } catch (error) {
            console.error('Failed to check notifications:', error);
        }
    }

    setupSystemMonitoring() {
        // Monitor system events and show notifications

        // Monitor device connection
        this.monitorDeviceConnection();

        // Monitor battery levels
        this.monitorBatteryLevel();

        // Monitor page visibility
        this.monitorPageVisibility();

        // Monitor online/offline status
        this.monitorOnlineStatus();
    }

    monitorDeviceConnection() {
        let lastStatus = 'connected';

        setInterval(async () => {
            try {
                const response = await fetch('/api/device-status/');
                const data = await response.json();

                if (data.status !== lastStatus) {
                    if (data.status === 'disconnected') {
                        this.show('Device Disconnected', 'Bionic hand has been disconnected', {
                            type: 'warning',
                            priority: 'high',
                            persistent: true,
                            actions: [
                                { label: 'Reconnect', action: 'reconnectDevice' },
                                { label: 'Dismiss', action: 'dismiss' }
                            ]
                        });
                    } else if (data.status === 'connected' && lastStatus === 'disconnected') {
                        this.show('Device Reconnected', 'Bionic hand is now connected', {
                            type: 'success'
                        });
                    }
                    lastStatus = data.status;
                }
            } catch (error) {
                console.error('Failed to check device status:', error);
            }
        }, 5000);
    }

    monitorBatteryLevel() {
        let lastBatteryLevel = 100;
        let lowBatteryWarningShown = false;

        setInterval(async () => {
            try {
                const response = await fetch('/api/battery-status/');
                const data = await response.json();

                if (data.level <= 20 && !lowBatteryWarningShown) {
                    this.show('Low Battery Warning', `Battery level is ${data.level}%. Please charge your device.`, {
                        type: 'warning',
                        priority: 'high',
                        persistent: true
                    });
                    lowBatteryWarningShown = true;
                } else if (data.level > 20) {
                    lowBatteryWarningShown = false;
                }

                if (data.level <= 5 && data.level > 0) {
                    this.show('Critical Battery Level', 'Device will shut down soon. Charge immediately!', {
                        type: 'error',
                        priority: 'critical',
                        persistent: true
                    });
                }

                lastBatteryLevel = data.level;
            } catch (error) {
                console.error('Failed to check battery status:', error);
            }
        }, 10000);
    }

    monitorPageVisibility() {
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                // Page became visible, check for missed notifications
                this.checkForNotifications();
            }
        });
    }

    monitorOnlineStatus() {
        window.addEventListener('online', () => {
            this.show('Connection Restored', 'Internet connection has been restored', {
                type: 'success'
            });
        });

        window.addEventListener('offline', () => {
            this.show('Connection Lost', 'Internet connection has been lost. Some features may not work.', {
                type: 'warning',
                persistent: true
            });
        });
    }

    show(title, message, options = {}) {
        const config = {
            type: options.type || 'info',
            priority: options.priority || 'normal',
            duration: options.duration || this.settings.defaultDuration,
            persistent: options.persistent || false,
            actions: options.actions || [],
            sound: options.sound !== false,
            vibration: options.vibration !== false,
            ...options
        };

        // Create notification ID
        const id = ++this.notificationId;

        // Create notification element
        const notification = this.createNotificationElement(id, title, message, config);

        // Store notification
        this.notifications.set(id, {
            element: notification,
            config: config,
            timestamp: new Date()
        });

        // Add to container
        this.container.appendChild(notification);

        // Show notification
        setTimeout(() => notification.classList.add('show'), 50);

        // Play sound
        if (config.sound && this.settings.enableSound) {
            this.sounds[config.type]?.play();
        }

        // Vibrate (if supported and enabled)
        if (config.vibration && this.settings.enableVibration && navigator.vibrate) {
            const vibrationPattern = {
                'success': [100],
                'error': [100, 50, 100],
                'warning': [200, 100, 200],
                'info': [100],
                'critical': [200, 100, 200, 100, 200]
            };
            navigator.vibrate(vibrationPattern[config.priority] || vibrationPattern[config.type] || [100]);
        }

        // Auto-dismiss if not persistent
        if (!config.persistent && config.duration > 0) {
            this.startProgressBar(notification, config.duration);
            setTimeout(() => this.dismiss(id), config.duration);
        }

        // Manage notification count
        this.manageNotificationCount();

        // Log notification
        this.logNotification(id, title, message, config);

        return id;
    }

    createNotificationElement(id, title, message, config) {
        const notification = document.createElement('div');
        notification.className = `notification ${config.type} priority-${config.priority}`;
        notification.dataset.id = id;

        const iconMap = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-triangle',
            warning: 'fas fa-exclamation-circle',
            info: 'fas fa-info-circle',
            system: 'fas fa-cog'
        };

        const actionsHtml = config.actions.length > 0 ? `
            <div class="notification-actions">
                ${config.actions.map((action, index) => `
                    <button class="notification-action ${action.primary ? 'primary' : ''}" 
                            onclick="notificationManager.handleAction(${id}, '${action.action}', ${index})">
                        ${action.label}
                    </button>
                `).join('')}
            </div>
        ` : '';

        notification.innerHTML = `
            <div class="notification-header">
                <div class="notification-title">
                    <i class="${iconMap[config.type] || iconMap.info} notification-icon"></i>
                    ${title}
                </div>
                <button class="notification-close" onclick="notificationManager.dismiss(${id})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="notification-message">${message}</div>
            ${actionsHtml}
            <div class="notification-timestamp">${new Date().toLocaleTimeString()}</div>
            ${!config.persistent ? '<div class="notification-progress"></div>' : ''}
        `;

        // Add priority-specific styling
        if (config.priority === 'critical') {
            notification.classList.add('priority-critical');
        }

        return notification;
    }

    startProgressBar(notification, duration) {
        const progressBar = notification.querySelector('.notification-progress');
        if (progressBar) {
            progressBar.style.width = '100%';
            progressBar.style.transition = `width ${duration}ms linear`;
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 50);
        }
    }

    dismiss(id) {
        const notification = this.notifications.get(id);
        if (notification) {
            notification.element.classList.remove('show');
            setTimeout(() => {
                if (notification.element.parentNode) {
                    notification.element.parentNode.removeChild(notification.element);
                }
                this.notifications.delete(id);
            }, 400);
        }
    }

    dismissAll() {
        this.notifications.forEach((notification, id) => {
            this.dismiss(id);
        });
    }

    handleAction(notificationId, actionType, actionIndex) {
        const notification = this.notifications.get(notificationId);
        if (!notification) return;

        switch (actionType) {
            case 'dismiss':
                this.dismiss(notificationId);
                break;

            case 'reconnectDevice':
                this.reconnectDevice();
                this.dismiss(notificationId);
                break;

            case 'viewDetails':
                // Open details modal or navigate to specific page
                console.log('View details action');
                break;

            default:
                // Custom action handler
                this.handleCustomAction(actionType, notification);
        }
    }

    async reconnectDevice() {
        try {
            const response = await fetch('/api/device/reconnect/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (response.ok) {
                this.show('Reconnecting...', 'Attempting to reconnect to bionic hand', {
                    type: 'info'
                });
            }
        } catch (error) {
            this.show('Reconnection Failed', 'Unable to reconnect to device', {
                type: 'error'
            });
        }
    }

    handleCustomAction(actionType, notification) {
        // Emit custom event for external handling
        const event = new CustomEvent('notificationAction', {
            detail: {
                actionType,
                notification
            }
        });
        document.dispatchEvent(event);
    }

    manageNotificationCount() {
        // Remove oldest notifications if exceeding max count
        if (this.notifications.size > this.settings.maxNotifications) {
            const oldestId = Math.min(...this.notifications.keys());
            this.dismiss(oldestId);
        }
    }

    logNotification(id, title, message, config) {
        // Log notification to console and potentially send to server
        console.log(`[Notification ${id}] ${config.type.toUpperCase()}: ${title} - ${message}`);

        // Optionally send to server for analytics
        this.sendNotificationLog(id, title, message, config);
    }

    async sendNotificationLog(id, title, message, config) {
        try {
            await fetch('/api/notifications/log/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    id,
                    title,
                    message,
                    type: config.type,
                    priority: config.priority,
                    timestamp: new Date().toISOString()
                })
            });
        } catch (error) {
            console.error('Failed to log notification:', error);
        }
    }

    // Convenience methods
    success(title, message, options = {}) {
        return this.show(title, message, { ...options, type: 'success' });
    }

    error(title, message, options = {}) {
        return this.show(title, message, { ...options, type: 'error' });
    }

    warning(title, message, options = {}) {
        return this.show(title, message, { ...options, type: 'warning' });
    }

    info(title, message, options = {}) {
        return this.show(title, message, { ...options, type: 'info' });
    }

    system(title, message, options = {}) {
        return this.show(title, message, { ...options, type: 'system' });
    }

    showSystemNotification(message, type = 'info') {
        // Show system-wide notification bar
        let statusBar = document.querySelector('.system-status-bar');
        if (!statusBar) {
            statusBar = document.createElement('div');
            statusBar.className = 'system-status-bar';
            document.body.appendChild(statusBar);
        }

        statusBar.innerHTML = `
            <div class="status-item">
                <div class="status-indicator ${type}"></div>
                <span>${message}</span>
            </div>
            <button onclick="this.parentElement.classList.remove('show')" style="background: none; border: none; color: white; cursor: pointer;">
                <i class="fas fa-times"></i>
            </button>
        `;

        statusBar.classList.add('show');

        // Auto-hide after 10 seconds
        setTimeout(() => {
            statusBar.classList.remove('show');
        }, 10000);
    }

    setupEventListeners() {
        // Listen for custom notification events
        document.addEventListener('notify', (event) => {
            const { title, message, options } = event.detail;
            this.show(title, message, options);
        });

        // Listen for settings changes
        document.addEventListener('notificationSettingsChange', (event) => {
            this.updateSettings(event.detail);
        });
    }

    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        this.saveSettings();

        // Update container position if changed
        if (newSettings.position) {
            this.container.className = `notification-container ${newSettings.position}`;
        }
    }

    loadSettings() {
        const saved = localStorage.getItem('notificationSettings');
        if (saved) {
            this.settings = { ...this.settings, ...JSON.parse(saved) };
        }
    }

    saveSettings() {
        localStorage.setItem('notificationSettings', JSON.stringify(this.settings));
    }

    getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
}

// Initialize notification manager
let notificationManager;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    notificationManager = new NotificationManager();

    // Make it globally available
    window.notificationManager = notificationManager;
});

// Global notification functions for easy use
window.showNotification = (title, message, options) => {
    return notificationManager?.show(title, message, options);
};

window.showSuccess = (title, message, options) => {
    return notificationManager?.success(title, message, options);
};

window.showError = (title, message, options) => {
    return notificationManager?.error(title, message, options);
};

window.showWarning = (title, message, options) => {
    return notificationManager?.warning(title, message, options);
};

window.showInfo = (title, message, options) => {
    return notificationManager?.info(title, message, options);
};