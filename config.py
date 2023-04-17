import argparse

parser=argparse.ArgumentParser(description='config info')
parser.add_argument('--api_key',default='8da5d3ad-7554-424e-a1c2-bfcead40dcdd')
parser.add_argument('--secret_key',default='E086EDAC65DF1E55DA72CA2483327CA2')
parser.add_argument('--passphrase',default='lxc123@LXC')
parser.add_argument('--Permissions',default='Read/Withdraw/Trade')
parser.add_argument('--use_server_time',default=False,type=bool)
parser.add_argument('--flag',default='1')

parser.add_argument('--stop_loss_multiplier',default='0.98',type=float,help='止损倍数')
parser.add_argument('--max_holding_period',default='20',type=int,help='最长持仓天数')
parser.add_argument('--stop_loss_period',default='5',type=int,help='止损触发期')
parser.add_argument('--trailing_stop_multiplier',default='0.98',type=float,help='移动止损倍数')
parser.add_argument('--trailing_stop_period',default='5',type=int,help='移动止损触发期')
parser.add_argument('--ccy_sell',default='BTC',help='查询余额使用')
parser.add_argument('--ccy_buy',default='USDT',help='查询余额使用')
parser.add_argument('--instId',default='BTC-USDT',help='购买和查询k线图使用')
parser.add_argument('--bar',default='15m',help='查询k线图的时间间隔')

args=parser.parse_args()