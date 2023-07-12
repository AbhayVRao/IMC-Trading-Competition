
import pandas as pd
import numpy as np
from typing import Dict, List
from datamodel import Listing, OrderDepth, Trade, TradingState, Order
import statistics

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
            """

            Only method required. It takes all buy and sell orders for all symbols as an input,
            and outputs a list of orders to be sent
            """
            # Initialize the method output dict as an empty dict
            result = {}

            # Iterate over all the keys (the available products) contained in the order depths
            for product in state.order_depths.keys():

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []
                df = pd.DataFrame(columns=['price','volume'])
                acceptable_price = 1
                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:
                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    # best_ask = min(order_depth.sell_orders.keys())
                    # best_ask_volume = order_depth.sell_orders[best_ask]
                    for order1_price in order_depth.sell_orders.keys():
                        new_row = pd.Series([order1_price,order_depth.sell_orders[order1_price]], index=['price', 'volume'])
                        df = df.append(new_row, ignore_index=True)
                if len(order_depth.sell_orders) == 0:
                   print('Error')

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                #     if best_ask < acceptable_price:
                #         # In case the lowest ask is lower than our fair value,
                #         # This presents an opportunity for us to buy cheaply
                #         # The code below therefore sends a BUY order at the price level of the ask,
                #         # with the same quantity
                #         # We expect this order to trade with the sell order
                #         print("BUY", str(-best_ask_volume) + "x", best_ask)
                #         orders.append(Order(product, best_ask, -best_ask_volume))
                 # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    # best_bid = max(order_depth.buy_orders.keys())
                    # best_bid_volume = order_depth.buy_orders[best_bid]
                    for order1_price in order_depth.buy_orders.keys():
                        new_row = pd.Series([order1_price,order_depth.buy_orders[order1_price]], index=['price', 'volume'])
                        df = df.append(new_row, ignore_index=True)
                    # if best_bid > acceptable_price:
                    #     print("SELL", str(best_bid_volume) + "x", best_bid)
                    #     orders.append(Order(product, best_bid, -best_bid_volume))
                # Add all the above orders to the result dict
                x = np.array(df.price).astype(str).astype(float)
                y = np.array(df.volume).astype(str).astype(float)
                #acceptable_price=9998
                #print(x.head(2))
                slope, intercept = np.polyfit(x, y, 1);
                acceptable_price = -intercept/slope
                if len(order_depth.sell_orders) > 0:
                  for selling_prices in order_depth.sell_orders.keys():
                    if(selling_prices < acceptable_price):
                      if product in state.position.keys() and order_depth.sell_orders[selling_prices] + state.position[product]<=-20:
                        print("BUY", str(order_depth.sell_orders[selling_prices]) + "x", selling_prices)
                        orders.append(Order(product, selling_prices, -order_depth.sell_orders[selling_prices]))
                        state.position[product] += order_depth.sell_orders[selling_prices]

                      if -order_depth.sell_orders[selling_prices]<=20 and product not in state.position.keys() :
                        print("BUY", str(order_depth.sell_orders[selling_prices]) + "x", selling_prices)
                        orders.append(Order(product, selling_prices, -order_depth.sell_orders[selling_prices]))
                        state.position[product] = order_depth.sell_orders[selling_prices]


                      if -order_depth.sell_orders[selling_prices]>20 and product not in state.position.keys() :
                        print("BUY", str(20) + "x", selling_prices)
                        orders.append(Order(product, selling_prices, 20))
                        state.position[product] = 20


                if len(order_depth.buy_orders) > 0:
                  for buying_prices in order_depth.buy_orders.keys():
                    if(buying_prices > acceptable_price):
                      if product in state.position.keys() and order_depth.buy_orders[buying_prices] + state.position[product]<=20:
                        print("SELL", str(order_depth.buy_orders[buying_prices]) + "x", buying_prices)
                        orders.append(Order(product, buying_prices, -order_depth.buy_orders[buying_prices]))
                        state.position[product] -= order_depth.buy_orders[buying_prices]

                      if order_depth.buy_orders[buying_prices]<20 and product not in state.position.keys() :
                        print("SELL", str(order_depth.buy_orders[buying_prices]) + "x", buying_prices)
                        orders.append(Order(product, buying_prices, -20))
                        state.position[product] = -order_depth.  buy_orders[buying_prices]


                      if order_depth.buy_orders[buying_prices]>20 and product not in state.position.keys() :
                        print("SELL", str(20) + "x", buying_prices)
                        orders.append(Order(product, buying_prices, -20))
                        state.position[product] = -20
                result[product] = orders
                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
            return result
