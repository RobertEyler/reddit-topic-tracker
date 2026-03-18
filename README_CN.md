# Reddit 话题追踪器 - 使用说明

## 📖 项目说明

这是一个轻量级的开源工具，用于追踪和分析 Reddit 社区的话题趋势。适用于研究人员、开发者和社区爱好者，帮助发现相关讨论并了解对话如何随时间演变。

## ✨ 主要功能

- **关键词搜索** — 在多个 subreddit 中按关键词或短语搜索帖子和评论
- **趋势分析** — 追踪话题热度在天、周、月的变化
- **参与度指标** — 按点赞数、评论数和活跃度对帖子排名
- **跨 Subreddit 发现** — 找到正在讨论某话题的社区
- **用户活动洞察** — 识别对话题讨论贡献最多的用户
- **导出支持** — 将结果保存为 CSV 或 JSON 格式以便进一步分析

## 🚀 快速开始

### 系统要求

- Python 3.8 或更高版本
- Reddit 账户和注册的应用程序（脚本类型）

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/reddit-topic-tracker.git
   cd reddit-topic-tracker
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置 Reddit API**

   在 https://www.reddit.com/prefs/apps 注册一个 Reddit 应用：
   - 点击 "创建应用" 或 "创建另一个应用"
   - 选择 "script" 类型
   - 填写名称和描述
   - redirect uri 填写：http://localhost:8080
   - 记录你的 `client_id` 和 `client_secret`

4. **创建环境变量文件**

   复制 `.env.example` 为 `.env`：
   ```bash
   copy .env.example .env
   ```
   
   编辑 `.env` 文件，填入你的 Reddit API 凭据：
   ```
   REDDIT_CLIENT_ID=你的客户端ID
   REDDIT_CLIENT_SECRET=你的客户端密钥
   REDDIT_USER_AGENT=reddit-topic-tracker/1.0 by u/你的用户名
   ```

## 📝 使用方法

### 基本搜索

```bash
# 搜索特定关键词
python tracker.py --keyword "人工智能" --subreddit "MachineLearning" --limit 100

# 在多个 subreddit 中搜索
python tracker.py --keyword "气候变化" --subreddit "science,environment,climate"

# 搜索所有 subreddit
python tracker.py --keyword "Python编程" --subreddit "all"
```

### 时间范围和排序

```bash
# 搜索过去一周的内容
python tracker.py --keyword "游戏" --timeframe week

# 按热度排序
python tracker.py --keyword "新闻" --sort hot

# 按最新排序
python tracker.py --keyword "科技" --sort new --timeframe day
```

### 趋势分析

```bash
# 按天分析趋势
python tracker.py --keyword "加密货币" --trends day

# 按周分析趋势
python tracker.py --keyword "股市" --trends week --timeframe month
```

### 数据导出

```bash
# 导出为 CSV
python tracker.py --keyword "机器学习" --export csv

# 导出为 JSON
python tracker.py --keyword "深度学习" --export json

# 同时导出 CSV 和 JSON
python tracker.py --keyword "数据科学" --export both
```

### 高级选项

```bash
# 显示前 20 个结果
python tracker.py --keyword "编程" --top 20

# 不显示摘要信息
python tracker.py --keyword "技术" --no-summary

# 组合多个选项
python tracker.py --keyword "人工智能" \
  --subreddit "MachineLearning,artificial,deeplearning" \
  --timeframe month \
  --sort top \
  --limit 200 \
  --trends week \
  --export both \
  --top 15
```

## 📊 输出说明

### 控制台输出

程序会在控制台显示以下信息：

1. **数据分析摘要** - 总体统计信息
   - 总帖子数、总分数、总评论数
   - 平均分数、平均评论数、平均点赞率
   - Subreddit 分布
   - 顶级贡献者

2. **参与度最高的帖子** - 按参与度排名的帖子列表
   - 标题、作者、社区
   - 分数、评论数、参与度分数
   - 帖子链接

3. **Subreddit 分布** - 各社区的帖子分布

4. **顶级贡献者** - 发帖最多的用户

5. **趋势分析** - 话题随时间的变化（如果启用）

### 导出文件

导出的文件保存在 `output/` 目录中，文件名包含时间戳：

- **posts_YYYYMMDD_HHMMSS.csv** - 帖子数据（CSV 格式）
- **posts_YYYYMMDD_HHMMSS.json** - 帖子数据（JSON 格式）
- **summary_YYYYMMDD_HHMMSS.txt** - 分析摘要文本
- **trends_YYYYMMDD_HHMMSS.csv** - 趋势分析数据

## 🔧 项目结构

```
reddit-topic-tracker/
│
├── tracker.py           # 主程序入口
├── config.py            # 配置管理模块
├── reddit_client.py     # Reddit API 客户端
├── data_processor.py    # 数据处理和分析模块
├── exporter.py          # 数据导出模块
│
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量示例
├── .gitignore          # Git 忽略文件
│
├── README.md           # 英文说明文档
├── README_CN.md        # 中文说明文档（本文件）
│
└── output/             # 导出文件目录（自动创建）
```

## ⚖️ API 合规性

本工具完全遵守 Reddit 的 API 服务条款和负责任构建者政策：

- ✅ 所有请求均通过 OAuth2 认证
- ✅ 遵守速率限制（每分钟最多 60 个请求）
- ✅ 不访问私有、NSFW 或需要登录的内容
- ✅ 不进行自动发帖、投票或发送消息
- ✅ 只进行只读操作

## 📄 许可证

MIT 许可证 - 可自由使用、修改和分发。

## 🤝 贡献

欢迎贡献和反馈！如有问题或建议，请提交 Issue 或 Pull Request。

## 📧 联系方式

如有问题，请通过 GitHub Issues 联系。

---

**提示：** 使用前请确保遵守 Reddit 的服务条款和你所在地区的法律法规。本工具仅用于研究和学习目的。
