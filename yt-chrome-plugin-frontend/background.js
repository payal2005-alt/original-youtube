// Background Service Worker for YouTube Sentiment Analysis Extension

console.log('🔧 Background script loaded at', new Date().toLocaleTimeString());

// Store dashboard data in memory (no storage delays)
let dashboardDataCache = null;

// Listen for messages from popup or dashboard
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('📨 Background received message:', request.action);
  console.log('⏰ Time:', new Date().toLocaleTimeString());
  console.log('📤 From sender:', sender.url);
  
  if (request.action === 'storeDashboardData') {
    console.log('💾 Storing dashboard data to memory cache...');
    console.log('📊 Data keys:', Object.keys(request.data || {}));
    dashboardDataCache = request.data;
    console.log('✅ Dashboard data cached successfully');
    console.log('🔍 Cache now contains:', Object.keys(dashboardDataCache || {}));
    sendResponse({ success: true, message: 'Data cached successfully' });
  }
  
  if (request.action === 'getDashboardData') {
    console.log('🔍 Getting dashboard data from cache...');
    console.log('📦 Cache status:', dashboardDataCache ? 'HAS DATA' : 'EMPTY');
    if (dashboardDataCache) {
      console.log('✅ Sending cached data to dashboard');
      console.log('🔍 Data keys:', Object.keys(dashboardDataCache));
      sendResponse({ success: true, data: dashboardDataCache });
    } else {
      console.warn('⚠️ No data in cache yet');
      sendResponse({ success: false, message: 'No data in cache' });
    }
  }

  if (request.action === 'closeDashboard') {
    console.log('🪟 Close dashboard request received');

    const closeTabById = (tabId) => {
      chrome.tabs.remove(tabId, () => {
        if (chrome.runtime.lastError) {
          console.warn('⚠️ Failed to close dashboard tab:', chrome.runtime.lastError.message);
          sendResponse({ success: false, message: chrome.runtime.lastError.message });
          return;
        }

        console.log('✅ Dashboard tab closed');
        sendResponse({ success: true });
      });
    };

    const activateReturnTabThenClose = (dashboardTabId) => {
      const returnTabId = request.returnTabId ? Number(request.returnTabId) : null;
      const canReturnToTab = Number.isInteger(returnTabId) && returnTabId > 0;

      if (canReturnToTab) {
        chrome.tabs.update(returnTabId, { active: true }, () => {
          if (chrome.runtime.lastError) {
            console.warn('⚠️ Failed to reactivate original tab:', chrome.runtime.lastError.message);
            closeTabById(dashboardTabId);
            return;
          }

          console.log('✅ Returned focus to original YouTube tab');
          closeTabById(dashboardTabId);
        });
        return;
      }

      closeTabById(dashboardTabId);
    };

    if (sender.tab && sender.tab.id !== undefined) {
      activateReturnTabThenClose(sender.tab.id);
      return true;
    }

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentTab = tabs && tabs[0];

      if (!currentTab || currentTab.id === undefined) {
        console.warn('⚠️ No active tab found to close');
        sendResponse({ success: false, message: 'No active tab found' });
        return;
      }

      activateReturnTabThenClose(currentTab.id);
    });

    return true;
  }
});

console.log('✅ Background message listener registered');


