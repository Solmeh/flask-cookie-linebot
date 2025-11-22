// Google Apps Script for Cookie Clicker Game Backend

// 設定 Google Sheets ID (部署前請先建立一個 Google Sheet 並填入 ID)
// Sheet 1 Name: "Users" (Headers: UserID, UserName, Cookies, LastCollectTime, AutoRate, CooldownLevel, CollectLevel)
// Sheet 2 Name: "Logs" (Headers: Timestamp, UserID, Action, Details)

var SPREADSHEET_ID = "1U46ReQmHb02a5Ph87GJ8yCagxmIkNk_VqDF_9oeMB9E"; // *** 請填入您的 Google Sheet ID ***

function doPost(e) {
    var lock = LockService.getScriptLock();
    lock.tryLock(10000);

    try {
        var params = JSON.parse(e.postData.contents);
        var action = params.action;
        var userId = params.userId;
        var userName = params.userName || "Unknown";

        var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
        var userSheet = ss.getSheetByName("Users");

        // 確保 Sheet 存在
        if (!userSheet) {
            userSheet = ss.insertSheet("Users");
            userSheet.appendRow(["UserID", "UserName", "Cookies", "LastCollectTime", "AutoRate", "CooldownLevel", "CollectLevel"]);
        }

        var userRow = findUserRow(userSheet, userId);
        var userData = null;

        if (userRow == -1) {
            // 新用戶註冊
            var now = new Date().getTime();
            // Initial: Cookies=0, LastCollectTime=0, AutoRate=0, CooldownLevel=0, CollectLevel=0
            userSheet.appendRow([userId, userName, 0, 0, 0, 0, 0]);
            userRow = userSheet.getLastRow();
            userData = { cookies: 0, lastCollect: 0, autoRate: 0, cooldownLevel: 0, collectLevel: 0 };
        } else {
            var values = userSheet.getRange(userRow, 3, 1, 5).getValues()[0];
            userData = {
                cookies: parseInt(values[0]),
                lastCollect: parseInt(values[1]),
                autoRate: parseInt(values[2]),
                cooldownLevel: parseInt(values[3]),
                collectLevel: parseInt(values[4])
            };
        }

        var result = {};

        if (action === "collect") {
            result = handleCollect(userSheet, userRow, userData);
        } else if (action === "upgrade") {
            var type = params.type; // 'auto', 'cooldown', 'lucky'
            result = handleUpgrade(userSheet, userRow, userData, type);
        } else if (action === "get_profile") {
            result = { status: "success", data: userData };
        } else {
            result = { status: "error", message: "Unknown action" };
        }

        return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(ContentService.MimeType.JSON);

    } catch (error) {
        return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() })).setMimeType(ContentService.MimeType.JSON);
    } finally {
        lock.releaseLock();
    }
}

function doGet(e) {
    var action = e.parameter.action;

    if (action === "leaderboard") {
        var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
        var userSheet = ss.getSheetByName("Users");
        var data = userSheet.getDataRange().getValues();
        var users = [];

        // Skip header
        for (var i = 1; i < data.length; i++) {
            users.push({
                name: data[i][1],
                cookies: parseInt(data[i][2])
            });
        }

        // Sort by cookies desc
        users.sort(function (a, b) { return b.cookies - a.cookies; });

        // Top 5
        var top5 = users.slice(0, 5);

        return ContentService.createTextOutput(JSON.stringify({ status: "success", data: top5 })).setMimeType(ContentService.MimeType.JSON);
    }

    return ContentService.createTextOutput("Cookie Game Backend Running").setMimeType(ContentService.MimeType.TEXT);
}

function findUserRow(sheet, userId) {
    var data = sheet.getDataRange().getValues();
    for (var i = 1; i < data.length; i++) {
        if (data[i][0] == userId) {
            return i + 1;
        }
    }
    return -1;
}

function handleCollect(sheet, row, data) {
    var now = new Date().getTime();
    var baseCooldown = 10 * 60 * 1000; // 10 mins
    // Cooldown reduction: 1 min per level, max 9 levels (1 min remaining)
    var cooldownReduction = Math.min(data.cooldownLevel, 9) * 60 * 1000;
    var cooldown = Math.max(1 * 60 * 1000, baseCooldown - cooldownReduction);

    if (now - data.lastCollect < cooldown) {
        var remaining = Math.ceil((cooldown - (now - data.lastCollect)) / 1000);
        return { status: "failed", message: "⏳ 冷卻中，請稍等 " + remaining + " 秒" };
    }

    // 1. Manual Collect: 1 + lucky level
    var manualAmount = 1 + data.collectLevel;

    // 2. Auto Production (Offline): 10 per level per hour
    var timeDiff = now - data.lastCollect; // ms since last collect
    var hoursPassed = timeDiff / (1000 * 60 * 60);
    var autoAmount = Math.floor(hoursPassed * (data.autoRate * 10));

    var totalAmount = manualAmount + autoAmount;
    var newCookies = data.cookies + totalAmount;

    sheet.getRange(row, 3).setValue(newCookies);
    sheet.getRange(row, 4).setValue(now);

    var msg = "🍪 領取成功！獲得 " + manualAmount + " 餅乾";
    if (autoAmount > 0) {
        msg += "\n🏭 自動化烤箱幫您烤了 " + autoAmount + " 餅乾！";
    }

    return { status: "success", message: msg, current_cookies: newCookies };
}

function handleUpgrade(sheet, row, data, type) {
    var cost = 0;
    var newLevel = 0;
    var msg = "";

    if (type === "auto") {
        // Cost: 10 * (level + 1)
        cost = 10 * (data.autoRate + 1);
        if (data.cookies < cost) return { status: "failed", message: "❌ 餅乾不足，需要 " + cost + " 餅乾" };

        newLevel = data.autoRate + 1;
        sheet.getRange(row, 3).setValue(data.cookies - cost);
        sheet.getRange(row, 5).setValue(newLevel);
        msg = "🏭 升級成功！自動化烤箱 Lv." + newLevel + "\n(每小時產量 +10)";

    } else if (type === "cooldown") {
        // Cost: 50 * (level + 1)
        cost = 50 * (data.cooldownLevel + 1);
        if (data.cookies < cost) return { status: "failed", message: "❌ 餅乾不足，需要 " + cost + " 餅乾" };

        if (data.cooldownLevel >= 9) return { status: "failed", message: "⚠️ 已達最高等級！" };

        newLevel = data.cooldownLevel + 1;
        sheet.getRange(row, 3).setValue(data.cookies - cost);
        sheet.getRange(row, 6).setValue(newLevel);
        msg = "⏳ 升級成功！時光機器 Lv." + newLevel + "\n(冷卻時間 -1 分鐘)";

    } else if (type === "lucky") {
        // Cost: 100 * (level + 1)
        cost = 100 * (data.collectLevel + 1);
        if (data.cookies < cost) return { status: "failed", message: "❌ 餅乾不足，需要 " + cost + " 餅乾" };

        newLevel = data.collectLevel + 1;
        sheet.getRange(row, 3).setValue(data.cookies - cost);
        sheet.getRange(row, 7).setValue(newLevel);
        msg = "🍀 升級成功！幸運餅乾 Lv." + newLevel + "\n(每次領取 +1)";

    } else {
        return { status: "error", message: "Unknown upgrade type" };
    }

    return { status: "success", message: msg, current_cookies: data.cookies - cost };
}
