from typing import List
from ..schemas import blog as blog_schema


def convert_payload(payload, votes):
    data: List[blog_schema.BlogOutput] = []
    for index, blog in enumerate(payload):
        blog_dict = blog_schema.BlogOutput(**blog.__dict__, votes=votes[index])
        data.append(blog_dict)
    return data
