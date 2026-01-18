#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
多股票回测结果分析脚本
分析不同行业、不同市值股票的回测表现
"""

import os
import pandas as pd
import glob

# 股票基本信息
def get_stock_info():
    return {
        "600519": {"name": "贵州茅台", "industry": "食品饮料（白酒）", "market_cap": "超大市值"},
        "000858": {"name": "五粮液", "industry": "食品饮料（白酒）", "market_cap": "大市值"},
        "000002": {"name": "万科A", "industry": "房地产", "market_cap": "大市值"},
        "601318": {"name": "中国平安", "industry": "非银金融（保险）", "market_cap": "大市值"},
        "002415": {"name": "海康威视", "industry": "电子（安防）", "market_cap": "中市值"},
        "300750": {"name": "宁德时代", "industry": "电气设备（锂电池）", "market_cap": "中市值"},
        "600036": {"name": "招商银行", "industry": "银行", "market_cap": "中市值"},
        "600276": {"name": "恒瑞医药", "industry": "医药生物", "market_cap": "中市值"},
        "300059": {"name": "东方财富", "industry": "非银金融（证券）", "market_cap": "中小市值"},
        "002594": {"name": "比亚迪", "industry": "汽车（新能源）", "market_cap": "中小市值"},
        "601012": {"name": "隆基绿能", "industry": "电气设备（光伏）", "market_cap": "中小市值"},
        "002241": {"name": "歌尔股份", "industry": "电子（消费电子）", "market_cap": "中小市值"},
    }

# 分析单只股票的回测结果
def analyze_single_backtest(file_path):
    # 提取股票代码
    file_name = os.path.basename(file_path)
    code = file_name.split('_')[0]
    
    # 读取回测结果
    df = pd.read_csv(file_path)
    
    # 计算整体收益率
    total_return = (df['future_price'].iloc[-1] - df['current_price'].iloc[0]) / df['current_price'].iloc[0]
    
    # 计算风险得分与收益率的相关性
    correlation = df['risk_score'].corr(df['future_return'])
    
    # 计算胜率
    win_rate = len(df[df['future_return'] > 0]) / len(df)
    
    # 计算不同风险等级的平均收益率
    risk_level_performance = df.groupby('risk_level')['future_return'].mean().to_dict()
    
    # 计算风险得分的统计信息
    risk_score_stats = {
        'mean': df['risk_score'].mean(),
        'min': df['risk_score'].min(),
        'max': df['risk_score'].max(),
        'std': df['risk_score'].std()
    }
    
    return {
        'code': code,
        'total_return': total_return,
        'correlation': correlation,
        'win_rate': win_rate,
        'risk_level_performance': risk_level_performance,
        'risk_score_stats': risk_score_stats,
        'sample_count': len(df)
    }

# 主函数
def main():
    # 获取回测结果文件列表
    backtest_files = glob.glob('backtest_results/*.csv')
    
    # 获取股票基本信息
    stock_info = get_stock_info()
    
    # 分析所有回测结果
    backtest_results = []
    for file_path in backtest_files:
        result = analyze_single_backtest(file_path)
        # 添加股票基本信息
        if result['code'] in stock_info:
            result.update(stock_info[result['code']])
        backtest_results.append(result)
    
    # 转换为DataFrame
    df_results = pd.DataFrame(backtest_results)
    
    # 保存原始分析结果
    df_results.to_csv('backtest_analysis_results.csv', index=False)
    
    # 按市值分组分析
    print("=== 按市值分组分析 ===")
    market_cap_analysis = df_results.groupby('market_cap').agg({
        'total_return': ['mean', 'std'],
        'correlation': 'mean',
        'win_rate': 'mean',
        'risk_score_stats': lambda x: pd.Series([item['mean'] for item in x]).mean()
    })
    print(market_cap_analysis)
    print()
    
    # 按行业分组分析
    print("=== 按行业分组分析 ===")
    industry_analysis = df_results.groupby('industry').agg({
        'total_return': ['mean', 'std'],
        'correlation': 'mean',
        'win_rate': 'mean',
        'risk_score_stats': lambda x: pd.Series([item['mean'] for item in x]).mean()
    })
    print(industry_analysis)
    print()
    
    # 整体分析
    print("=== 整体分析 ===")
    overall_analysis = df_results.agg({
        'total_return': ['mean', 'std'],
        'correlation': 'mean',
        'win_rate': 'mean',
        'risk_score_stats': lambda x: pd.Series([item['mean'] for item in x]).mean()
    })
    print(overall_analysis)
    print()
    
    # 打印每只股票的基本信息
    print("=== 单只股票回测结果 ===")
    for _, row in df_results.iterrows():
        print(f"{row['code']} ({row['name']}) - {row['industry']} - {row['market_cap']}")
        print(f"  整体收益率: {row['total_return']:.2%}")
        print(f"  风险得分与收益率相关性: {row['correlation']:.2f}")
        print(f"  胜率: {row['win_rate']:.2%}")
        print(f"  平均风险得分: {row['risk_score_stats']['mean']:.2f}")
        print(f"  风险得分范围: {row['risk_score_stats']['min']:.2f} - {row['risk_score_stats']['max']:.2f}")
        print()

if __name__ == "__main__":
    main()
