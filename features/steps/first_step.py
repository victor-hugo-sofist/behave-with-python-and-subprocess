from behave import *
import subprocess
import json
import random

GREEN = "\033[32m"
WHITE = "\033[0m"
RED = "\033[32m"


@given('i get stock list')
def step_impl(context):
    raw_result = subprocess.run(["curl", "http://127.0.0.1:5000/stocks/"],
                                shell=False,
                                text=True,
                                check=True,
                                capture_output=True)

    try:
        assert raw_result.returncode == 0
        assert raw_result.stdout != ""
    except AssertionError as e:
        print(f'Return Code: {raw_result.returncode}')
        print(f'stdout: {raw_result.stdout}')
        raise e
    except:
        raise e

    context.result = json.loads(raw_result.stdout)


@then('products should can have a valid information')
def step_impl(context):

    for stock in context.result["Content"]["Stocks"]:
        try:
            assert stock["Name"] != ""
            assert stock["Price"] >= 0.01
            assert len(stock["Symbol"]) >= 5
        except AssertionError as e:
            print(stock)
            raise e
        except:
            raise e


@then('products should can have a valid type information')
def step_impl(context):

    for stock in context.result["Content"]["Stocks"]:
        try:
            assert type(stock["Name"]) == str
            assert type(stock["Price"]) == float
            assert type(stock["Symbol"]) == str
        except AssertionError as e:
            print(stock)
            raise e
        except:
            raise e


@given('i update product "{product_symbol}" price')
def step_impl(context, product_symbol):

    context.product_symbol = product_symbol

    context.random_price = round(random.uniform(0.01, 100.00), 2)

    raw_result = subprocess.run(["curl",
                                 "-X",
                                 "PATCH",
                                 f"http://127.0.0.1:5000/stock/{product_symbol}/change/price/",
                                 "-H",
                                 "Content-Type: application/json",
                                 "-d",
                                 '{"Price": value}'.replace("value", str(context.random_price), 1)],
                                shell=False,
                                text=True,
                                check=True,
                                capture_output=True)

    try:
        assert raw_result.returncode == 0
    except AssertionError as e:
        print(f'Return Code: {raw_result.returncode}')
        print(f'stdout: {raw_result.stdout}')
        raise e
    except:
        raise e

    context.result = json.loads(raw_result.stdout)


@then('price should be updated')
def step_impl(context):

    for stock in context.result["Content"]["Stocks"]:
        if stock["Symbol"] == context.product_symbol:
            try:
                assert stock["Price"] == context.random_price
            except AssertionError as e:
                print(stock)
                raise e
            except:
                raise e

    subprocess.run(f"echo {GREEN}    New Price: {context.random_price}{WHITE}",
                   shell=True,
                   check=True)
