# Yelp评论爬取与情感分析工具

此项目是一个基于Python的工具，用于从Yelp抓取餐厅评论，分析评论的情感和情绪，并将结果保存到文件中。该工具使用 **ScraperAPI** 进行页面访问， **BeautifulSoup** 进行HTML解析， **AFINN** 进行情感分析，以及 **NRCLex** 进行情绪分析。

## 目录
- [项目概述](#项目概述)
- [环境要求](#环境要求)
- [工作原理](#工作原理)
  - [YelpScraper 类](#yelpscraper-类)
  - [ReviewAnalyzer 类](#reviewanalyzer-类)
  - [FileWriter 类](#filewriter-类)
- [快速上手](#快速上手)
- [使用方法](#使用方法)
- [保存和查看结果](#保存和查看结果)
- [注意事项](#注意事项)

---

## 项目概述

该工具通过以下步骤来分析Yelp上餐厅的评论：
1. 使用AFINN情感分析库对评论进行情感分析，将评论分类为正面、中立或负面。
2. 使用NRCLex情绪分析库识别评论中的主要情绪。

分析结果会保存在以下文件中：
- `sentiment_analysis_results.csv` 用于存储情感分析结果。
- `emotions_analysis.txt` 用于存储详细的情绪分析结果。

## 环境要求

- **Python 3.x**
- **依赖库**： `requests`, `beautifulsoup4`, `pandas`, `random`, `time`, `afinn`, `nrclex`

安装所需库：
```bash
pip install requests beautifulsoup4 pandas afinn nrclex
```

## 工作原理

### YelpScraper 类

`YelpScraper` 类负责：
- **生成URL**：根据查询关键词和指定地点生成Yelp的搜索页面URL。
- **获取页面内容**：使用ScraperAPI抓取Yelp页面内容，并在遇到错误时进行重试。
- **提取评论**：使用BeautifulSoup解析页面内容，提取评论。

**关键方法**：
- `get_yelp_urls`：根据查询关键词生成分页的搜索URL列表。
- `fetch_page_content`：通过ScraperAPI抓取页面内容，并处理403、429和500等错误。
- `scrape_reviews`：为每个生成的URL抓取评论，并返回评论数据列表。
- `extract_restaurant_name` 和 `extract_reviews`：解析HTML内容，找到餐厅名称和评论文本。

### ReviewAnalyzer 类

`ReviewAnalyzer` 类用于分析评论的情感和情绪：
- **AFINN情感分析**：计算每条评论的情感得分，并标记为正面、中立或负面。
- **NRC情绪分析**：识别每条评论的主要情绪。

**关键方法**：
- `analyze_sentiment_afinn`：为每条评论计算情感得分和标签。
- `analyze_emotions_nrc`：为每条评论识别主要情绪。

### FileWriter 类

`FileWriter` 类将分析结果保存到文件：
- `save_sentiment_results`：将情感得分和标签保存到CSV文件。
- `save_emotions_results`：将主要情绪保存到文本文件。

## 快速上手

1. **添加您的ScraperAPI密钥**：在`main()`函数中替换`api_key`为您的ScraperAPI密钥。
2. **设置地点**（可选）：初始化`YelpScraper`时，可以设置`location`参数来指定搜索地点。

## 使用方法

运行脚本的主函数：
```bash
python yelp_scraper.py
```

`main`函数的执行流程：
1. 初始化`YelpScraper`、`ReviewAnalyzer` 和 `FileWriter`类。
2. 根据指定的查询关键词（默认为`restaurants`）抓取评论。
3. 对评论进行情感和情绪分析。
4. 保存分析结果。

## 保存和查看结果

- **情感分析结果**：保存于`sentiment_analysis_results.csv`，包含以下列：
  - `Review`：评论文本
  - `Score`：情感得分（正面、负面或中立）
  - `Sentiment`：情感标签（正面、负面或中立）
  - `Restaurant`：餐厅名称

- **情绪分析结果**：保存于`emotions_analysis.txt`，每条记录包含以下信息：
  - `Restaurant`：餐厅名称
  - `Review`：评论文本
  - `Emotions`：由NRCLex检测的主要情绪

## 注意事项

1. **ScraperAPI密钥**：请确保使用有效的ScraperAPI密钥来抓取Yelp页面。
2. **代理和速率限制**：此脚本使用ScraperAPI并设置了随机延迟，以避免被速率限制。遇到阻止问题时，可以调整`time.sleep`的时间间隔。
3. **HTML结构**：CSS选择器（例如，`'y-css-hcgwj4'`）可能会变化，可能需要更新`extract_restaurant_name` 和 `extract_reviews` 方法。

---