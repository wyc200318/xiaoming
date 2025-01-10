# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


def product_order_number(sid):
    sid = int(sid)
    if sid == 1:
        return {"订单数目": 100}
    else:
        return {"订单数目": 200}

# 描述输入的sid
class ProductOrderNumberInput(BaseModel):
    sid: int = Field(description="商品id")


def product_price(sid):
    sid = int(sid)
    if sid == 1:
        return {"价格": 35.25}
    else:
        return {"价格": 36.2}


class ProductPriceInput(BaseModel):
    sid: int = Field(description="商品id")
