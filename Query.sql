-- 禁用外键约束（必须加！）
SET FOREIGN_KEY_CHECKS = 0;

-- 生成清空所有表的 SQL（把 your_database 换成你的库名）
SELECT CONCAT('TRUNCATE TABLE `', table_name, '`;')
FROM information_schema.tables
WHERE table_schema = 'emotion_chat'  -- 替换为你的数据库名
AND table_type = 'BASE TABLE';

-- 执行完清空后，重新开启外键约束
SET FOREIGN_KEY_CHECKS = 1;