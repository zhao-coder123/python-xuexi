-- Day 8: MySQL 基础入门练习

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS ai_admin_demo
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- 2. 选择数据库
USE ai_admin_demo;

-- 3. 如果之前练过，先删除旧表
DROP TABLE IF EXISTS users;

-- 4. 创建 users 表
CREATE TABLE users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键 id',
  username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名，唯一',
  nickname VARCHAR(50) NOT NULL COMMENT '昵称',
  age TINYINT UNSIGNED NOT NULL COMMENT '年龄',
  email VARCHAR(100) DEFAULT NULL UNIQUE COMMENT '邮箱，唯一',
  status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1 启用，0 禁用',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT='用户表';

-- 5. 插入数据
INSERT INTO users (username, nickname, age, email, status)
VALUES
  ('minda', 'Minda', 24, 'minda@example.com', 1),
  ('tom', 'Tom', 26, 'tom@example.com', 1),
  ('alice', 'Alice', 22, 'alice@example.com', 0);

-- 6. 查询全部用户
SELECT * FROM users;

-- 7. 查询启用状态的用户
SELECT id, username, nickname, status
FROM users
WHERE status = 1;

-- 8. 查询单个用户
SELECT * FROM users WHERE id = 1;

-- 9. 更新用户信息
UPDATE users
SET nickname = 'Tom Lee', status = 0
WHERE id = 2;

-- 10. 删除用户
DELETE FROM users WHERE id = 3;

-- 11. 再次查看结果
SELECT * FROM users;
