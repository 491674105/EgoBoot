from math import ceil


class Page:
    # 页码
    page_no = -1
    # 页面记录数
    page_size = -1
    # 上一页
    pre_page = -1
    # 下一页
    next_page = -1
    # 总页数
    total_page = -1
    # 总记录数
    total_counts = -1

    data = None

    def __init__(self, page_no, page_size, total_counts, data):
        self.page_no = page_no
        self.page_size = page_size

        self.total_counts = total_counts
        self.data = data

        if self.page_size > 0:
            self.total_page = ceil(self.total_counts / self.page_size)
        else:
            self.total_page = 0

        self.pre_page = self.page_no - 1
        if self.total_page <= 0:
            self.next_page = 0
        elif self.total_page - 1 == self.page_no:
            self.next_page = self.page_no
        else:
            self.next_page = self.page_no + 1

    def body(self):
        return {
            "page_no": self.page_no,
            "page_size": self.page_size,
            "pre_page": self.pre_page,
            "next_page": self.next_page,
            "total_page": self.total_page,
            "total_counts": self.total_counts,
            "data": self.data
        }
