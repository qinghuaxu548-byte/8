#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
多股票回测测试脚本
测试不同行业、不同市值的股票样本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import FinancialRiskAgent

def main():
    # 创建风险代理实例
    agent = FinancialRiskAgent()
    
    # 选择不同行业、不同市值的股票样本
    stocks = [
        # 大市值股票
        "600519",  # 贵州茅台 - 食品饮料（白酒）- 超大市值
        "000858",  # 五粮液 - 食品饮料（白酒）- 大市值
        "000002",  # 万科A - 房地产 - 大市值
        "601318",  # 中国平安 - 非银金融（保险）- 大市值
        
        # 中市值股票
        "002415",  # 海康威视 - 电子（安防）- 中市值
        "300750",  # 宁德时代 - 电气设备（锂电池）- 中市值
        "600036",  # 招商银行 - 银行 - 中市值
        "600276",  # 恒瑞医药 - 医药生物 - 中市值
        
        # 小市值股票
        "300059",  # 东方财富 - 非银金融（证券）- 中小市值
        "002594",  # 比亚迪 - 汽车（新能源）- 中小市值
        "601012",  # 隆基绿能 - 电气设备（光伏）- 中小市值
        "002241",  # 歌尔股份 - 电子（消费电子）- 中小市值
    ]
    
    # 回测参数
    start_date = "2025-01-18"
    end_date = "2026-01-18"
    rebalance_period = 30
    
    # 遍历股票列表进行回测
    for code in stocks:
        print(f"\n{'-'*50}")
        print(f"开始回测股票：{code}")
        print(f"{'-'*50}")
        
        try:
            # 执行回测
            result = agent.backtest(code, start_date, end_date, rebalance_period)
            
            if result:
                print(f"\n{'-'*50}")
                print(f"股票 {code} 回测完成！")
                print(f"{'-'*50}")
            else:
                print(f"\n{'-'*50}")
                print(f"股票 {code} 回测失败！")
                print(f"{'-'*50}")
                
        except Exception as e:
            print(f"\n{'-'*50}")
            print(f"股票 {code} 回测异常：{e}")
            print(f"{'-'*50}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'-'*50}")
    print(f"所有股票回测完成！")
    print(f"{'-'*50}")

if __name__ == "__main__":
    main()
