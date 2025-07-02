# 餐飲店營收與叫菜管理系統

基於Django 5.2和Line LIFF的餐飲店管理系統，用於店長每日營收回報和食材訂購管理。此專案為提案展示用途，使用模擬資料，重點展現系統功能和使用者介面。

## 技術架構
- **後端框架**: Django 5.2
- **前端整合**: Line LIFF (Line Front-end Framework)
- **資料處理**: 使用Django內建的模擬資料，不連接實際資料庫
- **通知服務**: Line Messaging API模擬
- **報表輸出**: 使用Python的openpyxl生成Excel檔案

## 主要功能

### 店長端功能 (Line LIFF介面)
1. **每日營收回報**
   - 簡潔的營收輸入表單
   - 支援當日營收金額輸入
   - 一鍵提交至後台
   - 店內歷史營收紀錄查看

2. **每日叫菜功能**
   - 下午5點前完成食材訂購
   - 常用食材快速選擇介面
   - 數量調整器 (+ / - 按鈕)
   - 訂單預覽和提交確認

### 後台管理功能 (Web介面)
1. **營收管理**
   - 每日各店營收總覽儀表板
   - 營收趨勢圖表顯示
   - 按日期、分店篩選功能
   - 營收統計數據

2. **叫菜管理**
   - 查看各分店叫菜狀況
   - 食材需求彙總表
   - 叫菜完成狀態指示器
   - 歷史叫菜紀錄查詢

3. **報表功能**
   - Excel格式營收報表匯出
   - Excel格式食材訂購報表匯出
   - 自訂報表日期區間
   - 一鍵下載功能

4. **通知系統**
   - 下午4點自動檢查叫菜狀態
   - 未完成叫菜的店家推播提醒
   - Line通知模擬介面

## 安裝與設定

1. 建立虛擬環境並啟用
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. 安裝相依套件
   ```
   pip install -r requirements.txt
   ```

3. 執行資料庫遷移
   ```
   python manage.py migrate
   ```

4. 生成模擬資料
   ```
   python manage.py generate_mock_data
   ```

5. 啟動開發伺服器
   ```
   python manage.py runserver
   ```

## 專案結構
```
restaurant_management/
├── manage.py
├── requirements.txt
├── restaurant_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── liff_interface/      # Line LIFF相關功能
│   ├── admin_dashboard/     # 後台管理介面
│   ├── mock_data/          # 模擬資料管理
│   └── notifications/      # 通知系統
└── static/
    ├── css/
    ├── js/
    └── images/
```

## 使用方法

### 店長端 (LIFF介面)
- 訪問 `/liff/` 進入店長介面
- 可使用營收回報、叫菜功能
- 查看歷史紀錄

### 管理端 (後台介面)
- 訪問 `/dashboard/` 進入後台管理介面
- 查看營收統計與圖表
- 管理叫菜狀態
- 下載報表

## 展示用途說明
本專案為提案展示用途，使用模擬資料，主要展現系統功能和使用者介面設計。實際部署時需進行以下調整：

1. 設定真實的Line LIFF ID和Channel Access Token
2. 連接實際的資料庫系統
3. 設定適當的身份驗證和授權機制
4. 實作完整的Line通知功能
5. 加強資料安全性和錯誤處理 