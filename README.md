# 年报对照平台 MVP

本仓库提供“后端 API + 算法模块 + 前端 UI + 批量导入 + 自动识别 + 导出模板”的端到端最小可用版本，支持政府信息公开工作年度报告的采集、入库、比对与报告导出。

## 目录结构

```
/api        FastAPI 服务与核心算法
/web        Next.js 14 前端
/docker     容器化运行脚本
/tests      Pytest 单测
```

## 快速开始

### 本地开发

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

前端：

```bash
cd web
npm install
npm run dev
```

### Docker Compose

```bash
make up
make logs
make down
```

## 功能概览

- **采集入库**：支持文本/文件上传，自动解析章节与重点表格。
- **自动识别**：基于域名映射与别名库判定地区、机关与年份，并返回置信度。
- **表格与文本比对**：0 同值剔除、勾稽校验、句级语义匹配、数字事实抽取。
- **批量导入**：CSV 模板批量提交，返回逐条识别结果。
- **导出模板**：Jinja2 生成 HTML，可扩展为 PDF/Word。
- **AI 预留**：统一的向量与语义差异接口，后续可切换至大模型。

## 测试

```bash
pytest
```

测试覆盖单位归一、勾稽校验、模板句剔除、自动识别、表格 0 剔除、数字事实比对以及端到端 ingest/compare 流程。

## 环境变量

参考 `.env.example`，填写数据库、Redis 及 AI 模型配置即可。

## 报告导出

调用 `/diff/{left}/{right}` 获取对照结果，再将 JSON 注入 `api/templates/report.html.j2` 渲染，可进一步集成 WeasyPrint 生成 PDF。
