# Day 16: 文件上传

今天重点：

- Multipart 上传
- 文件存储策略
- 文件元数据记录
- 安全注意事项

## 运行方式

```bash
cd 2026-05-01-day16
python3 -m uvicorn app:app --reload
```

## 测试示例

```bash
curl -X POST "http://127.0.0.1:8000/files/upload" -F "file=@/path/to/demo.png"
curl "http://127.0.0.1:8000/files"
```

## 查漏补缺

1. 上传接口不能只保存文件，还要记录元数据
2. 文件类型和大小都应该校验
3. 原始文件名不能直接无脑作为最终存储名
