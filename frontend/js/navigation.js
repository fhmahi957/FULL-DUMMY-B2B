// frontend/js/navigation.js
// Centralized role-based navigation and user profile management

window.BizLinkNav = {
    // Menu configuration by role
    menuConfig: {
        admin: {
            menu: [
                { icon: '📊', label: 'Dashboard', href: 'dashboard.html', roles: ['admin'] },
                { icon: '📦', label: 'Orders', href: 'orders.html', roles: ['admin', 'manager', 'operator'] },
                { icon: '💸', label: 'Refund', href: 'refunds.html', roles: ['admin', 'manager'] },
                { icon: '👥', label: 'Leads', href: 'leads.html', roles: ['admin', 'manager', 'operator'] },
            ],
            management: [
                { icon: '🔍', label: 'Manual Reviews', href: 'reviews.html', roles: ['admin', 'manager'] },
                { icon: '📧', label: 'Scheduled Emails', href: 'scheduled-emails.html', roles: ['admin', 'manager'] },
                { icon: '⚠️', label: 'Error Logs', href: 'errors.html', roles: ['admin', 'manager', 'operator'] },
            ],
            others: [
                { icon: '⚙️', label: 'Settings', href: 'settings.html', roles: ['admin', 'manager'] },
            ]
        },
        manager: {
            menu: [
                { icon: '📊', label: 'Dashboard', href: 'dashboard-manager.html', roles: ['admin', 'manager'] },
                { icon: '📦', label: 'Orders', href: 'orders.html', roles: ['admin', 'manager', 'operator'] },
                { icon: '💸', label: 'Refund', href: 'refunds.html', roles: ['admin', 'manager'] },
                { icon: '👥', label: 'Leads', href: 'leads.html', roles: ['admin', 'manager', 'operator'] },
            ],
            management: [
                { icon: '🔍', label: 'Manual Reviews', href: 'reviews.html', roles: ['admin', 'manager'] },
                { icon: '📧', label: 'Scheduled Emails', href: 'scheduled-emails.html', roles: ['admin', 'manager'] },
                { icon: '⚠️', label: 'Error Logs', href: 'errors.html', roles: ['admin', 'manager', 'operator'] },
            ],
            others: [
                { icon: '⚙️', label: 'Settings', href: 'settings.html', roles: ['admin', 'manager'] },
            ]
        },
        operator: {
            menu: [
                { icon: '📊', label: 'Dashboard', href: 'dashboard-operator.html', roles: ['operator'] },
                { icon: '📦', label: 'Orders', href: 'orders.html', roles: ['admin', 'manager', 'operator'] },
                { icon: '👥', label: 'Leads', href: 'leads.html', roles: ['admin', 'manager', 'operator'] },
            ],
            management: [
                { icon: '⚠️', label: 'Error Logs', href: 'errors.html', roles: ['admin', 'manager', 'operator'] },
            ],
            others: []
        }
    },

    // Initialize navigation and user profile - call this ONCE per page
    init() {
        const user = BizLinkAuth.getUser();
        const role = user.role || 'operator';

        this.renderSidebar(role);
        this.initUserProfile(user);
    },

    // Render role-appropriate sidebar navigation
    renderSidebar(role) {
        const config = this.menuConfig[role] || this.menuConfig.operator;
        const nav = document.querySelector('nav');
        if (!nav) return;

        let html = '<p class="px-4 text-xs font-semibold text-biz-muted uppercase mb-2">Menu</p>';

        // Render main menu items
        config.menu.forEach(item => {
            const isActive = window.location.pathname.includes(item.href) ||
                window.location.href.includes(item.href);
            html += `
                <a href="${item.href}" class="nav-link ${isActive ? 'active' : ''}">
                    ${item.icon} ${item.label}
                </a>
            `;
        });

        // Render management section if items exist
        if (config.management && config.management.length > 0) {
            html += '<p class="px-4 text-xs font-semibold text-biz-muted uppercase mt-6 mb-2">Management</p>';
            config.management.forEach(item => {
                const isActive = window.location.pathname.includes(item.href) ||
                    window.location.href.includes(item.href);
                html += `
                    <a href="${item.href}" class="nav-link ${isActive ? 'active' : ''}">
                        ${item.icon} ${item.label}
                    </a>
                `;
            });
        }

        // Render others section if items exist
        if (config.others && config.others.length > 0) {
            html += '<p class="px-4 text-xs font-semibold text-biz-muted uppercase mt-6 mb-2">Others</p>';
            config.others.forEach(item => {
                const isActive = window.location.pathname.includes(item.href) ||
                    window.location.href.includes(item.href);
                html += `
                    <a href="${item.href}" class="nav-link ${isActive ? 'active' : ''}" id="settings-link">
                        ${item.icon} ${item.label}
                    </a>
                `;
            });
        }

        nav.innerHTML = html;
    },

    // Initialize user profile display - consistent across all pages
    initUserProfile(user) {
        const role = user.role || 'operator';
        const roleName = role.charAt(0).toUpperCase() + role.slice(1);
        const initial = (user.name || user.email?.charAt(0) || 'U').toUpperCase();

        const updates = [
            { id: 'user-name', value: user.name || 'User' },
            { id: 'user-role', value: `${roleName} Workspace` },
            { id: 'user-avatar', value: initial },
            { id: 'header-avatar', value: initial }
        ];

        updates.forEach(({ id, value }) => {
            const el = document.getElementById(id);
            if (el && el.textContent !== value) {
                el.textContent = value;
            }
        });
    },

    // Helper: Get current user role
    getCurrentRole() {
        return BizLinkAuth.getRole();
    },

    // Helper: Check if current user has access to a feature
    hasAccess(requiredRoles) {
        const role = this.getCurrentRole();
        return requiredRoles.includes(role);
    }
};