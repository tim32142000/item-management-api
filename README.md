# Experiment API

一個使用 FastAPI 建立的實驗資料管理 API，提供實驗紀錄（名稱、頻率、阻尼、振幅）的新增、查詢、更新、刪除功能，並以 SQLite 作為資料儲存。

## 專案結構

```
.
├── main.py              # FastAPI 進入點，定義路由
├── models.py             # Pydantic 資料模型（請求／回應）
├── database_models.py    # 資料庫用的 Experiment dataclass
├── database.py            # SQLite 連線與 CRUD 操作
├── service.py             # 商業邏輯層（驗證規則、交易控制）
├── requirements.txt      # 相依套件
└── tests/
    └── test_api.py        # pytest 測試
```

## 使用套件

- **FastAPI**：Web API 框架
- **SQLite**：資料儲存
- **Pydantic**：資料驗證
- **pytest / httpx**：測試

## 安裝

```bash
pip install -r requirements.txt
```

## 啟動伺服器

```bash
uvicorn main:app --reload
```

啟動後可至 `http://127.0.0.1:8000/docs` 查看自動產生的 Swagger API 文件。

## API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/` | 確認服務是否正常運作 |
| POST | `/experiments` | 建立新的實驗紀錄 |
| GET | `/experiments` | 取得所有實驗紀錄 |
| GET | `/experiments/{id}` | 取得單一實驗紀錄 |
| PUT | `/experiments/{id}` | 更新指定的實驗紀錄 |
| DELETE | `/experiments/{id}` | 刪除指定的實驗紀錄 |

### 資料欄位

| 欄位 | 型別 | 限制 |
|------|------|------|
| name | string | — |
| frequency | float | 必須 > 0 |
| damping | float | 必須 ≥ 0 |
| amplitude | float | 必須 > 0 且不可大於 100（於 service 層驗證） |

### 建立實驗範例

```bash
curl -X POST http://127.0.0.1:8000/experiments \
  -H "Content-Type: application/json" \
  -d '{"name": "test experiment", "frequency": 2.5, "damping": 0.2, "amplitude": 4.7}'
```

## 專案架構說明

- **`database.py`**：負責直接與 SQLite 溝通，包含建表、CRUD 語法。
- **`service.py`**：包裝資料庫操作，加入商業規則（例如振幅上限 100）並管理 commit / rollback 交易。
- **`main.py`**：定義 FastAPI 路由，將 HTTP 請求轉換成 service 呼叫，並處理錯誤（404 / 400 / 422）。
- **`models.py` / `database_models.py`**：分別對應 API 層（Pydantic）與資料庫層（dataclass）的資料結構。

## 執行測試

```bash
pytest
```

測試會使用暫時性的 SQLite 資料庫檔案，不會影響正式環境的資料。

---