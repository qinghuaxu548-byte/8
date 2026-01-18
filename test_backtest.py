import sys
import os
from datetime import datetime, timedelta

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入FinancialRiskAgent
from agent import FinancialRiskAgent

# 测试回测功能
if __name__ == "__main__":
    print("初始化FinancialRiskAgent...")
    agent = FinancialRiskAgent()
    
    try:
        # 使用不同的股票代码测试，尝试使用贵州茅台
        code = "600519"  # 贵州茅台的股票代码
        print(f"\n测试回测功能，股票代码：{code}")
        
        # 设置回测时间范围（最近一年）
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        # 运行回测
        print(f"回测时间范围：{start_date} 至 {end_date}")
        print(f"再平衡周期：30天")
        print(f"\n开始回测...")
        
        backtest_result = agent.backtest(code, start_date, end_date, rebalance_period=30)
        
        if backtest_result is not None:
            print("\n回测功能测试成功！")
            print(f"\n回测结果统计：")
            print(f"回测时间点数量：{len(backtest_result)}")
            print(f"平均风险得分：{backtest_result['risk_score'].mean():.2f}")
            print(f"平均未来收益率：{backtest_result['future_return'].mean() * 100:.2f}%")
        else:
            print("\n回测功能测试失败！")
        
        print("\n回测功能测试完成！")
    except Exception as e:
        print(f"\n回测功能测试失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    sys.exit(0)