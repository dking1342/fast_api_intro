from typing import List
from ..schemas import blog as blog_schema


def convert_payload(payload):
    data: List[blog_schema.BlogOutput] = []
    for blog in payload:
        blog_dict = blog_schema.BlogOutput(**blog.__dict__)
        data.append(blog_dict)
    return data
