// Example: How to update accounts_list.html with i18n

// 1. Add i18n.js to the page head:
// <script src="/static/js/i18n.js"></script>

// 2. Add language switcher to navigation or header:
/*
<div class="lang-switcher">
    <button onclick="setLanguage('zh-hans')" class="lang-btn" id="lang-zh">中文</button>
    <button onclick="setLanguage('en')" class="lang-btn" id="lang-en">EN</button>
</div>
*/

// 3. Update loadAccounts function to use translations:

async function loadAccounts() {
    try {
        const mode = currentMode;
        const response = await API.get(`/accounts/?mode=${mode}`);
        accounts = response.results || response;
        
        if (accounts.length === 0) {
            document.getElementById('accountsList').innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📊</div>
                    <div>${t('no_data')}</div>
                </div>
            `;
            return;
        }
        
        document.getElementById('accountsList').innerHTML = accounts.map(account => `
            <div class="account-card">
                <div class="account-header">
                    <span class="account-name">${account.name || account.market_type_display}</span>
                    <span class="account-badge badge-${account.mode}">${account.mode === 'SIM' ? t('simulation') : t('real')}</span>
                </div>
                <div class="account-info">
                    <div class="account-info-item">
                        <span class="account-info-label">${t('market_type')}</span>
                        <span class="account-info-value">${translateMarketType(account.market_type)}</span>
                    </div>
                    <div class="account-info-item">
                        <span class="account-info-label">${t('currency')}</span>
                        <span class="account-info-value">${account.currency_display || account.currency}</span>
                    </div>
                    <div class="account-info-item">
                        <span class="account-info-label">${t('start_cash')}</span>
                        <span class="account-info-value">${formatNumber(account.start_cash)} ${account.currency}</span>
                    </div>
                    <div class="account-info-item">
                        <span class="account-info-label">${t('current_balance')}</span>
                        <span class="account-info-value">${formatNumber(account.current_cash)} ${account.currency}</span>
                    </div>
                </div>
                <div style="margin-top: 12px;">
                    <button class="btn btn-primary btn-sm" onclick="enterAccount(${account.id})">${t('enter_account')}</button>
                    <span style="margin-left: 10px; font-size: 12px; color: #666;">
                        ${t('trade_count')}: ${account.trade_count} ${t('trades_count')}
                    </span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load accounts:', error);
        showError(t('error'));
    }
}

// 4. Add helper function to translate market types:
function translateMarketType(type) {
    const translations = {
        'zh-hans': {
            'US': '美股',
            'HK': '港股',
            'CN': 'A股',
            'CRYPTO': '加密货币'
        },
        'en': {
            'US': 'US Stocks',
            'HK': 'HK Stocks',
            'CN': 'CN Stocks',
            'CRYPTO': 'Cryptocurrency'
        }
    };
    return translations[getCurrentLanguage()][type] || type;
}

// 5. Initialize language on page load:
document.addEventListener('DOMContentLoaded', function() {
    // Set active language button
    const lang = getCurrentLanguage();
    document.getElementById('lang-' + (lang === 'zh-hans' ? 'zh' : 'en')).classList.add('active');
    
    // Load data with translations
    loadAccounts();
});

// 6. Add CSS for language switcher:
/*
.lang-switcher {
    display: flex;
    gap: 5px;
}

.lang-btn {
    padding: 6px 12px;
    border: 1px solid #ddd;
    background: white;
    color: #666;
    cursor: pointer;
    border-radius: 4px;
    font-size: 13px;
    transition: all 0.3s;
}

.lang-btn:hover {
    background: #f5f5f5;
}

.lang-btn.active {
    background: #667eea;
    color: white;
    border-color: #667eea;
}
*/
