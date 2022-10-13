import pyupbit
import time

access_key = "ymw81x6cbtTm964KRKq6BR8NAVJrI6Gxnei9HKr4"
secret_key = "KLJPvX2mfDxfzbvafDQxTaf87JWpSji47vwHnG4m"

if __name__ == '__main__':
    upbit = pyupbit.Upbit(access_key, secret_key)  # 로그인

    # 미채결된 주문들 취소
    result = upbit.get_order("KRW-XRP")
    for order in result:
        if order['side'] == 'bid':  # 매수 주문인 경우 매수는 bid, 매도는 ask로 표기
            uuid = order['uuid']
            upbit.cancel_order(uuid)
            time.sleep(0.3)

    # 보유한 코인 시장가 매도 주문
    xrp_coin = upbit.get_balance("KRW-XRP")
    if xrp_coin > 0:
        upbit.sell_market_order("KRW-XRP", xrp_coin)

    # 매수 주문
    current_xrp_price = pyupbit.get_current_price("KRW-XRP")
    buy_coin = [
        current_xrp_price * (0.98 - 0.01 * i)
        for i in range(4, 10)
    ]

    ticker_buy_coin = [
        pyupbit.get_tick_size(price) for price in buy_coin
    ]

    money = upbit.get_balance("KRW") # 보유한 원화

    buy_coin_amount = money / sum(ticker_buy_coin) * (1 - 0.0005)  # 수수료 고려

    for price in ticker_buy_coin:
        upbit.buy_limit_order("KRW-XRP", price, buy_coin_amount)
        time.sleep(0.3)
